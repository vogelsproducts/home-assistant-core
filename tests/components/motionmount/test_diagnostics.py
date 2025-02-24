"""Tests for the diagnostics data provided by the MotionMount integration."""

import pytest
from syrupy import SnapshotAssertion

from homeassistant.core import HomeAssistant

from tests.common import MockConfigEntry
from tests.components.diagnostics import get_diagnostics_for_config_entry
from tests.typing import ClientSessionGenerator


@pytest.mark.freeze_time("2019-11-11 09:10:32+00:00")
async def test_diagnostics(
    hass: HomeAssistant,
    hass_client: ClientSessionGenerator,
    mock_config_entry: MockConfigEntry,
    snapshot: SnapshotAssertion,
) -> None:
    """Test diagnostics for config entry."""
    #    assert await get_diagnostics_for_config_entry(hass, hass_client, mock_config_entry) == "blub"
    assert (
        await get_diagnostics_for_config_entry(hass, hass_client, mock_config_entry)
        == snapshot
    )
