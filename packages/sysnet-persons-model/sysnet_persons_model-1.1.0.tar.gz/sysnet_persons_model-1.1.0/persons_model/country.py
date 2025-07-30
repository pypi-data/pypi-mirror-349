from __future__ import annotations

from typing import Optional

from pydantic import BaseModel, Field
from pydantic.v1 import StrictStr, StrictInt


class CountryType(BaseModel):
    code_n3: Optional[StrictInt] = Field(default=None, description="ISO 3166-1 numeric-3", examples=[4])
    code_a2: Optional[StrictStr] = Field(default=None, description="ISO 3166-1 alpha-2", examples=["AF"])
    code_a3: Optional[StrictStr] = Field(default=None, description="ISO 3166-1 alpha-3", examples=["AFG"])
    value_cz_full: Optional[StrictStr] = Field(default=None, description='Úplný český název státu', examples=['Afghánská islámská republika'])
    value_cz_short: Optional[StrictStr] = Field(default=None, description='Krátký český název státu', examples=['Afghánistán'])
    value_en_full: Optional[StrictStr] = Field(default=None, description='Úplný anglický název státu', examples=['the Islamic Republic of Afghanistan'])
    value_en_short: Optional[StrictStr] = Field(default=None, description='Krátký anglický název státu', examples=['Afghanistan'])
