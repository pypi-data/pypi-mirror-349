from datetime import datetime
from typing import Optional
from uuid import UUID

from pydantic import BaseModel, ConfigDict, AliasPath, Field
from pydantic.alias_generators import to_camel


class Mission(BaseModel):
    """
    Mission class returned from the registry API
    """

    model_config = ConfigDict(alias_generator=to_camel)

    #: Mission unique identifier.
    uuid: UUID = Field(validation_alias=AliasPath("@uuid"))

    #: Mission ID.
    id: int

    #: Datetime when the mission was created.
    created: datetime

    #: Datetime when the mission was last modified.
    last_modified: datetime

    #: Mission name.
    name: str

    #: Description.
    description: Optional[str] = None

    #: Datetime when the mission starts.
    start_date: datetime

    #: Datetime when the mission ends.
    end_date: datetime
