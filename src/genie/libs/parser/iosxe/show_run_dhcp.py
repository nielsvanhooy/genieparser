import logging

from genie.metaparser import MetaParser, Any
import re

logger = logging.getLogger(__name__)


class ShowRunDhcpSchema(MetaParser):
    schema = {
        "dhcp": {
            Any(): {
                'vrf': str,
                'vrf_global': str,
                'subnet': str,
                'subnet_mask': str,
                'next_hop': str,
                'forward_address': str,
                'route_name': str,
                'metric': str,
                'track_object': str,
                'permanent': str,
                'tag': str,
                'parsing_leftovers': str,
            }
        }
    }


class ShowRunDhcp(ShowRunDhcpSchema):
    # note below command does not exist.
    # there is no command that filters all dhcp info (unless regex on cli)
    # but that is not a good option. better to leverage python for that
    # the real command we will run is show running-config.
    cli_command = "show running-config dhcp"

    # SEVERAL DIFFERENT REAL WORLD EXAMPLES
    """
    no ip dhcp conflict logging
    !
    ip dhcp pool BGB00045-0
     network 172.16.1.0 255.255.255.0
    !
    ip dhcp pool hatseflats-1
     network 172.16.2.0 255.255.255.0
    !
    ip dhcp excluded-address 10.0.11.0 10.0.11.2
    !
    ip dhcp pool ONE-1
     network 10.0.11.0 255.255.255.0
     default-router 10.0.11.1 
     domain-name dhcpdomein
    !
    """
    def cli(self, output=None):
        real_cmd = "show running-config"
        out = self.device.execute(real_cmd) if output is None else output

        dhcp = {}

        # you would use below regex if you h
        p_get_dhcp_pool_blocks = re.compile(
            r'(?P<dhcp_pool_block>ip dhcp pool[\s\S]*?(?=\n.*?\!))')
        lala = p_get_dhcp_pool_blocks.findall(out)
        match_block = re.search(p_get_dhcp_pool_blocks, out)


        for line in out.splitlines():
            line = line.strip()


