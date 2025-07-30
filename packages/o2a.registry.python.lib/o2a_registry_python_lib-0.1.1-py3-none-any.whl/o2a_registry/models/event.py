from datetime import datetime
from typing import Optional
from uuid import UUID

from pydantic import BaseModel, ConfigDict, AliasPath, Field
from pydantic.alias_generators import to_camel

from o2a_registry.models.vocable import Vocable


class Event(BaseModel):
    """
    Event class returned from the registry API
    """

    model_config = ConfigDict(alias_generator=to_camel)

    #: Event unique identifier.
    uuid: UUID = Field(validation_alias=AliasPath("@uuid"))

    #: Event ID.
    id: int

    #: Datetime when the event starts.
    start_date: datetime

    #: Datetime when the event stops.
    end_date: datetime

    #: Latitude of the events location in degrees. Should be between -90° and 90°.
    latitude: Optional[float] = None

    #: Longitude of the events location in degrees. Should be between -180° and 180°.
    longitude: Optional[float] = None

    #: Elevation above/below the sea-surface of the events location in meter.
    elevation: Optional[float] = None

    #: Label for the event. Should be unique for an item.
    label: str

    #: Description
    description: Optional[str] = None

    #: Event-Type
    type: Vocable
