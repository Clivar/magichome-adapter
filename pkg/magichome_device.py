"""Magic Home adapter for WebThings Gateway."""

from gateway_addon import Device
from flux_led import WifiLedBulb

from .magichome_property import MagicHomeBulbProperty
from .util import rgb_to_hex


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
                    rgb_to_hex(*dev.getRgb())
                )
                if dev.rgbwcapable:
                    self.properties['warmWhite'] = MagicHomeBulbProperty(
                        self,
                        'warmWhite',
                        {
                            '@type': 'LevelProperty',
                            'title': 'Warm white',
                            'type': 'integer',
                            'unit': 'percent',
                            'minimum': 0,
                            'maximum': 255
                        },
                        dev.warm_white
                    )
                    if dev.protocol == "LEDENET":
                        self.properties['coldWhite'] = MagicHomeBulbProperty(
                            self,
                            'coldWhite',
                            {
                                '@type': 'LevelProperty',
                                'title': 'Cold white',
                                'type': 'integer',
                                'minimum': 0,
                                'maximum': 255
                            },
                            dev.cold_white
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
                        dev.brightness
                    )
            if dev.mode == 'ww':
                self.properties['warmwhite'] = MagicHomeBulbProperty(
                    self,
                    'warmwhite',
                    {
                        '@type': 'LevelProperty',
                        'title': 'WarmWhite',
                        'type': 'integer',
                        'minimum': 0,
                        'maximum': 255
                    },
                    dev.warm_white
                )
            self.properties['on'] = MagicHomeBulbProperty(
                self,
                'on',
                {
                    '@type': 'OnOffProperty',
                    'title': 'On/Off',
                    'type': 'boolean',
                },
                dev.is_on
            )
