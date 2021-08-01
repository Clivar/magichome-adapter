# magichome-adapter

Magic Home bulb adapter for WebThings Gateway.

## Supported devices
- RGB (not tested but should work)
- RGBW (not tested but should work)
- RGBWW (tested)
- RGBCW (ongoing, not supported)
- Single color (tested)

## Getting started
1. Link your device to your wifi network.  
You can use the MagicHome app or use `initial_setup.py` (don't forget to edit the script with your ssid and password)
2. Pair the device to your gateway.  
If the device is in the same network (subnet) as the gateway, it will autodiscover (make sure multicast traffic is not filtered).  
If the device is not in the same network. Add the device ip manually in settings.
3. Done!

## Development

If you're running this add-on outside of the official gateway image for the Raspberry Pi, i.e. you're running on a development machine, you'll need to do the following (adapt as necessary for non-Ubuntu/Debian):

```
sudo pip3 install git+https://github.com/WebThingsIO/gateway-addon-python.git
```
