def test_hello():
    """Simple test to verify the test runner works."""
    assert True, "Basic test passed"

def test_import():
    """Test that we can import from our package."""
    from baresquare_core_py import logger
    assert logger is not None, "Logger module imported successfully"
