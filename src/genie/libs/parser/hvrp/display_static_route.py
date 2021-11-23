from genie.metaparser import MetaParser, Any
import re
import logging


class DisplayStaticrouteSchema(MetaParser):
    schema = {
        "ip_routes": {
            Any(): {
                # 'vrf': str,
                'subnet': str,
                'subnet_mask': str,
                'next_hop': str,
                # 'forward_address': str,
                # 'route_name': str,
                'metric': str,
                # 'track_object': str,
            }
        }
    }


class DisplayStaticroute(DisplayStaticrouteSchema):
    cli_command = "display current-configuration | include ^ip route-static"

    """
    ip route-static 0.0.0.0 0.0.0.0 213.162.171.193 preference 1
    ip route-static 0.0.0.0 0.0.0.0 Tunnel0/0/10 preference 5
    ip route-static 10.127.249.45 255.255.255.255 Cellular0/0/0 preference 10
    ip route-static 145.7.64.247 255.255.255.255 NULL0 preference 250
    ip route-static 145.13.71.128 255.255.255.128 213.162.171.193 preference 1
    ip route-static 145.13.71.128 255.255.255.128 NULL0 preference 250
    ip route-static 145.13.71.128 255.255.255.128 Tunnel0/0/10 preference 5
    ip route-static 145.13.71.128 255.255.255.128 Cellular0/0/0 preference 10
    ip route-static 145.13.76.0 255.255.255.0 213.162.171.193 preference 1
    ip route-static 145.13.76.0 255.255.255.0 NULL0 preference 250
    ip route-static 145.13.76.0 255.255.255.0 Tunnel0/0/10 preference 5
    ip route-static 145.13.76.0 255.255.255.0 Cellular0/0/0 preference 10
    ip route-static 192.168.28.0 255.255.255.0 213.162.171.193 preference 1
    ip route-static 192.168.28.0 255.255.255.0 NULL0 preference 250
    ip route-static 192.168.28.0 255.255.255.0 Tunnel0/0/10 preference 5
    ip route-static 192.168.28.0 255.255.255.0 Cellular0/0/0 preference 10
    """

    def cli(self, output=None):
        out = self.device.execute(
            self.cli_command) if output is None else output

        ip_routes_dict = {}

        result_dict = {}

        p0 = re.compile(
            r'^ip\sroute-static\s+(?P<subnet>\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3})\s+(?P<subnet_mask>\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3})\s+(?P<next_hop>\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}|\w.*?)\s+preference\s+(?P<metric>\d{0,3})')
        logging.debug(out)
        for count, line in enumerate(out.splitlines()):
            line = line.strip()

            match = p0.match(line)
            if match:
                if 'ip_routes' not in ip_routes_dict:
                    result_dict = ip_routes_dict.setdefault('ip_routes', {})
                # vrf = match.groupdict()['vrf'] or ''
                subnet = match.groupdict()['subnet']
                subnet_mask = match.groupdict()['subnet_mask']
                next_hop = match.groupdict()['next_hop']
                # forward_address = match.groupdict()['forward_address'] or ''
                # track_object = match.groupdict()['track_object'] or \
                #                match.groupdict()['track_object_two'] or ''
                metric = match.groupdict()['metric'] or \
                         match.groupdict()['metric_two'] or ''
                # name = match.groupdict()['name'] or \
                #        match.groupdict()['name_two'] or ''
                result_dict[count] = {
                    # 'vrf': vrf,
                    'subnet': subnet,
                    'subnet_mask': subnet_mask,
                    'next_hop': next_hop,
                    # 'forward_address': forward_address,
                    # 'route_name': name,
                    'metric': metric,
                    # 'track_object': track_object
                }
                continue
        return ip_routes_dict
