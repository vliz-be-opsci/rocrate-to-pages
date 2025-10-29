# Utility functions to extract metadata from RO-Crate files for Open Graph tags
import json
import os
from typing import Dict, Optional

from utils.singleton.logger import get_logger

logger = get_logger()


def extract_rocrate_metadata(rocrate_path: str) -> Dict[str, Optional[str]]:
    """
    Extract metadata from ro-crate-metadata.json file for use in Open Graph tags.

    :param rocrate_path: Path to the directory containing ro-crate-metadata.json
    :return: Dictionary with extracted metadata fields
    """
    metadata = {
        "og_title": None,
        "og_description": None,
        "og_type": "dataset",  # Default for RO-Crate datasets
        "og_url": None,
        "og_image": None,
        "author": None,
        "datePublished": None,
    }

    # Construct path to ro-crate-metadata.json
    rocrate_file = os.path.join(rocrate_path, "ro-crate-metadata.json")

    # Check if file exists
    if not os.path.isfile(rocrate_file):
        logger.warning(f"ro-crate-metadata.json not found at {rocrate_file}")
        return metadata

    try:
        with open(rocrate_file, "r", encoding="utf-8") as f:
            rocrate_data = json.load(f)

        # Find the root dataset (entity with @id = "./")
        graph = rocrate_data.get("@graph", [])
        root_dataset = None

        for entity in graph:
            if entity.get("@id") == "./":
                root_dataset = entity
                break

        if not root_dataset:
            logger.warning("No root dataset found in ro-crate-metadata.json")
            return metadata

        # Extract metadata fields
        metadata["og_title"] = root_dataset.get("name")
        metadata["og_description"] = root_dataset.get("description")
        metadata["og_url"] = root_dataset.get("url")
        metadata["og_image"] = root_dataset.get("image")
        metadata["datePublished"] = root_dataset.get("datePublished")

        # Handle author (can be a list or single value)
        author = root_dataset.get("author")
        if author:
            if isinstance(author, list) and len(author) > 0:
                # Try to resolve author reference
                author_id = (
                    author[0].get("@id")
                    if isinstance(author[0], dict)
                    else author[0]
                )
                # Look up author in graph
                for entity in graph:
                    if entity.get("@id") == author_id:
                        metadata["author"] = entity.get("name")
                        break
            elif isinstance(author, dict):
                metadata["author"] = author.get("name")
            elif isinstance(author, str):
                metadata["author"] = author

        logger.debug(f"Extracted metadata: {metadata}")

    except Exception as e:
        logger.error(f"Error reading ro-crate-metadata.json: {e}")
        logger.debug(f"Error details: {e}", exc_info=True)

    return metadata
