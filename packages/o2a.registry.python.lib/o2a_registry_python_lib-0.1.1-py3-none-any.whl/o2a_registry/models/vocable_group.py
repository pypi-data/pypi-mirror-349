from uuid import UUID

from pydantic import BaseModel, ConfigDict, AliasPath, Field
from pydantic.alias_generators import to_camel


class VocableGroup(BaseModel):
    """
    Vocable group returned by the registry API.
    """

    model_config = ConfigDict(alias_generator=to_camel)

    #: Unique identifier of the vocable.
    uuid: UUID = Field(validation_alias=AliasPath("@uuid"))

    #: Vocable group ID.
    id: int

    #: Vocable group name.
    name: str

    #: Vocable group system name.
    system_name: str
