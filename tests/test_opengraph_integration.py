"""Integration tests for Open Graph tag generation in HTML templates."""

import os
import sys
import tempfile
import json
import shutil

import pytest
from jinja2 import Template

# Add src directory to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "src"))


def test_index_html_open_graph_tags():
    """Test that index.html template includes Open Graph meta tags."""
    # Load template directly
    template_path = os.path.join(
        os.path.dirname(__file__), "..", "src", "templates", "index.html"
    )
    with open(template_path, "r") as f:
        template = Template(f.read())

    # Fill template with test data
    kwargs = {
        "title": "test-repo",
        "version": "v1.0",
        "description": "Test description",
        "theme": "main",
        "space_to_pages_homepage": "https://test.com",
        "og_title": "Test Dataset",
        "og_description": "Test dataset description",
        "og_type": "dataset",
        "og_url": "https://example.com/dataset",
        "og_image": "https://example.com/image.jpg",
        "author": "John Doe",
        "datePublished": "2021-11-25T11:27:08+00:00",
    }

    html_content = template.render(**kwargs)

    # Verify Open Graph tags are present
    assert (
        '<meta property="og:title" content="Test Dataset" />' in html_content
    )
    assert (
        '<meta property="og:description" content="Test dataset description" />'
        in html_content
    )
    assert '<meta property="og:type" content="dataset" />' in html_content
    assert (
        '<meta property="og:url" content="https://example.com/dataset" />'
        in html_content
    )
    assert (
        '<meta property="og:image" content="https://example.com/image.jpg" />'
        in html_content
    )

    # Verify Twitter Card tags
    assert (
        '<meta name="twitter:card" content="summary_large_image" />'
        in html_content
    )
    assert (
        '<meta name="twitter:title" content="Test Dataset" />' in html_content
    )

    # Verify additional metadata
    assert '<meta name="author" content="John Doe" />' in html_content
    assert (
        '<meta name="date" content="2021-11-25T11:27:08+00:00" scheme="ISO8601" />'
        in html_content
    )

    # Verify FAIR signposting
    assert 'rel="describedby"' in html_content
    assert 'rel="alternate"' in html_content
    assert 'rel="canonical"' in html_content


def test_index_html_optional_fields():
    """Test that template handles missing optional Open Graph fields."""
    template_path = os.path.join(
        os.path.dirname(__file__), "..", "src", "templates", "index.html"
    )
    with open(template_path, "r") as f:
        template = Template(f.read())

    # Fill template with minimal data (no optional fields)
    kwargs = {
        "title": "test-repo",
        "version": "v1.0",
        "description": "Test description",
        "theme": "main",
        "space_to_pages_homepage": "https://test.com",
        "og_title": "Test Dataset",
        "og_description": "Test dataset description",
        "og_type": "dataset",
        "og_url": None,
        "og_image": None,
        "author": None,
        "datePublished": None,
    }

    html_content = template.render(**kwargs)

    # Verify required tags are present
    assert (
        '<meta property="og:title" content="Test Dataset" />' in html_content
    )
    assert (
        '<meta property="og:description" content="Test dataset description" />'
        in html_content
    )
    assert '<meta property="og:type" content="dataset" />' in html_content

    # Verify optional tags are not rendered when values are None
    # The Jinja2 template uses {% if og_url %} so these should not appear
    assert 'property="og:url"' not in html_content
    assert 'property="og:image"' not in html_content
    assert (
        'name="author"' not in html_content
        or 'content="None"' not in html_content
    )
    assert (
        'name="date"' not in html_content
        or 'content="None"' not in html_content
    )


