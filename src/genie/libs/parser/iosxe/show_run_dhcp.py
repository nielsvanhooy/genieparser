import logging
from genie.metaparser import MetaParser
from genie.metaparser.util.schemaengine import Any, Optional
import re
from netaddr import AddrFormatError, IPAddress, IPNetwork

logger = logging.getLogger(__name__)

# all cisco options
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


def create_cidr_notation(subnet, mask):
    try:
        cidr = IPNetwork(f"{subnet}/{mask}").prefixlen
        # ex:  10.0.0.0/24
        return f"{subnet}/{cidr}"
    except AddrFormatError:
        return "0.0.0.0"


def check_if_ip_in_network(ipaddress, network, subnet_mask):
    cidr = create_cidr_notation(network, subnet_mask)
    return IPAddress(ipaddress) in IPNetwork(cidr)


def extract_excluded_ip_address(exclude_addresses, subnet, subnet_mask):
    """
    Used in: DHCP Pools
    Example: ip dhcp excluded-address x.x.x.x x.x.x.x
    two conditions:
    exclude host:
        check if ip is in range --> add in exclude address as start and end
    exclude range
        check if first is in range --> exit when not
        if in range check, second --> if ok than add both to exclude address
        as start and end address

    If none matches return empty string
    :param settings:
    :return:
    """
    excluded_ip_addresses = {}

    for exclude_address in exclude_addresses:
        in_network = True
        in_network = check_if_ip_in_network(
            exclude_address,
            subnet,
            subnet_mask)
        if not in_network:
            break

        if len(exclude_addresses) > 1:
            excluded_ip_addresses = {'start': exclude_addresses[0],
                                     'end': exclude_addresses[1]}
        else:
            excluded_ip_addresses = {'start': exclude_addresses[0],
                                     'end': exclude_addresses[0]}

    return excluded_ip_addresses


