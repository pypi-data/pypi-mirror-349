use anyhow::Result;
use pyo3::prelude::*;
use pyo3::types::{PyBool, PyDict, PyFloat, PyInt, PyList, PyString};
use pyo3::{PyObject, PyResult, Python};
use std::collections::HashMap;
use std::fs;
use std::path::PathBuf;
use toml::Value as Toml;

/// Reads a TOML file from the given path and returns a Python dictionary
/// representing the top-level keys.
///
/// # Errors
///
/// If the file could not be read, or if the TOML could not be parsed,
/// an error is returned.
pub fn toml_to_py(py: Python<'_>, path: &str) -> PyResult<Py<PyDict>> {
    match read_toml_to_hashmap(&PathBuf::from(path)) {
        Ok(map) => {
            let dict = PyDict::new(py);
            for (k, v) in map.into_iter() {
                dict.set_item(k, toml_value_to_py(py, v)?)?;
            }
            Ok(dict.into())
        }
        Err(e) => Err(pyo3::exceptions::PyValueError::new_err(e.to_string())),
    }
}

/// Reads a TOML file from the given path and returns a HashMap of its top-level
/// keys to TOML values.
///
/// # Errors
///
/// If the file could not be read, or if the TOML could not be parsed,
/// an error is returned.
fn read_toml_to_hashmap(path: &PathBuf) -> Result<HashMap<String, Toml>> {
    let content = fs::read_to_string(path)?;
    let value: Toml = content.parse()?;

    let mut map = HashMap::new();
    for (key, value) in value.as_table().unwrap().iter() {
        map.insert(key.to_string(), value.clone());
    }

    Ok(map)
}

/// Converts a toml::Value to a Python object.
///
/// # Errors
///
/// If the toml::Value is not one of the supported types, an error is returned.
///
/// The supported types are:
///
/// - `Toml::String`: Corresponds to Python's `str`
/// - `Toml::Integer`: Corresponds to Python's `int`
/// - `Toml::Float`: Corresponds to Python's `float`
/// - `Toml::Boolean`: Corresponds to Python's `bool`
/// - `Toml::Array`: Corresponds to Python's `list`
/// - `Toml::Table`: Corresponds to Python's `dict`
fn toml_value_to_py(py: Python<'_>, v: Toml) -> PyResult<PyObject> {
    match v {
        Toml::String(s) => Ok(PyString::new(py, s.as_str()).into()),
        Toml::Integer(i) => Ok(PyInt::new(py, i).into()),
        Toml::Float(f) => Ok(PyFloat::new(py, f).into()),
        Toml::Boolean(b) => Ok(PyBool::new(py, b).to_owned().into()),
        Toml::Array(a) => {
            let list = PyList::empty(py);
            for v in a {
                list.append(toml_value_to_py(py, v)?)?;
            }
            Ok(list.into())
        }
        Toml::Table(t) => {
            let dict = PyDict::new(py);
            for (k, v) in t {
                dict.set_item(k, toml_value_to_py(py, v)?)?;
            }
            Ok(dict.into())
        }
        _ => Err(pyo3::exceptions::PyValueError::new_err(
            "Unsupported TOML value type".to_string(),
        )),
    }
}
