"""Magic Home adapter for WebThings Gateway."""
from gateway_addon import Property
from .util import hex_to_rgb


class MagicHomeBulbProperty(Property):
    """Property type for Magic Home smart bulbs."""

    def __init__(self, device, name, description, value):
        """
        Initialize the object.

        device -- the Device this property belongs to
        name -- name of the property
        description -- description of the property, as a dictionary
        value -- current value of this property
        """
        Property.__init__(self, device, name, description)
        self.set_cached_value(value)

    def set_value(self, value):
        """
        Set the current value of the property.

        value -- the value to set
        """
        try:
            if self.name == 'on':
                if value:
                    self.device.dev.turnOn()
                else:
                    self.device.dev.turnOff()
            elif self.name == 'color':
                self.device.setRgbw(*hex_to_rgb(value))
            elif self.name == 'brightness':
                self.device.setRgbw(brightness=value)
            elif self.name == 'coldwhite':
                self.device.setRgbw(cold_white=value)
            elif self.name == 'warmwhite':
                self.device.setRgbw(warm_white=value)
            else:
                return
        except (OSError, UnboundLocalError):
            return

        self.set_cached_value(value)
        self.device.notify_property_changed(self)

    def update(self):
        """
        Update the current value, if necessary.
        """
        if self.name == 'on':
            value = self.device.is_on
        elif self.name == 'color':
            value = self.device.color
        elif self.name == 'brightness':
            value = self.device.brightness
        elif self.name == 'coldwhite':
            value = self.device.cold_white
        elif self.name == 'warmwhite':
            value = self.device.warm_white
        else:
            return

        if value != self.value:
            self.set_cached_value(value)
            self.device.notify_property_changed(self)
