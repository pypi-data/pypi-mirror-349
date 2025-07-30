from datetime import datetime
from typing import Optional
from uuid import UUID

from pydantic import BaseModel, ConfigDict, AliasPath, Field
from pydantic.alias_generators import to_camel

from o2a_registry.models.item_state import ItemState
from o2a_registry.models.vocable import Vocable


class Item(BaseModel):
    """
    Item class returned from the registry API
    """

    model_config = ConfigDict(alias_generator=to_camel)

    #: Item unique identifier.
    uuid: UUID = Field(validation_alias=AliasPath("@uuid"))

    #: Item ID.
    id: int

    #: Datetime when the item was created in the registry.
    created: Optional[datetime] = None

    #: Datetime when the item was last modified in the registry.
    last_modified: datetime

    #: Identifier code of the item. Follows the template "type.system_name:short_name".
    code: str

    #: Short name of the item. Should be unique.
    short_name: str

    #: Long name of the item.
    long_name: str

    #: handle.net handle (not a URL itself).
    citation: Optional[str] = None

    #: Item status.
    status: ItemState

    #: Item type.
    type: Vocable

    #: Description.
    description: Optional[str] = None

    #: Item model name.
    model: Optional[str] = None

    #: Item manufacturer name.
    manufacturer: Optional[str] = None

    #: Item serial number.
    serial_number: Optional[str] = None

    #: Instructions how to operate the item.
    operation_instructions: Optional[str] = None

    #: Inventory number.
    inventory_number: Optional[str] = None

    #: ID of the item on which the item is mounted. Is zero, if the item is not mounted.
    parent_id: int = 0
