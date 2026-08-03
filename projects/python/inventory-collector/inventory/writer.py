import json
from pathlib import Path
from typing import Any
import logging


logger = logging.getLogger(__name__)


# def write_inventory(data, filename="inventory.json"):
#     project_root = Path(__file__).parent.parent
#     output_file = project_root / filename

#     with output_file.open("w", encoding="utf-8") as file:
#         json.dump(data, file, indent=4)


# defining the function with type hints
def write_inventory(
    data: dict[str, Any],
    filename: str = "inventory.json",
    ) -> None:

    """
    Write the inventory dictionary to a JSOn file.

    Args:
        data: Invnetory data to serialize.
        filename: Output JSON filename.

    Raises:
        OSError: If the file cannot be written.
        TypeError: if the data cannot be serialized.
    """

    # project_root = Path(__file__).parent.parent
    # introducing named variable, it converts the path to its canonical absolute form
    project_root = Path(__file__).resolve().parent.parent
    output_file = project_root / filename

    try:
        with output_file.open("w", encoding="utf-8", ) as file:
            json.dump(data, file, indent=4,  ensure_ascii=False,)
    except (OSError, TypeError):
        logger.exception(" Failed to write inventory file '%s .", output_file,)
        # print(f"failed to write invnetory file: {error}")
        raise
