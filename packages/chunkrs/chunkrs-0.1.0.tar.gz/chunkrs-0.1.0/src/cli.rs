use clap::Parser;
use pyo3::prelude::*;
use std::path::PathBuf;

use crate::downloader::download;

#[derive(Parser)]
#[command(name = "chunkrs")]
#[command(about = "Fast parallel downloading utility", long_about = None)]
pub struct Args {
    /// URL to download from
    #[arg(required = true)]
    url: String,

    /// Path to save the file to
    #[arg(required = true)]
    output_file: PathBuf,

    /// Size of each chunk in bytes
    #[clap(short, long, default_value_t = 8 * 1024 * 1024)]
    chunk_size: u64,

    /// Maximum number of parallel connections
    #[clap(short = 'p', long, default_value_t = 10_000)]
    max_parallel: usize,

    /// Enable verbose output
    #[arg(short, long)]
    verbose: bool,

    /// Disable verbose output (default)
    #[arg(short = 'q', long = "quiet", conflicts_with = "verbose")]
    quiet: bool,
}

#[pyfunction]
pub fn cli_main() -> PyResult<()> {
    // Drop the first additional binary argument
    let argv = std::env::args().skip(1).collect::<Vec<String>>();

    let cli = Args::parse_from(argv);
    let verbose = cli.verbose || !cli.quiet;

    // Call the download function and properly handle its result
    pyo3::Python::with_gil(|py| {
        py.allow_threads(|| {
            match download(
                &cli.url,
                cli.output_file,
                cli.chunk_size,
                cli.max_parallel,
                verbose,
            ) {
                Ok(_) => Ok(()),
                Err(e) => Err(e),
            }
        })
    })
}
