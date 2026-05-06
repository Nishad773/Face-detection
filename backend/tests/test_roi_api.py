from app.schemas.roi import ROIResponse


def test_roi_response_schema_fields() -> None:
    fields = ROIResponse.model_fields
    assert "session_id" in fields
    assert "timestamp" in fields
    assert "width" in fields
    assert "height" in fields
