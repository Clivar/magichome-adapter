"""Test flux_led behaviour during reverse engineering"""
from flux_led import WifiLedBulb


def main():
    device = WifiLedBulb('')
    print(device.getClock())
    device.setRgb(0, 0, 0, brightness=20)
    print(device.brightness)


if __name__ == '__main__':
    main()