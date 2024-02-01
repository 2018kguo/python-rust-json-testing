# # Run maturin develop in venv first
import sys

import time

from dataclasses import asdict, dataclass
import orjson as json
from pydantic import BaseModel
from datetime import datetime

from typing import Union, Optional


# #[derive(Serialize, Deserialize)]
# pub struct MyStruct {
#     pub list_field1: Vec<FieldOneStruct>,
#     pub list_field2: Vec<FieldTwoStruct>
# }   

# #[derive(Serialize, Deserialize)]
# pub struct FieldOneStruct {
#     pub field1str: String,
#     pub field1int: i32,
#     pub field1float: f32,
#     pub field1bool: bool,
#     pub field1list: Vec<String>,
#     pub field1dict: Vec<Value>,
# }

# #[derive(Serialize, Deserialize)]

# pub struct FieldTwoStruct {
#     pub field2str: String,
#     pub field2int: i32,
#     pub field2float: f32,
#     pub field2bool: bool,
#     pub field2list: Vec<String>,
#     pub field2dict: Vec<Value>,
# }


@dataclass
class MyStruct:
    list_field1: list
    list_field2: list

@dataclass
class FieldOneStruct:
    field1str: str
    field1int: int
    field1float: float
    field1bool: bool
    field1list: list
    field1dict: list[dict]

@dataclass
class FieldTwoStruct:
    field2str: str
    field2int: int
    field2float: float
    field2bool: bool
    field2list: list
    field2dict: list[dict]


class FieldOneStructPydantic(BaseModel):
    field1str: str
    field1int: int
    field1float: float
    field1bool: bool
    field1list: list
    field1dict: list[dict]

class FieldTwoStructPydantic(BaseModel):
    field2str: str
    field2int: int
    field2float: float
    field2bool: bool
    field2list: list
    field2dict: list[dict]


class MyStructPydantic(BaseModel):
    list_field1: list[FieldOneStructPydantic]
    list_field2: list[FieldTwoStructPydantic]


def dataclass_to_dict(obj):
    if isinstance(obj, MyStruct):
        return {
            "list_field1": [dataclass_to_dict(item) for item in obj.list_field1],
            "list_field2": [dataclass_to_dict(item) for item in obj.list_field2],
        }
    if isinstance(obj, (FieldOneStruct, FieldTwoStruct)):
        return asdict(obj)
    elif isinstance(obj, list):
        return [dataclass_to_dict(item) for item in obj]
    elif isinstance(obj, dict):
        return {key: dataclass_to_dict(value) for key, value in obj.items()}
    else:
        return obj


def dict_to_mystruct_dataclass(dict):
    return MyStruct(
        list_field1=[dict_to_field1_dataclass(item) for item in dict["list_field1"]],
        list_field2=[dict_to_field2_dataclass(item) for item in dict["list_field2"]],
    )

def dict_to_field1_dataclass(dict):
    return FieldOneStruct(
        field1str=dict["field1str"],
        field1int=dict["field1int"],
        field1float=dict["field1float"],
        field1bool=dict["field1bool"],
        field1list=dict["field1list"],
        field1dict=dict["field1dict"],
    )

def dict_to_field2_dataclass(dict):
    return FieldTwoStruct(
        field2str=dict["field2str"],
        field2int=dict["field2int"],
        field2float=dict["field2float"],
        field2bool=dict["field2bool"],
        field2list=dict["field2list"],
        field2dict=dict["field2dict"],
    )

LIST_SIZE = 5000

dict = {
    "list_field1": [
        {
            "field1str": "hello",
            "field1int": 1,
            "field1float": 1.0,
            "field1bool": True,
            "field1list": ["hello", "world"],
            "field1dict": [{"hello": "world"}],
        } for _ in range(LIST_SIZE)
    ],
    "list_field2": [
        {
            "field2str": "hello",
            "field2int": 1,
            "field2float": 1.0,
            "field2bool": True,
            "field2list": ["hello", "world"],
            "field2dict": [{"hello": "world"}],
        } for _ in range(LIST_SIZE)
    ],
}

# dict_json_string = json.dumps(dict)
# with open("test.json", "w") as f:
#     f.write(dict_json_string.decode("utf-8"))

dict_json_string = open("test.json", "r").read()

start = time.time()

# regular dataclasses
for i in range(0, 100):
    json_data = json.loads(dict_json_string)
    struct = dict_to_mystruct_dataclass(json_data)
    deserialized_data = dataclass_to_dict(struct)
    json_str = json.dumps(deserialized_data).decode("utf-8")
end = time.time()
print("Time taken for attr in python with regular dataclasses: ", end - start)

# pydantic
start = time.time()
for i in range(0, 100):
    json_data = json.loads(dict_json_string)
    struct = MyStructPydantic(
        list_field1=[FieldOneStructPydantic(**item) for item in json_data["list_field1"]],
        list_field2=[FieldTwoStructPydantic(**item) for item in json_data["list_field2"]],
    )
    deserialized_data = str(struct.model_dump_json())
end = time.time()
print("Time taken for attr in python with pydantic: ", end - start)



# start = time.time()
# test = eval("my_struct" + raw_str)
# end = time.time()
# print("Time taken for attr in rust: ", end - start)

# start = time.time()
# my_struct = pyo3_example.from_json(nested_json)
# end = time.time()
# print("Time taken for rust load: ", end - start)



# print("Time taken: ", end - start)





# json_str = """{
#     "field1": "hello",
#     "nested_struct": {
#         "field2": "world",
#         "nested": {
#             "field1": "hello"
#         }
#     }
# }"""
# my_struct = pyo3_example.from_json(json_str)
# my_struct.update_nested_struct_field("test")
# new_json_str = pyo3_example.to_json(my_struct)
# assert new_json_str == """{"field1":"hello","nested_struct":{"field2":"test","nested":{"field1":"hello","nested_struct":null}}}"""






# start = time.time()
# json_data = json.loads(json_str)
# deserialized_data = from_json(json_data)
# end = time.time()
# print("Time taken for python load: ", end - start)


# start = time.time()
# my_struct = pyo3_example.from_json(json_str)
# end = time.time()
# print("Time taken for rust load: ", end - start)