from datetime import datetime
from typing import Optional
from uuid import UUID

from pydantic import BaseModel, ConfigDict, AliasPath, Field
from pydantic.alias_generators import to_camel


class Contact(BaseModel):
    """
    Contact class returned from the registry API
    """

    model_config = ConfigDict(alias_generator=to_camel)

    #: Contact unique identifier.
    uuid: UUID = Field(validation_alias=AliasPath("@uuid"))

    #: Contact ID.
    id: int

    #: Datetime when the contact was created in the registry.
    created: Optional[datetime] = None

    #: Datetime when the contact was last modified in the registry.
    last_modified: datetime

    #: Contacts first name.
    first_name: Optional[str] = None

    #: Contacts last name.
    last_name: Optional[str] = None

    #: Contact email.
    email: str

    #: Open Researcher and Contributor ID URL (https://orcid.org/).
    orcid: Optional[str] = None

    #: Telephone number.
    telephone: Optional[str] = None

    #: Postal code.
    postal_code: Optional[str] = None

    #: City name.
    city: Optional[str] = None

    #: Administrative area name.
    administrative_area: Optional[str] = None

    #: Country name.
    country: Optional[str] = None

    #: Research Organization Registry URL (https://ror.org/).
    ror: Optional[str] = None
