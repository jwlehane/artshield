import pytest
from pydantic import ValidationError
# These imports are expected to fail initially
from backend.processor import ProtectionParams, ProtectionResult, ProtectionType, Intensity

def test_protection_params_defaults():
    """Test default values for ProtectionParams."""
    params = ProtectionParams(image_path="test.jpg")
    assert params.image_path == "test.jpg"
    assert params.protection_type == ProtectionType.CLOAK_AND_TAG
    assert params.intensity == Intensity.MEDIUM
    assert params.output_path is None
    assert params.metadata == {}

def test_protection_params_validation():
    """Test validation for ProtectionParams."""
    with pytest.raises(ValidationError):
        ProtectionParams(image_path=None)

def test_protection_result_success():
    """Test successful ProtectionResult creation."""
    result = ProtectionResult(
        success=True,
        original_path="test.jpg",
        protected_path="test_protected.jpg",
        message="Success"
    )
    assert result.success is True
    assert result.original_path == "test.jpg"
    assert result.protected_path == "test_protected.jpg"
    assert result.message == "Success"
    assert result.error is None

def test_protection_result_failure():
    """Test failed ProtectionResult creation."""
    result = ProtectionResult(
        success=False,
        original_path="test.jpg",
        error="Something went wrong"
    )
    assert result.success is False
    assert result.original_path == "test.jpg"
    assert result.protected_path is None
    assert result.error == "Something went wrong"
