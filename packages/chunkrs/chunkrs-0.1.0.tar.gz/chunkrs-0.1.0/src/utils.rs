use anyhow::Error;
use pyo3::{exceptions::PyRuntimeError, PyErr};

/// Conditionally prints a message if the verbose flag is true
#[macro_export]
macro_rules! verbose_println {
    ($verbose:expr, $($arg:tt)*) => {
        if $verbose {
            println!($($arg)*);
        }
    };
}

pub use crate::verbose_println;

pub fn to_pyerr(err: Error) -> PyErr {
    PyErr::new::<PyRuntimeError, _>(err.to_string())
}
