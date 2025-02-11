"""Tests for the MotionMount Binary Sensor platform."""

from unittest.mock import MagicMock

import pytest

from homeassistant.core import HomeAssistant

from tests.common import MockConfigEntry


@pytest.mark.parametrize(
    ("is_moving", "state"),
    [
        (False, "off"),
        (True, "on"),
    ],
)
async def test_moving_states(
    hass: HomeAssistant,
    mock_config_entry: MockConfigEntry,
    mock_motionmount: MagicMock,
    is_moving: bool,
    state: str,
) -> None:
    """Tests the state attributes."""
    mock_config_entry.add_to_hass(hass)

    mock_motionmount.is_authenticated = True
    mock_motionmount.is_moving = is_moving

    assert await hass.config_entries.async_setup(mock_config_entry.entry_id)

    assert hass.states.get("binary_sensor.my_motionmount_moving").state == state
