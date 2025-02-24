"""Tests for the MotionMount Select platform."""

from unittest.mock import MagicMock

from homeassistant.core import HomeAssistant

from tests.common import MockConfigEntry


async def test_preset_states(
    hass: HomeAssistant,
    mock_config_entry: MockConfigEntry,
    mock_motionmount: MagicMock,
) -> None:
    """Tests the state attributes."""
    mock_config_entry.add_to_hass(hass)

    mock_motionmount.is_authenticated = True
    assert await hass.config_entries.async_setup(mock_config_entry.entry_id)

    assert hass.states.get("select.my_motionmount_preset").state == "unknown"

    mock_motionmount.is_moving = False

    for callback in mock_motionmount.add_listener.call_args_list:
        callback[0][0]()
    await hass.async_block_till_done()

    assert hass.states.get("select.my_motionmount_preset").state == "unknown"
