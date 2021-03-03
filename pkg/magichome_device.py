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
            self._type.append('ColorControl')
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
        if self.supports_color_temperature:
            if 'ColorControl' not in self._type:
                self._type.append('ColorControl')

            self.properties['colorTemperature'] = MagicHomeBulbProperty(
                self,
                'colorTemperature',
                {
                    '@type': 'ColorTemperatureProperty',
                    'title': 'Color Temperature',
                    'type': 'integer',
                    'unit': 'kelvin',
                    'minimum': 2700,
                    'maximum': 6500
                },
                self.color_temperature
            )
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

    def setRgb(self, r=None, g=None, b=None,
               brightness=None):
        """Sets the color values."""
        if self.supports_color:
            if not r and not g and not b:
                (r, g, b) = self.dev.getRgb()
            if not brightness:
                brightness = self.brightness

            self.dev.setRgb(
                r, g, b,
                brightness=percentToByte(brightness))
        else:
            self.dev.setRgb(r=percentToByte(brightness),
                            g=0, b=0, brightness=0)

    def setColorTemperature(self, temperature):
        self.dev.setWhiteTemperature(
            temperature, brightness=self.dev.brightness)

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
        if self.supports_color:
            return byteToPercent(self.dev.brightness)
        else:
            (r, _, _) = self.dev.getRgb()
            return byteToPercent(r)

    @property
    def color(self):
        """
        Returns the color in hex (#xxxxxx)
        """
        if not self.supports_color:
            return None
        return rgb_to_hex(*self.dev.getRgb())

    @property
    def color_temperature(self):
        if not self.supports_color_temperature:
            return None
        return (1 -
                (self.dev.warm_white*255/percentToByte(self.brightness)/255)
                )*3800

    @property
    def supports_color(self):
        return (self.dev.mode == "color" and
                not (self.dev.raw_state[1] == 0x21 or
                     self.dev.raw_state[1] == 0x41))

    @property
    def supports_color_temperature(self):
        return self.dev.protocol == 'LEDENET'
