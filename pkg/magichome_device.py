"""Magic Home adapter for WebThings Gateway."""

from gateway_addon import Device
from flux_led import WifiLedBulb
import threading
import time

from .magichome_property import MagicHomeBulbProperty
from .util import rgb_to_hex

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
        self.dev = dev

        try:
            self.dev.connect(2)
            self.dev.update_state()
        except (OSError, UnboundLocalError):
            pass

        t = threading.Thread(target=self.poll)
        t.daemon = True
        t.start()

        if isinstance(dev, WifiLedBulb):
            if dev.mode == 'color':
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
                if dev.rgbwcapable:
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
                    if dev.protocol == "LEDENET":
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
                else:
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
            if dev.mode == 'ww':
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

    @property
    def is_on(self):
        return self.dev.is_on

    @property
    def brightness(self):
        return self.dev.brightness

    @property
    def warmwhite(self):
        return self.dev.warm_white / 255 * 100

    @property
    def coldwhite(self):
        return self.dev.cold_white / 255 * 100

    @property
    def color(self):
        return rgb_to_hex(*self.dev.getRgb())
