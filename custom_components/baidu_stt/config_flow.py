from __future__ import annotations

from typing import Any
import homeassistant.helpers.config_validation as cv
import voluptuous as vol
import logging
from homeassistant.config_entries import ConfigFlow
from homeassistant.const import CONF_API_KEY
from .manifest import manifest

from homeassistant.config_entries import ConfigFlow        ##, OptionsFlow, ConfigEntry
from homeassistant.data_entry_flow import FlowResult
from homeassistant.core import callback
from .const import (
    DOMAIN,
    NAME,
    )
#from . import DOMAIN

_LOGGER = logging.getLogger(__name__)

CONF_APP_ID = "app_id"
CONF_SECRET_KEY = "secret_key"

class ConfigFlowHandler(ConfigFlow, domain=DOMAIN):

    async def async_step_user(
        self, user_input: dict[str, Any] | None = None
    ) -> FlowResult:
        
        data_schema = vol.Schema({})
        errors = {}
        if self._async_current_entries():
            return self.async_abort(reason="single_instance_allowed")

        if user_input is None:
            _LOGGER.debug("Baidu Stt start async_step_user")
            return self.async_show_form(
                step_id="user",
                data_schema=vol.Schema(
                    {
                        vol.Required(CONF_APP_ID, default=""): cv.string,
                        vol.Required(CONF_API_KEY, default=""): cv.string,
                        vol.Required(CONF_SECRET_KEY, default=""): cv.string,
                    },
                ),
                errors=errors,
            )

        _LOGGER.debug("Baidu stt start async_create_entry")
#        return self.async_create_entry(title=manifest.name, data=user_input)
        return self.async_create_entry(title = NAME, data=user_input)