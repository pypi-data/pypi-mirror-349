from __future__ import annotations

from typing import Optional, List

from pydantic import BaseModel, Field
from pydantic.v1 import StrictStr, StrictInt
from sysnet_pyutils.models.general import ListTypeBase, CodeValueType


class CountryType(BaseModel):
    code_n3: Optional[StrictInt] = Field(default=None, description="ISO 3166-1 numeric-3", examples=[4])
    code_a2: Optional[StrictStr] = Field(default=None, description="ISO 3166-1 alpha-2", examples=["AF"])
    code_a3: Optional[StrictStr] = Field(default=None, description="ISO 3166-1 alpha-3", examples=["AFG"])
    value_cz_full: Optional[StrictStr] = Field(default=None, description='Úplný český název státu', examples=['Afghánská islámská republika'])
    value_cz_short: Optional[StrictStr] = Field(default=None, description='Krátký český název státu', examples=['Afghánistán'])
    value_en_full: Optional[StrictStr] = Field(default=None, description='Úplný anglický název státu', examples=['the Islamic Republic of Afghanistan'])
    value_en_short: Optional[StrictStr] = Field(default=None, description='Krátký anglický název státu', examples=['Afghanistan'])


class CountryListType(ListTypeBase):
    """
    Seznam vrácených zemí
    """
    hits: Optional[int] = Field(default=None, description="celkový počet vybraných položek")
    entries: Optional[List[Optional[CountryType]]] = Field(default=None, description='Seznam položek')


class CountryMapType(ListTypeBase):
    """
    Seznam vrácených zemí (code/value)
    """
    hits: Optional[int] = Field(default=None, description="celkový počet vybraných položek")
    entries: Optional[List[Optional[CodeValueType]]] = Field(default=None, description='Seznam položek')
