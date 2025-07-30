from datetime import datetime
from typing import Optional

from pydantic import BaseModel, Field, ConfigDict, AliasGenerator
from pydantic.alias_generators import to_camel


class EditMission(BaseModel):
    """
    Mission class to edit an item in the registry.
    """

    model_config = ConfigDict(
        alias_generator=AliasGenerator(serialization_alias=to_camel)
    )

    #: Mission name.
    name: Optional[str] = Field(None, min_length=1)

    #: Description.
    description: Optional[str] = Field(None, min_length=1)

    #: Datetime when the mission starts.
    start_date: Optional[datetime] = None

    #: Datetime when the mission ends.
    end_date: Optional[datetime] = None
