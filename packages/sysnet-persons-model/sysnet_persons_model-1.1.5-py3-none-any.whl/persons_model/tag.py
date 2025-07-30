from __future__ import annotations

from typing import List, Optional

from pydantic import BaseModel, Field
from sysnet_pyutils.models.general import ListTypeBase


class TagItemType(BaseModel):
    """
    Značka
    """
    tag: Optional[str] = Field(default=None, description="Vlastní značka (Permity, RL, Stanoviska)")
    color: Optional[str] = Field(default=None, description="HTML kód barvy tagu")


class TagListType(ListTypeBase):
    """
    Seznam vrácených tagů
    """
    hits: Optional[int] = Field(default=None, description="celkový počet vybraných položek")
    entries: Optional[List[Optional[TagItemType]]] = None


class TagType(BaseModel):
    """
    Seznam tagů v datovém objektu
    """
    taglist: Optional[List[Optional[TagItemType]]] = None
