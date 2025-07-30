from uuid import UUID

from pydantic import BaseModel, ConfigDict, AliasPath, Field
from pydantic.alias_generators import to_camel

from o2a_registry.models.contact import Contact
from o2a_registry.models.vocable import Vocable


class ItemContact(BaseModel):
    """
    Relationship between a contact and an item in the registry.
    """

    model_config = ConfigDict(alias_generator=to_camel)

    #: Unique identifier for the relationship.
    uuid: UUID = Field(validation_alias=AliasPath("@uuid"))

    #: ID of the relationship.
    id: int

    #: Contact for the item.
    contact: Contact

    #: Role of the contact for the item.
    role: Vocable
