# Built-in Modules
import typing


# Local Modules
# from quantsapp._models import ApiResponseStatus_Type
from quantsapp import _models as generic_models


# -- Enums -------------------------------------------------------------------------------------------


# -- Typed Dicts -------------------------------------------------------------------------------------

class ApiResponseLogin_Type(typing.TypedDict):
    status: generic_models.ApiResponseStatus_Type
    msg: typing.Optional[str]
    jwt_token: str

# -- Pydantic Models ---------------------------------------------------------------------------------
