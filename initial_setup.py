import socket
import time
import sys

DISCOVERY_PORT = 48899


def find_devices(bind_ip='', timeout=2) -> list:
    """
    Scans the local subnet for Magic Home devices by using a broadcast

    bind_ip -- in case the host is using multiple network interfaces,
    specify the ip of that local interface
    timeout -- specify how long it should wait after the broadcast
    for devices to respond
    """
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    sock.bind((bind_ip, DISCOVERY_PORT))
    sock.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)

    msg = "HF-A11ASSISTHREAD".encode('ascii')

    # set the time at which we will quit the search
    quit_time = time.time() + timeout

    # outer loop for query send
    while True:
        if time.time() > quit_time:
            break
        # send out a broadcast query
        sock.sendto(msg, ('<broadcast>', DISCOVERY_PORT))

        # inner loop waiting for responses
        ips = []
        while True:
            sock.settimeout(1)
            try:
                data, addr = sock.recvfrom(64)
            except socket.timeout:
                data = None
                if time.time() > quit_time:
                    break

            if data is None:
                continue
            if data == msg:
                continue

            data = data.decode('ascii')
            data_split = data.split(',')
            if len(data_split) < 3:
                continue
            ips.append(data_split[0])
        return ips


def configureWifi(ip, ssid, key):
    """
    Re-configures the wifi settings of the specified Magic Home device

    ip -- the ip of the device
    ssid -- name of the wireless network
    key -- password of the wireless network
    """
    sock = socket.socket(
        socket.AF_INET,  # Internet
        socket.SOCK_DGRAM  # UDP
    )
    sock.setsockopt(socket.SOL_SOCKET,
                    socket.SO_BROADCAST,
                    1)
    sock.settimeout(2)

    # connect to network
    sock.sendto('HF-A11ASSISTHREAD'.encode('ascii'),
                (ip, DISCOVERY_PORT))
    data, addr = sock.recvfrom(1024)
    data = data.decode('ascii')
    socketip, socketmac, sockethost = data.split(',')
    print('Device identifies as the following: IP="%s", MAC="%s", Host="%s"' %
          (socketip, socketmac, sockethost))
    sock.sendto('+ok='.encode('ascii'),
                (ip, DISCOVERY_PORT))  # ack
    sock.sendto('AT+WSSSID={}\r'.format(ssid).encode('ascii'),
                (ip, DISCOVERY_PORT))
    data, addr = sock.recvfrom(1024)

    data = data.decode('ascii')
    if data.rstrip() != '+ok=':
        print('FATAL - got "%s" in response to set SSID' %
              data.rstrip(), file=sys.stderr)
        sys.exit(1)

    sock.sendto('AT+WSKEY=WPA2PSK,AES,{}\r'.format(key).encode('ascii'),
                (ip, DISCOVERY_PORT))
    data, addr = sock.recvfrom(1024)

    data = data.decode('ascii')
    if data.rstrip() != '+ok=':
        print('FATAL - got "%s" in response to set KEY' %
              data.rstrip(), file=sys.stderr)
        sys.exit(1)

    sock.sendto('AT+WMODE=STA\r'.encode('ascii'),
                (ip, DISCOVERY_PORT))
    data, addr = sock.recvfrom(1024)

    data = data.decode('ascii')
    if data.rstrip() != '+ok=':
        print('FATAL - got "%s" in response to set MODE' %
              data.rstrip(), file=sys.stderr)
        sys.exit(1)

    sock.sendto("AT+Z\r".encode('ascii'),
                (ip, DISCOVERY_PORT))  # no return
    print("connect complete to \"%s\"" % ssid)
