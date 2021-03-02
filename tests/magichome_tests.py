"""Test flux_led behaviour during reverse engineering"""
from flux_led import WifiLedBulb


def main():
    device = WifiLedBulb('10.10.21.100')
    print(hex(device.raw_state[1]))


if __name__ == '__main__':
    main()
