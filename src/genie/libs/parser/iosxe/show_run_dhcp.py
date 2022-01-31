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
    # testing was done with below strings
    """
    no ip dhcp conflict logging
    ip dhcp excluded-address 10.1.1.2 10.1.1.10
    ip dhcp excluded-address vrf lala 10.2.2.0 10.2.2.244
    !
    ip dhcp pool hatseflats-1
     network 172.16.2.0 255.255.255.0
    !
    ip dhcp pool hatseflats-2
     network 172.16.3.0 255.255.255.0
    !
    ip dhcp pool ONE-1
     domain-name nelis.nl
     dns-server 10.1.1.99 
     option 150 ip 10.1.1.100 
     netbios-name-server 10.1.1.101 
     netbios-node-type h-node
    !
    !
    ip dhcp excluded-address 10.0.11.0 10.0.11.2
    !
    ip dhcp pool ONE-1
     network 10.0.11.0 255.255.255.0
     default-router 10.0.11.1 
     option 150 ip 3.3.3.3 4.4.4.4
     domain-name dhcpdomein
    !
    !\r\nip dhcp pool hatseflats-1\r\n network 172.16.2.0 255.255.255.0\r\n!
    """

    def cli(self, output=None):
        real_cmd = "show running-config"
        out = self.device.execute(real_cmd) if output is None else output

        dhcp = {}

        # you would use below regex if you h
        p_get_dhcp_pool_blocks = re.compile(
            r'(?P<dhcp_pool_block>ip dhcp pool[\s\S]*?(?=\n.*?\!))')

        p_get_dhcp_excluded = re.compile(
            r"ip dhcp excluded-address ((?P<start_range>[0-9\.x]+))\s+(?P<end_range>[0-9\.x]+)")
        p_get_dhcp_excluded_vrf = re.compile(
            r"ip dhcp excluded-address (vrf (?P<vrf>.*?\s)(?P<start_range>[0-9\.x]+))\s+(?P<end_range>[0-9\.x]+)")

        get_dhcp_excluded = p_get_dhcp_excluded.findall(out)
        get_dhcp_excluded_vrf = p_get_dhcp_excluded_vrf.findall(out)
        get_dhcp_pool_blocks = p_get_dhcp_pool_blocks.findall(out)

        for line in out.splitlines():
            line = line.strip()

            #all cisco options
            """
            one-gv-2595bk-41(config)#ip dhcp pool lol 
            one-gv-2595bk-41(dhcp-config)#?
            DHCP pool configuration commands:
              accounting           Send Accounting Start/Stop messages
              address              Configure a reserved address
              authorization        Obtain address allocation information from AAA
              bootfile             Boot file name
              class                Specify a DHCP class
              client-identifier    Client identifier
              client-name          Client name
              default-router       Default routers
              dns-server           DNS servers
              domain-name          Domain name
              exit                 Exit from DHCP pool configuration mode
              hardware-address     Client hardware address
              host                 Client IP address and mask
              import               Programatically importing DHCP option parameters
              lease                Address lease time
              netbios-name-server  NetBIOS (WINS) name servers
              netbios-node-type    NetBIOS node type
              network              Network number and mask
              next-server          Next server in boot process
              no                   Negate a command or set its defaults
              option               Raw DHCP options
              origin               Configure the origin of the pool
              relay                Function as a DHCP relay
              remember             Remember released bindings
              renew                Configure renewal policy
              reserved-only        Only allocate reserved addresses
              server               Configure the server ID option value
              subnet               Subnet allocation commands
              update               Dynamic updates
              utilization          Configure various utilization parameters
              vrf                  Associate this pool with a VRF
            
            one-gv-2595bk-41(dhcp-config)#exit
            one-gv-2595bk-41(config)#ip dhc
            one-gv-2595bk-41(config)#ip dhcp ?
              aaa                        Configure aaa attributes
              auto-broadcast             Configure auto broadcast feature
              binding                    DHCP address bindings
              bootp                      BOOTP specific configuration
              class                      Configure DHCP classes
              compatibility              Compatibility configuration
              conflict                   DHCP address conflict parameters
              database                   Configure DHCP database agents
              drop-inform                Drop inform message if enabled
              excluded-address           Prevent DHCP from assigning certain addresses
              global-options             Configure global DHCP options
              limit                      Limit DHCP Lease
              limited-broadcast-address  Use all 1's broadcast address
              ping                       Specify ping parameters used by DHCP
              pool                       Configure DHCP address pools
              relay                      DHCP relay agent parameters
              remember                   Remember released bindings
              route                      Specify the type of routes for clients on unnumbered interfaces
              smart-relay                Enable Smart Relay feature
              subscriber-id              Global subscriber-id configuration
              support                    Configure support for certain features
              update                     Configure dynamic updates
              use                        Configure use of certain parameters during allocation
            """