def test_dataset_catalogue_index_open_graph():
    """Test that dataset_catalogue_index.html includes Open Graph tags."""
    template_path = os.path.join(
        os.path.dirname(__file__),
        "..",
        "src",
        "templates",
        "dataset_catalogue_index.html",
    )
    with open(template_path, "r") as f:
        template = Template(f.read())

    kwargs = {
        "title": "test-repo",
        "description": "Dataset catalogue description",
        "theme": "main",
        "rocrates": ["crate1", "crate2"],
        "config": {"base_uri": "https://example.com/"},
        "space_to_pages_homepage": "https://test.com",
        "base_uri": "https://example.com/",
    }

    html_content = template.render(**kwargs)

    # Verify Open Graph tags
    assert (
        '<meta property="og:title" content="Dataset Catalogue for test-repo" />'
        in html_content
    )
    assert (
        '<meta property="og:description" content="Dataset catalogue description" />'
        in html_content
    )
    assert '<meta property="og:type" content="website" />' in html_content
    assert (
        '<meta property="og:url" content="https://example.com/" />'
        in html_content
    )

    # Verify FAIR signposting
    assert 'rel="describedby"' in html_content
    assert 'type="text/turtle"' in html_content


def test_overarching_index_open_graph():
    """Test that overarching_index.html includes Open Graph tags."""
    template_path = os.path.join(
        os.path.dirname(__file__),
        "..",
        "src",
        "templates",
        "overarching_index.html",
    )
    with open(template_path, "r") as f:
        template = Template(f.read())

    kwargs = {
        "title": "test-repo",
        "description": "RO-Crate index description",
        "theme": "main",
        "rocrates": ["v1.0", "v2.0"],
        "config": {
            "RELEASE_versioning": "tag",
            "base_uri": "https://example.com/",
        },
        "space_to_pages_homepage": "https://test.com",
        "base_uri": "https://example.com/",
    }

    html_content = template.render(**kwargs)

    # Verify Open Graph tags
    assert (
        '<meta property="og:title" content="RO-Crate Index for test-repo" />'
        in html_content
    )
    assert (
        '<meta property="og:description" content="RO-Crate index description" />'
        in html_content
    )
    assert '<meta property="og:type" content="website" />' in html_content
    assert (
        '<meta property="og:url" content="https://example.com/" />'
        in html_content
    )


def test_parse_semver():
    """Test semver parsing and sorting logic."""
    from utils.gh_pages_builder import parse_semver
    
    versions = ["v1.0.0", "v2.0.0-beta.1", "v2.0.0", "v1.1.0", "v0.0.1"]
    
    # Sort descending (most recent first)
    sorted_versions = sorted(versions, key=parse_semver, reverse=True)
    
    assert sorted_versions == ["v2.0.0", "v2.0.0-beta.1", "v1.1.0", "v1.0.0", "v0.0.1"]


def test_overarching_index_rendering_pills():
    """Test that overarching_index.html renders versions as button-like pills."""
    template_path = os.path.join(
        os.path.dirname(__file__),
        "..",
        "src",
        "templates",
        "overarching_index.html",
    )
    with open(template_path, "r", encoding="utf-8") as f:
        template = Template(f.read())

    # Mock structure that build_index_html passes to overarching_index.html
    rocrates = [
        {"name": "draft", "is_latest": False, "is_draft": True},
        {"name": "v2.0.0", "is_latest": True, "is_draft": False},
        {"name": "v1.0.0", "is_latest": False, "is_draft": False},
    ]

    kwargs = {
        "title": "test-repo",
        "description": "RO-Crate index description",
        "theme": "main",
        "rocrates": rocrates,
        "config": {
            "RELEASE_versioning": "tag",
            "base_uri": "https://example.com/",
            "draft_folder_name": "draft"
        },
        "space_to_pages_homepage": "https://test.com",
        "base_uri": "https://example.com/",
    }

    html_content = template.render(**kwargs)

    # Check that draft pill is rendered with dashed border and gear icon/entity
    assert "btn-outline-secondary" in html_content
    assert "border-dashed" in html_content
    assert "&#9881;&#65039;" in html_content
    assert "draft" in html_content

    # Check that latest version is rendered as a filled primary button pill with the "latest" badge
    assert "btn-primary" in html_content
    assert "v2.0.0" in html_content
    assert "latest" in html_content

    # Check that standard version is rendered as outline primary button pill
    assert "btn-outline-primary" in html_content
    assert "v1.0.0" in html_content


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
