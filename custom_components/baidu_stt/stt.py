"""Support for Baidu speech to text service."""
from __future__ import annotations
import logging
import voluptuous as vol
from collections.abc import AsyncIterable
from homeassistant.components.tts import CONF_LANG, PLATFORM_SCHEMA, Provider
from homeassistant.const import CONF_API_KEY
from homeassistant.components import stt
from homeassistant.config_entries import ConfigEntry
from homeassistant.core import HomeAssistant
from homeassistant.helpers.entity_platform import AddEntitiesCallback
import homeassistant.helpers.config_validation as cv

from aip import AipSpeech
#from . import DOMAIN
from .const import DOMAIN
_LOGGER = logging.getLogger(__name__)

from homeassistant.components.stt import (
    AudioBitRates,
    AudioChannels,
    AudioCodecs,
    AudioFormats,
    AudioSampleRates,
    Provider,
    SpeechMetadata,
    SpeechResult,
    SpeechResultState,
)


CONF_APP_ID = "app_id"
CONF_SECRET_KEY = "secret_key"

LANGUAGES_Dictionary = {
	'普通话': 1537,
	'英语': 1737, 
	'粤语': 1637, 
	'四川话': 1837
}

SUPPORTED_LANGUAGES= list(LANGUAGES_Dictionary.keys())
DEFAULT_LANG = "普通话"

PLATFORM_SCHEMA = PLATFORM_SCHEMA.extend(
    {
        vol.Required(CONF_APP_ID): cv.string,
        vol.Required(CONF_API_KEY): cv.string,
        vol.Required(CONF_SECRET_KEY): cv.string,
    }
)

async def async_setup_entry(
    hass: HomeAssistant,
    config_entry: ConfigEntry,
    async_add_entities: AddEntitiesCallback,
) -> None:
    async_add_entities([BaiduSTT(hass, config_entry)])

class BaiduSTT(stt.SpeechToTextEntity):
    def __init__(self, hass: HomeAssistant, config_entry: ConfigEntry) -> None:
        #   """Init Baidu STT Entity."""
        # self._app_data = {
            # "appid": config_entry.data[CONF_APP_ID],
            # "apikey": config_entry.data[CONF_API_KEY],
            # "secretkey": config_entry.data[CONF_SECRET_KEY],
        # }
        hass.data.setdefault(DOMAIN, {})
        self.appid = config_entry.data[CONF_APP_ID]
        self.apikey = config_entry.data[CONF_API_KEY]
        self.secretkey = config_entry.data[CONF_SECRET_KEY]
        self._attr_name = 'BaiduStt'
        self._attr_unique_id = f"{config_entry.entry_id[:7]}-stt"

    @property
    def supported_languages(self) -> list[str]:
        """Return a list of supported languages."""
        return SUPPORTED_LANGUAGES

    @property
    def supported_formats(self) -> list[AudioFormats]:
        """Return a list of supported formats."""
        return [AudioFormats.WAV, AudioFormats.OGG]

    @property
    def supported_codecs(self) -> list[AudioCodecs]:
        """Return a list of supported codecs."""
        return [AudioCodecs.PCM, AudioCodecs.OPUS]

    @property
    def supported_bit_rates(self) -> list[AudioBitRates]:
        """Return a list of supported bitrates."""
        return [AudioBitRates.BITRATE_16]

    @property
    def supported_sample_rates(self) -> list[AudioSampleRates]:
        """Return a list of supported samplerates."""
        return [AudioSampleRates.SAMPLERATE_16000]

    @property
    def supported_channels(self) -> list[AudioChannels]:
        """Return a list of supported channels."""
        return [AudioChannels.CHANNEL_MONO]

    async def async_process_audio_stream(
        self, metadata: SpeechMetadata, stream: AsyncIterable[bytes]
    ) -> SpeechResult:
        _LOGGER.debug("Baidu Speech to text process_audio_stream start")
        # Collect data
        audio_data = bytes() ### 声明空的字节变量
        async for chunk in stream:
            audio_data += chunk
        
        _LOGGER.debug(f"Baidu Speech to text process_audio_stream transcribe: {len(audio_data)} bytes")

        # """Process an audio stream to STT service."""

        # aip_speech = AipSpeech(
            # str(self._app_data["appid"]),
            # self._app_data["apikey"],
            # self._app_data["secretkey"],
        # )
        stream_langugage =LANGUAGES_Dictionary[metadata.language]
        aip_speech = AipSpeech(self.appid, self.apikey, self.secretkey)
        try:
            response_json = await self.hass.async_add_executor_job( aip_speech.asr,audio_data, 'pcm', 16000, {'dev_pid':stream_langugage,})
            _LOGGER.debug(f"Received response from Baidu REST-API-PythonSDK with {response_json}")
            if  response_json['err_no'] == 0:
                response =''.join(response_json['result'])
                _LOGGER.info(f"Baidu Speech to text process_audio_stream end: {response}")
                return SpeechResult(response, SpeechResultState.SUCCESS)
            else:
                return stt.SpeechResult(f"识别出现异常: {response_json['err_msg']}", stt.SpeechResultState.SUCCESS)
                
        except Exception as err:
            _LOGGER.exception("Error processing audio stream: %s", err)
            return stt.SpeechResult('识别连接出现异常，请检查密钥是否正确，或者联系插件作者寻求帮助', stt.SpeechResultState.SUCCESS)

        return SpeechResult(None, SpeechResultState.ERROR)
      
