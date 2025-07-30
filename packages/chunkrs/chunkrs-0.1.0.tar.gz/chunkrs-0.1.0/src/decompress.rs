use flate2::read::GzDecoder;
use pyo3::exceptions::PyValueError;
use pyo3::prelude::*;
use std::fs::{self, File};
use std::path::PathBuf;
use tar::Archive;

/// Decompress a tarball file to a target directory.
///
/// Args:
///     input_file: Path to the compressed tarball
///     output_dir: Directory where contents should be extracted
///
/// Returns:
///     Number of files extracted or raises an exception on error
#[pyfunction]
pub fn decompress_tarball(input_file: PathBuf, output_dir: PathBuf) -> PyResult<usize> {
    // Check if input file exists
    if !input_file.exists() {
        return Err(PyValueError::new_err(format!(
            "Input file does not exist: {}",
            input_file.as_path().display()
        )));
    }

    // Create output directory if it doesn't exist
    if !output_dir.exists() {
        fs::create_dir_all(&output_dir).map_err(|e| {
            PyValueError::new_err(format!("Failed to create output directory: {}", e))
        })?;
    }

    // Open the input file
    let input_file = File::open(&input_file)
        .map_err(|e| PyValueError::new_err(format!("Failed to open input file: {}", e)))?;

    // Create a gzip decoder
    let gz_decoder = GzDecoder::new(input_file);

    // Create a tar archive from the gzip decoder
    let mut archive = Archive::new(gz_decoder);

    // Extract all contents to the output directory
    let mut count = 0;

    // Process each entry in the archive
    let entries = archive
        .entries()
        .map_err(|e| PyValueError::new_err(format!("Failed to read archive entries: {}", e)))?;

    for entry in entries {
        let mut entry =
            entry.map_err(|e| PyValueError::new_err(format!("Failed to read entry: {}", e)))?;

        // Get the path of the entry
        let path = entry
            .path()
            .map_err(|e| PyValueError::new_err(format!("Failed to get entry path: {}", e)))?;

        // Create the full path by joining with the output directory
        let output_file_path = output_dir.join(path);

        // Create parent directories if they don't exist
        if let Some(parent) = output_file_path.parent() {
            if !parent.exists() {
                fs::create_dir_all(parent).map_err(|e| {
                    PyValueError::new_err(format!("Failed to create directory: {}", e))
                })?;
            }
        }

        // Extract the file
        entry
            .unpack(&output_file_path)
            .map_err(|e| PyValueError::new_err(format!("Failed to extract file: {}", e)))?;

        count += 1;
    }

    Ok(count)
}
