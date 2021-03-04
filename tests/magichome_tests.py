"""Test flux_led behaviour during reverse engineering"""
from flux_led import WifiLedBulb


def main():
    device = WifiLedBulb('<ip>')
    print(hex(device.raw_state[1]))


if __name__ == '__main__':
    main()
