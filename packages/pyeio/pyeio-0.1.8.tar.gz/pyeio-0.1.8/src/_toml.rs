use pyo3::prelude::*;
use pyo3::types::{PyAny, PyDict, PyList, PyString, PyTuple};
use toml::Value as TomlValue;

/// Loads TOML from a string.
#[pyfunction]
fn loads(py: Python, s: &str) -> PyResult<PyObject> {
    match s.parse::<TomlValue>() {
        Ok(value) => toml_value_to_pyobject(py, value),
        Err(e) => Err(PyErr::new::<pyo3::exceptions::PyValueError, _>(
            e.to_string(),
        )),
    }
}

/// Loads TOML from a file-like object.
#[pyfunction]
fn load(py: Python, f: &PyAny) -> PyResult<PyObject> {
    let read_method = f.getattr("read")?;
    let s: String = read_method.call0()?.extract()?;
    loads(py, &s)
}

/// Dumps Python object to a TOML string.
#[pyfunction]
fn dumps(py: Python, obj: &PyAny) -> PyResult<String> {
    let value = pyobject_to_toml_value(obj)?;
    match toml::to_string(&value) {
        Ok(s) => Ok(s),
        Err(e) => Err(PyErr::new::<pyo3::exceptions::PyValueError, _>(
            e.to_string(),
        )),
    }
}

/// Dumps Python object to a file-like object as TOML.
#[pyfunction]
fn dump(py: Python, obj: &PyAny, f: &PyAny) -> PyResult<()> {
    let s = dumps(py, obj)?;
    let write_method = f.getattr("write")?;
    write_method.call1((s,))?;
    Ok(())
}

/// Converts TOML Value to Python object.
fn toml_value_to_pyobject(py: Python, value: TomlValue) -> PyResult<PyObject> {
    match value {
        TomlValue::String(s) => Ok(PyString::new(py, &s).into()),
        TomlValue::Integer(i) => Ok(i.into_py(py)),
        TomlValue::Float(f) => Ok(f.into_py(py)),
        TomlValue::Boolean(b) => Ok(b.into_py(py)),
        TomlValue::Datetime(dt) => Ok(PyString::new(py, &dt.to_string()).into()),
        TomlValue::Array(arr) => {
            let list = PyList::empty(py);
            for item in arr {
                list.append(toml_value_to_pyobject(py, item)?)?;
            }
            Ok(list.into())
        }
        TomlValue::Table(table) => {
            let dict = PyDict::new(py);
            for (k, v) in table {
                dict.set_item(k, toml_value_to_pyobject(py, v)?)?;
            }
            Ok(dict.into())
        }
    }
}

/// Converts Python object to TOML Value.
fn pyobject_to_toml_value(obj: &PyAny) -> PyResult<TomlValue> {
    if let Ok(s) = obj.extract::<String>() {
        Ok(TomlValue::String(s))
    } else if let Ok(i) = obj.extract::<i64>() {
        Ok(TomlValue::Integer(i))
    } else if let Ok(f) = obj.extract::<f64>() {
        Ok(TomlValue::Float(f))
    } else if let Ok(b) = obj.extract::<bool>() {
        Ok(TomlValue::Boolean(b))
    } else if obj.is_instance_of::<PyList>()? || obj.is_instance_of::<PyTuple>()? {
        let seq = obj.downcast::<pyo3::types::PySequence>()?;
        let mut arr = Vec::new();
        for item in seq.iter()? {
            arr.push(pyobject_to_toml_value(item?)?);
        }
        Ok(TomlValue::Array(arr))
    } else if obj.is_instance_of::<PyDict>()? {
        let dict = obj.downcast::<PyDict>()?;
        let mut table = toml::map::Map::new();
        for (key, value) in dict {
            let key_str = key.extract::<String>()?;
            table.insert(key_str, pyobject_to_toml_value(value)?);
        }
        Ok(TomlValue::Table(table))
    } else {
        Err(PyErr::new::<pyo3::exceptions::PyTypeError, _>(
            "Unsupported type",
        ))
    }
}

/// Module definition
#[pymodule]
fn toml_ext(py: Python, m: &PyModule) -> PyResult<()> {
    m.add_function(wrap_pyfunction!(load, m)?)?;
    m.add_function(wrap_pyfunction!(loads, m)?)?;
    m.add_function(wrap_pyfunction!(dump, m)?)?;
    m.add_function(wrap_pyfunction!(dumps, m)?)?;
    Ok(())
}
