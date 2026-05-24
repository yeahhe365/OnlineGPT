"""
Shared pytest fixtures for the OnlineGPT testing suite.

This module provides common fixtures that can be used across all test files.
"""

import os
import sys
import tempfile
import pytest
from unittest.mock import Mock, MagicMock, patch
from pathlib import Path

# Add the OnlineGPT directory to the Python path for imports
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'OnlineGPT'))


@pytest.fixture
def temp_dir():
    """Create a temporary directory for tests."""
    with tempfile.TemporaryDirectory() as tmpdir:
        yield Path(tmpdir)


@pytest.fixture
def temp_file(temp_dir):
    """Create a temporary file for tests."""
    temp_file_path = temp_dir / "test_file.txt"
    temp_file_path.write_text("test content")
    yield temp_file_path


@pytest.fixture
def mock_requests():
    """Mock the requests module."""
    mock_response = Mock()
    mock_response.status_code = 200
    mock_response.text = "<html><body>Test content</body></html>"
    mock_response.headers = {'content-type': 'text/html'}
    
    with patch('requests.get', return_value=mock_response) as mock_get:
        yield mock_get


@pytest.fixture
def mock_beautiful_soup():
    """Mock BeautifulSoup for HTML parsing tests."""
    mock_soup = MagicMock()
    mock_soup.find_all.return_value = []
    mock_soup.get_text.return_value = "Mock text content"
    
    with pytest.mock.patch('bs4.BeautifulSoup', return_value=mock_soup) as mock_bs:
        yield mock_bs


@pytest.fixture
def sample_search_results():
    """Provide sample search results for testing."""
    return [
        {
            'title': 'Test Result 1',
            'url': 'https://example.com/1',
            'snippet': 'This is a test search result snippet',
            'source': 'test_engine'
        },
        {
            'title': 'Test Result 2',
            'url': 'https://example.com/2',
            'snippet': 'Another test search result snippet',
            'source': 'test_engine'
        }
    ]


@pytest.fixture
def mock_config():
    """Provide mock configuration settings."""
    return {
        'max_results': 10,
        'timeout': 30,
        'user_agent': 'Test Agent/1.0',
        'search_engines': ['test_engine1', 'test_engine2'],
        'output_format': 'txt'
    }


@pytest.fixture
def mock_logger():
    """Mock logger for testing logging functionality."""
    return Mock()


@pytest.fixture
def mock_qt_widget():
    """Mock Qt widget for testing GUI components."""
    from unittest.mock import MagicMock
    
    mock_widget = MagicMock()
    mock_widget.text.return_value = "test text"
    mock_widget.isChecked.return_value = False
    mock_widget.setEnabled = MagicMock()
    mock_widget.setText = MagicMock()
    
    return mock_widget


@pytest.fixture
def sample_html_content():
    """Provide sample HTML content for parsing tests."""
    return """
    <html>
        <head><title>Test Page</title></head>
        <body>
            <h1>Test Heading</h1>
            <p>This is test content for parsing.</p>
            <a href="https://example.com">Test Link</a>
        </body>
    </html>
    """


@pytest.fixture
def mock_file_system(temp_dir):
    """Mock file system operations."""
    test_files = {
        'test.txt': 'Test file content',
        'results.json': '{"results": []}',
        'config.ini': '[settings]\nkey=value'
    }
    
    for filename, content in test_files.items():
        (temp_dir / filename).write_text(content)
    
    yield temp_dir


@pytest.fixture(autouse=True)
def setup_test_environment(monkeypatch):
    """
    Automatically set up test environment for all tests.
    This fixture runs automatically for every test.
    """
    # Set environment variables for testing
    monkeypatch.setenv('TESTING', '1')
    monkeypatch.setenv('LOG_LEVEL', 'DEBUG')
    
    # Mock any external dependencies that shouldn't run during tests
    yield