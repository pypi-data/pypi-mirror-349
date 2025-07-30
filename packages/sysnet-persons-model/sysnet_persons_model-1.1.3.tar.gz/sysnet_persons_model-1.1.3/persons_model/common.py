from __future__ import annotations

from datetime import datetime
from typing import List, Optional

from pydantic import BaseModel, Field, StrictStr, StrictBool, StrictInt
from sysnet_pyutils.models.general import LocationType, PhoneNumberType, MailAddressType, BaseEnum

from persons_model.tag import TagType


class RegistryEnum(BaseEnum):
    CRZP = 'crzp'


class RegistryType(BaseModel):
    """
    Reference na identifikační údaje
    """
    name: Optional[RegistryEnum] = Field(default=RegistryEnum.CRZP, description="Název identifikační služby (CRŽP, Google, Facebook, ...)")
    uuid: Optional[StrictStr] = Field(default=None, description="identifikátor uuid")
    uri: Optional[StrictStr] = Field(default=None, description="identifikátor uri")
    other: Optional[StrictStr] = Field(default=None, description="Jiný identifikátor")
    date_synchronized: Optional[datetime] = Field(default=None, description="Datum a čas")

    @property
    def identifier(self) -> StrictStr:
        return self.uuid or self.uri or self.other

class RedundantType(BaseModel):
    """
    Redundantní záznam
    """ # noqa: E501
    name: Optional[StrictStr] = Field(default=None, description="Název útvaru")
    code: Optional[StrictStr] = Field(default=None, description="Kód útvaru")
    location: Optional[LocationType] = Field(default=None, description='Lokalita')
    note: Optional[StrictStr] = Field(default=None, description="Libovolná poznámka")


class DepartmentType(RedundantType):
    """
    Útvar organizace
    """ # noqa: E501
    parent: Optional[StrictStr] = Field(default=None, description="Nadřízený subjekt")


class ContactType(BaseModel):
    """
    Kontaktní údaje
    """ # noqa: E501
    identifier: Optional[StrictStr] = Field(default=None, description="identifikátor uuid")
    first_name: Optional[StrictStr] = Field(default=None, description="Křestní jméno")
    last_name: Optional[StrictStr] = Field(default=None, description="Příjmení")
    degree_before: Optional[List[Optional[StrictStr]]] = Field(default=None, description="Tituly před jménem")
    degree_after: Optional[List[Optional[StrictStr]]] = Field(default=None, description="Tituly za jménem")
    full_name: Optional[StrictStr] = Field(default=None, description="Celé jméno pro zobrazení a tisk")
    birthdate: Optional[datetime] = Field(default=None, description="Datum narození")
    phone: Optional[List[Optional[PhoneNumberType]]] = Field(default=None, description="Telefonní číslo")
    phone_default: Optional[StrictInt] = Field(default=0, description="Index hlavního telefonního čísla", alias="phoneDefault")
    email: Optional[List[Optional[MailAddressType]]] = Field(default=None, description="Elektronická pošta")
    email_default: Optional[StrictInt] = Field(default=0, description="Index hlavní adresy elektronické pošty")
    web: Optional[StrictStr] = Field(default=None, description="Webová stránka subjektu")
    isds: Optional[StrictStr] = Field(default=None, description="Identifikátor datové schránky")
    reference: Optional[StrictStr] = Field(default=None, description="identifikátor uuid")


class MemberType(BaseModel):
    """
    Členský záznam
    """ # noqa: E501
    identifier: Optional[StrictStr] = Field(default=None, description="identifikátor uuid")
    is_person: Optional[StrictBool] = Field(default=False, description="Typ členského záznamu (individual/person)")
    name: Optional[StrictStr] = Field(default=None, description="Název, jméno člena")
    membership: Optional[MembershipEnum] = Field(default=None, description="Typ členství (admin/representative/employee)")


class IssuingType(BaseModel):
    """
    Údaje pro vydávání dokladů
    """
    code: Optional[StrictStr] = Field(default=None, description="Kód vydavatele, kterým se rozliší například detašovaná pracoviště")
    tags: Optional[TagType] = Field(default=None, description='Seznam tagů')
    representative: Optional[StrictStr] = Field(default=None, description="Statutární zástupce vydávajícího orgánu")
    authority: Optional[StrictStr] = Field(default=None, description="Vydávající výkonný orgán")
    place: Optional[StrictStr] = Field(default=None, description="Místo vydání dokumentu")
    note: Optional[StrictStr] = Field(default=None, description="Poznámka")


class MembershipEnum(BaseEnum):
    # Typ členství (admin/representative/employee)
    ADMIN = 'admin'     # Správce subjektu
    REPRESENTATIVE = 'representative'   # Statutární zástupce subjektu
    EMPLOYEE = 'employee'   # Zaměstnanec
    DEPARTMENT = 'department'   # Organizační jednotka
    GENERAL = 'general'     # Obecné členství (např. partner, externista)
    OTHER = 'other'         # Jiné
    NONE = ''
