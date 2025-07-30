from pydantic_core import PydanticSerializationUnexpectedValue
from pydantic.annotated_handlers import GetCoreSchemaHandler
from pydantic import (
    ValidationError,
    ValidatorFunctionWrapHandler,
    BaseModel,
)
from pydantic_core import core_schema
from pydantic_core.core_schema import (
    CoreSchema,
    SerializationInfo,
    any_schema,
    dict_schema,
    list_schema,
    tuple_schema,
    set_schema,
    bool_schema,
    int_schema,
    str_schema,
    float_schema,
    no_info_after_validator_function,
    no_info_wrap_validator_function,
    plain_serializer_function_ser_schema,
)
