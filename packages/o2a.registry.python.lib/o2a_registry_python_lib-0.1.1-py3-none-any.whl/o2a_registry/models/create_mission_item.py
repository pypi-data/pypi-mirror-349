from pydantic import BaseModel, Field, ConfigDict, AliasGenerator
from pydantic.alias_generators import to_camel


class CreateMissionItem(BaseModel):
    """
    Class for assigning an item to a mission.
    """

    model_config = ConfigDict(
        alias_generator=AliasGenerator(serialization_alias=to_camel)
    )

    #: Item ID.
    item_id: int = Field(..., gt=0)
