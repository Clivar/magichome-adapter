"""Magic Home adapter for WebThings Gateway."""

from gateway_addon import Adapter, Database
from flux_led import BulbScanner, WifiLedBulb
import socket

from .magichome_device import MagicHomeBulb


_TIMEOUT = 3


class MagicHomeAdapter(Adapter):
    """Adapter for Magic Home smart home devices."""

    def __init__(self, verbose=False):
        """
        Initialize the object.

        verbose -- whether or not to enable verbose logging
        """
        self.name = self.__class__.__name__
        Adapter.__init__(self,
                         'magichome-adapter',
                         'magichome-adapter',
                         verbose=verbose)

        self.pairing = False
        self.start_pairing(_TIMEOUT)

    def _add_from_config(self):
        """Attempt to add all configured devices."""
        database = Database('magichome-adapter')
        if not database.open():
            return

        config = database.load_config()
        database.close()

        if not config or 'addresses' not in config:
            return

        for address in config['addresses']:
            try:
                sock = socket.socket(
                    socket.AF_INET,  # Internet
                    socket.SOCK_DGRAM  # UDP
                )
                sock.setsockopt(socket.SOL_SOCKET,
                                socket.SO_BROADCAST,
                                1)
                sock.settimeout(2)  # seconds - in reality << 1 is needed

                # connect to network
                sock.sendto('HF-A11ASSISTHREAD'.encode('ascii'),
                            (address, 48899))
                data, addr = sock.recvfrom(1024)
                data = data.decode('ascii')
                socketip, socketmac, socketmodel = data.split(',')
                dev = dict()
                dev['ipaddr'] = socketip
                dev['id'] = socketmac
                dev['model'] = socketmodel
            except (OSError, UnboundLocalError) as e:
                print('Failed to connect to {}: {}'.format(address, e))
                continue

            if dev:
                self._add_device(dev)

    def start_pairing(self, timeout):
        """
        Start the pairing process.

        timeout -- Timeout in seconds at which to quit pairing
        """
        if self.pairing:
            return

        self.pairing = True

        self._add_from_config()
        scanner = BulbScanner()
        for device in scanner.scan(timeout=min(timeout, _TIMEOUT)):
            if not self.pairing:
                break

            self._add_device(device)

        self.pairing = False

    def _add_device(self, dev):
        """
        Add the given device, if necessary.

        dev -- the device object
        """
        _id = 'magichome-' + dev['id']
        if _id not in self.devices:
            device = MagicHomeBulb(
                self, _id, WifiLedBulb(dev['ipaddr']))
            self.handle_device_added(device)

    def cancel_pairing(self):
        """Cancel the pairing process."""
        self.pairing = False
