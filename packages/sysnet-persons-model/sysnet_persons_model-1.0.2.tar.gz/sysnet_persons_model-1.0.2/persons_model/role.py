from __future__ import annotations
from typing import Optional, List

from pydantic import BaseModel, StrictStr, Field, StrictInt, StrictBool
from sysnet_pyutils.models.general import ListTypeBase, BaseEnum, MetadataEssentialType

from persons_model.common import RegistryType
from persons_model.tag import TagType


class RoleCategoryEnum(BaseEnum):
    INDIVIDUAL = 'individual'
    PERSONAL = 'personal'
    SECURITY = 'security'
    OTHER = 'other'

class RoleCategoryType(BaseModel):
    """
    Kategorie rolí: osobní, subjektová, bezpečnostní
    """
    individual: Optional[StrictBool] = Field(default=False, description="osobní role")
    personal: Optional[StrictBool] = Field(default=False, description="subjektová role")
    security: Optional[StrictBool] = Field(default=False, description="bezpečnostní role")
    other: Optional[StrictBool] = Field(default=False, description="jiná role")


class RoleBaseType(BaseModel):
    code: Optional[StrictStr] = Field(default=None, description="Kód role")
    name: Optional[StrictStr] = Field(default=None, description="Název role")
    categories: Optional[RoleCategoryType] = Field(default=None, description="Kategorie rolí: osobní, subjektová, bezpečnostní")
    note: Optional[StrictStr] = Field(default=None, description='Libovolná poznámka')


class RoleType(RoleBaseType):
    """
    RoleType
    """
    identifier: Optional[StrictStr] = Field(default=None, description="identifikátor uuid")
    registry: Optional[RegistryType] = Field(default=None, description="registry uuid")
    holders_individual: Optional[List[Optional[StrictStr]]] = Field(default=None, description="Nositelé role - jednotlivci")
    holders_personal: Optional[List[Optional[StrictStr]]] = Field(default=None, description="Nositelé role - osoby")
    admins_individual: Optional[List[Optional[StrictStr]]] = Field(default=None, description="Správci role - jednotlivci")
    admins_personal: Optional[List[Optional[StrictStr]]] = Field(default=None, description="Správci role - osoby")
    tags: Optional[TagType] = Field(default=None, description="Seznam značek")
    document: Optional[MetadataEssentialType] = Field(default=None, description='Metadata')


class RoleListType(ListTypeBase):
    """
    Seznam vrácených rolí
    """
    hits: Optional[StrictInt] = Field(default=None, description="celkový počet vybraných položek")
    entries: Optional[List[Optional[RoleBaseType]]] = Field(default=None, description='Seznam položek')


class RoleEntryType(RoleBaseType):
    """
    Položka seznamu rolí v kontextu
    """
    identifier: Optional[StrictStr] = Field(default=None, description="identifikátor uuid")
