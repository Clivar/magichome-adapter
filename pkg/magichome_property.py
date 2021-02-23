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
        if self.name == 'on':
            if value:
                self.device.dev.turnOn()
            else:
                self.device.dev.turnOff()
        elif self.name == 'color':
            self.device.dev.setRgb(
                *hex_to_rgb(value), brightness=self.device.dev.brightness)
        elif self.name == 'brightness':
            self.device.dev.setRgb(*self.device.dev.getRgb(), brightness=value)
        else:
            return
        self.set_cached_value(value)
        self.device.notify_property_changed(self)
