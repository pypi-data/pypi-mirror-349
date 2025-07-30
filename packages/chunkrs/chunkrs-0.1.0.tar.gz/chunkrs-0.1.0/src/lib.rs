use pyo3::prelude::*;

mod cli;
mod decompress;
mod downloader;
mod utils;

#[pymodule]
fn chunkrs(m: &Bound<'_, PyModule>) -> PyResult<()> {
    m.add_function(wrap_pyfunction!(decompress::decompress_tarball, m)?)?;
    m.add_function(wrap_pyfunction!(downloader::download, m)?)?;
    m.add_function(wrap_pyfunction!(cli::cli_main, m)?)?;
    Ok(())
}
