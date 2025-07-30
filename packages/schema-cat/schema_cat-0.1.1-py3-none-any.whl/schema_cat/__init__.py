"""schema-cat: A Python library for typed prompts."""
import logging
from typing import Type

from pydantic import BaseModel

logger = logging.getLogger("schema_cat")


def hello_world():
    """Entry function that returns 'Hello World'."""
    return "Hello World"


def schema_to_xml(schema):
    pass


def prompt_with_schema(prompt: str, schema: Type[BaseModel]) -> BaseModel:
    xml: str = schema_to_xml(schema)
    pass
