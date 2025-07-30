from typing import Optional

from pydantic import BaseModel, ConfigDict, EmailStr, Field, AliasGenerator
from pydantic.alias_generators import to_camel

from o2a_registry.validation import ORCID_URL, ROR_URL


class EditContact(BaseModel):
    """
    Contact class for editing a contact in the registry.
    """

    model_config = ConfigDict(
        alias_generator=AliasGenerator(serialization_alias=to_camel)
    )

    #: Contacts first name. Must be at least two characters long.
    first_name: Optional[str] = Field(None, min_length=2)

    #: Contacts last name. Must be at least two characters long.
    last_name: Optional[str] = Field(None, min_length=2)

    #: Contact email.
    email: Optional[EmailStr] = None

    #: Open Researcher and Contributor ID URL string (https://orcid.org/).
    orcid: Optional[ORCID_URL] = None

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

    #: Research Organization Registry URL string (https://ror.org/).
    ror: Optional[ROR_URL] = None
