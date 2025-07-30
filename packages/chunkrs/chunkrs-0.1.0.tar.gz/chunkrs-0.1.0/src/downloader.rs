use pyo3::prelude::*;
use pyo3::{exceptions::PyRuntimeError, PyErr, PyResult};
use std::fs::{File, OpenOptions};
use std::io::{Seek, SeekFrom, Write};
use std::path::PathBuf;
use std::sync::{Arc, Mutex};
use std::time::Instant;

use anyhow::{Context, Result};
use futures_util::StreamExt;
use indicatif::{MultiProgress, ProgressBar, ProgressStyle};
use pretty_bytes::converter::convert;
use reqwest::header::{HeaderMap, HeaderValue, CONTENT_LENGTH, RANGE};
use reqwest::Client;

use crate::utils::*;

#[tokio::main]
#[pyfunction]
#[pyo3(signature = (url, output_file, chunk_size=8 * 1024 * 1024, max_parallel=10_000, verbose=true))]
pub async fn download(
    url: &str,
    output_file: PathBuf,
    chunk_size: u64,
    max_parallel: usize,
    verbose: bool,
) -> PyResult<()> {
    verbose_println!(verbose, "Starting download from: {}", url);
    verbose_println!(verbose, "Output file: {}", output_file.display());
    verbose_println!(verbose, "Chunk size: {}", convert(chunk_size as f64));
    if max_parallel != 10_000 {
        verbose_println!(verbose, "Max parallel connections: {}", max_parallel);
    }

    // Create a HTTP client
    let client = Client::new();

    // Get file size with a HEAD request
    let resp = client
        .head(*&url)
        .send()
        .await
        .context("Failed to send HEAD request")
        .map_err(to_pyerr)?;

    if !resp.status().is_success() {
        return Err(PyErr::new::<PyRuntimeError, _>(format!(
            "Failed to fetch URL: HTTP {}",
            resp.status()
        )));
    }

    let file_size = if let Some(content_length) = resp.headers().get(CONTENT_LENGTH) {
        content_length
            .to_str()
            .context("Invalid Content-Length header encoding")
            .map_err(to_pyerr)?
            .parse::<u64>()
            .context("Invalid Content-Length header value")
            .map_err(to_pyerr)?
    } else {
        return Err(PyErr::new::<PyRuntimeError, _>(
            "Content-Length header not found",
        ));
    };

    verbose_println!(verbose, "File size: {} bytes", file_size);

    // Create output file and set its size
    {
        let file = OpenOptions::new()
            .create(true)
            .write(true)
            .truncate(true)
            .open(&output_file)
            .context("Failed to create output file")
            .map_err(to_pyerr)?;

        file.set_len(file_size)
            .context("Failed to set output file size")
            .map_err(to_pyerr)?;
    }

    // Calculate number of chunks based on chunk size
    let num_chunks = (file_size + chunk_size - 1) / chunk_size;

    // Limit to max_parallel if specified
    let num_chunks = std::cmp::min(num_chunks, max_parallel as u64) as usize;

    // Setup progress tracking
    let multi_progress = if verbose {
        MultiProgress::new()
    } else {
        // Create a hidden MultiProgress when not verbose
        let mp = MultiProgress::new();
        mp.set_draw_target(indicatif::ProgressDrawTarget::hidden());
        mp
    };

    let main_progress = multi_progress.add(ProgressBar::new(file_size));
    if verbose {
        main_progress.set_style(
            ProgressStyle::default_bar()
                .template("{spinner:.green} [{elapsed_precise}] [{bar:40.cyan/blue}] {bytes}/{total_bytes} ({eta})")
                .unwrap()
                .progress_chars("#>-"),
        );
    } else {
        // Use hidden progress bar when not verbose
        main_progress.set_draw_target(indicatif::ProgressDrawTarget::hidden());
    }

    let start_time = Instant::now();
    let total_progress = Arc::new(Mutex::new(0u64));

    // Shared file handle
    let file = Arc::new(Mutex::new(
        OpenOptions::new()
            .write(true)
            .open(&output_file)
            .context("Failed to open output file for writing")
            .map_err(to_pyerr)?,
    ));

    // Create chunk download tasks
    let mut handles = Vec::with_capacity(num_chunks);

    for i in 0..num_chunks {
        let start = i as u64 * chunk_size;
        let end = if i == num_chunks - 1 {
            file_size - 1
        } else {
            (i as u64 + 1) * chunk_size - 1
        };

        // Skip empty chunks
        if start >= file_size {
            continue;
        }

        let url = url.to_string(); // Clone the string, not the reference
        let client = client.clone();
        let chunk_progress = multi_progress.add(ProgressBar::new(end - start + 1));

        if verbose {
            chunk_progress.set_style(
                ProgressStyle::default_bar()
                    .template(
                        "{spinner:.green} Chunk {pos} [{bar:30.cyan/blue}] {bytes}/{total_bytes}",
                    )
                    .unwrap()
                    .progress_chars("=> "),
            );
        } else {
            // Hide chunk progress bars when not verbose
            chunk_progress.set_draw_target(indicatif::ProgressDrawTarget::hidden());
        }

        let main_progress = main_progress.clone();
        let total_progress = total_progress.clone();
        let file = file.clone();
        let task_verbose = verbose;

        handles.push(tokio::spawn(async move {
            if let Err(e) = download_chunk(
                client,
                &url,
                start,
                end,
                i,
                chunk_progress,
                main_progress,
                total_progress,
                file,
                task_verbose,
            )
            .await
            {
                if task_verbose {
                    eprintln!("Error downloading chunk {}: {}", i, e);
                }
            }
        }));
    }

    // Wait for all tasks to complete
    for handle in handles {
        let _ = handle
            .await
            .map_err(|e| PyErr::new::<PyRuntimeError, _>(format!("Task join error: {}", e)))?;
    }

    if verbose {
        main_progress.finish_with_message("Download complete");
    }

    let elapsed = start_time.elapsed();
    let download_speed = file_size as f64 / elapsed.as_secs_f64();

    verbose_println!(
        verbose,
        "Downloaded {} bytes in {:.2} seconds ({:.2} MB/s)",
        convert(file_size as f64),
        elapsed.as_secs_f64(),
        download_speed / (1024.0 * 1024.0)
    );

    Ok(())
}

