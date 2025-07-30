mod bib_tools;
mod typst_tools;

use pyo3::prelude::*;
use pyo3_log::init;

/// A Python module implemented in Rust. The name of this function must match
/// the `lib.name` setting in the `Cargo.toml`, else Python will not be able to
/// import the module.
#[pymodule]
#[pyo3(name = "rust")]
fn rust(python: Python, m: &Bound<'_, PyModule>) -> PyResult<()> {
    init();

    bib_tools::register(python, m)?;
    typst_tools::register(python, m)?;
    Ok(())
}
