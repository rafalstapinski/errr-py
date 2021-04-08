from typing import Any, Dict, List, Optional, Union

from pydantic import BaseModel


class PythonEntity(BaseModel):
    name: str
    value: str
    type: str


class Frame(BaseModel):
    lineno: int
    source: str
    filename: str
    locals: List[PythonEntity]


class Error(BaseModel):
    type: str
    value: str
    lineno: int


class Report(BaseModel):
    stack: List[Frame]
    error: Error
