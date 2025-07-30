from typing import List, Optional, Sequence

import aiohttp
from pydantic import TypeAdapter

from o2a_registry.models import EditMission, CreateContact, EditContact
from o2a_registry.models.create_event import CreateEvent
from o2a_registry.models.create_mission import CreateMission
from o2a_registry.models.all_query import AllQuery
from o2a_registry.models.contact import Contact
from o2a_registry.models.create_item import CreateItem
from o2a_registry.models.create_mission_item import CreateMissionItem
from o2a_registry.models.edit_event import EditEvent
from o2a_registry.models.edit_item import EditItem
from o2a_registry.models.event import Event
from o2a_registry.models.item import Item
from o2a_registry.models.item_contact import ItemContact
from o2a_registry.models.item_reference import ItemReference
from o2a_registry.models.item_state import ItemState
from o2a_registry.models.vocable import Vocable
from o2a_registry.models.mission import Mission
from o2a_registry.models.mission_contact import MissionContact
from o2a_registry.models.vocable_group import VocableGroup
from o2a_registry.reference_resolver import resolve_references
from o2a_registry.resolve_query_parameters import resolve_query_parameters
from o2a_registry.rest_adapter import RestAdapter


class RegistryApi:
    """Registry API Wrapper"""

    def __init__(self, hostname: str, ssl: bool = True) -> None:
        """
        Initializes the Registry API Wrapper.

        :param hostname: Hostname (e.g. registry.sandbox.o2a-data.de).
        :param ssl: If the requests are send with SSL.
        """
        self._rest_adapter = RestAdapter(hostname, ssl)

    async def login(self, username: str, password: str) -> None:
        """
        Log in to the registry. This is only required if you want to create, edit or delete information in the registry. Use either your AWI username and password or your email and API token.

        :param username: AWI username or email.
        :param password: passwort or API token.
        :raises aiohttp.ClientResponseError: If the request fails.
        """
        await self._rest_adapter.login("auth/login", username, password)

    async def logged_in(self) -> bool:
        """
        Checks, if you are currently logged in.

        :return: If currently logged in.
        :raises aiohttp.ClientResponseError: If the request fails.
        """
        try:
            await self._rest_adapter.get("/auth/loggedin")
            return True
        except aiohttp.ClientResponseError as e:
            if e.status == 401:
                return False
            raise e

    async def get_items(
        self,
        where: Optional[str] = None,
        sorts: Optional[List[str]] = None,
        offset: Optional[int] = None,
        hits: Optional[int] = None,
    ) -> List[Item]:
        """
        Returns a list of items in the registry.

        :param where: RSQL QUERY (e.g. "id==90").
        :param sorts: List of field names to sort by.
        :param offset: Number of records to skip before returning data.
        :param hits: Number of records to return.
        :return: List of items in the registry.
        :raises aiohttp.ClientResponseError: If the request fails.
        """
        data = await self._rest_adapter.get(
            "items" + resolve_query_parameters(where, sorts, offset, hits)
        )

        data = resolve_references(data, "status")
        data = resolve_references(data, "vocableGroup")
        data = resolve_references(data, "type")

        query_response: AllQuery[Item] = AllQuery[Item].model_validate_json(data)

        return query_response.records

    async def get_item(self, item_id: int) -> Item:
        """
        Gets the item with the specified ID for the registry.

        :param item_id: item ID.
        :return: item with the specified ID.
        :raises aiohttp.ClientResponseError: If the request fails.
        """
        data = await self._rest_adapter.get(f"items/{item_id}")
        return Item.model_validate_json(data)

    async def edit_item(self, item_id: int, item: EditItem) -> None:
        """
        Edits the item with the specified ID for the registry. Only the set entries in the EditItem will be edited.

        :param item_id: item ID of the item to be edited.
        :param item: EditItem specifying the changes.
        :raises aiohttp.ClientResponseError: If the request fails.
        """
        await self._rest_adapter.put(f"items/{item_id}", data=item)

    async def create_item(self, item: CreateItem) -> None:
        """
        Creates a new item in the registry.

        :param item: Item to create in the registry.
        :raises aiohttp.ClientResponseError: If the request fails.
        """
        await self._rest_adapter.post("items", data=item)

    async def delete_item(self, item_id: int) -> None:
        """
        Deletes an item from the registry.

        :param item_id: item ID of the item to be deleted.
        :raises aiohttp.ClientResponseError: If the request fails.
        """
        await self._rest_adapter.delete(f"items/{item_id}")

    async def create_item_version(self, item_id: int) -> None:
        """
        Creates a new version for an item in the registry.

        :param item_id: item ID of the item for which a new version is to be created.
        :raises aiohttp.ClientResponseError: If the request fails.
        """
        await self._rest_adapter.post(f"items/{item_id}/versions")

    async def get_item_contacts(
        self,
        item_id: int,
        where: Optional[str] = None,
        sorts: Optional[List[str]] = None,
        offset: Optional[int] = None,
        hits: Optional[int] = None,
    ) -> List[ItemContact]:
        """
        Gets all item contacts associated with the specified item.

        :param item_id: item ID.
        :param where: RSQL QUERY (e.g. "id==90").
        :param sorts: List of field names to sort by.
        :param offset: Number of records to skip before returning data.
        :param hits: Number of records to return.
        :return: List of item contacts associated with the specified item.
        :raises aiohttp.ClientResponseError: If the request fails.
        """
        data = await self._rest_adapter.get(
            f"items/{item_id}/contacts"
            + resolve_query_parameters(where, sorts, offset, hits)
        )

        data = resolve_references(data, "contact")
        data = resolve_references(data, "vocableGroup")
        data = resolve_references(data, "role")

        query_response: AllQuery[ItemContact] = AllQuery[
            ItemContact
        ].model_validate_json(data)
        return query_response.records

    async def get_item_contact(
        self, item_id: int, contact_id: int
    ) -> List[ItemContact]:
        """
        Gets the item contact for the specified item and contact.

        :param item_id: item ID.
        :param contact_id: contact ID.
        :return: Item contact for the specified item and contact.
        :raises aiohttp.ClientResponseError: If the request fails.
        """
        data = await self._rest_adapter.get(f"items/{item_id}/contacts/{contact_id}")

        data = resolve_references(data, "contact")
        data = resolve_references(data, "vocableGroup")
        data = resolve_references(data, "role")

        type_adapter = TypeAdapter(List[ItemContact])
        return type_adapter.validate_json(data)

    async def create_item_contact(
        self, item_id: int, contact_id: int, roles: List[int]
    ):
        """
        Creates a new item contact for a specified item and contact in the registry.

        :param item_id: item ID.
        :param contact_id: contact ID.
        :param roles: List of role IDs.
        :raises aiohttp.ClientResponseError: If the request fails.
        """
        await self._rest_adapter.post(
            f"items/{item_id}/contacts/{contact_id}", data=roles
        )

    async def delete_item_contact(self, item_id: int, contact_id: int) -> None:
        """
        Deletes an item contact for the specified item and contact in the registry.

        :param item_id: item ID.
        :param contact_id: contact ID.
        :raises aiohttp.ClientResponseError: If the request fails.
        """
        await self._rest_adapter.delete(f"items/{item_id}/contacts/{contact_id}")

    async def get_missions(
        self,
        where: Optional[str] = None,
        sorts: Optional[List[str]] = None,
        offset: Optional[int] = None,
        hits: Optional[int] = None,
    ) -> List[Mission]:
        """
        Gets missions from the registry.

        :param where: RSQL QUERY (e.g. "id==90").
        :param sorts: List of field names to sort by.
        :param offset: Number of records to skip before returning data.
        :param hits: Number of records to return.
        :return: List of missions stored in the registry.
        :raises aiohttp.ClientResponseError: If the request fails.
        """
        data = await self._rest_adapter.get(
            "missions" + resolve_query_parameters(where, sorts, offset, hits)
        )

        query_response: AllQuery[Mission] = AllQuery[Mission].model_validate_json(data)

        return query_response.records

    async def get_mission(self, mission_id: int) -> Mission:
        """
        Gets the mission with the specified ID.

        :param mission_id: mission ID.
        :return: Mission with the specified ID.
        :raises aiohttp.ClientResponseError: If the request fails.
        """
        data = await self._rest_adapter.get(f"missions/{mission_id}")
        return Mission.model_validate_json(data)

    async def create_mission(self, mission: CreateMission):
        """
        Creates a new mission in the registry.

        :param mission: mission to create.
        :raises aiohttp.ClientResponseError: If the request fails.
        """
        await self._rest_adapter.post("missions", data=mission)

    async def edit_mission(self, mission_id: int, mission: EditMission):
        """
        Edits a mission in the registry. Only set field in the EditMission are changed.

        :param mission_id: mission ID.
        :param mission: mission containing the fields which are edited.
        :raises aiohttp.ClientResponseError: If the request fails.
        """
        await self._rest_adapter.put(f"missions/{mission_id}", data=mission)

    async def delete_mission(self, mission_id: int) -> None:
        """
        Deletes a mission from the registry.

        :param mission_id: mission ID.
        :raises aiohttp.ClientResponseError: If the request fails.
        """
        await self._rest_adapter.delete(f"missions/{mission_id}")

    async def get_mission_items(
        self,
        mission_id: int,
        where: Optional[str] = None,
        sorts: Optional[List[str]] = None,
        offset: Optional[int] = None,
        hits: Optional[int] = None,
    ) -> List[ItemReference]:
        """
        Gets all items associated with the specified mission. Does only return references to the items.

        :param mission_id: mission ID.
        :param where: RSQL QUERY (e.g. "id==90").
        :param sorts: List of field names to sort by.
        :param offset: Number of records to skip before returning data.
        :param hits: Number of records to return.
        :return: List of references of items associated with the specified mission.
        :raises aiohttp.ClientResponseError: If the request fails.
        """
        data = await self._rest_adapter.get(
            f"missions/{mission_id}/items"
            + resolve_query_parameters(where, sorts, offset, hits)
        )

        query_response: AllQuery[ItemReference] = AllQuery[
            ItemReference
        ].model_validate_json(data)
        return query_response.records

    async def create_mission_items(
        self, mission_id: int, mission_items: Sequence[CreateMissionItem]
    ) -> None:
        """
        Associate a list of items to a mission.

        :param mission_id: mission ID.
        :param mission_items: List of mission items.
        :raises aiohttp.ClientResponseError: If the request fails.
        """
        await self._rest_adapter.post(
            f"missions/{mission_id}/items", data=mission_items
        )

    async def delete_mission_items(self, mission_id: int):
        """
        Removes the association between a specified mission and all its associated items.

        :param mission_id: mission ID.
        :raises aiohttp.ClientResponseError: If the request fails.
        """
        await self._rest_adapter.delete(f"missions/{mission_id}/items")

    async def get_mission_contacts(
        self,
        mission_id: int,
        where: Optional[str] = None,
        sorts: Optional[List[str]] = None,
        offset: Optional[int] = None,
        hits: Optional[int] = None,
    ) -> List[MissionContact]:
        """
        Gets contacts associated with the specified mission.

        :param mission_id: mission ID.
        :param where: RSQL QUERY (e.g. "id==90").
        :param sorts: List of field names to sort by.
        :param offset: Number of records to skip before returning data.
        :param hits: Number of records to return.
        :return: List of mission contacts associated with the specified mission.
        :raises aiohttp.ClientResponseError: If the request fails.
        """
        data = await self._rest_adapter.get(
            f"missions/{mission_id}/contacts"
            + resolve_query_parameters(where, sorts, offset, hits)
        )

        data = resolve_references(data, "contact")
        data = resolve_references(data, "vocableGroup")
        data = resolve_references(data, "role")

        query_response: AllQuery[MissionContact] = AllQuery[
            MissionContact
        ].model_validate_json(data)
        return query_response.records

    async def get_mission_contact(
        self, mission_id: int, contact_id: int
    ) -> List[MissionContact]:
        """
        Get a mission contacts for a specified mission and contact.

        :param mission_id: mission ID.
        :param contact_id: contact ID.
        :return: List of mission contacts associated with the specified mission and contact.
        :raises aiohttp.ClientResponseError: If the request fails.
        """
        data = await self._rest_adapter.get(
            f"missions/{mission_id}/contacts/{contact_id}"
        )
        type_adapter = TypeAdapter(List[MissionContact])
        return type_adapter.validate_json(data)

    async def create_mission_contact(
        self, mission_id: int, contact_id: int, roles: List[int]
    ):
        """
        Create a mission contact for a specified mission and contact in the registry.

        :param mission_id: mission ID.
        :param contact_id: contact ID.
        :param roles: List of role IDs.
        :raises aiohttp.ClientResponseError: If the request fails.
        """
        await self._rest_adapter.post(
            f"missions/{mission_id}/contacts/{contact_id}", data=roles
        )

    async def delete_mission_contact(self, mission_id: int, contact_id: int) -> None:
        """
        Deletes a mission contact from the registry.
        :param mission_id: mission ID.
        :param contact_id: contact ID.
        :raises aiohttp.ClientResponseError: If the request fails.
        """
        await self._rest_adapter.delete(f"missions/{mission_id}/contacts/{contact_id}")

    async def get_contacts(
        self,
        where: Optional[str] = None,
        sorts: Optional[List[str]] = None,
        offset: Optional[int] = None,
        hits: Optional[int] = None,
    ) -> List[Contact]:
        """
        Get contacts from the registry.

        :param where: RSQL QUERY (e.g. "id==90").
        :param sorts: List of field names to sort by.
        :param offset: Number of records to skip before returning data.
        :param hits: Number of records to return.
        :return: List of contacts.
        :raises aiohttp.ClientResponseError: If the request fails.
        """
        data = await self._rest_adapter.get(
            "contacts" + resolve_query_parameters(where, sorts, offset, hits)
        )

        query_response: AllQuery[Contact] = AllQuery[Contact].model_validate_json(data)

        return query_response.records

    async def get_contact(self, contact_id: int) -> Contact:
        """
        Gets a contact from the registry.

        :param contact_id: contact ID.
        :return: Contact with the specified contact ID.
        :raises aiohttp.ClientResponseError: If the request fails.
        """
        data = await self._rest_adapter.get(f"contacts/{contact_id}")

        return Contact.model_validate_json(data)

    async def create_contact(self, contact: CreateContact) -> None:
        """
        Create a contact in the registry.

        :param contact: new contact.
        :return: None
        :raises aiohttp.ClientResponseError: If the request fails.
        """
        await self._rest_adapter.post("contacts", data=contact)

    async def edit_contact(self, contact_id: int, contact: EditContact) -> None:
        """
        Edits a contact in the registry. Only the set entries in the EditContact will be edited.

        :param contact_id: contact ID.
        :param contact: contact containing the fields which are edited.
        :raises aiohttp.ClientResponseError: If the request fails.
        """
        await self._rest_adapter.put(f"contacts/{contact_id}", data=contact)

    async def delete_contact(self, contact_id: int) -> None:
        """
        Deletes a contact in the registry.

        :param contact_id: contact ID.
        :raises aiohttp.ClientResponseError: If the request fails.
        """
        await self._rest_adapter.delete(f"contacts/{contact_id}")

    async def get_events(
        self,
        item_id: int,
        where: Optional[str] = None,
        sorts: Optional[List[str]] = None,
        offset: Optional[int] = None,
        hits: Optional[int] = None,
    ) -> List[Event]:
        """
        Gets events from the registry.

        :param item_id: item ID.
        :param where: RSQL QUERY (e.g. "id==90").
        :param sorts: List of field names to sort by.
        :param offset: Number of records to skip before returning data.
        :param hits: Number of records to return.
        :return: List of events in the registry.
        :raises aiohttp.ClientResponseError: If the request fails.
        """
        data = await self._rest_adapter.get(
            f"items/{item_id}/events"
            + resolve_query_parameters(where, sorts, offset, hits)
        )

        data = resolve_references(data, "vocableGroup")
        data = resolve_references(data, "type")

        query_response: AllQuery[Event] = AllQuery[Event].model_validate_json(data)
        return query_response.records

    async def get_event(self, item_id: int, event_id: int) -> Event:
        """
        Gets an event for an item from the registry.

        :param item_id: item ID.
        :param event_id: event ID.
        :return: Event with the specified event ID.
        :raises aiohttp.ClientResponseError: If the request fails.
        """
        data = await self._rest_adapter.get(f"items/{item_id}/events/{event_id}")
        return Event.model_validate_json(data)

    async def create_event(self, item_id: int, event: CreateEvent) -> None:
        """
        Creates an event for an item from the registry.

        :param item_id: item ID.
        :param event: event to create.
        :raises aiohttp.ClientResponseError: If the request fails.
        """
        await self._rest_adapter.post(f"items/{item_id}/events", data=event)

    async def edit_event(self, item_id: int, event_id: int, event: EditEvent) -> None:
        """
        Edits an event for an item.

        :param item_id: item ID.
        :param event_id: event ID.
        :param event: event containing the fields which are edited.
        :raises aiohttp.ClientResponseError: If the request fails.
        """
        await self._rest_adapter.put(f"items/{item_id}/events/{event_id}", data=event)

    async def delete_event(self, item_id: int, event_id: int) -> None:
        """
        Deletes an event for an item.

        :param item_id: item ID.
        :param event_id: event ID.
        :raises aiohttp.ClientResponseError: If the request fails.
        """
        await self._rest_adapter.delete(f"items/{item_id}/events/{event_id}")

    async def get_vocable_groups(
        self,
        where: Optional[str] = None,
        sorts: Optional[List[str]] = None,
        offset: Optional[int] = None,
        hits: Optional[int] = None,
    ) -> List[VocableGroup]:
        """
        Gets vocable groups from the registry.

        :param where: RSQL QUERY (e.g. "id==90").
        :param sorts: List of field names to sort by.
        :param offset: Number of records to skip before returning data.
        :param hits: Number of records to return.
        :return: List of vocable groups in the registry.
        :raises aiohttp.ClientResponseError: If the request fails.
        """
        data = await self._rest_adapter.get(
            "vocable-groups" + resolve_query_parameters(where, sorts, offset, hits)
        )
        query_response = AllQuery[VocableGroup].model_validate_json(data)
        return query_response.records

    async def get_vocable_group(self, group_id: int) -> VocableGroup:
        """
        Gets a vocable group from the registry.

        :param group_id: vocable group ID.
        :return: Vocable group with the specified ID.
        """
        data = await self._rest_adapter.get(f"vocable-groups/{group_id}")
        return VocableGroup.model_validate_json(data)

    async def get_vocables(
        self,
        where: Optional[str] = None,
        sorts: Optional[List[str]] = None,
        offset: Optional[int] = None,
        hits: Optional[int] = None,
    ) -> List[Vocable]:
        """
        Gets vocables from the registry.

        :param where: RSQL QUERY (e.g. "id==90").
        :param sorts: List of field names to sort by.
        :param offset: Number of records to skip before returning data.
        :param hits: Number of records to return.
        :return: List of vocables in the registry.
        :raises aiohttp.ClientResponseError: If the request fails.
        """
        data = await self._rest_adapter.get(
            "vocables" + resolve_query_parameters(where, sorts, offset, hits)
        )
        data = resolve_references(data, "vocableGroup")
        query_response = AllQuery[Vocable].model_validate_json(data)
        return query_response.records

    async def get_vocable(self, vocable_id: int) -> Vocable:
        """
        Gets a vocable from the registry.

        :param vocable_id: vocable ID.
        :return: Vocable with the specified ID.
        """
        data = await self._rest_adapter.get(f"vocables/{vocable_id}")
        return Vocable.model_validate_json(data)

    async def get_states(
        self,
        where: Optional[str] = None,
        sorts: Optional[List[str]] = None,
        offset: Optional[int] = None,
        hits: Optional[int] = None,
    ) -> List[ItemState]:
        """
        Gets states from the registry.

        :param where: RSQL QUERY (e.g. "id==90").
        :param sorts: List of field names to sort by.
        :param offset: Number of records to skip before returning data.
        :param hits: Number of records to return.
        :return: List of states in the registry.
        :raises aiohttp.ClientResponseError: If the request fails.
        """
        data = await self._rest_adapter.get(
            "states" + resolve_query_parameters(where, sorts, offset, hits)
        )
        query_response = AllQuery[ItemState].model_validate_json(data)
        return query_response.records

    async def get_state(self, state_id: int) -> ItemState:
        """
        Gets a state from the registry.

        :param state_id: state ID.
        :return: State with the specified ID.
        """
        data = await self._rest_adapter.get(f"states/{state_id}")
        return ItemState.model_validate_json(data)

    async def close(self):
        """
        Closes the registry wrapper.
        """
        await self._rest_adapter.close()


ProductionAPI = RegistryApi("registry.o2a-data.de")
SandboxAPI = RegistryApi("registry.sandbox.o2a-data.de")
