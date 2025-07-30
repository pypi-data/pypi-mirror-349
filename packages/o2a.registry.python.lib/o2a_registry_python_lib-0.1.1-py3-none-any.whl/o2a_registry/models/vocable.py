from datetime import datetime
from uuid import UUID

from pydantic import BaseModel, ConfigDict, AliasPath, Field
from pydantic.alias_generators import to_camel

from o2a_registry.models.vocable_group import VocableGroup


class Vocable(BaseModel):
    """
    Vocable returned by the registry API.
    """

    model_config = ConfigDict(alias_generator=to_camel)

    #: Unique identifier of the vocable.
    uuid: UUID = Field(validation_alias=AliasPath("@uuid"))

    #: Vocable ID.
    id: int

    #: Datetime when the vocable was last modified.
    last_modified: datetime

    #: General name of the vocable.
    general_name: str

    #: System name of the vocable.
    system_name: str

    #: Description of the vocable.
    description: str

    #: Vocabulary/Party which defined the vocable.
    vocabulary: str

    #: Vocable concept definition.
    vocable_value: str

    #: The vocable group to which the vocable belongs.
    vocable_group: VocableGroup
