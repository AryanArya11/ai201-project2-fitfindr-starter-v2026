import json
from pathlib import Path

import config

MEMORY_FILE = config.ROOT / ".fitfindr" / "wardrobe.json"


def load_wardrobe(path: Path) -> dict:
    wardrobe = json.loads(path.read_text(encoding="utf-8"))

    if not isinstance(wardrobe, dict):
        raise ValueError("The wardrobe must be a JSON object.")

    if not isinstance(wardrobe.get("items"), list):
        raise ValueError("The wardrobe must contain an items list.")

    for item in wardrobe["items"]:
        required = ("id", "name", "category", "colors", "style_tags")
        if not isinstance(item, dict) or any(
            field not in item for field in required
        ):
            raise ValueError(
                "Each item needs id, name, category, colors, and style_tags."
            )

    return wardrobe


def save_wardrobe(wardrobe: dict) -> None:
    MEMORY_FILE.parent.mkdir(parents=True, exist_ok=True)
    temporary = MEMORY_FILE.with_suffix(".tmp")
    temporary.write_text(
        json.dumps(wardrobe, indent=2),
        encoding="utf-8",
    )
    temporary.replace(MEMORY_FILE)