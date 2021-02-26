# magichome-adapter

Magic Home bulb adapter for WebThings Gateway.

## Initial configuration of your Magic Home device
The initial pairing of a device to your wifi network cannot be done with this adapter.
Reason being that the gateway should in that case connect to the device's wifi network for a while.

However what could be done, is create an WebThings addon that allows gateways with wired connections 
and an (unused) wifi connection to perform the pairing. This addon can then provide instructions to change the gateways settings to connect to the device's wifi network.
Afterwards the addon will discover the device's ip and pair it to the user specified wifi network.

For now: use `initial_setup.py` to perform the pairing manually

## Requirements

If you're running this add-on outside of the official gateway image for the Raspberry Pi, i.e. you're running on a development machine, you'll need to do the following (adapt as necessary for non-Ubuntu/Debian):

```
sudo pip3 install git+https://github.com/WebThingsIO/gateway-addon-python.git
```