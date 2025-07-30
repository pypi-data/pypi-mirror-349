use anyhow::Result;
use pyo3::prelude::*;
use pyo3::types::{PyBool, PyDict, PyFloat, PyInt, PyList, PyString};
use pyo3::{PyObject, PyResult, Python};
use quick_xml::de::from_str;
use serde_json::Value as JsonValue;
use std::fs;
use std::path::PathBuf;

/// Reads an XML file from the given path and returns a Python dictionary
/// representing the root element.
///
/// # Errors
///
/// If the file could not be read, or if the XML could not be parsed,
/// an error is returned.
///
/// If the root element is not an object, an error is returned.
pub fn xml_to_py(py: Python<'_>, path: &str) -> PyResult<Py<PyDict>> {
    match read_xml_to_json(&PathBuf::from(path)) {
        Ok(json) => match json {
            JsonValue::Object(map) => {
                let dict = PyDict::new(py);
                for (k, v) in map.into_iter() {
                    dict.set_item(k, json_value_to_py(py, v)?)?;
                }
                Ok(dict.into())
            }
            _ => Err(pyo3::exceptions::PyValueError::new_err(
                "XML root is not an object".to_string(),
            )),
        },
        Err(e) => Err(pyo3::exceptions::PyValueError::new_err(e.to_string())),
    }
}

/// Reads an XML file from the given path and returns its contents as JSON.
///
/// # Errors
///
/// If the file could not be read, or if the XML could not be parsed,
/// an error is returned.
fn read_xml_to_json(path: &PathBuf) -> Result<JsonValue> {
    let content = fs::read_to_string(path)?;
    let json: JsonValue = from_str(&content)?;
    Ok(json)
}

/// Converts a serde_json::Value into a Python object.
///
/// # Errors
///
/// If the JSON value is a number that can't be converted to an i64, u64, or f64,
/// an error is returned.
fn json_value_to_py(py: Python<'_>, v: JsonValue) -> PyResult<PyObject> {
    match v {
        JsonValue::Null => Ok(py.None()),
        JsonValue::Bool(b) => Ok(PyBool::new(py, b).to_owned().into()),
        JsonValue::Number(n) => {
            if let Some(i) = n.as_i64() {
                Ok(PyInt::new(py, i).into())
            } else if let Some(u) = n.as_u64() {
                Ok(PyInt::new(py, u as i64).into())
            } else if let Some(f) = n.as_f64() {
                Ok(PyFloat::new(py, f).into())
            } else {
                Err(pyo3::exceptions::PyValueError::new_err(
                    "Unsupported number type".to_string(),
                ))
            }
        }
        JsonValue::String(s) => Ok(PyString::new(py, &s).into()),
        JsonValue::Array(arr) => {
            let list = PyList::empty(py);
            for v in arr {
                list.append(json_value_to_py(py, v)?)?;
            }
            Ok(list.into())
        }
        JsonValue::Object(map) => {
            let dict = PyDict::new(py);
            for (k, v) in map {
                dict.set_item(k, json_value_to_py(py, v)?)?;
            }
            Ok(dict.into())
        }
    }
}
