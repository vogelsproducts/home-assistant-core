"""Tests for the MotionMount Number platform."""

from unittest.mock import MagicMock

import pytest

from homeassistant.core import HomeAssistant
from homeassistant.exceptions import HomeAssistantError

from tests.common import MockConfigEntry


@pytest.mark.parametrize(
    "extension",
    [
        None,
        0,
        50,
        100,
    ],
)
async def test_extension_states(
    hass: HomeAssistant,
    mock_config_entry: MockConfigEntry,
    mock_motionmount: MagicMock,
    extension: int,
) -> None:
    """Tests the state attributes."""
    mock_config_entry.add_to_hass(hass)

    mock_motionmount.is_authenticated = True
    mock_motionmount.extension = extension

    assert await hass.config_entries.async_setup(mock_config_entry.entry_id)

    assert hass.states.get("number.my_motionmount_extension").state == str(
        float(extension or 0)
    )


async def test_extension_value(
    hass: HomeAssistant,
    mock_config_entry: MockConfigEntry,
    mock_motionmount: MagicMock,
) -> None:
    """Test setting a value."""
    mock_config_entry.add_to_hass(hass)
    mock_motionmount.is_authenticated = True
    assert await hass.config_entries.async_setup(mock_config_entry.entry_id)

    await hass.services.async_call(
        "number",
        "set_value",
        {"entity_id": "number.my_motionmount_extension", "value": 10},
        blocking=True,
    )

    assert mock_motionmount.set_extension.call_count == 1
    assert mock_motionmount.set_extension.call_args_list[0][0][0] == 10


async def test_extension_exception(
    hass: HomeAssistant,
    mock_config_entry: MockConfigEntry,
    mock_motionmount: MagicMock,
) -> None:
    """Test setting a value with exception."""
    mock_config_entry.add_to_hass(hass)

    mock_motionmount.is_authenticated = True
    mock_motionmount.set_extension.side_effect = TimeoutError()

    assert await hass.config_entries.async_setup(mock_config_entry.entry_id)

    with pytest.raises(
        HomeAssistantError, match="Failed to communicate with MotionMount"
    ):
        not await hass.services.async_call(
            "number",
            "set_value",
            {"entity_id": "number.my_motionmount_extension", "value": 9},
            blocking=True,
        )

    assert mock_motionmount.set_extension.call_count == 1


@pytest.mark.parametrize(
    "turn",
    [
        None,
        -100,
        0,
        100,
    ],
)
async def test_turn_states(
    hass: HomeAssistant,
    mock_config_entry: MockConfigEntry,
    mock_motionmount: MagicMock,
    turn: int,
) -> None:
    """Tests the state attributes."""
    mock_config_entry.add_to_hass(hass)

    mock_motionmount.is_authenticated = True
    mock_motionmount.turn = turn

    assert await hass.config_entries.async_setup(mock_config_entry.entry_id)

    assert hass.states.get("number.my_motionmount_turn").state == str(-float(turn or 0))


async def test_turn_value(
    hass: HomeAssistant,
    mock_config_entry: MockConfigEntry,
    mock_motionmount: MagicMock,
) -> None:
    """Test setting a value."""
    mock_config_entry.add_to_hass(hass)

    mock_motionmount.is_authenticated = True

    assert await hass.config_entries.async_setup(mock_config_entry.entry_id)

    await hass.services.async_call(
        "number",
        "set_value",
        {"entity_id": "number.my_motionmount_turn", "value": -9},
        blocking=True,
    )

    assert mock_motionmount.set_turn.call_count == 1
    assert mock_motionmount.set_turn.call_args_list[0][0][0] == 9


async def test_turn_exception(
    hass: HomeAssistant,
    mock_config_entry: MockConfigEntry,
    mock_motionmount: MagicMock,
) -> None:
    """Test setting a value with exception."""
    mock_config_entry.add_to_hass(hass)

    mock_motionmount.is_authenticated = True
    mock_motionmount.set_turn.side_effect = TimeoutError()

    assert await hass.config_entries.async_setup(mock_config_entry.entry_id)

    with pytest.raises(
        HomeAssistantError, match="Failed to communicate with MotionMount"
    ):
        not await hass.services.async_call(
            "number",
            "set_value",
            {"entity_id": "number.my_motionmount_turn", "value": -9},
            blocking=True,
        )

    assert mock_motionmount.set_turn.call_count == 1
