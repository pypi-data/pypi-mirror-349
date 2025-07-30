from datetime import datetime
from typing import Optional
from uuid import UUID

from pydantic import BaseModel, ConfigDict, AliasPath, Field
from pydantic.alias_generators import to_camel


class ItemReference(BaseModel):
    """
    Reference to an item in the registry.
    """

    model_config = ConfigDict(alias_generator=to_camel)

    #: Unique identifier for the reference.
    uuid: UUID = Field(validation_alias=AliasPath("@uuid"))

    #: ID of the reference.
    id: int

    #: Item ID.
    item_id: int

    #: Datetime when the reference was created.
    created: Optional[datetime] = None

    #: Datetime when the reference was last modified.
    last_modified: datetime
