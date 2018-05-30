import socket
import ipaddress as ip

class PortScanner:

    """ Simple port scanner."""

    def __init__(self, timeout=0):
        if timeout != 0:
            socket.setdefaulttimeout(timeout)


    def scan_port(self, ip, port):
        """Checks if the specified port is available

        :param ip: IP to check
        :param port: Port number to check
        :return: True if port is open, otherwise False is returned

        """

        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        result = sock.connect_ex((str(ip), int(port)))
        sock.close()
        if result == 0:
            return True
        else:
            return False

    def get_service_name(self, port):
        """Attempts to get service name running on specified port from /etc/services/

        :param port: Port number to check
        :return: Service name or empty string in case it is unable
        """

        try:
            service_name = socket.getservbyport(port)
        except:
            service_name = ""

        return service_name

    def get_ip_range(self, ip_string):
        """Attempts to parse ip_string and return all possible IP's in range

        Returns ValueError if something went wrong

        :param ip_string: String containing interval like "127.0.0.1 - 128.0.0.1"
        :return: Object generating sequence of IP addresses in specified range
        """

        ip_string = str(ip_string).replace(" ", "")
        ip_intervals = ip_string.split(",")
        for interval in ip_intervals:
            try:
                start = socket.gethostbyname(interval)
                end = start
            except socket.gaierror:
                parts = interval.split("-")
                start, end = parts[0:2]
            start = ip.ip_address(start)
            end = ip.ip_address(end)
            if start > end:
                raise ValueError
            while start <= end:
                yield start
                start += 1

    def get_port_range(self, port_string):
        """Attempts to parse port string and return all available ports in range

        :param port_string:
        :return:
        """
        port_string = str(port_string).replace(" ", "")
        port_intervals = port_string.split(",")
        for interval in port_intervals:
            start, end = interval.split("-")[0:2]
            start = int(start)
            end = int(end)
            if start > end:
                raise ValueError
            if not ((0 <= start <= 65535) or (0 <= end <= 65535)):
                raise ValueError
            while start <= end:
                yield start
                start += 1


    def get_subnet_addresses(self, ip_address, mask):
        """Takes ip address and mask and returns range of all addresses in network

        :param ip_address:
        :param mask:
        :return:
        """
        ip_interface = ip.ip_interface(ip_address + "/" + mask)
        return ip_interface.network.hosts()

    def scan(self, ip_range, port_range):
        """Scans ports specified in port_range for every IP in ip_range

        :param ip_range:
        :param port_range:
        :return: dictionary of IP values
        """

        pass
