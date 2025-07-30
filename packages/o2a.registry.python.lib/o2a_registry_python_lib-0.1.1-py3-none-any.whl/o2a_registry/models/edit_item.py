from typing import Optional, Union

from pydantic import BaseModel, ConfigDict, AliasGenerator, Field
from pydantic.alias_generators import to_camel

from o2a_registry.models.workflow import MountWorkflow, UnMountWorkflow


class EditItem(BaseModel):
    """
    Item class to edit an item in the registry.
    """

    model_config = ConfigDict(
        alias_generator=AliasGenerator(serialization_alias=to_camel)
    )

    #: Short name of the item. Should be unique.
    short_name: Optional[str] = None

    #: Long name of the item.
    long_name: Optional[str] = None

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

    #: handle.net handle (not a URL itself).
    citation: Optional[str] = None

    #: ID of the item on which the item is mounted. Is zero, if the item is not mounted.
    parent_id: int = 0

    #: ID of the item's status.
    status_id: Optional[int] = Field(None, gt=0)

    #: ID of the item's type.
    type_id: Optional[int] = Field(None, gt=0)

    #: If set, creates a mount/unmount event. Should be specified, if the :py:attr:`~parent_id` is changed.
    workflow: Optional[Union[MountWorkflow, UnMountWorkflow]] = None
