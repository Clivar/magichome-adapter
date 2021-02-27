"""Magic Home adapter for WebThings Gateway."""

from gateway_addon import Device
from flux_led import WifiLedBulb
import threading
import time

from .magichome_property import MagicHomeBulbProperty
from .util import byteToPercent, percentToByte, rgb_to_hex

_POLL_INTERVAL = 5


class MagicHomeBulb(Device):
    """Magic Home smart bulb type."""

    def __init__(self, adapter, _id, dev):
        """
        Initialize the object.

        adapter -- the Adapter managing this device
        _id -- ID of this device
        dev -- WifiLedBulb
        """
        Device.__init__(self,
                        adapter,
                        _id)
        self._type.extend(['OnOffSwitch', 'Light'])
        if isinstance(dev, WifiLedBulb):
            self.dev = dev
        else:
            print("Unknown device")
            raise Exception

        try:
            self.dev.connect(2)
            self.dev.update_state()
        except (OSError, UnboundLocalError):
            pass

        t = threading.Thread(target=self.poll)
        t.daemon = True
        t.start()

        if self.supports_color:
            self.properties['color'] = MagicHomeBulbProperty(
                self,
                'color',
                {
                    '@type': 'ColorProperty',
                    'title': 'Color',
                    'type': 'string',
                },
                self.color
            )
        if self.supports_brightness:
            self.properties['brightness'] = MagicHomeBulbProperty(
                self,
                'brightness',
                {
                    '@type': 'BrightnessProperty',
                    'title': 'Brightness',
                    'type': 'integer',
                    'unit': 'percent',
                    'minimum': 0,
                    'maximum': 100
                },
                self.brightness
            )
        if self.supports_warm_white:
            self.properties['warmwhite'] = MagicHomeBulbProperty(
                self,
                'warmwhite',
                {
                    '@type': 'LevelProperty',
                    'title': 'Warm white',
                    'type': 'integer',
                    'unit': 'percent',
                    'minimum': 0,
                    'maximum': 100
                },
                self.warm_white
            )
        if self.supports_cold_white:
            self.properties['coldwhite'] = MagicHomeBulbProperty(
                self,
                'coldwhite',
                {
                    '@type': 'LevelProperty',
                    'title': 'Cold white',
                    'type': 'integer',
                    'unit': 'percent',
                    'minimum': 0,
                    'maximum': 100
                },
                self.cold_white
            )
        self.properties['on'] = MagicHomeBulbProperty(
            self,
            'on',
            {
                '@type': 'OnOffProperty',
                'title': 'On/Off',
                'type': 'boolean',
            },
            self.is_on
        )

    def poll(self):
        """Poll the device for changes."""
        while True:
            time.sleep(_POLL_INTERVAL)
            try:
                self.dev.connect(2)
                self.dev.update_state()
            except (OSError, UnboundLocalError):
                continue

            for prop in self.properties.values():
                prop.update()

    def setRgbw(self, r=None, g=None, b=None,
                warm_white=None,
                cold_white=None,
                brightness=None):
        """Sets the color values."""
        if not r and not g and not b:
            (r, g, b) = self.dev.getRgb()
        if not brightness:
            brightness = self.brightness
        if not warm_white:
            warm_white = self.warm_white
        if not cold_white:
            cold_white = self.cold_white

        self.dev.setRgbw(
            r, g, b,
            w=percentToByte(warm_white),
            w2=percentToByte(cold_white),
            brightness=percentToByte(brightness))

    @property
    def is_on(self):
        """
        Defines wether the LED is on or off
        Returns true or false
        """
        return self.dev.is_on

    @property
    def brightness(self):
        """
        Returns the brightness in percent (0-100)
        """
        if not self.supports_brightness:
            return None
        return byteToPercent(self.dev.brightness)

    @property
    def warm_white(self):
        """
        Returns warm white in percent (0-100)
        """
        if not self.supports_warm_white:
            return None
        return byteToPercent(self.dev.warm_white)

    @property
    def cold_white(self):
        """
        Returns cold white in percent (0-100)
        """
        if not self.supports_cold_white:
            return None
        return byteToPercent(self.dev.cold_white)

    @property
    def color(self):
        """
        Returns the color in hex (#xxxxxx)
        """
        if not self.supports_color:
            return None
        return rgb_to_hex(*self.dev.getRgb())

    @property
    def supports_color(self):
        return self.dev.mode == "color"

    @property
    def supports_brightness(self):
        return self.dev.mode != 'ww'

    @property
    def supports_warm_white(self):
        return self.dev.mode == 'ww' or self.dev.rgbwcapable

    @property
    def supports_cold_white(self):
        return self.dev.protocol == "LEDENET" and self.dev.rgbwcapable
