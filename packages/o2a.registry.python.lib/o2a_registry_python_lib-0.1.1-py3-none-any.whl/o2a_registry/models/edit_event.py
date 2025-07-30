from datetime import datetime
from typing import Optional

from pydantic import BaseModel, ConfigDict, AliasGenerator, Field
from pydantic.alias_generators import to_camel


class EditEvent(BaseModel):
    """
    Event class for editing an event in the registry.
    """

    model_config = ConfigDict(
        alias_generator=AliasGenerator(serialization_alias=to_camel)
    )

    #: Datetime when the event starts.
    start_date: Optional[datetime] = None

    #: Datetime when the event stops.
    end_date: Optional[datetime] = None

    #: Longitude of the events location in degrees. Should be between -180° and 180°.
    longitude: Optional[float] = Field(None, gt=-180, lt=180)

    #: Latitude of the events location in degrees. Should be between -90° and 90°.
    latitude: Optional[float] = Field(None, gt=-90, lt=90)

    #: Elevation above the sea-surface of the events location in meter. For locations below the sea-surface, the elevation should be negative.
    elevation: Optional[float] = None

    #: Label for the event. Should be unique for an item.
    label: Optional[str] = Field(None, min_length=1)

    #: Description
    description: Optional[str] = Field(None, min_length=1)

    #: Event-Type
    type_id: Optional[int] = Field(None, gt=0)