class ShowRunDhcpSchema(MetaParser):
    schema = {
        "dhcp": {
            Optional("global_settings"): {
            },
            Optional("dhcp_pools"): {
                Any(): {
                    Optional("domain"): str,
                    Optional("gateway"): str,
                    Optional("vrf"): str,
                    Optional("netbios_name_servers"): list,
                    Optional("dhcp_excludes"): list,
                    Optional("networks"): [{
                        Optional("ip"): str,
                        Optional("subnet_mask"): str,
                        Optional("secundary"): bool,
                    }],
                    Optional("dhcp_options"): [{
                        Optional("option"): str,
                        Optional("type"): str,
                        Optional("data"): str
                    }],
                    Optional("lease_time"): str
                },
            },
        },
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

        # below regex extracts blocks op dhcp pools until the ! char:
        # !
        # ip dhcp pool hatseflats-2
        #  network 172.16.3.0 255.255.255.0
        # !
        p_get_dhcp_pool_blocks = re.compile(
            r'(?P<dhcp_pool_block>ip dhcp pool[\s\S]*?(?=\n.*?\!))')

        # note: can be multiples of below in a configuration
        # ex: ip dhcp excluded-address 10.0.11.0 10.0.11.2
        # ex: ip dhcp excluded-address vrf lala 10.0.11.0 10.0.11.2
        p_get_dhcp_excluded = re.compile(
            r"^ip dhcp excluded-address (.*?)(?P<excludes>[0-9]+.*)$")

        # regex extraction patterns for inside a block
        # note that we stripped the ident space of it
        #
        # ex:  domain-name Wijnen.local
        p_block_pool_name = re.compile(r"^ip dhcp pool (?P<pool_name>.*)$")
        p_block_domain = re.compile(r"^domain-name (?P<domain_name>.*$)")

        # ex:  default-router 10.24.125.254
        # ex:  default-router hostname.com
        p_block_gateway = re.compile(
            r"^default-router (?P<gateway>\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}|\w.*)$")

        # ex:  network 10.0.10.160 255.255.255.240
        p_block_network = re.compile(
            r"^network\s(?P<ip>\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3})\s+(?P<subnet_mask>\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3})$")
        # ex:  network 10.0.10.160 255.255.255.240 secondary
        p_block_network_secondary = re.compile(
            r"^network\s(?P<ip>\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3})\s+(?P<subnet_mask>\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3})\s+(?P<secondary>secondary)$")

        # note: there are a lot of options. for parsing we do not opinionate
        # we also dont do matching in the option data.
        # because it can contain almost everything
        p_block_options = re.compile(
            r"^option\s(?P<option>\d+)\s(?P<type>\w+)\s(?P<data>.*)$")

        # we capture everything after the keyword and split it later.
        # ex:  netbios-name-server 172.16.1.21 domain2.com
        # ex:  netbios-name-server domain1.com domain2.com
        # ex:  netbios-name-server 172.16.1.21 172.14.9.2
        p_block_netbios_servers = re.compile(
            r"^netbios-name-server\s(?P<netbios_servers>.*)$")

        # lease can be in format: lease 0, lease 0 0, lease 0 0 0
        # where the zero can be a number. in format hour minute second
        # or with the word infinite.
        p_block_lease_time = re.compile(
            r"^lease\s+(?P<lease_options>infinite|.*)$")

        # ex:  vrf my_first_vrf
        p_block_vrf = re.compile(r"^vrf\s+(?P<vrf>.*)$")

        # try except for routers without pools
        get_dhcp_pool_blocks = p_get_dhcp_pool_blocks.findall(out)

        excludes_list = []
        for line in out.splitlines():
            line = line.strip()

            m = p_get_dhcp_excluded.match(line)
            if m:
                excludes = m.groupdict()["excludes"]
                excludes_list.append(excludes.split(" "))

        dhcp_pools = {}
        for block in get_dhcp_pool_blocks:
            for line in block.splitlines():
                line = line.strip()

                m = p_block_pool_name.match(line)
                if m:
                    pool_name = m.groupdict()['pool_name']
                    # the name of the pool defines the dict
                    # we also setup the structure
                    dhcp_pools[pool_name] = {}
                    dhcp_pools[pool_name]['networks'] = []
                    dhcp_pools[pool_name]['options'] = []
                    dhcp_pools[pool_name]['dhcp_excludes'] = []

                m = p_block_domain.match(line)
                if m:
                    domain_name = m.groupdict()['domain_name']
                    dhcp_pools[pool_name]['domain'] = domain_name

                m = p_block_gateway.match(line)
                if m:
                    gateway = m.groupdict()['gateway']
                    dhcp_pools[pool_name]['gateway'] = gateway

                m = p_block_network.match(line)
                if m:
                    ip = m.groupdict()['ip']
                    subnet = m.groupdict()['subnet_mask']
                    network = {
                        "ip": ip,
                        "subnet_mask": subnet,
                        "secondary": False,
                    }
                    dhcp_pools[pool_name]['networks'].append(network)
                    # make sure there are excludes otherwise useless
                    if len(excludes_list) >= 1:
                        for excluded in excludes_list:
                            matched = extract_excluded_ip_address(
                                excluded,
                                network['ip'],
                                network['subnet_mask'],
                            )
                            if matched:
                                dhcp_pools[pool_name]['dhcp_excludes'].append(
                                    matched)

                m = p_block_network_secondary.match(line)
                if m:
                    ip = m.groupdict()['ip']
                    subnet = m.groupdict()['subnet_mask']
                    secondary = True if m.groupdict()['secondary'] else False
                    network = {
                        "ip": ip,
                        "subnet_mask": subnet,
                        "secondary": secondary,
                    }
                    dhcp_pools[pool_name]['networks'].append(network)
                    # make sure there are excludes otherwise useless
                    if len(excludes_list) >= 1:
                        for excluded in excludes_list:
                            matched = extract_excluded_ip_address(
                                excluded,
                                network['ip'],
                                network['subnet_mask'],
                            )
                            if matched:
                                dhcp_pools[pool_name]['dhcp_excludes'].append(
                                    matched)

                m = p_block_options.match(line)
                if m:
                    option = m.groupdict()['option']
                    type = m.groupdict()['type']
                    data = m.groupdict()['data']
                    option = {
                        "option": option,
                        "type": type,
                        "data": data,
                    }
                    dhcp_pools[pool_name]['options'].append(option)

                m = p_block_netbios_servers.match(line)
                if m:
                    # perhaps we dont need to split.
                    # but then its a not a nice list
                    _ = m.groupdict()['netbios_servers']
                    netbios_servers = _.split(" ")
                    dhcp_pools[pool_name]['netbios_servers'] = netbios_servers

                m = p_block_lease_time.match(line)
                if m:
                    lease_time = m.groupdict()['lease_options']
                    dhcp_pools[pool_name]['lease_time'] = lease_time

                m = p_block_vrf.match(line)
                if m:
                    vrf = m.groupdict()['vrf']
                    dhcp_pools[pool_name]['vrf'] = vrf

        loeloe = "lala"