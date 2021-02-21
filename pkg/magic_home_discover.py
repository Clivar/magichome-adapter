from flux_led import WifiLedBulb


def main():
    device = WifiLedBulb('10.10.21.100')
    print(device.getClock())
    print(hex(device.raw_state[4]))


if __name__ == '__main__':
    main()
