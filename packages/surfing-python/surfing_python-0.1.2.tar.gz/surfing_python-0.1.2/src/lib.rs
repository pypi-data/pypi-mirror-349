use pyo3::{exceptions::PyValueError, prelude::*};

/// Extract a json from a text
#[pyfunction]
pub fn extract_json_to_string(input: &str) -> PyResult<String> {
    match surfing::extract_json_to_string(input) {
        Ok(result) => Ok(result),
        Err(error) => Err(
            PyValueError::new_err(error.to_string())
        ),
    }
}

/// A Python module implemented in Rust.
#[pymodule]
fn surfing_python(m: &Bound<'_, PyModule>) -> PyResult<()> {
    m.add_function(wrap_pyfunction!(extract_json_to_string, m)?)?; 
    Ok(())
}