async fn download_chunk(
    client: Client,
    url: &str,
    start: u64,
    end: u64,
    chunk_index: usize,
    chunk_progress: ProgressBar,
    main_progress: ProgressBar,
    total_progress: Arc<Mutex<u64>>,
    file: Arc<Mutex<File>>,
    verbose: bool,
) -> Result<()> {
    let mut headers = HeaderMap::new();
    headers.insert(
        RANGE,
        HeaderValue::from_str(&format!("bytes={}-{}", start, end))
            .context("Failed to create Range header")?,
    );

    let resp = client
        .get(url)
        .headers(headers)
        .send()
        .await
        .context("Failed to send GET request")?;

    if !resp.status().is_success() {
        if verbose {
            chunk_progress.abandon_with_message("Failed");
        }
        anyhow::bail!(
            "Failed to download chunk {}: HTTP {}",
            chunk_index,
            resp.status()
        );
    }

    // Download and write chunk directly to file
    let mut bytes_written = 0u64;
    let mut stream = resp.bytes_stream();

    while let Some(chunk_result) = stream.next().await {
        let chunk = chunk_result.context("Failed to read chunk data")?;
        let chunk_size = chunk.len() as u64;

        // Write to file at the correct position
        let mut file_guard = file.lock().unwrap();
        file_guard
            .seek(SeekFrom::Start(start + bytes_written))
            .context("Failed to seek in output file")?;
        file_guard
            .write_all(&chunk)
            .context("Failed to write to output file")?;
        drop(file_guard);

        // Update progress
        bytes_written += chunk_size;
        chunk_progress.inc(chunk_size);

        // Update total progress
        let mut total = total_progress.lock().unwrap();
        *total += chunk_size;
        main_progress.set_position(*total);
    }

    // Finish the progress bar based on verbose setting
    if verbose {
        chunk_progress.finish_and_clear();
    }
    Ok(())
}
