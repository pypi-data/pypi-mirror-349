from datetime import datetime
from uuid import UUID

from pydantic import BaseModel, ConfigDict, AliasPath, Field
from pydantic.alias_generators import to_camel


class ItemState(BaseModel):
    """
    State of an item returned by the registry API.
    """

    model_config = ConfigDict(alias_generator=to_camel)

    #: Unique identifier of the state.
    uuid: UUID = Field(validation_alias=AliasPath("@uuid"))

    #: ID of the state.
    id: int

    #: Datetime when the state was last modified.
    last_modified: datetime

    #: Name of the state.
    name: str

    #: Description of the state.
    meta: str
