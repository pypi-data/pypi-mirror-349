from datetime import datetime
from typing import Optional

from pydantic import BaseModel, Field, ConfigDict, AliasGenerator
from pydantic.alias_generators import to_camel


class CreateMission(BaseModel):
    """
    Mission class to create a new contact in the registry.
    """

    model_config = ConfigDict(
        alias_generator=AliasGenerator(serialization_alias=to_camel)
    )

    #: Mission name.
    name: str = Field(..., min_length=1)

    #: Description.
    description: Optional[str] = Field(None, min_length=1)

    #: Datetime when the mission starts.
    start_date: datetime

    #: Datetime when the mission ends.
    end_date: datetime
