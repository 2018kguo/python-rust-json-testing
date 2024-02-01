use rayon::prelude::*;
use std::fs;
use std::io;

// use pyo3::prelude::*;
// use pyo3::exceptions::PyValueError;
use serde::{Deserialize, Serialize};
use serde_json::Value;
// use serde_json::Value;

#[derive(Serialize, Deserialize)]
pub struct MyStruct {
    pub list_field1: Vec<FieldOneStruct>,
    pub list_field2: Vec<FieldTwoStruct>
}   

#[derive(Serialize, Deserialize)]
pub struct FieldOneStruct {
    pub field1str: String,
    pub field1int: i32,
    pub field1float: f32,
    pub field1bool: bool,
    pub field1list: Vec<String>,
    pub field1dict: Vec<Value>,
}

#[derive(Serialize, Deserialize)]

pub struct FieldTwoStruct {
    pub field2str: String,
    pub field2int: i32,
    pub field2float: f32,
    pub field2bool: bool,
    pub field2list: Vec<String>,
    pub field2dict: Vec<Value>,
}

#[cfg(test)]
mod tests {
    use std::time::Instant;

    use super::*;

    #[test]
    fn test_nested_deserialization() {
        let filename = "test.json";
        let json_str = fs::read_to_string(filename).unwrap();
        
        let start = Instant::now();
        let num_threads = rayon::current_num_threads();
        println!("Number of threads: {}", num_threads);
        (0..100).into_par_iter().for_each(|_| {
            let value: MyStruct = serde_json::from_str(&json_str).unwrap();
            let _json_str = serde_json::to_string(&value).unwrap();
            // Do something with json_str if needed
        });
        let duration = start.elapsed();
        println!("my_function took with rayon {:?}", duration);

        let start = Instant::now();
        for i in 0..100 {
            let mut value: MyStruct = serde_json::from_str(&json_str).unwrap();
            let _json_str = serde_json::to_string(&value).unwrap();
        }
        let duration = start.elapsed();
        println!("my_function took without rayon {:?}", duration);
    }
}