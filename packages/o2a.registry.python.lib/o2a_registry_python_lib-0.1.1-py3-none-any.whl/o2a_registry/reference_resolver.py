import re
from copy import copy


def resolve_references(json_input: str, key: str) -> str:
    output = copy(json_input)
    unresolved_uuids = set(re.findall(rf"\"{key}\":\"([^\"]+)\"", output))

    for uuid in unresolved_uuids:
        match = re.search(
            rf"\"{key}\":{{\"@uuid\":\"{uuid}\".*\"@uuid\":\"{uuid}\"}}", output
        )

        if match is None:
            raise ValueError(f"Could not resolve reference {uuid}")

        resolved_object = match.group(0)
        output = output.replace(f'"{key}":"{uuid}"', resolved_object)

    return output
