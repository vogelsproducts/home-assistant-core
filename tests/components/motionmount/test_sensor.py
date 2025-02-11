"""Tests for the MotionMount Sensor platform."""

from unittest.mock import MagicMock

from motionmount import MotionMountSystemError
import pytest

from homeassistant.core import HomeAssistant

from tests.common import MockConfigEntry


@pytest.mark.usefixtures("entity_registry_enabled_by_default")
@pytest.mark.parametrize(
    ("system_status", "state"),
    [
        (None, "none"),
        (MotionMountSystemError.MotorError, "motor"),
        (MotionMountSystemError.ObstructionDetected, "obstruction"),
        (MotionMountSystemError.TVWidthConstraintError, "tv_width_constraint"),
        (MotionMountSystemError.HDMICECError, "hdmi_cec"),
        (MotionMountSystemError.InternalError, "internal"),
    ],
)
async def test_error_status_sensor_states(
    hass: HomeAssistant,
    mock_config_entry: MockConfigEntry,
    mock_motionmount: MagicMock,
    system_status: MotionMountSystemError,
    state: str,
) -> None:
    """Tests the state attributes."""
    mock_config_entry.add_to_hass(hass)

    mock_motionmount.is_authenticated = True
    mock_motionmount.system_status = [system_status]

    assert await hass.config_entries.async_setup(mock_config_entry.entry_id)

    assert hass.states.get("sensor.my_motionmount_error_status").state == state
