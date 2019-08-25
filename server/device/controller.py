import socket
import logging as log


class Controller:
    def __init__(self, ips: list = [], port: int = 10001):
        """
        Initialize the device controller and "open" a socket.


        :param ips: list
        :param port: int
        """
        self._ips = ips
        self._port = port
        self._sock = socket.socket(
            socket.AF_INET,
            socket.SOCK_DGRAM,
            socket.IPPROTO_UDP
        )

        if len(self._ips) < 1:
            log.warning("No devices has been added yet")

    def set_port(self, port: int) -> int:
        """ Set the port to which the device controller needs to send the packets to.

        Make sure that the port is same as the one set on your device.
        :rtype: int
        :param port: int
        """

        self._port = port
        return self._port

    def list_devices(self) -> list:
        """ Returns a list of IP addresses of devices which are added.

        :return: list
        """

        return self._ips

    def add_devices(self, ip_list: list) -> list:
        """ Add a new device by providing it's IP address.
        If there's only one new device then it should also be in a single item list.

        :param ip_list: list
        :return: list
        """

        self._ips.extend(ip_list)
        return self._ips

    def remove_devices(self, start: int, end: int) -> list:
        """ Remove a set of devices and return the new list.

        :param start: int
        :param end: int
        :return: list
        """

        del self._ips[start: end + 1]
        return self._ips

    def send_all(self, payload: list) -> None:
        """ Send a payload to all the devices

        :param payload: list
        """

        for i, device in enumerate(self._ips):
            self.send_to(i, payload)

    def send_to(self, index: int, payload: list) -> None:
        """ Send the payload to an individual device by providing it's index.

        :param index: int
        :param payload: list
        """

        try:
            self._sock.sendto(bytes(payload), (self._ips[index], self._port))
        except IndexError:
            log.error("Device %i does not exist", index)
        except OSError as error:
            log.error("Couldn't inform %s: %s", self._ips[index], error)
