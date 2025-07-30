from datetime import datetime

from pydantic import BaseModel, ConfigDict, AliasGenerator, Field
from pydantic.alias_generators import to_camel


class MountWorkflow(BaseModel):
    """
    Class to automatically create a mount event, when editing or creating an item with :py:class:`o2a_registry.models.EditItem` or :py:class:`o2a_registry.models.EditItem`.
    """

    model_config = ConfigDict(
        alias_generator=AliasGenerator(serialization_alias=to_camel)
    )

    #: Label of the mount event.
    mount_label: str = Field(..., min_length=1)

    #: Datetime when the item was/is mounted.
    mount_date: datetime

    #: If a version should be automatically created for the item.
    version: bool = False


class UnMountWorkflow(BaseModel):
    """
    Class to automatically create a mount event, when editing or creating an item with :py:class:`o2a_registry.models.EditItem` or :py:class:`o2a_registry.models.EditItem`.
    """

    model_config = ConfigDict(
        alias_generator=AliasGenerator(serialization_alias=to_camel)
    )

    #: Label of the mount event.
    unmount_label: str = Field(..., min_length=1)

    #: Datetime when the item was/is mounted.
    unmount_date: datetime

    #: If a version should be automatically created for the item.
    version: bool = False
