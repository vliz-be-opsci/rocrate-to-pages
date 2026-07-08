"""Tests for metadata extraction and Open Graph tag generation."""

import json
import os
import tempfile
import shutil
from pathlib import Path
import sys

import pytest

# Add src directory to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "src"))

from utils.metadata_extractor import extract_rocrate_metadata


def test_extract_rocrate_metadata_basic():
    """Test extracting metadata from a basic RO-Crate."""
    # Create a temporary directory with ro-crate-metadata.json
    with tempfile.TemporaryDirectory() as tmpdir:
        rocrate_data = {
            "@context": "https://w3id.org/ro/crate/1.1/context",
            "@graph": [
                {
                    "@id": "ro-crate-metadata.json",
                    "@type": "CreativeWork",
                    "about": {"@id": "./"},
                    "conformsTo": {"@id": "https://w3id.org/ro/crate/1.1"},
                },
                {
                    "@id": "./",
                    "@type": "Dataset",
                    "name": "Test Dataset",
                    "description": "This is a test dataset",
                    "url": "https://example.com/dataset",
                    "image": "https://example.com/image.jpg",
                    "datePublished": "2021-11-25T11:27:08+00:00",
                },
            ],
        }

        rocrate_file = os.path.join(tmpdir, "ro-crate-metadata.json")
        with open(rocrate_file, "w") as f:
            json.dump(rocrate_data, f)

        # Extract metadata
        metadata = extract_rocrate_metadata(tmpdir)

        # Verify extracted metadata
        assert metadata["og_title"] == "Test Dataset"
        assert metadata["og_description"] == "This is a test dataset"
        assert metadata["og_type"] == "dataset"
        assert metadata["og_url"] == "https://example.com/dataset"
        assert metadata["og_image"] == "https://example.com/image.jpg"
        assert metadata["datePublished"] == "2021-11-25T11:27:08+00:00"


def test_extract_rocrate_metadata_with_author():
    """Test extracting metadata with author information."""
    with tempfile.TemporaryDirectory() as tmpdir:
        rocrate_data = {
            "@context": "https://w3id.org/ro/crate/1.1/context",
            "@graph": [
                {
                    "@id": "ro-crate-metadata.json",
                    "@type": "CreativeWork",
                    "about": {"@id": "./"},
                    "conformsTo": {"@id": "https://w3id.org/ro/crate/1.1"},
                },
                {
                    "@id": "./",
                    "@type": "Dataset",
                    "name": "Test Dataset",
                    "description": "Test description",
                    "author": [{"@id": "#author1"}],
                },
                {"@id": "#author1", "@type": "Person", "name": "John Doe"},
            ],
        }

        rocrate_file = os.path.join(tmpdir, "ro-crate-metadata.json")
        with open(rocrate_file, "w") as f:
            json.dump(rocrate_data, f)

        metadata = extract_rocrate_metadata(tmpdir)

        assert metadata["author"] == "John Doe"


def test_extract_rocrate_metadata_missing_file():
    """Test handling of missing ro-crate-metadata.json file."""
    with tempfile.TemporaryDirectory() as tmpdir:
        metadata = extract_rocrate_metadata(tmpdir)

        # Should return default values
        assert metadata["og_title"] is None
        assert metadata["og_description"] is None
        assert metadata["og_type"] == "dataset"


def test_extract_rocrate_metadata_minimal():
    """Test extracting metadata from minimal RO-Crate."""
    with tempfile.TemporaryDirectory() as tmpdir:
        rocrate_data = {
            "@context": "https://w3id.org/ro/crate/1.1/context",
            "@graph": [
                {
                    "@id": "ro-crate-metadata.json",
                    "@type": "CreativeWork",
                    "about": {"@id": "./"},
                    "conformsTo": {"@id": "https://w3id.org/ro/crate/1.1"},
                },
                {
                    "@id": "./",
                    "@type": "Dataset",
                    "datePublished": "2021-11-25T11:27:08+00:00",
                },
            ],
        }

        rocrate_file = os.path.join(tmpdir, "ro-crate-metadata.json")
        with open(rocrate_file, "w") as f:
            json.dump(rocrate_data, f)

        metadata = extract_rocrate_metadata(tmpdir)

        # Should handle missing optional fields gracefully
        assert metadata["og_title"] is None
        assert metadata["og_description"] is None
        assert metadata["datePublished"] == "2021-11-25T11:27:08+00:00"


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
