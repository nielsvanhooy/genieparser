''' show_bgp.py

IOSXE parsers for the following show commands:

    * 'show bgp all'
    * 'show bgp {address_family} all'
    * 'show bgp {address_family} rd {rd}'
    * 'show bgp {address_family} vrf {vrf}'
    ----------------------------------------------------------------------------
    * 'show bgp all detail'
    * 'show bgp {address_family} vrf {vrf} detail'
    * 'show bgp {address_family} rd {rd} detail'
    ----------------------------------------------------------------------------
    * 'show bgp summary'
    * 'show bgp {address_family} summary'
    * 'show bgp {address_family} vrf {vrf} summary'
    * 'show bgp {address_family} rd {rd} summary'
    * 'show bgp all summary'
    * 'show bgp {address_family} all summary'
    ----------------------------------------------------------------------------
    * 'show bgp all neighbors'
    * 'show bgp all neighbors {neighbor}'
    * 'show bgp {address_family} all neighbors'
    * 'show bgp {address_family} all neighbors {neighbor}'
    * 'show bgp neighbors'
    * 'show bgp neighbors {neighbor}'
    * 'show bgp {address_family} neighbors'
    * 'show bgp {address_family} neighbors {neighbor}'
    * 'show bgp {address_family} vrf {vrf} neighbors'
    * 'show bgp {address_family} vrf {vrf} neighbors {neighbor}'
    ----------------------------------------------------------------------------
    * 'show bgp all neighbors {neighbor} advertised-routes'
    * 'show bgp {address_family} all neighbors {neighbor} advertised-routes'
    * 'show bgp neighbors {neighbor} advertised-routes'
    * 'show bgp {address_family} neighbors {neighbor} advertised-routes'
    ----------------------------------------------------------------------------
    * 'show bgp all neighbors {neighbor} received-routes'
    * 'show bgp {address_family} all neighbors {neighbor} received-routes'
    * 'show bgp neighbors {neighbor} received-routes'
    * 'show bgp {address_family} neighbors {neighbor} received-routes'
    ----------------------------------------------------------------------------
    * 'show bgp all neighbors {neighbor} routes'
    * 'show bgp {address_family} all neighbors {neighbor} routes'
    * 'show bgp neighbors {neighbor} routes'
    * 'show bgp {address_family} neighbors {neighbor} routes'
    * 'show bgp {address_family} vrf {vrf} neighbors {neighbor} routes'
    ----------------------------------------------------------------------------
    * show bgp all cluster-ids
    ----------------------------------------------------------------------------
    * show bgp all neighbors {neighbor} policy
    ----------------------------------------------------------------------------
    ----------------------------------------------------------------------------
    ----------------------------------------------------------------------------


    * show bgp vrf {vrf} all summary
    * show bgp vrf {vrf} {route}
    * show bgp {address_family} vrf {vrf} {route}
    * show bgp {address_family} {route}
    * show bgp l2vpn evpn evi {evi_id} route-type {route_type}
    * 'show bgp * all summary | include network'
'''

# Python
import re

# Metaparser
from genie.metaparser import MetaParser
from genie.metaparser.util.schemaengine import Schema, Any, Or, Optional

# Parser
from genie.libs.parser.iosxe.show_vrf import ShowVrf


# ============================================
# Schema for:
#   * 'show bgp all'
#   * 'show bgp {address_family} all'
#   * 'show bgp {address_family} rd {rd}'
#   * 'show bgp {address_family} vrf {vrf}'
#   * 'show ip bgp all'
#   * 'show ip bgp {address_family} all'
#   * 'show ip bgp'
#   * 'show ip bgp {address_family}'
#   * 'show ip bgp {address_family} rd {rd}'
#   * 'show ip bgp {address_family} vrf {vrf}'
# ============================================
class ShowBgpSchema(MetaParser):

    ''' Schema for:
        * 'show bgp all'
        * 'show bgp {address_family} all'
        * 'show bgp {address_family} rd {rd}'
        * 'show bgp {address_family} vrf {vrf}'
        * 'show ip bgp all'
        * 'show ip bgp {address_family} all'
        * 'show ip bgp'
        * 'show ip bgp {address_family}'
        * 'show ip bgp {address_family} rd {rd}'
        * 'show ip bgp {address_family} vrf {vrf}'
    '''

    schema = {
        'vrf':
            {Any():
                {'address_family':
                    {Any():
                        {Optional('bgp_table_version'): int,
                        Optional('route_identifier'): str,
                        Optional('vrf_route_identifier'): str,
                        Optional('route_distinguisher'): str,
                        Optional('default_vrf'): str,
                        Optional('af_private_import_to_address_family'): str,
                        Optional('pfx_count'): int,
                        Optional('pfx_limit'): int,
                        Optional('routes'):
                            {Optional(Any()):
                                {Optional('index'):
                                    {Optional(Any()):
                                        {Optional('next_hop'): str,
                                        Optional('status_codes'): str,
                                        Optional('metric'): int,
                                        Optional('localpref'): int,
                                        Optional('weight'): int,
                                        Optional('path'): str,
                                        Optional('origin_codes'): str,
                                        },
                                    },
                                },
                            },
                        },
                    },
                },
            },
        }


# ============================================
# Super Parser for:
#   * 'show bgp all'
#   * 'show bgp {address_family} all'
#   * 'show bgp {address_family} rd {rd}'
#   * 'show bgp {address_family} vrf {vrf}'
#   * 'show ip bgp all'
#   * 'show ip bgp {address_family} all'
#   * 'show ip bgp'
#   * 'show ip bgp {address_family}'
#   * 'show ip bgp {address_family} rd {rd}'
#   * 'show ip bgp {address_family} vrf {vrf}'
# ============================================
class ShowBgpSuperParser(ShowBgpSchema):

    ''' Super Parser for:
        * 'show bgp all'
        * 'show bgp {address_family} all'
        * 'show bgp {address_family} rd {rd}'
        * 'show bgp {address_family} vrf {vrf}'
        * 'show ip bgp all'
        * 'show ip bgp {address_family} all'
        * 'show ip bgp'
        * 'show ip bgp {address_family}'
        * 'show ip bgp {address_family} rd {rd}'
        * 'show ip bgp {address_family} vrf {vrf}'
    '''

    def cli(self, address_family='', vrf='', output=None):

        # Init dictionary
        route_dict = {}
        af_dict = {}
        if not vrf:
            vrf = 'default'
        if address_family:
            original_address_family = address_family
        index = 1
        bgp_table_version = local_router_id = ''
        metric = localpref = weight = ''
        status_codes = ''
        prefix = ""
        origin_codes_info = origin_codes_data = ""

        # For address family: IPv4 Unicast
        p1 = re.compile(r'^\s*For +address +family:'
                        r' +(?P<address_family>[\S\s]+)$')

        # BGP table version is 25, Local Router ID is 10.186.101.1
        p2 = re.compile(r'^\s*BGP +table +version +is'
                        r' +(?P<bgp_table_version>[0-9]+), +[Ll]ocal +[Rr]outer'
                        r' +ID +is +(?P<local_router_id>(\S+))$')

        #     Network          Next Hop            Metric LocPrf Weight Path
        # *>   [5][65535:1][0][24][10.1.1.0]/17
        # *>  100:2051:VEID-2:Blk-1/136
        #  *>   [3][3001:1][*][*][1.1.1.1]/14
        # *m   [2][2.2.2.2:1][0][48][000C293B2157][0][*]/20
        p3_1 = re.compile(r'^\s*(?P<status_codes>(s|x|S|d|h|\*|\>|m|\s)+)?'
                          r'(?P<path_type>(i|e|c|l|a|r|I))?\s*'
                          r'(?P<prefix>[a-zA-Z0-9\.\:\/\[\]\,\-\*]+)'
                          r'(?: *(?P<param>[a-zA-Z0-9\.\:\/\[\]\,]+))?$')

        #     Network          Next Hop            Metric LocPrf Weight Path
        # * i                  10.4.1.1               2219    100      0 200 33299 51178 47751 {27016} e
        #                      0.0.0.0                  0         32768 ?
        # *>                    0.0.0.0                 0         32768 ?
        # r>                    0.0.0.0                 0         32768 ?
        # *m                    0.0.0.0                 0         32768 ?
        # * i                  ::FFFF:10.4.1.1        2219    100      0 200 33299 51178 47751 {27016} e
        p3_2 = re.compile(r'^\s*(?P<status_codes>(s|x|S|d|h|\*|\>|m|r|\s)+)?'
                          r'(?P<path_type>(i|e|c|l|a|r|I))?\s{10,20}'
                          r'(?P<next_hop>[a-zA-Z0-9\.\:]+)'
                          r' +(?P<metric>(?:\d+(?=[ \d]{13}\d ))?) +(?P<local_prf>(?:\d+(?=[ \d]{6}\d ))?) +(?P<weight>\d+)'
                          r'(?P<termination>[\s\S]+)$')

        # Network            Next Hop            Metric     LocPrf     Weight Path
        # *    10.36.3.0/24       10.36.3.254                0             0 65530 ?
        # *>   10.1.1.0/24     0.0.0.0                  0         32768 ?
        # *>i 10.1.2.0/24      10.4.1.1               2219    100      0 200 33299 51178 47751 {27016} e
        # *m 10.1.2.0/24      10.4.1.1               2219    100      0 200 33299 51178 47751 {27016} e
        # *>i 2001:db8:cdc9:121::/64   ::FFFF:10.4.1.1        2219    100      0 200 33299 51178 47751 {27016} e
        # *>  100:2051:VEID-2:Blk-1/136
        # *>i10.1.1.0/24   0.0.0.0                   0    100      0 1234 60000 ?
        p4 = re.compile(r'^\s*(?P<status_codes>(?:s|x|S|d|h|m|r|\*|\>|\s)+)?'
                        r'(?P<path_type>(?:i|e|c|l|a|r|I))? *'
                        r'(?P<prefix>[a-zA-Z0-9\.\:\/\-\[\]]+) +'
                        r'(?P<next_hop>[a-zA-Z0-9\.\:]+) +'
                        r'(?P<metric>(?:\d+(?=[ \d]{13}\d ))?) +'
                        r'(?P<local_prf>(?:\d+(?=[ \d]{6}\d ))?) +'
                        r'(?P<weight>\d+)(?P<path>[0-9 \S\{\}]+)$')

        # AF-Private Import to Address-Family: L2VPN E-VPN, Pfx Count/Limit: 2/1000
        p5 = re.compile(r'^\s*AF-Private +Import +to +Address-Family:'
                        r' +(?P<af_private_import_to_address_family>[\s\S]+),'
                        r' +Pfx +Count/Limit:'
                        r' +(?P<pfx_count>[\d]+)\/+(?P<pfx_limit>[\d]+)$')

        # Route Distinguisher: 200:1
        # Route Distinguisher: 300:1 (default for vrf VRF1) VRF Router ID 10.94.44.44
        p6 = re.compile(r'^\s*Route +Distinguisher *: '
                        r'+(?P<route_distinguisher>(\S+))'
                        r'( +\(default for vrf +(?P<default_vrf>(\S+))\))?'
                        r'( +VRF Router ID (?P<vrf_router_id>(\S+)))?$')

        for line in output.splitlines():
            line = line.rstrip()

            # For address family: IPv4 Unicast
            m = p1.match(line)
            if m:
                address_family = str(m.groupdict()['address_family']).lower()
                original_address_family = address_family
                continue

            # BGP table version is 25, Local Router ID is 10.186.101.1
            m = p2.match(line)
            if m:
                bgp_table_version = int(m.groupdict()['bgp_table_version'])
                local_router_id = str(m.groupdict()['local_router_id'])
                continue

            #     Network          Next Hop            Metric LocPrf Weight Path
            # *>   [5][65535:1][0][24][10.1.1.0]/17
            # *>  100:2051:VEID-2:Blk-1/136
            m = p3_1.match(line)
            if m:
                # Get keys
                if m.groupdict()['status_codes']:
                    status_codes = m.groupdict()['status_codes']
                path_type = ''
                if m.groupdict()['path_type']:
                    path_type = str(m.groupdict()['path_type'])
                if path_type:
                    status_codes = status_codes + path_type
                else:
                    status_codes = status_codes.rstrip()

                if m.groupdict()['prefix']:
                    prefix = str(m.groupdict()['prefix'])
                index = 0
                continue

            #     Network          Next Hop            Metric LocPrf Weight Path
            # * i                  10.4.1.1               2219    100      0 200 33299 51178 47751 {27016} e
            #                      0.0.0.0                  0         32768 ?
            # *>                    0.0.0.0                 0         32768 ?
            # * i                  ::FFFF:10.4.1.1        2219    100      0 200 33299 51178 47751 {27016} e
            m = p3_2.match(line)
            if m:
                # Get keys
                path_type = ""
                path_info = ""
                if m.groupdict()['status_codes']:
                    status_codes = m.groupdict()['status_codes']
                if m.groupdict()['path_type']:
                    path_type = m.groupdict()['path_type']

                if m.groupdict()['next_hop']:
                    next_hop = m.groupdict()['next_hop']

                if path_type:
                    status_codes = status_codes + path_type
                else:
                    status_codes = status_codes.rstrip()

                if m.groupdict()['termination']:
                    termination = m.groupdict()['termination']
                    m3 = re.compile(r'(?: *(?P<path>[0-9\{\}\s]+))?'
                                    r' +(?P<origin_codes>(i|e|\?|\|))$').match(termination)
                    if m3 and m3.groupdict()['path']:
                        path_info = m3.groupdict()['path']
                    if m3 and m3.groupdict()['origin_codes']:
                        origin_codes_info = m3.groupdict()['origin_codes']

                if m.groupdict()['metric']:
                    metric = int(m.groupdict()['metric'])
                if m.groupdict()['weight']:
                    weight = int(m.groupdict()['weight'])
                if m.groupdict()['local_prf']:
                    localpref = int(m.groupdict()['local_prf'])

                index += 1
                # Init dict
                if 'vrf' not in route_dict:
                    route_dict['vrf'] = {}
                if vrf not in route_dict['vrf']:
                    route_dict['vrf'][vrf] = {}
                if 'address_family' not in route_dict['vrf'][vrf]:
                    route_dict['vrf'][vrf]['address_family'] = {}

                if address_family not in route_dict['vrf'][vrf]['address_family']:
                    route_dict['vrf'][vrf]['address_family'][address_family] = {}

                # Set af_dict
                af_dict = route_dict['vrf'][vrf]['address_family'][address_family]

                if 'routes' not in af_dict:
                    af_dict['routes'] = {}
                if prefix not in af_dict['routes']:
                    af_dict['routes'][prefix] = {}
                if 'index' not in af_dict['routes'][prefix]:
                    af_dict['routes'][prefix]['index'] = {}
                if index not in af_dict['routes'][prefix]['index']:
                    af_dict['routes'][prefix]['index'][index] = {}
                if index not in af_dict['routes'][prefix]['index']:
                    af_dict['routes'][prefix]['index'][index] = {}

                # Set keys
                if status_codes:
                    af_dict['routes'][prefix]['index'][index]['status_codes'] = status_codes

                if m.groupdict()['next_hop']:
                    af_dict['routes'][prefix]['index'][index]['next_hop'] = next_hop
                if m.groupdict()['local_prf']:
                    af_dict['routes'][prefix]['index'][index]['localpref'] = localpref
                if m.groupdict()['weight']:
                    af_dict['routes'][prefix]['index'][index]['weight'] = weight
                if m.groupdict()['metric']:
                    af_dict['routes'][prefix]['index'][index]['metric'] = metric

                if path_info:
                     af_dict['routes'][prefix]['index'][index]['path'] = path_info
                if origin_codes_info:
                    af_dict['routes'][prefix]['index'][index]['origin_codes'] = origin_codes_info

                continue

            # Network            Next Hop            Metric     LocPrf     Weight Path
            # *    10.36.3.0/24       10.36.3.254                0             0 65530 ?
            # *>   10.1.1.0/24     0.0.0.0                  0         32768 ?
            # *>i 10.1.2.0/24      10.4.1.1               2219    100      0 200 33299 51178 47751 {27016} e
            # *>i 2001:db8:cdc9:121::/64   ::FFFF:10.4.1.1        2219    100      0 200 33299 51178 47751 {27016} e
            # *>  100:2051:VEID-2:Blk-1/136
            m = p4.match(line)
            if m:
                path_type = ""
                path_data = ""
                if m.groupdict()['prefix']:
                    prefix = m.groupdict()['prefix']
                    index = 1

                # Get keys
                if m.groupdict()['status_codes']:
                    status_codes = m.groupdict()['status_codes']
                if m.groupdict()['path_type']:
                    path_type = m.groupdict()['path_type']

                if path_type:
                    status_codes = status_codes + path_type
                else:
                    status_codes = status_codes.rstrip()

                if m.groupdict()['path']:
                    path_1 = m.groupdict()['path']
                    m3 = re.compile(r'(?: *(?P<path_inner>[0-9\{\}\s\,]+))?'
                                    r' +(?P<origin_codes_inner>(i|e|\?|\|))$').match(path_1)
                    if m3:
                        path_data = m3.groupdict()['path_inner']
                        origin_codes_data = m3.groupdict()['origin_codes_inner']
                if m.groupdict()['next_hop']:
                    next_hop = m.groupdict()['next_hop']

                if m.groupdict()['metric']:
                    metric = int(m.groupdict()['metric'])
                if m.groupdict()['weight']:
                    weight = int(m.groupdict()['weight'])
                if m.groupdict()['local_prf']:
                    localpref = int(m.groupdict()['local_prf'])

                # Init dict
                if 'vrf' not in route_dict:
                    route_dict['vrf'] = {}
                if vrf not in route_dict['vrf']:
                    route_dict['vrf'][vrf] = {}
                if 'address_family' not in route_dict['vrf'][vrf]:
                    route_dict['vrf'][vrf]['address_family'] = {}

                if address_family not in route_dict['vrf'][vrf]['address_family']:
                    route_dict['vrf'][vrf]['address_family'][address_family] = {}

                # Set af_dict
                af_dict = route_dict['vrf'][vrf]['address_family'][address_family]
                if 'routes' not in af_dict:
                    af_dict['routes'] = {}
                if prefix not in af_dict['routes']:
                    af_dict['routes'][prefix] = {}
                if 'index' not in af_dict['routes'][prefix]:
                    af_dict['routes'][prefix]['index'] = {}
                if index not in af_dict['routes'][prefix]['index']:
                    af_dict['routes'][prefix]['index'][index] = {}
                if index not in af_dict['routes'][prefix]['index']:
                    af_dict['routes'][prefix]['index'][index] = {}

                # Set keys
                if status_codes:
                    af_dict['routes'][prefix]['index'][index]['status_codes'] = status_codes
                if path_data:
                    af_dict['routes'][prefix]['index'][index]['path'] = path_data
                if m.groupdict()['next_hop']:
                    af_dict['routes'][prefix]['index'][index]['next_hop'] = next_hop
                if m.groupdict()['local_prf']:
                    af_dict['routes'][prefix]['index'][index]['localpref'] = localpref
                if m.groupdict()['weight']:
                    af_dict['routes'][prefix]['index'][index]['weight'] = weight
                if m.groupdict()['metric']:
                    af_dict['routes'][prefix]['index'][index]['metric'] = metric
                if origin_codes_data:
                    af_dict['routes'][prefix]['index'][index]['origin_codes'] = origin_codes_data
                continue

            # AF-Private Import to Address-Family: L2VPN E-VPN, Pfx Count/Limit: 2/1000
            m = p5.match(line)
            if m:
                af_private_import_to_address_family = m.groupdict()['af_private_import_to_address_family']
                pfx_count = int(m.groupdict()['pfx_count'])
                pfx_limit = int(m.groupdict()['pfx_limit'])

                if 'vrf' not in route_dict:
                    route_dict['vrf'] = {}
                if vrf not in route_dict['vrf']:
                    route_dict['vrf'][vrf] = {}

                if 'address_family' not in route_dict['vrf'][vrf]:
                    route_dict['vrf'][vrf]['address_family'] = {}
                if new_address_family not in route_dict['vrf'][vrf]['address_family']:
                    route_dict['vrf'][vrf]['address_family'][new_address_family] = {}

                route_dict['vrf'][vrf]['address_family'][new_address_family] \
                    ['af_private_import_to_address_family'] = af_private_import_to_address_family

                route_dict['vrf'][vrf]['address_family'][new_address_family] \
                    ['pfx_count'] = pfx_count

                route_dict['vrf'][vrf]['address_family'][new_address_family] \
                        ['pfx_limit'] = pfx_limit

                continue

            # Route Distinguisher: 200:1
            # Route Distinguisher: 300:1 (default for vrf VRF1) VRF Router ID 10.94.44.44
            m = p6.match(line)
            if m:
                route_distinguisher = str(m.groupdict()['route_distinguisher'])
                new_address_family = original_address_family + ' RD ' + route_distinguisher

                # Init dict
                if m.groupdict()['default_vrf']:
                    vrf = m.groupdict()['default_vrf']

                if 'vrf' not in route_dict:
                    route_dict['vrf'] = {}
                if vrf not in route_dict['vrf']:
                    route_dict['vrf'][vrf] = {}

                if 'address_family' not in route_dict['vrf'][vrf]:
                    route_dict['vrf'][vrf]['address_family'] = {}
                if new_address_family not in route_dict['vrf'][vrf]['address_family']:
                    route_dict['vrf'][vrf]['address_family'][new_address_family] = {}

                # Set keys
                route_dict['vrf'][vrf]['address_family'][new_address_family]\
                    ['bgp_table_version'] = bgp_table_version
                route_dict['vrf'][vrf]['address_family'][new_address_family]\
                    ['route_identifier'] = local_router_id
                route_dict['vrf'][vrf]['address_family'][new_address_family]\
                    ['route_distinguisher'] = route_distinguisher

                if vrf:
                    route_dict['vrf'][vrf]['address_family'][new_address_family]['default_vrf'] = \
                    vrf

                if m.groupdict()['vrf_router_id']:
                    route_dict['vrf'][vrf]['address_family'][new_address_family]['vrf_route_identifier'] = \
                        str(m.groupdict()['vrf_router_id'])


                # Reset address_family key and af_dict for use in other regex
                address_family = new_address_family
                af_dict = route_dict['vrf'][vrf]['address_family'][address_family]

                # Init routes dict
                if 'routes' not in af_dict:
                    del af_dict

                continue

        return route_dict


# ===================================
# Parser for:
#   * 'show bgp all'
#   * 'show bgp {address_family} all'
# ===================================
class ShowBgpAll(ShowBgpSuperParser, ShowBgpSchema):

    ''' Parser for:
        * 'show bgp all'
        * 'show bgp {address_family} all'
    '''

    cli_command = ['show bgp {address_family} all', 
                    'show bgp all',
                    ]
    exclude = ['bgp_table_version']

    def cli(self, address_family='', output=None):
        ret_dict = {}
        restricted_list = ['ipv4 unicast', 'ipv6 unicast']

        if output is None:
            # Build command
            if address_family:
                if address_family not in restricted_list:
                    cmd = self.cli_command[0].format(address_family=address_family)
                else:
                    return ret_dict
            else:
                cmd = self.cli_command[1]
            # Execute command
            show_output = self.device.execute(cmd)
        else:
            show_output = output

        # Call super
        return super().cli(output=show_output, address_family=address_family)



# =============================================
# Parser for:
#   * 'show bgp {address_family} rd {rd}'
#   * 'show bgp {address_family} vrf {vrf}'
#   * 'show bgp {address_family} unicast'
# =============================================
class ShowBgp(ShowBgpSuperParser, ShowBgpSchema):

    ''' Parser for:
        * 'show bgp {address_family} rd {rd}'
        * 'show bgp {address_family} vrf {vrf}'
        * 'show bgp {address_family} unicast'
    '''

    cli_command = ['show bgp {address_family} vrf {vrf}',
                   'show bgp {address_family} rd {rd}',
                   'show bgp {address_family}',
                   'show bgp {address_family} evi {evi}']

    def cli(self, address_family='', rd='', vrf='', evi='', output=None):
        cmd = None
        if output is None:
            # Build command
            if address_family and vrf:
                cmd = self.cli_command[0].format(address_family=address_family,
                                                 vrf=vrf)
            elif address_family and rd:
                cmd = self.cli_command[1].format(address_family=address_family,
                                                 rd=rd)
            elif address_family and evi:
                cmd = self.cli_command[3].format(address_family=address_family,
                                                 evi=evi)
            elif address_family and not vrf and not rd:
                cmd = self.cli_command[2].format(address_family=address_family)
                                                                                                  
            # Execute command
            show_output = self.device.execute(cmd)
        else:
            show_output = output

        # Call super
        return super().cli(output=show_output, vrf=vrf,
                           address_family=address_family)



#-------------------------------------------------------------------------------


# ======================================================
# Schema for:
#   * 'show bgp all detail'
#   * 'show ip bgp all detail'
#   * 'show bgp {address_family} vrf {vrf} detail'
#   * 'show bgp {address_family} rd {rd} detail'
#   * 'show ip bgp {address_family} vrf {vrf} detail'
#   * 'show ip bgp {address_family} rd {rd} detail'
# ======================================================
class ShowBgpAllDetailSchema(MetaParser):

    ''' Schema for:
        * 'show bgp all detail'
        * 'show ip bgp all detail'
        * 'show bgp {address_family} vrf {vrf} detail'
        * 'show bgp {address_family} rd {rd} detail'
        * 'show ip bgp {address_family} vrf {vrf} detail'
        * 'show ip bgp {address_family} rd {rd} detail'
    '''

    schema = {
        'instance':
            {'default':
                {'vrf':
                    {Any():
                        {'address_family':
                            {Any():
                                {Optional('route_distinguisher'): str,
                                Optional('default_vrf'): str,
                                Optional('prefixes'):
                                    {Any():
                                        {Optional('paths'): str,
                                        Optional('available_path'): str,
                                        Optional('best_path'): str,
                                        Optional('table_version'): str,
                                        Optional('nlri_data'):
                                            {Optional('route-type'): str,
                                             Optional('rd'): str,
                                             Optional('esi'): str,
                                             Optional('eti'): str,
                                             Optional('mac_len'): str,
                                             Optional('mac'): str,
                                             Optional('ip_len'): str,
                                             Optional('ip_prefix'): str,
                                             Optional('orig_rtr_len'): str,
                                             Optional('orig_rtr_id'): str,
                                             Optional('mcast_src_len'): str,
                                             Optional('mcast_src'): str,
                                             Optional('mcast_group_len'): str,
                                             Optional('mcast_group_addr'): str,
                                             Optional('max_resp_time'): str,
                                             Optional('subnet'): str
                                            },
                                        Optional('index'):
                                            {Any():
                                                {
                                                Optional('mpls_labels'): {
                                                    'in': str,
                                                    'out': str,
                                                },
                                                Optional('next_hop'): str,
                                                Optional('next_hop_igp_metric'): str,
                                                Optional('gateway'): str,
                                                Optional('route_info'): str,
                                                Optional('route_status'): str,
                                                Optional('imported_path_from'): str,
                                                Optional('imported_safety_path'): bool,
                                                Optional('next_hop_via'): str,
                                                Optional('update_group'): Any(),
                                                Optional('status_codes'): str,
                                                Optional('origin_codes'): str,
                                                Optional('metric'): int,
                                                Optional('inaccessible'): bool,
                                                Optional('localpref'): int,
                                                Optional('atomic_aggregate'): bool,
                                                Optional('multipath'): str,
                                                Optional('weight'): str,
                                                Optional('originator'): str,
                                                Optional('refresh_epoch'): int,
                                                Optional('recipient_pathid'): str,
                                                Optional('transfer_pathid'): str,
                                                Optional('aggregated_by_as'): str,
                                                Optional('aggregated_by_address'): str,
                                                Optional('community'): str,
                                                Optional('igmpmld'):
                                                    {Optional('version'): str,
                                                    Optional('filter_mode'): str
                                                    },
                                                Optional('ext_community'): str,
                                                Optional('recursive_via_connected'): bool,
                                                Optional('agi_version'): int,
                                                Optional('ve_block_size'): int,
                                                Optional('label_base'): int,
                                                Optional('cluster_list'): str,
                                                Optional('pmsi'):
                                                    {Optional('tun_type'): str,
                                                     Optional('vni'): str,
                                                     Optional('tun_id'):
                                                         {Optional('tun_endpoint'): str,
                                                          Optional('local'): bool,
                                                         }
                                                    },
                                                Optional('evpn'):
                                                    {Optional('ext_community'): str,
                                                    Optional('encap'): str,
                                                    Optional('evpn_esi'): str,
                                                    Optional('local_vtep'): str,
                                                    Optional('gateway_address'): str,
                                                    Optional('label'): int,
                                                    Optional('router_mac'): str,
                                                    Optional('recursive_via_connected'): bool,
                                                    },
                                                 Optional('binding_sid'): {
                                                    Optional('sid'): str,
                                                    Optional('color'): str,
                                                    Optional('state'): str,
                                                    },
                                                 Optional('local_vxlan_vtep'):
                                                    {Optional('encap'): str,
                                                    Optional('local_router_mac'): str,
                                                    Optional('vtep_ip'): str,
                                                    Optional('vrf'): str,
                                                    Optional('vni'): str,
                                                    Optional('bdi'): str,
                                                    },
                                                },
                                            },
                                        }
                                    },
                                },
                            },
                        },
                    },
                },
            },
        }


# ======================================================
# Super Parser for:
#   * 'show bgp all detail'
#   * 'show ip bgp all detail'
#   * 'show bgp {address_family} vrf {vrf} detail'
#   * 'show bgp {address_family} rd {rd} detail'
#   * 'show ip bgp {address_family} vrf {vrf} detail'
#   * 'show ip bgp {address_family} rd {rd} detail'
# ======================================================
class ShowBgpDetailSuperParser(ShowBgpAllDetailSchema):

    ''' Super Parser for:
        * 'show bgp all detail'
        * 'show ip bgp all detail'
        * 'show bgp {address_family} vrf {vrf} detail'
        * 'show bgp {address_family} rd {rd} detail'
        * 'show ip bgp {address_family} vrf {vrf} detail'
        * 'show ip bgp {address_family} rd {rd} detail'
    '''

    def cli(self, address_family='', vrf='', rd='', evi='', rt='', output=None):
        # Init dictionary
        ret_dict = {}
        subdict = ''
        next_line_update_group = False
        route_distinguisher = ''
        new_address_family = ''
        original_address_family = address_family
        refresh_epoch_flag = False
        route_info = ''
        route_status = ''
        aggregated_by_as = ''
        aggregated_by_address = ''
        imported_path_from = ''
        imported_safety_path = False
        refresh_epoch = None
        cmd_vrf = vrf if vrf else None
        default_vrf = None
        nlri_data = {}
        # For address family: IPv4 Unicast
        # For address family: L2VPN E-VPN
        p1 = re.compile(r'^For +address +family:'
                        r' +(?P<address_family>[a-zA-Z0-9\-\s]+)$')

        # Paths: (1 available, best #1, table default)
        # Paths: (1 available, best #1, table VRF1)
        # Paths: (1 available, best #1, no table)
        # Paths: (1 available, best #1, table default, RIB-failure(17))
        p2 = re.compile(r'^Paths: +\((?P<paths>(?P<available_path>[0-9]+) +available\, '
                        r'+(no +best +path|best +\#(?P<best_path>[0-9]+))\,?(?: +(table +('
                        r'?P<vrf_id>\S+?)|no +table))?,?(?: +(.*))?)\)')

        # Route Distinguisher: 100:100 (default for vrf VRF1)
        # Route Distinguisher: 65535:1 (default for vrf evpn1)
        # Route Distinguisher: 65109:3051
        # Route Distinguisher: 10.100.1.1:3014 (default for vrf vrf1)
        p2_1 = re.compile(r'^Route +Distinguisher:'
                          r' +(?P<route_distinguisher>[0-9.\:]+)'
                          r'(?: +\(default +for +vrf +(?P<vrf_id>(\S+))\))?$')

        # BGP routing table entry for 10.4.1.1/32, version 4
        # BGP routing table entry for [100:100]2001:11:11::11/128, version 2
        # BGP routing table entry for 100:100:10.229.11.11/32, version 2
        # BGP routing table entry for 2001:DB8:1:1::/64, version 5
        # BGP routing table entry for 2001:2:2:2::2/128, version 2
        # BGP routing table entry for [5][65535:1][0][24][10.36.3.0]/17, version 3
        # BGP routing table entry for 10.100.1.1:3014:0.0.0.0/0, version 74438
        p3_1 = re.compile(r'^BGP +routing +table +entry +for +(\[[0-9]+\])?'
                        r'((?P<route_distinguisher>((\[[0-9]+[\:][0-9]+\])'
                        r'|[0-9]+])|([0-9.]+[:][0-9]+[:])))?(\[[0-9]+\])?'
                        r'(\[[0-9]+\])?(?P<router_id>((\[[0-9]+[\.][0-9]+[\.]'
                        r'[0-9]+[\.][0-9]+\][\/][0-9]+)|([0-9]+[\.][0-9]+[\.]'
                        r'[0-9]+[\.][0-9]+[\/][0-9]+)|([a-zA-Z0-9]+[\:]'
                        r'[a-zA-Z0-9]+[\:][a-zA-Z0-9]+[\:][\:][a-zA-Z0-9]+'
                        r'[\/][0-9]+)|([a-zA-Z0-9]+[\:][a-zA-Z0-9]+[\:]'
                        r'[a-zA-Z0-9]+[\:][a-zA-Z0-9]+[\:][\:][\/][0-9]+)|'
                        r'([a-zA-Z0-9]+[\:][a-zA-Z0-9]+[\:][a-zA-Z0-9]+[\:]'
                        r'[a-zA-Z0-9]+[\:][\:][0-9]+[\/][0-9]+)))\, +version '
                        r'+(?P<prefix_table_version>[0-9]+)$')

        # BGP routing table entry for 65109:3051:VEID-1:Blk-1/136, version 2
        p3_2 = re.compile(r'^BGP +routing +table +entry +for'
                          r' +(?:(?P<rd>([0-9\:\[\]]+)))?:(?P<router_id>(\S+)),?'
                          r' +version +(?P<version>(\d+))$')

        # BGP routing table entry for [route_type][rd][...][...][...], version 48
        p3_3 = re.compile(r'^BGP +routing +table +entry +for'
                          r' +(?P<router_id>(\[[0-9]\]\[[0-9\.]+[\:][0-9]+\](\[.+\])+[\/][0-9]+))\, +version '
                          r'+(?P<prefix_table_version>[0-9]+)$')

        # 10.1.1.2 from 10.1.1.2 (10.1.1.2)
        # 10.16.2.2 (metric 11) (via default) from 10.16.2.2 (10.16.2.2)
        # :: (via vrf VRF1) from 0.0.0.0 (10.1.1.1)
        # 192.168.0.1 (inaccessible) from 192.168.0.9 (192.168.0.9)
        # 172.17.111.1 (via vrf SH_BGP_VRF100) from 172.17.111.1 (10.5.5.5)
        p4 = re.compile(r'^((?P<next_hop>[a-zA-Z0-9\.\:]+)'
                        r'(( +\(metric +(?P<next_hop_igp_metric>[0-9]+)\))|'
                        r'( +\((?P<inaccessible>inaccessible)\)))?'
                        r'( +\(via +(?P<next_hop_via>[\S\s]+)\))? +'
                        r'from +(?P<gateway>[a-zA-Z0-9\.\:]+)'
                        r' +\((?P<originator>[0-9\.]+)\))$')

        # Origin incomplete, metric 0, localpref 100, valid, internal
        # Origin incomplete, metric 0, localpref 100, valid, internal, best
        # Origin incomplete, metric 0, localpref 100, weight 32768, valid, sourced, best
        # Origin IGP, localpref 100, valid, external, atomic-aggregate
        # Origin IGP, localpref 100, valid, external, atomic-aggregate, best
        # Origin IGP, localpref 100, valid, external, multipath
        # Origin IGP, localpref 100, valid, external, multipath, best
        # Origin IGP, localpref 100, valid, external, multipath(oldest)
        p5 = re.compile(r'^Origin +(?P<origin>[a-zA-Z]+),(?: +metric '
                        r'+(?P<metric>[0-9]+),?)?(?: +localpref '
                        r'+(?P<locprf>[0-9]+),?)?(?: +weight '
                        r'+(?P<weight>[0-9]+),?)?(?: +(?P<valid>valid?,))?(?: '
                        r'+(?P<sourced>sourced?,))?(?: +(?P<state>(internal|'
                        r'external|local)\,?))?(?: '
                        r'+(?P<aggregate>atomic-aggregate?))?(\,)?(?: '
                        r'+(?P<multipath>multipath(?:\(\w+\))?))?(\,)?(?: '
                        r'+(?P<best>best))?$')

        # Advertised to update-groups:
        p6_1 = re.compile(r'^Advertised +to +update-groups *:$')

        # Not advertised to any peer
        p6_2 = re.compile(r'^Not +advertised +to +any +peer$')

        # 3
        # 38         44         45
        p6_3 = re.compile(r'(?P<group1>(\d+))'
                          r'(?: +(?P<group2>(\d+)))?(?: +(?P<group3>(\d+)))?')

        # Refresh Epoch 1
        p7 = re.compile(r'^Refresh +Epoch +(?P<refresh_epoch>[0-9]+)$')

        # Extended Community: RT:65535:1 ENCAP:8 Router MAC:001E.7AFF.FCD2
        p8 = re.compile(r'^Extended +Community\:'
                        r' +(?P<ext_community>([a-zA-Z0-9\-\:]+)) +ENCAP *:'
                        r'(?P<encap>(\d+)) +Router +(?P<router_mac>(\S+))$')

        # Extended Community: SoO:65109:999 RT:65109:50
        # Extended Community: RT:0:3051 RT:65109:3051 L2VPN L2:0x0:MTU-1500
        # Extended Community: RT:65109:50 RT:65109:51 , recursive-via-connected
        # Extended Community: RT:1:1 RT:100:101 MVPN AS:100:0.0.0.0
        p8_2 = re.compile(r'^Extended +Community *:'
                          r' +(?P<ext_community>([a-zA-Z0-9\-\:\s\.]+))'
                          r'(?: *, +(?P<recursive>(recursive-via-connected)))?$')

        p8_21 = re.compile(r'^(RT|Color|0x88|So0|Cost:pre-bestpath).*$')

        # Community: 62000:1
        # Community: 1:1 65100:101 65100:175 65100:500 65100:601 65151:65000 65351:1
        p8_3 = re.compile(r'^Community: +(?P<community>[\S+\s]+)$')

        # AGI version(0), VE Block Size(10) Label Base(16)
        p8_4 = re.compile(r'^AGI +version\((?P<agi_version>(\d+))\),'
                          r' +VE +Block +Size\((?P<ve_block_size>(\d+))\)'
                          r' +Label +Base\((?P<label_base>(\d+))\)$')

        # Originator: 192.168.165.220, Cluster list: 0.0.0.61
        p8_5 = re.compile(r'^\s*Originator: +(?P<originator>(\S+)),'
                          r' +Cluster +list: +(?P<cluster_list>(\S+))$')
        
        p8_6 = re.compile(r'^\s*PMSI Attribute: Flags.*'
                          r'Tunnel type:(?P<tun_type>.+),'
                          r' length.+vni:(?P<vni>.+)'
                          r' tunnel identifier: ((< Tunnel Endpoint: (?P<tun_endpoint>.+) >)|(?P<local>0000 0000))$')

        # rx pathid: 0, tx pathid: 0
        p9 = re.compile(r'^rx +pathid\: +(?P<recipient_pathid>[0-9x]+)\,'
                        r' +tx +pathid\:'
                        r' +(?P<transfer_pathid>[0-9x]+)$')

        # EVPN ESI: 00000000000000000000, Gateway Address: 0.0.0.0, local vtep: 10.21.33.33, Label 30000
        # EVPN ESI: 00000000000000000000, Label1 2000101
        p10 = re.compile(r'^EVPN +ESI\: +(?P<evpn_esi>[0-9]+)\,\s+'
                         r'(Gateway +Address\:\s+(?P<gateway_address>[a-zA-Z0-9\.\:]+)\,\s+)?'
                         r'(local vtep\: +(?P<local_vtep>[a-zA-Z0-9\.\:]+)\,\s+)?'
                         r'[L|l]abel\d* +(?P<label>[0-9]+)$')

        # Local vxlan vtep:
        # Local irb vxlan vtep
        p11 = re.compile(r'^Local\s+(irb\s+)?vxlan\s+vtep\:$')

        # bdi:BDI200
        # core-bdi:BDI200
        p12 = re.compile(r'^(core-)?bdi\:(?P<bdi>[A-Z0-9]+)$')

        # vrf:evpn1, vni:30000
        # vrf:evpn1, l3-vni:30000
        p13 = re.compile(r'^vrf\:(?P<vrf>[a-zA-Z0-9]+)\,'
                         r'\s+(.+-)?vni\:(?P<vni>[0-9]+)$')

        # local router mac:001E.7AFF.FCD2
        p14 = re.compile(r'^local +router +mac\:'
                         r'(?P<local_router_mac>[a-zA-Z0-9\.]+)$')

        # encap:8
        p15 = re.compile(r'^encap\:(?P<encap>[0-9]+)$')

        # vtep-ip:10.21.33.33
        p16 = re.compile(r'^vtep-ip\:(?P<vtep_ip>[a-zA-Z0-9\.\:]+)$')

        # Local
        # 65530
        # Local, imported path from base
        # 200 33299 51178 47751 {27016}
        # 200 33299 51178 47751 {27016}, imported path from 200:2:10.1.1.0/24 (global)
        # 400 33299 51178 47751 {27016}, imported path from [400:1]2001:db8:a69:5a4::/64 (VRF2)
        # 62000, (Received from a RR-client)
        # 2, imported safety path from 50000:2:172.17.0.0/16
        # 4210105002 4210105502 4210105001 4210105507 4210105007 4210105220 65000 65151 65501, (aggregated by 65251 10.160.0.61), (received & used)
        # 4210105002 4210105502 4210105001 4210105507 4210105007 4210105220 65000 65151 65501, (aggregated by 65251 2001:db8:4::1), (received & used)
        # 4210105002 4210105502 4210105001 4210105507 4210105007 4210105220 65000 65151 65501, (aggregated by 65251 FE80:CD00:0:CDE:1257:0:211E:729C), (received & used)
        p17 = re.compile(r'^(?P<route_info>[a-zA-Z0-9\-\.\{\}\s\(\)\/\:\[\]]+)'
                       r'(\,)?(?: +\(aggregated +by +(?P<aggregated_by>[\w\s\.\:]'
                       r'+)\)(\,))?(?: +(?P<route_status>[A-Za-z0-9\.\:\/\(\)\s'
                       r'\[\]\-\&]+))?$')
        
        # mpls labels in/out nolabel/64402
        p18 = re.compile(r'^mpls +labels +in\/out +(?P<in>\w+)\/(?P<out>\w+)$')

        # IGMP/MLD v1/v2/v3, exclude, max response time:
        p19 = re.compile(r'^IGMP/MLD\s+(?P<version>v\d|v\d,\s*v\d)(,\s+(?P<filter_mode>\w+))?$')

        # binding SID: 28 (color - 7) (state - UP)
        p20 = re.compile(r'^binding +SID\:' r' +(?P<sid>([a-zA-Z0-9]+))'
                 r'( +\(color[ ]{0,1}[-][ ]{0,1}(?P<color>[0-9]+)\))'
                 r'(( +\(state +\- +(?P<state>[A-Za-z]+)\)))?$')

        for line in output.splitlines():
            line = line.strip()
            # For address family: IPv4 Unicast
            # For address family: L2VPN E-VPN
            m = p1.match(line)
            if m:
                index = 0
                address_family = m.groupdict()['address_family'].lower()
                original_address_family = address_family
                if 'instance' not in ret_dict:
                    ret_dict['instance'] = {}
                if 'default' not in ret_dict['instance']:
                    ret_dict['instance']['default'] = {}
                if 'vrf' not in ret_dict['instance']['default']:
                    ret_dict['instance']['default']['vrf'] = {}
                continue

            # Paths: (1 available, best #1, table default)
            # Paths: (1 available, best #1, table VRF1)
            # Paths: (1 available, best #1, no table)
            # Paths: (1 available, best #1, table default, RIB-failure(17))
            m = p2.match(line)
            if m:
                group = m.groupdict()
                original_address_family = address_family.lower()

                if 'instance' not in ret_dict:
                    ret_dict['instance'] = {}
                if 'default' not in ret_dict['instance']:
                    ret_dict['instance']['default'] = {}
                if 'vrf' not in ret_dict['instance']['default']:
                    ret_dict['instance']['default']['vrf'] = {}

                paths = group['paths']
                available_path = group['available_path']

                if group['best_path']:
                    best_path = group['best_path']
                else:
                    best_path = ''

                if group['vrf_id']:
                    vrf = group['vrf_id']
                elif cmd_vrf:
                    vrf = cmd_vrf
                elif default_vrf and default_vrf != 'None':
                    vrf = default_vrf
                else:
                    vrf = 'default'

                vrf_dict = ret_dict.setdefault('instance', {}).setdefault('default', {}).\
                                        setdefault('vrf', {}).setdefault(vrf, {})

                address_family_dict = vrf_dict.setdefault('address_family', {})

                # Adding the new_address_family that contains the RD info
                if new_address_family:
                    if new_address_family not in address_family_dict:
                        new_addr_family_dict = address_family_dict.setdefault(new_address_family, {})
                    if 'prefixes' not in new_addr_family_dict:
                        new_addr_family_dict['prefixes'] = {}
                    if prefixes not in new_addr_family_dict['prefixes']:
                        new_addr_family_dict['prefixes'][prefixes] = {}

                    # Adding the keys we got from 'BGP routing table' line
                    new_addr_family_dict['prefixes'][prefixes]['table_version'] = prefix_table_version
                    if nlri_data:
                        new_addr_family_dict['prefixes'][prefixes]['nlri_data'] = nlri_data

                    # Adding the keys we got from 'Route Distinguisher' line
                    if route_distinguisher:
                        new_addr_family_dict['route_distinguisher'] = route_distinguisher
                        if default_vrf:
                            new_addr_family_dict['default_vrf'] = default_vrf

                    new_addr_family_dict['prefixes'][prefixes]['available_path'] = available_path
                    new_addr_family_dict['prefixes'][prefixes]['best_path'] = best_path
                    new_addr_family_dict['prefixes'][prefixes]['paths'] = paths
                else:
                    if address_family not in address_family_dict:
                        address_family_dict[address_family] = {}
                    if 'prefixes' not in address_family_dict[address_family]:
                        address_family_dict[address_family]['prefixes'] = {}
                    if prefixes not in address_family_dict[address_family]['prefixes']:
                        address_family_dict[address_family]['prefixes'][prefixes] = {}

                    # Adding the keys we got from 'BGP routing table' line
                    address_family_dict[address_family]['prefixes']\
                        [prefixes]['table_version'] = prefix_table_version

                    if nlri_data:
                        address_family_dict[address_family]['prefixes']\
                            [prefixes]['nlri_data'] = nlri_data
                    # Adding the keys we got from 'Route Distinguisher' line
                    if route_distinguisher:
                        address_family_dict[address_family]['route_distinguisher'] = route_distinguisher
                        if default_vrf:
                            address_family_dict[address_family]['default_vrf'] = default_vrf

                    address_family_dict[address_family]['prefixes']\
                        [prefixes]['available_path'] = available_path
                    address_family_dict[address_family]['prefixes'][prefixes]['best_path'] = best_path
                    address_family_dict[address_family]['prefixes'][prefixes]['paths'] = paths

            # Route Distinguisher: 100:100 (default for vrf VRF1)
            # Route Distinguisher: 65535:1 (default for vrf evpn1)
            # Route Distinguisher: 10.100.1.1:3014 (default for vrf vrf1)
            m = p2_1.match(line)
            if m:
                route_distinguisher = m.groupdict()['route_distinguisher']
                default_vrf = m.groupdict()['vrf_id']

                if address_family == 'vpnv4 unicast' or address_family == 'vpnv6 unicast':
                    new_address_family = original_address_family + ' RD ' + route_distinguisher

                # Init dict
                if 'instance' not in ret_dict:
                    ret_dict['instance'] = {}
                if 'default' not in ret_dict['instance']:
                    ret_dict['instance']['default'] = {}
                if 'vrf' not in ret_dict['instance']['default']:
                    ret_dict['instance']['default']['vrf'] = {}
                continue

            # BGP routing table entry for 10.4.1.1/32, version 4
            # BGP routing table entry for [100:100]2001:11:11::11/128, version 2
            # BGP routing table entry for 100:100:10.229.11.11/32, version 2
            # BGP routing table entry for 2001:DB8:1:1::/64, version 5
            # BGP routing table entry for 2001:2:2:2::2/128, version 2
            # BGP routing table entry for [5][65535:1][0][24][10.36.3.0]/17, version 3
            # BGP routing table entry for 10.100.1.1:3014:0.0.0.0/0, version 74438
            m = p3_1.match(line)
            if m:
                update_group = 0
                index = 0
                prefixes = m.groupdict()['router_id']
                prefixes = prefixes.replace('[', '')
                prefixes = prefixes.replace(']', '')
                prefix_table_version = m.groupdict()['prefix_table_version']
                continue

            # BGP routing table entry for 65109:3051:VEID-1:Blk-1/136, version 2
            m = p3_2.match(line)
            if m:
                update_group = 0
                index = 0
                prefixes = m.groupdict()['router_id']
                prefixes = prefixes.replace('[', '')
                prefixes = prefixes.replace(']', '')
                prefix_table_version = m.groupdict()['version']
                continue
            
            # For all EVPN route-types 1-8
            # BGP routing table entry for [1][2.2.2.2:1000][AAAABBBBCCCCDDDDEEEE][10000]/23, version 26
            # BGP routing table entry for [2][120:120][0][40][AABBCCDDEF00][0][*]/20, version 35
            # BGP routing table entry for [2][2.2.2.2:1000][10000][48][022651BDC81C][32][0.0.0.0]/24, version 28
            # BGP routing table entry for [2][22.2.2.2:1000][10000][48][022651BDC81C][128][1000::1]/36, version 36
            # BGP routing table entry for [3][40.0.0.3:164][0][32][40.0.0.3]/17, version 30
            # BGP routing table entry for [4][2.2.2.2:1000][AAAABBBBCCCCDDDDEEEE][32]/23, version 32
            # BGP routing table entry for [5][100:100][4231][32][1.1.1.1]/17, version 37
            # BGP routing table entry for [5][20.0.0.1:31000][0][32][250.250.250.22]/17, version 34
            # BGP routing table entry for [6][7.7.7.7:11][0][32][10.10.10.10][32][19.0.101.1][32][224.0.0.1]/27, version 27
            # BGP routing table entry for [6][117901063:11][0][128][A0A:A0A:A0A:A0A:A0A:A0A:A0A:A0A][128][1300:6501:1300:6501:1300:6501:1300:6501][128][E000:1:E000:1:E000:1:E000:1]/63, version 33
            # BGP routing table entry for [7][7.7.7.7:11][0000000000AABBCCDDEE][0][32][10.10.10.10][32][19.0.101.1][32][224.0.0.1]/37, version 29
            # BGP routing table entry for [8][7.7.7.7:11][0000000000AABBCCDDEE][0][32][10.10.10.10][32][19.0.101.1][32][224.0.0.1][4112]/41, version 31
            m = p3_3.match(line)
            if m:
                nlri_data = {}
                update_group = 0
                index = 0
                prefixes = m.groupdict()['router_id']
                if prefixes.startswith('[6]'):
                    # BGP routing table entry for [6][7.7.7.7:11][0][32][10.10.10.10][32][19.0.101.1][32][224.0.0.1]/27, version 27
                    # BGP routing table entry for [6][117901063:11][0][128][A0A:A0A:A0A:A0A:A0A:A0A:A0A:A0A][128][1300:6501:1300:6501:1300:6501:1300:6501][128][E000:1:E000:1:E000:1:E000:1]/63, version 33
                    rt6_prefix_re = re.compile(r'\[(?P<rt>[0-9])\]'
                                                r'\[(?P<rd>[0-9\.]+[\:][0-9]+)\]'
                                                r'\[(?P<eti>[0-9]+)\]'
                                                r'\[(?P<mcast_src_len>[0-9]+)\]'
                                                r'(\[(?P<mcast_src>.+)\])?'
                                                r'\[(?P<mcast_group_len>[0-9]+)\]'
                                                r'\[(?P<mcast_group_addr>.+)\]'
                                                r'\[(?P<orig_rtr_len>[0-9]+)\]'
                                                r'\[(?P<orig_rtr_id>.+)\]'
                                                r'\/(?P<subnet>[0-9]+)')
                    rt6_mo = rt6_prefix_re.match(prefixes)
                    if rt6_mo:
                        rt6_dict = rt6_mo.groupdict()
                        nlri_data['route-type'] = '6'
                        nlri_data['rd'] = rt6_dict['rd']
                        nlri_data['eti'] = rt6_dict['eti']
                        nlri_data['mcast_src_len'] = rt6_dict['mcast_src_len']
                        nlri_data['mcast_src'] = rt6_dict['mcast_src']
                        nlri_data['mcast_group_len'] = rt6_dict['mcast_group_len']
                        nlri_data['mcast_group_addr'] = rt6_dict['mcast_group_addr']
                        nlri_data['orig_rtr_len'] = rt6_dict['orig_rtr_len']
                        nlri_data['orig_rtr_id'] = rt6_dict['orig_rtr_id']
                        nlri_data['subnet'] = rt6_dict['subnet']

                elif prefixes.startswith('[3]'):
                    # BGP routing table entry for [3][40.0.0.3:164][0][32][40.0.0.3]/17, version 30
                    rt3_prefix_re = re.compile(r'\[(?P<rt>[0-9])\]'
                                                r'\[(?P<rd>[0-9\.]+[\:][0-9]+)\]'
                                                r'\[(?P<eti>[0-9]+)\]'
                                                r'\[(?P<ip_len>[0-9]+)\]'
                                                r'(\[(?P<orig_rtr_id>.+)\])?'
                                                r'\/(?P<subnet>[0-9]+)')
                    rt3_mo = rt3_prefix_re.match(prefixes)
                    if rt3_mo:
                        rt3_dict = rt3_mo.groupdict()
                        nlri_data['route-type'] = '3'
                        nlri_data['rd'] = rt3_dict['rd']
                        nlri_data['eti'] = rt3_dict['eti']
                        nlri_data['ip_len'] = rt3_dict['ip_len']
                        if rt3_dict['orig_rtr_id']:
                            nlri_data['orig_rtr_id'] = rt3_dict['orig_rtr_id']
                        nlri_data['subnet'] = rt3_dict['subnet']
                        
                elif prefixes.startswith('[1]'):
                    # BGP routing table entry for [1][2.2.2.2:1000][AAAABBBBCCCCDDDDEEEE][10000]/23, version 26
                    rt1_prefix_re = re.compile(r'\[(?P<rt>[0-9])\]'
                                                r'\[(?P<rd>[0-9\.]+[\:][0-9]+)\]'
                                                r'\[(?P<esi>.+)\]'
                                                r'\[(?P<eti>[0-9]+)\]'
                                                r'\/(?P<subnet>[0-9]+)')
                    rt1_mo = rt1_prefix_re.match(prefixes)
                    if rt1_mo:
                        rt1_dict = rt1_mo.groupdict()
                        nlri_data['route-type'] = '1'
                        nlri_data['rd'] = rt1_dict['rd']
                        nlri_data['esi'] = rt1_dict['esi']
                        nlri_data['eti'] = rt1_dict['eti']
                        nlri_data['subnet'] = rt1_dict['subnet']

                elif prefixes.startswith('[2]'):
                    # BGP routing table entry for [2][2.2.2.2:1000][10000][48][022651BDC81C][32][0.0.0.0]/24, version 28
                    # BGP routing table entry for [2][22.2.2.2:1000][10000][48][022651BDC81C][128][1000::1]/36, version 36
                    rt2_prefix_re = re.compile(r'\[(?P<rt>[0-9])\]'
                                                r'\[(?P<rd>[0-9\.]+[\:][0-9]+)\]'
                                                r'\[(?P<eti>[0-9]+)\]'
                                                r'\[(?P<mac_len>[0-9]+)\]'
                                                r'\[(?P<mac>.+)\]'
                                                r'\[(?P<ip_len>[0-9]+)\]'
                                                r'(\[(?P<ip_prefix>.+)\])?'
                                                r'\/(?P<subnet>[0-9]+)')
                    
                    rt2_mo = rt2_prefix_re.match(prefixes)
                    if rt2_mo:
                        rt2_dict = rt2_mo.groupdict()
                        nlri_data['route-type'] = '2'
                        nlri_data['rd'] = rt2_dict['rd']
                        nlri_data['eti'] = rt2_dict['eti']
                        nlri_data['mac_len'] = rt2_dict['mac_len']
                        nlri_data['mac'] = rt2_dict['mac']
                        nlri_data['ip_len'] = rt2_dict['ip_len']
                        if int(rt2_dict['ip_len']) > 0:
                            if rt2_dict['ip_prefix']:
                                nlri_data['ip_prefix'] = rt2_dict['ip_prefix']
                        nlri_data['subnet'] = rt2_dict['subnet']

                elif prefixes.startswith('[4]'):
                    # BGP routing table entry for [4][2.2.2.2:1000][AAAABBBBCCCCDDDDEEEE][32]/23, version 32
                    rt4_prefix_re = re.compile(r'\[(?P<rt>[0-9])\]'
                                                r'\[(?P<rd>[0-9\.]+[\:][0-9]+)\]'
                                                r'\[(?P<esi>.+)\]'
                                                r'\[(?P<ip_len>[0-9]+)\]'
                                                r'(\[(?P<orig_rtr_id>.+)\])?'
                                                r'\/(?P<subnet>[0-9]+)')
                    
                    rt4_mo = rt4_prefix_re.match(prefixes)
                    if rt4_mo:
                        rt4_dict = rt4_mo.groupdict()
                        nlri_data['route-type'] = '4'
                        nlri_data['rd'] = rt4_dict['rd']
                        nlri_data['esi'] = rt4_dict['esi']
                        nlri_data['ip_len'] = rt4_dict['ip_len']
                        if rt4_dict['orig_rtr_id']:
                            nlri_data['orig_rtr_id'] = rt4_dict['orig_rtr_id']
                        nlri_data['subnet'] = rt4_dict['subnet']

                elif prefixes.startswith('[5]'):
                    # BGP routing table entry for [5][100:100][4231][32][1.1.1.1]/17, version 37
                    # BGP routing table entry for [5][20.0.0.1:31000][0][32][250.250.250.22]/17, version 34
                    rt5_prefix_re = re.compile(r'\[(?P<rt>[0-9])\]'
                                                r'\[(?P<rd>[0-9\.]+[\:][0-9]+)\]'
                                                r'\[(?P<eti>[0-9]+)\]'
                                                r'\[(?P<ip_len>[0-9]+)\]'
                                                r'(\[(?P<ip_prefix>.+)\])?'
                                                r'\/(?P<subnet>[0-9]+)')
                    
                    rt5_mo = rt5_prefix_re.match(prefixes)
                    if rt5_mo:
                        rt5_dict = rt5_mo.groupdict()
                        nlri_data['route-type'] = '5'
                        nlri_data['rd'] = rt5_dict['rd']
                        nlri_data['eti'] = rt5_dict['eti']
                        nlri_data['ip_len'] = rt5_dict['ip_len']
                        if int(rt5_dict['ip_len']) > 0:
                            if rt5_dict['ip_prefix']:
                                nlri_data['ip_prefix'] = rt5_dict['ip_prefix']
                        nlri_data['subnet'] = rt5_dict['subnet']

                elif prefixes.startswith('[7]'):
                    # BGP routing table entry for [7][7.7.7.7:11][0000000000AABBCCDDEE][0][32][10.10.10.10][32][19.0.101.1][32][224.0.0.1]/37, version 29
                    rt7_prefix_re = re.compile(r'\[(?P<rt>[0-9])\]'
                                                r'\[(?P<rd>[0-9\.]+[\:][0-9]+)\]'
                                                r'\[(?P<esi>.+)\]'
                                                r'\[(?P<eti>[0-9]+)\]'
                                                r'\[(?P<mcast_src_len>[0-9]+)\]'
                                                r'(\[(?P<mcast_src>.+)\])?'
                                                r'\[(?P<mcast_group_len>[0-9]+)\]'
                                                r'\[(?P<mcast_group_addr>.+)\]'
                                                r'\[(?P<orig_rtr_len>[0-9]+)\]'
                                                r'\[(?P<orig_rtr_id>.+)\]'
                                                r'\/(?P<subnet>[0-9]+)')

                    rt7_mo = rt7_prefix_re.match(prefixes)
                    if rt7_mo:
                        rt7_dict = rt7_mo.groupdict()
                        nlri_data['route-type'] = '7'
                        nlri_data['rd'] = rt7_dict['rd']
                        nlri_data['esi'] = rt7_dict['esi']
                        nlri_data['eti'] = rt7_dict['eti']
                        nlri_data['mcast_src_len'] = rt7_dict['mcast_src_len']
                        if int(rt7_dict['mcast_src_len']) > 0:
                            if rt7_dict['mcast_src']:
                                nlri_data['mcast_src'] = rt7_dict['mcast_src']
                        nlri_data['mcast_group_len'] = rt7_dict['mcast_group_len']
                        nlri_data['mcast_group_addr'] = rt7_dict['mcast_group_addr']
                        nlri_data['orig_rtr_len'] = rt7_dict['orig_rtr_len']
                        nlri_data['orig_rtr_id'] = rt7_dict['orig_rtr_id']
                        nlri_data['subnet'] = rt7_dict['subnet']

                elif prefixes.startswith('[8]'):
                    # BGP routing table entry for [8][7.7.7.7:11][0000000000AABBCCDDEE][0][32][10.10.10.10][32][19.0.101.1][32][224.0.0.1][4112]/41, version 31
                    rt8_prefix_re = re.compile(r'\[(?P<rt>[0-9])\]'
                                                r'\[(?P<rd>[0-9\.]+[\:][0-9]+)\]'
                                                r'\[(?P<esi>.+)\]'
                                                r'\[(?P<eti>[0-9]+)\]'
                                                r'\[(?P<mcast_src_len>[0-9]+)\]'
                                                r'(\[(?P<mcast_src>.+)\])?'
                                                r'\[(?P<mcast_group_len>[0-9]+)\]'
                                                r'\[(?P<mcast_group_addr>.+)\]'
                                                r'\[(?P<orig_rtr_len>[0-9]+)\]'
                                                r'\[(?P<orig_rtr_id>.+)\]'
                                                r'\[(?P<max_resp_time>[0-9]+)\]'
                                                r'\/(?P<subnet>[0-9]+)')

                    rt8_mo = rt8_prefix_re.match(prefixes)
                    if rt8_mo:
                        rt8_dict = rt8_mo.groupdict()
                        nlri_data['route-type'] = '8'
                        nlri_data['rd'] = rt8_dict['rd']
                        nlri_data['esi'] = rt8_dict['esi']
                        nlri_data['eti'] = rt8_dict['eti']
                        nlri_data['mcast_src_len'] = rt8_dict['mcast_src_len']
                        if int(rt8_dict['mcast_src_len']) > 0:
                            if rt8_dict['mcast_src']:
                                nlri_data['mcast_src'] = rt8_dict['mcast_src']
                        nlri_data['mcast_group_len'] = rt8_dict['mcast_group_len']
                        nlri_data['mcast_group_addr'] = rt8_dict['mcast_group_addr']
                        nlri_data['orig_rtr_len'] = rt8_dict['orig_rtr_len']
                        nlri_data['orig_rtr_id'] = rt8_dict['orig_rtr_id']
                        nlri_data['max_resp_time'] = rt8_dict['max_resp_time']
                        nlri_data['subnet'] = rt8_dict['subnet']


                prefix_table_version = m.groupdict()['prefix_table_version']
                continue
            
            # 10.1.1.2 from 10.1.1.2 (10.1.1.2)
            # 10.16.2.2 (metric 11) (via default) from 10.16.2.2 (10.16.2.2)
            # :: (via vrf VRF1) from 0.0.0.0 (10.1.1.1)
            # 192.168.0.1 (inaccessible) from 192.168.0.9 (192.168.0.9)
            # 172.17.111.1 (via vrf SH_BGP_VRF100) from 172.17.111.1 (10.5.5.5)
            m = p4.match(line)
            if m:
                index += 1
                group = m.groupdict()

                if new_address_family:
                    if 'index' not in new_addr_family_dict['prefixes'][prefixes]:
                        new_addr_family_dict['prefixes'][prefixes]['index'] = {}
                    if index not in new_addr_family_dict['prefixes'][prefixes]['index']:
                        new_addr_family_dict['prefixes'][prefixes]['index'][index] = {}
                        subdict = new_addr_family_dict['prefixes'][prefixes]['index'][index]

                    for i in ['next_hop', 'gateway', 'originator']:
                        subdict[i] = group[i]

                    if group['next_hop_igp_metric']:
                        subdict['next_hop_igp_metric'] = group['next_hop_igp_metric']

                    if group['inaccessible']:
                        subdict['inaccessible'] = True
                    else:
                        subdict['inaccessible'] = False

                    if group['next_hop_via']:
                        subdict['next_hop_via'] = group['next_hop_via']

                    # Adding update_group to each index
                    if update_group:
                        subdict['update_group'] = update_group
                else:
                    if 'index' not in address_family_dict[address_family]['prefixes'][prefixes]:
                        address_family_dict[address_family]['prefixes'][prefixes]['index'] = {}
                    if index not in address_family_dict[address_family]['prefixes'][prefixes]['index']:
                        address_family_dict[address_family]['prefixes'][prefixes]['index'][index] = {}
                        subdict = address_family_dict[address_family]['prefixes'][prefixes]['index'][index]

                    for i in ['next_hop', 'gateway', 'originator']:
                        subdict[i] = group[i]

                    if group['next_hop_igp_metric']:
                        subdict['next_hop_igp_metric'] = group['next_hop_igp_metric']

                    if group['next_hop_via']:
                        subdict['next_hop_via'] = group['next_hop_via']

                    # Adding update_group to each index
                    if update_group:
                        subdict['update_group'] = update_group
                continue

            # Origin incomplete, metric 0, localpref 100, valid, internal
            # Origin incomplete, metric 0, localpref 100, valid, internal, best
            # Origin incomplete, metric 0, localpref 100, weight 32768, valid, sourced, best
            # Origin IGP, localpref 100, valid, external, atomic-aggregate
            # Origin IGP, localpref 100, valid, external, atomic-aggregate, best
            # Origin IGP, localpref 100, valid, external, multipath
            # Origin IGP, localpref 100, valid, external, multipath, best
            # Origin IGP, localpref 100, valid, external, multipath(oldest)
            m = p5.match(line)
            if m:
                group = m.groupdict()
                status_codes = ''

                if group['aggregate']:
                    subdict['atomic_aggregate'] = True
                if group['multipath']:
                    subdict['multipath'] = group['multipath']
                if group['locprf']:
                     subdict['localpref'] = int(group['locprf'])
                if group['metric']:
                     subdict['metric'] = int(group['metric'])
                if group['weight']:
                    subdict['weight'] = group['weight']

                if group['origin']:
                    origin = str(group['origin'])
                    if origin == 'incomplete':
                        subdict['origin_codes'] = '?'
                    elif origin == 'EGP':
                        subdict['origin_codes'] = 'e'
                    else:
                        subdict['origin_codes'] = 'i'

                if group['valid']:
                    status_codes += '* '
                if group['best']:
                    status_codes = status_codes.rstrip()
                    status_codes += '>'
                if group['state']:
                    state = group['state']
                    if state == 'internal':
                        status_codes += 'i'

                subdict['status_codes'] = status_codes

                # Adding the keys we got from 'Refresh Epoch' line
                if refresh_epoch:
                    subdict['refresh_epoch'] = refresh_epoch

                # Adding the keys we got from 'route_info' line
                if route_info:
                    subdict['route_info'] = route_info
                   
                # Adding the keys we got from 'route_status' line                   
                if route_status:
                    subdict['route_status'] = route_status
                    
                # Adding the keys we got from 'imported_path_from' line                   
                if imported_path_from:
                    subdict['imported_path_from'] = imported_path_from

                # Adding the keys we got from 'imported_safety_path' line                   
                if imported_safety_path:
                    subdict['imported_safety_path'] = imported_safety_path

                # Add key to dictionary
                if aggregated_by_as:
                    subdict['aggregated_by_as'] = aggregated_by_as

                if aggregated_by_address:
                    subdict['aggregated_by_address'] = aggregated_by_address

                continue

            # Advertised to update-groups:
            m = p6_1.match(line)
            if m:
                next_line_update_group = True
                continue

            # Not advertised to any peer
            m = p6_2.match(line)
            if m:
                next_line_update_group = False
                continue

            # 3
            # # 38         44         45
            m = p6_3.match(line)
            if m and next_line_update_group:
                group = m.groupdict()
                if group['group2'] or group['group3']:
                    update_group = []
                    for item in group:
                        if group[item]:
                            update_group.append(int(group[item]))
                            # in-place sort is more efficient
                            update_group.sort()
                else:
                    update_group = int(group['group1'])
                next_line_update_group = False
                continue

            # Refresh Epoch 1
            m = p7.match(line)
            if m:
                refresh_epoch_flag = True
                refresh_epoch = int(m.groupdict()['refresh_epoch'])
                continue

            # Extended Community: RT:65535:1 ENCAP:8 Router MAC:001E.7AFF.FCD2
            m = p8.match(line)
            if m:
                group = m.groupdict()

                if 'evpn' not in subdict:
                    subdict['evpn'] = {}

                ext_community = group['ext_community']
                subdict['evpn']['ext_community'] = ext_community

                if group['encap']:
                    subdict['evpn']['encap'] = group['encap']
                if group['router_mac']:
                    subdict['evpn']['router_mac'] = group['router_mac']
                continue

            # Extended Community: SoO:65109:999 RT:65109:50
            # Extended Community: RT:0:3051 RT:65109:3051 L2VPN L2:0x0:MTU-1500
            # Extended Community: RT:65109:50 RT:65109:51 , recursive-via-connected
            m = p8_2.match(line)
            if m:
                group = m.groupdict()
                ext_community = group['ext_community']

                if 'evpn' in subdict:
                    subdict['evpn']['ext_community'] = ext_community
                    if group['recursive']:
                        subdict['evpn']['recursive_via_connected'] = True
                else:
                    subdict['ext_community'] = ext_community
                    if group['recursive']:
                        subdict['recursive_via_connected'] = True
                continue

            m = p8_21.match(line)
            if m:
                group = m.group()
                if 'evpn' in subdict:
                    subdict['evpn']['ext_community'] = f"{subdict['evpn']['ext_community']} {group}"
                else:
                    subdict['ext_community'] = f"{subdict['ext_community']} {group}"
                continue

            # Community: 62000:1
            # Community: 1:1 65100:101 65100:175 65100:500 65100:601 65151:65000 65351:1
            m = p8_3.match(line)
            if m:
                subdict['community'] = m.groupdict()['community']
                continue

            # AGI version(0), VE Block Size(10) Label Base(16)
            m = p8_4.match(line)
            if m:
                group = m.groupdict()

                for i in ['agi_version', 've_block_size', 'label_base']:
                    subdict[i] = int(group[i])

                continue

            # Originator: 192.168.165.220, Cluster list: 0.0.0.61
            m = p8_5.match(line)
            if m:
                subdict['cluster_list'] = m.groupdict()['cluster_list']
                continue

            m = p8_6.match(line)
            if m:
                subdict['pmsi'] = {}
                subdict['pmsi']['tun_type'] = m.groupdict()['tun_type']
                subdict['pmsi']['vni'] = m.groupdict()['vni']
                subdict['pmsi']['tun_id'] = {}
                if m.groupdict()['tun_endpoint'] is not None:
                    subdict['pmsi']['tun_id']['tun_endpoint'] = m.groupdict()['tun_endpoint']
                if m.groupdict()['local'] is not None:
                    subdict['pmsi']['tun_id']['local'] = True

            # rx pathid: 0, tx pathid: 0
            m = p9.match(line)
            if m:
                subdict['recipient_pathid'] = m.groupdict()['recipient_pathid']
                subdict['transfer_pathid'] = m.groupdict()['transfer_pathid']
                continue
            
            # mpls labels in/out nolabel/64402
            m = p18.match(line)
            if m:
                group = m.groupdict()

                mpls_labels_dict = subdict.setdefault('mpls_labels', {})
                mpls_labels_dict.update({'in': group['in']})
                mpls_labels_dict.update({'out': group['out']})
                continue

            # IGMP/MLD v3, exclude
            # IGMP/MLD v3, include
            # IGMP/MLD v2
            # IGMP/MLD v1
            # IGMP/MLD v2, v3, exclude
            m = p19.match(line)
            if m:
                subdict['igmpmld'] = {}
                group = m.groupdict()
                subdict['igmpmld']['version'] = group['version']
                if group['filter_mode']:
                    subdict['igmpmld']['filter_mode'] = group['filter_mode']
                continue

            # binding SID: 28 (color - 7) (state - UP)
            m = p20.match(line)
            if m:
                group = m.groupdict()
                if 'binding_sid' not in subdict:
                    subdict['binding_sid'] = {}
                for i in ['sid', 'color']:
                    subdict['binding_sid'][i] = group[i]
                if group['state']:
                    subdict['binding_sid']['state'] = str(group['state'])
                continue

            # EVPN ESI: 00000000000000000000, Gateway Address: 0.0.0.0, local vtep: 10.21.33.33, Label 30000
            # EVPN ESI: 00000000000000000000, Label1 2000101
            m = p10.match(line)
            if m:
                group = m.groupdict()
                if 'evpn' not in subdict:
                    subdict['evpn'] = {}

                for i in ['evpn_esi', 'local_vtep', 'gateway_address']:
                    if group[i]:
                        subdict['evpn'][i] = group[i]

                subdict['evpn']['label'] = int(group['label'])
                continue

            # Local vxlan vtep:
            m = p11.match(line)
            if m:
                if 'local_vxlan_vtep' not in subdict:
                    subdict['local_vxlan_vtep'] = {}

                local_vxlan_vtep = True
                continue

            # bdi:BDI200
            # local router mac:001E.7AFF.FCD2
            # encap:8
            # vtep-ip:10.21.33.33
            m = p12.match(line) or p14.match(line)\
                or p15.match(line) or p16.match(line)
            if m and local_vxlan_vtep:
                group = m.groupdict()
                k = list(group)[0]
                subdict['local_vxlan_vtep'][k] = group[k]
                continue

            # vrf:evpn1, vni:30000
            m = p13.match(line)
            if m and local_vxlan_vtep:
                subdict['local_vxlan_vtep']['vrf'] = m.groupdict()['vrf']
                subdict['local_vxlan_vtep']['vni'] = m.groupdict()['vni']
                continue

            # Local
            # 65530
            # Local, imported path from base
            # 200 33299 51178 47751 {27016}
            # 200 33299 51178 47751 {27016}, imported path from 200:2:10.1.1.0/24 (global)
            # 400 33299 51178 47751 {27016}, imported path from [400:1]2001:db8:a69:5a4::/64 (VRF2)
            # 62000, (Received from a RR-client)
            # 4210105002 4210105502 4210105001 4210105507 4210105007 4210105220 65000 65151 65501, (aggregated by 65251 10.160.0.61), (received & used)
            # 4210105002 4210105502 4210105001 4210105507 4210105007 4210105220 65000 65151 65501, (aggregated by 65251 2001:db8:4::1), (received & used)
            # 4210105002 4210105502 4210105001 4210105507 4210105007 4210105220 65000 65151 65501, (aggregated by 65251 FE80:CD00:0:CDE:1257:0:211E:729C), (received & used)
            m = p17.match(line)
            if m and refresh_epoch_flag or m and m.groupdict()['route_info']:
                group = m.groupdict()
                route_info = group['route_info']

                if group['route_status']:
                    temp_route_status = group['route_status'].strip(' ')
                    if temp_route_status.startswith('(') and temp_route_status.endswith(')'):
                        route_status = temp_route_status.strip("()")
                    elif 'imported path from' in temp_route_status:
                        imported_path_from = temp_route_status.lstrip('imported path from')
                        imported_safety_path = False
                        route_status = ''
                    elif 'imported safety path from' in temp_route_status:
                        imported_path_from = temp_route_status.lstrip('imported safety path from')
                        imported_safety_path = True
                        route_status = ''

                if group['aggregated_by']:
                    output = group['aggregated_by'].split(' ')
                    aggregated_by_as = output[0]
                    aggregated_by_address = output[1]

                refresh_epoch_flag = False
                continue

        return ret_dict


# =================================================
# Parser for:
#   * 'show bgp all detail'
#   * 'show bgp vrf {vrf} {route}'
#   * 'show bgp {address_family} vrf {vrf} {route}'
# =================================================
class ShowBgpAllDetail(ShowBgpDetailSuperParser, ShowBgpAllDetailSchema):

    ''' Parser for:
        * 'show bgp all detail'
        * 'show bgp vrf {vrf} {route}'
        * 'show bgp {address_family} vrf {vrf} {route}'
        * 'show bgp {address_family} {route}'
    '''

    cli_command = ['show bgp all detail',
                    'show bgp vrf {vrf} {route}',
                    'show bgp {address_family} vrf {vrf} {route}',
                    'show bgp {address_family} {route}'
                   ]
    exclude = ['table_version', 'refresh_epoch', 'best_path', 'status_codes', 'transfer_pathid', 'paths']


    def cli(self, vrf='', route='', address_family='',output=None):
        if output is None:
            if vrf and route:
                if address_family:
                    cmd = self.cli_command[2].format(vrf=vrf,
                        route=route,
                        address_family=address_family)
                else:
                    address_family = 'vpnv4 unicast'
                    cmd = self.cli_command[1].format(vrf=vrf,
                        route=route)
            # elif address_family and route:
            #     cmd = self.cli_command[3].format(address_family=address_family, route=route) 
            else:
                cmd = self.cli_command[0]
            # Execute command
            show_output = self.device.execute(cmd)
        else:
            show_output = output

        # Call super
        return super().cli(address_family=address_family,output=show_output)




# ================================================
# Parser for:
#   * 'show bgp {address_family} vrf {vrf} detail'
#   * 'show bgp {address_family} rd {rd} detail'
# ================================================
class ShowBgpDetail(ShowBgpDetailSuperParser, ShowBgpAllDetailSchema):

    ''' Parser for:
        * 'show bgp {address_family} vrf {vrf} detail'
        * 'show bgp {address_family} rd {rd} detail'
    '''

    cli_command = ['show bgp {address_family} vrf {vrf} detail',
                   'show bgp {address_family} rd {rd} detail',
                   ]

    def cli(self, address_family='', vrf='', rd='', output=None):

        # Init dict
        ret_dict = {}

        if output is None:
            if address_family and vrf:
                cmd = self.cli_command[0].format(address_family=address_family,
                                                 vrf=vrf)
            elif address_family and rd:
                cmd = self.cli_command[1].format(address_family=address_family,
                                                 rd=rd)
            else:
                return ret_dict
            # Execute command
            show_output = self.device.execute(cmd)
        else:
            show_output = output

        # Call super
        return super().cli(output=show_output, vrf=vrf, rd=rd,
                           address_family=address_family)



# =====================================================
# Schema for:
#   * 'show bgp summary'
#   * 'show bgp {address_family} summary'
#   * 'show bgp {address_family} vrf {vrf} summary'
#   * 'show bgp {address_family} rd {rd} summary'
#   * 'show bgp all summary'
#   * 'show bgp {address_family} all summary'
#   * 'show ip bgp summary'
#   * 'show ip bgp {address_family} summary'
#   * 'show ip bgp {address_family} vrf {vrf} summary'
#   * 'show ip bgp {address_family} rd {rd} summary'
#   * 'show ip bgp all summary'
#   * 'show ip bgp {address_family} all summary'
# =====================================================
class ShowBgpSummarySchema(MetaParser):

    ''' Schema for
        * 'show bgp summary'
        * 'show bgp {address_family} summary'
        * 'show bgp {address_family} vrf {vrf} summary'
        * 'show bgp {address_family} rd {rd} summary'
        * 'show bgp all summary'
        * 'show bgp {address_family} all summary'
        * 'show ip bgp summary'
        * 'show ip bgp {address_family} summary'
        * 'show ip bgp {address_family} vrf {vrf} summary'
        * 'show ip bgp {address_family} rd {rd} summary'
        * 'show ip bgp all summary'
        * 'show ip bgp {address_family} all summary'
    '''

    schema = {
        'bgp_id': Or(int,str),
        'vrf':
            {Any():
                {Optional('neighbor'):
                    {Any():
                        {'address_family':
                            {Any():
                                {'version': int,
                                'as': Or(int, str),
                                'msg_rcvd': int,
                                'msg_sent': int,
                                'tbl_ver': int,
                                'input_queue': int,
                                'output_queue': int,
                                'up_down': str,
                                'state_pfxrcd': str,
                                Optional('route_identifier'): str,
                                Optional('local_as'): Or(int, str),
                                Optional('bgp_table_version'): int,
                                Optional('routing_table_version'): int,
                                Optional('prefixes'):
                                    {'total_entries': int,
                                    'memory_usage': int,
                                    },
                                Optional('path'):
                                    {'total_entries': int,
                                    'memory_usage': int,
                                    },
                                Optional('cache_entries'):
                                    {Any():
                                        {'total_entries': int,
                                        'memory_usage': int,
                                        },
                                    },
                                Optional('entries'):
                                    {Any():
                                        {'total_entries': int,
                                        'memory_usage': int,
                                        },
                                    },
                                Optional('community_entries'):
                                    {'total_entries': int,
                                    'memory_usage': int,
                                    },
                                Optional('attribute_entries'): str,
                                Optional('total_memory'): int,
                                Optional('activity_prefixes'): str,
                                Optional('activity_paths'): str,
                                Optional('scan_interval'): int,
                                },
                            },
                        },
                    },
                },
            },
        }


# ==================================================
# Super Parser for:
#   * 'show bgp summary'
#   * 'show bgp {address_family} summary'
#   * 'show bgp {address_family} vrf {vrf} summary'
#   * 'show bgp {address_family} rd {rd} summary'
#   * 'show bgp all summary'
#   * 'show bgp {address_family} all summary'
#   * 'show ip bgp summary'
#   * 'show ip bgp {address_family} summary'
#   * 'show ip bgp {address_family} vrf {vrf} summary'
#   * 'show ip bgp {address_family} rd {rd} summary'
#   * 'show ip bgp all summary'
#   * 'show ip bgp {address_family} all summary'
# ==================================================
class ShowBgpSummarySuperParser(ShowBgpSummarySchema):

    ''' Parser for:
        * 'show bgp summary'
        * 'show bgp {address_family} summary'
        * 'show bgp {address_family} vrf {vrf} summary'
        * 'show bgp {address_family} rd {rd} summary'
        * 'show bgp all summary'
        * 'show bgp {address_family} all summary'
        * 'show ip bgp summary'
        * 'show ip bgp {address_family} summary'
        * 'show ip bgp {address_family} vrf {vrf} summary'
        * 'show ip bgp {address_family} rd {rd} summary'
        * 'show ip bgp all summary'
        * 'show ip bgp {address_family} all summary'
    '''

    def cli(self, address_family='', vrf='', rd='',  cmd='', output=None):

        # Init vars
        sum_dict = {}
        cache_dict = {}
        entries_dict = {}
        bgp_config_dict = {}
        passed_vrf = vrf

        if not vrf:
            vrf ='default'

        show_vrf_output = None
        if ('rd' in cmd and 'summary' in cmd and
            output != '% RD does not match the default RD of any VRF'):
            obj = ShowVrf(device=self.device)
            show_vrf_output = obj.parse()
            # try:
            #     show_vrf_output = obj.parse()
            # except Exception:
            #     pass

        if address_family.lower() not in ['ipv4 unicast', 'ipv6 unicast']:
           
            if ('all summary' in cmd and 
                output != '% RD does not match the default RD of any VRF'):

                if 'vpnv4' in address_family:
                    commands_list = ['show run | sec address-family ipv4 vrf']
                elif 'vpnv6' in address_family:
                    commands_list = ['show run | sec address-family ipv6 vrf']
                else:
                    commands_list = ['show run | sec address-family ipv4 vrf',
                                     'show run | sec address-family ipv6 vrf']
                
                for command in commands_list:
                    out_vrf = self.device.execute(command)

                    rc1 = re.compile(r'address\-family\s+(?P<address_family>'
                                      r'ipv4|ipv6)\s+vrf\s+(?P<vrf>\S+)')

                    rc2 = re.compile(r'neighbor\s+(?P<neighbor_address>\S+)\s+'
                                r'remote\-as\s+(?P<remote_as>\S+)')

                    flag_address_family = False            

                    for line in out_vrf.splitlines():
                        line = line.strip()

                        result = rc1.match(line)
                        if result:
                            groupdict = result.groupdict()
                            address_family_d = bgp_config_dict.setdefault(groupdict['address_family'], {})
                            vrf_dict = address_family_d.setdefault(groupdict['vrf'], {})

                            flag_address_family = True
                            continue

                        if flag_address_family:
                            result = rc2.match(line)
                            if result:
                                groupdict = result.groupdict()
                                neighbor_dict = vrf_dict.setdefault(groupdict['neighbor_address'], {})
                                neighbor_dict['remote_as'] = groupdict['remote_as']
                            continue

        # For address family: IPv4 Unicast
        p1 = re.compile(r'^For address family: +(?P<address_family>[a-zA-Z0-9\s\-\_]+)$')

        # BGP router identifier 192.168.111.1, local AS number 100
        # BGP router identifier 30.1.107.78, local AS number 304.304
        p2 = re.compile(r'^BGP +router +identifier'
                         r' +(?P<route_identifier>[0-9\.\:]+), +local +AS'
                         r' +number +(?P<local_as>[0-9\.]+)$')

        # BGP table version is 28, main routing table version 28
        p3 = re.compile(r'^BGP +table +version +is'
                         r' +(?P<bgp_table_version>[0-9]+),'
                         r' +main +routing +table +version'
                         r' +(?P<routing_table_version>[0-9]+)$')

        # 27 network entries using 6696 bytes of memory
        p4 = re.compile(r'^(?P<networks>[0-9]+) +network +entries +using'
                         r' +(?P<bytes>[0-9]+) +bytes +of +memory$')

        # 27 path entries using 3672 bytes of memory
        p5 = re.compile(r'^(?P<path>[0-9]+) +path +entries +using'
                         r' +(?P<memory_usage>[0-9]+) +bytes +of +memory$')

        # 2 BGP rrinfo entries using 48 bytes of memory
        # 201 BGP AS-PATH entries using 4824 bytes of memory
        p5_1 = re.compile(r'^(?P<num_entries>([0-9]+)) +BGP'
                           r' +(?P<entries_type>(\S+)) +entries +using'
                           r' +(?P<entries_byte>[0-9]+) +bytes +of +memory$')

        # 4 BGP extended community entries using 96 bytes of memory
        p5_2 = re.compile(r'^(?P<num_community_entries>[0-9]+) +BGP +extended'
                           r' +community +entries +using'
                           r' +(?P<memory_usage>[0-9]+) +bytes +of +memory$')

        # 1/1 BGP path/bestpath attribute entries using 280 bytes of memory
        p6 = re.compile(r'^(?P<attribute_entries>(\S+)) +BGP'
                         r' +(?P<attribute_type>(\S+)) +attribute +entries'
                         r' +using +(?P<bytes>[0-9]+) +bytes +of +memory$')

        # 0 BGP route-map cache entries using 0 bytes of memory
        # 0 BGP filter-list cache entries using 0 bytes of memory
        p6_1 = re.compile(r'^(?P<num_cache_entries>([0-9]+)) +BGP'
                           r' +(?P<cache_type>(\S+)) +cache +entries +using'
                           r' +(?P<cache_byte>[0-9]+) +bytes +of +memory$')

        # BGP using 10648 total bytes of memory
        p7 = re.compile(r'^BGP +using +(?P<total_memory>[0-9]+) +total +bytes'
                         r' +of +memory$')

        # BGP activity 47/20 prefixes, 66/39 paths, scan interval 60 secs
        p8 = re.compile(r'^BGP +activity +(?P<activity_prefixes>(\S+))'
                         r' +prefixes, +(?P<activity_paths>(\S+)) +paths, +scan'
                         r' +interval +(?P<scan_interval>[0-9]+) +secs$')

        # Neighbor        V           AS MsgRcvd MsgSent   TblVer  InQ OutQ Up/Down  State/PfxRcd
        # 192.168.111.1       4          100       0       0        1    0    0 01:07:38 Idle
        # 192.168.4.1       4          100       0       0        1    0    0 never    Idle
        # 192.168.51.1       4          100       0       0        1    0    0 01:07:38 Idle
        p9 = re.compile(r'^ *(?P<our_entry>\*)?(?P<neighbor>[a-zA-Z0-9\.\:]+) +(?P<version>[0-9]+)'
                         r' +(?P<as>[0-9]+(\.\d+)?) +(?P<msg_rcvd>[0-9]+)'
                         r' +(?P<msg_sent>[0-9]+) +(?P<tbl_ver>[0-9]+)'
                         r' +(?P<inq>[0-9]+) +(?P<outq>[0-9]+)'
                         r' +(?P<up_down>[a-zA-Z0-9\:]+)'
                         r' +(?P<state>[a-zA-Z0-9\(\)\s]+)$')

        #  Neighbor        V           AS MsgRcvd MsgSent   TblVer  InQ OutQ Up/Down  State/PfxRcd
        #  2001:DB8:20:4:6::6
        #           4          400      67      73       66    0    0 01:03:11        5
        #  *2001::100:1:2:1
        #                  4        65001       7       7      198    0    0 00:00:02        1
        p10 = re.compile(r'^(?P<our_entry>\*)?(?P<neighbor>[a-zA-Z0-9\.\:]+)$')

        p11 = re.compile(r'^(?P<version>[0-9]+)'
                          r' +(?P<as>[0-9]+(\.\d+)?) +(?P<msg_rcvd>[0-9]+)'
                          r' +(?P<msg_sent>[0-9]+) +(?P<tbl_ver>[0-9]+)'
                          r' +(?P<inq>[0-9]+) +(?P<outq>[0-9]+)'
                          r' +(?P<up_down>[a-zA-Z0-9\:]+)'
                         r' +(?P<state>[a-zA-Z0-9\(\)\s]+)$')

        for line in output.splitlines():

            line = line.strip()

            # For address family: IPv4 Unicast
            m = p1.match(line)
            if m:
                # Save variables for use later
                address_family = m.groupdict()['address_family'].lower()
                if not vrf:
                    vrf = 'default'
                attribute_entries = ""
                num_prefix_entries = ""
                path_total_entries = ""
                total_memory = ""
                activity_paths = ""
                activity_prefixes = ""
                scan_interval = ""
                cache_dict = {}
                entries_dict = {}
                num_community_entries = ""
                continue

            # BGP router identifier 192.168.111.1, local AS number 100
            # BGP router identifier 30.1.107.78, local AS number 304.304
            m = p2.match(line)
            if m:
                route_identifier = m.groupdict()['route_identifier']
                try:
                    local_as = int(m.groupdict()['local_as'])
                except:
                    local_as = m.groupdict()['local_as']

                sum_dict['bgp_id'] = local_as
                continue

            # BGP table version is 28, main routing table version 28
            m = p3.match(line)
            if m:
                bgp_table_version = int(m.groupdict()['bgp_table_version'])
                routing_table_version = int(m.groupdict()['routing_table_version'])
                continue

            # 27 network entries using 6696 bytes of memory
            m = p4.match(line)
            if m:
                num_prefix_entries = int(m.groupdict()['networks'])
                num_memory_usage = int(m.groupdict()['bytes'])
                continue

            # 27 path entries using 3672 bytes of memory
            m = p5.match(line)
            if m:
                path_total_entries = int(m.groupdict()['path'])
                path_memory_usage = int(m.groupdict()['memory_usage'])
                continue

            # 2 BGP rrinfo entries using 48 bytes of memory
            m = p5_1.match(line)
            if m:
                num_entries = int(m.groupdict()['num_entries'])
                entries_type = str(m.groupdict()['entries_type'])
                entries_byte = int(m.groupdict()['entries_byte'])
                entries_dict[entries_type] = {}
                entries_dict[entries_type]['total_entries'] = num_entries
                entries_dict[entries_type]['memory_usage'] = entries_byte
                continue

            # 4 BGP extended community entries using 96 bytes of memory
            m = p5_2.match(line)
            if m:
                num_community_entries = int(m.groupdict()['num_community_entries'])
                community_memory_usage = int(m.groupdict()['memory_usage'])
                continue

            # 1/1 BGP path/bestpath attribute entries using 280 bytes of memory
            m = p6.match(line)
            if m:
                attribute_entries = str(m.groupdict()['attribute_entries'])
                attribute_type = str(m.groupdict()['attribute_type'])
                attribute_memory_usage = int(m.groupdict()['bytes'])
                continue

            # 0 BGP route-map cache entries using 0 bytes of memory
            m = p6_1.match(line)
            if m:
                num_cache_entries = int(m.groupdict()['num_cache_entries'])
                cache_type = str(m.groupdict()['cache_type'])
                cache_byte = int(m.groupdict()['cache_byte'])

                cache_dict[cache_type] = {}
                cache_dict[cache_type]['total_entries'] = num_cache_entries
                cache_dict[cache_type]['memory_usage'] = cache_byte
                continue

            # BGP using 10648 total bytes of memory
            m = p7.match(line)
            if m:
                total_memory = int(m.groupdict()['total_memory'])
                continue

            # BGP activity 47/20 prefixes, 66/39 paths, scan interval 60 secs
            m = p8.match(line)
            if m:
                activity_prefixes = str(m.groupdict()['activity_prefixes'])
                activity_paths = str(m.groupdict()['activity_paths'])
                scan_interval = str(m.groupdict()['scan_interval'])
                continue

            # Neighbor        V           AS MsgRcvd MsgSent   TblVer  InQ OutQ Up/Down  State/PfxRcd
            # 192.168.111.1       4          100       0       0        1    0    0 01:07:38 Idle
            # 192.168.4.1       4          100       0       0        1    0    0 never    Idle
            # 192.168.51.1       4          100       0       0        1    0    0 01:07:38 Idle
            # 30.1.10.1       4      304.304    6953   38119   136088    0    0 00:50:14     2540
            # 30.2.10.1       4      304.304    6347   38120   136088    0    0 00:50:13     2580
            # 30.3.10.1       4      301.301    7722   38113   136088    0    0 00:50:14     4439
            m = p9.match(line)
            if m:
                # Add neighbor to dictionary
                neighbor = str(m.groupdict()['neighbor'])
                try:
                    neighbor_as = int(m.groupdict()['as'])
                except:
                    neighbor_as = m.groupdict()['as']
                if not passed_vrf:
                    if address_family not in ['ipv4 unicast', 'ipv6 unicast']:
                        if 'all summary' in cmd:
                            for ipv, vrfs_dict in bgp_config_dict.items():
                                for vrf_value, neighbors_value in vrfs_dict.items():
                                    for local_neighbor, as_num in neighbors_value.items():
                                        if (local_neighbor == neighbor and
                                            as_num['remote_as'] == str(neighbor_as)):
                                            vrf = vrf_value
                                            neighbors_value.pop(local_neighbor, '')
                                            break
                                    else:
                                        continue
                                    break
                                else:
                                    continue
                                break                                
                            else:
                                vrf = 'default'                    
                    else:
                        vrf = 'default'

                    if 'rd' in cmd and 'summary' in cmd:
                        if show_vrf_output:
                            for vrf_value, vrf_dict in show_vrf_output['vrf'].items():
                                if vrf_dict.get('route_distinguisher', '') == rd:
                                    vrf = vrf_value
                                    break
                        else:
                            vrf = 'default'

                nbr_dict = sum_dict.setdefault('vrf', {}).setdefault(vrf, {})\
                           .setdefault('neighbor', {}).setdefault(neighbor, {})

                nbr_af_dict = nbr_dict.setdefault('address_family', {})\
                                      .setdefault(address_family, {})

                # Add keys for this address_family
                nbr_af_dict['version'] = int(m.groupdict()['version'])
                nbr_af_dict['as'] = neighbor_as
                nbr_af_dict['msg_rcvd'] = int(m.groupdict()['msg_rcvd'])
                nbr_af_dict['msg_sent'] = int(m.groupdict()['msg_sent'])
                nbr_af_dict['tbl_ver'] = int(m.groupdict()['tbl_ver'])
                nbr_af_dict['input_queue'] = int(m.groupdict()['inq'])
                nbr_af_dict['output_queue'] = int(m.groupdict()['outq'])
                nbr_af_dict['up_down'] = str(m.groupdict()['up_down'])
                nbr_af_dict['state_pfxrcd'] = str(m.groupdict()['state'])
                nbr_af_dict['route_identifier'] = route_identifier
                nbr_af_dict['local_as'] = local_as
                nbr_af_dict['bgp_table_version'] = bgp_table_version
                nbr_af_dict['routing_table_version'] = routing_table_version

                try:
                # Assign variables
                    if attribute_entries:
                        nbr_af_dict['attribute_entries'] = attribute_entries
                    if num_prefix_entries:
                        nbr_af_dict['prefixes'] = {}
                        nbr_af_dict['prefixes']['total_entries'] = num_prefix_entries
                        nbr_af_dict['prefixes']['memory_usage'] = num_memory_usage

                    if path_total_entries:
                        nbr_af_dict['path'] = {}
                        nbr_af_dict['path']['total_entries'] = path_total_entries
                        nbr_af_dict['path']['memory_usage'] = path_memory_usage

                    if total_memory:
                        nbr_af_dict['total_memory'] = total_memory

                    if activity_prefixes:
                        nbr_af_dict['activity_prefixes'] = activity_prefixes

                    if activity_paths:
                        nbr_af_dict['activity_paths'] = activity_paths

                    if scan_interval:
                        nbr_af_dict['scan_interval'] = int(scan_interval)

                    if len(cache_dict):
                        nbr_af_dict['cache_entries'] = cache_dict

                    if len(entries_dict):
                        nbr_af_dict['entries'] = entries_dict

                    if num_community_entries:
                        nbr_af_dict['community_entries'] = {}
                        nbr_af_dict['community_entries']['total_entries'] = num_community_entries
                        nbr_af_dict['community_entries']['memory_usage'] = community_memory_usage
                except Exception:
                    pass
            else:
                # when neighbor info break down to 2 lines.
                #  Neighbor        V           AS MsgRcvd MsgSent   TblVer  InQ OutQ Up/Down  State/PfxRcd
                #  2001:DB8:20:4:6::6
                #           4          400      67      73       66    0    0 01:03:11        5
                m = p10.match(line)
                if m :
                    # Add neighbor to dictionary
                    neighbor = str(m.groupdict()['neighbor'])
                    if sum_dict.get('vrf'):
                        if 'neighbor' not in sum_dict['vrf'][vrf]:
                            sum_dict['vrf'][vrf]['neighbor'] = {}
                        if neighbor not in sum_dict['vrf'][vrf]['neighbor']:
                            sum_dict['vrf'][vrf]['neighbor'][neighbor] = {}
                        nbr_dict = sum_dict['vrf'][vrf]['neighbor'][neighbor]

                    # Add address family to this neighbor
                    if 'address_family' not in nbr_dict:
                        nbr_dict['address_family'] = {}
                    if address_family not in nbr_dict['address_family']:
                        nbr_dict['address_family'][address_family] = {}
                    nbr_af_dict = nbr_dict['address_family'][address_family]

                m = p11.match(line)
                if m:
                    # Add keys for this address_family
                    nbr_af_dict['version'] = int(m.groupdict()['version'])
                    try:
                        nbr_af_dict['as'] = int(m.groupdict()['as'])
                    except:
                        nbr_af_dict['as'] = m.groupdict()['as']
                    nbr_af_dict['msg_rcvd'] = int(m.groupdict()['msg_rcvd'])
                    nbr_af_dict['msg_sent'] = int(m.groupdict()['msg_sent'])
                    nbr_af_dict['tbl_ver'] = int(m.groupdict()['tbl_ver'])
                    nbr_af_dict['input_queue'] = int(m.groupdict()['inq'])
                    nbr_af_dict['output_queue'] = int(m.groupdict()['outq'])
                    nbr_af_dict['up_down'] = str(m.groupdict()['up_down'])
                    nbr_af_dict['state_pfxrcd'] = str(m.groupdict()['state'])
                    nbr_af_dict['route_identifier'] = route_identifier
                    nbr_af_dict['local_as'] = local_as
                    nbr_af_dict['bgp_table_version'] = bgp_table_version
                    nbr_af_dict['routing_table_version'] = routing_table_version

                    try:
                        # Assign variables
                        if attribute_entries:
                            nbr_af_dict['attribute_entries'] = attribute_entries
                        if num_prefix_entries:
                            nbr_af_dict['prefixes'] = {}
                            nbr_af_dict['prefixes']['total_entries'] = num_prefix_entries
                            nbr_af_dict['prefixes']['memory_usage'] = num_memory_usage

                        if path_total_entries:
                            nbr_af_dict['path'] = {}
                            nbr_af_dict['path']['total_entries'] = path_total_entries
                            nbr_af_dict['path']['memory_usage'] = path_memory_usage

                        if total_memory:
                            nbr_af_dict['total_memory'] = total_memory

                        if activity_prefixes:
                            nbr_af_dict['activity_prefixes'] = activity_prefixes

                        if activity_paths:
                            nbr_af_dict['activity_paths'] = activity_paths

                        if scan_interval:
                            nbr_af_dict['scan_interval'] = int(scan_interval)

                        if len(cache_dict):
                            nbr_af_dict['cache_entries'] = cache_dict

                        if len(entries_dict):
                            nbr_af_dict['entries'] = entries_dict

                        if num_community_entries:
                            nbr_af_dict['community_entries'] = {}
                            nbr_af_dict['community_entries']['total_entries'] = num_community_entries
                            nbr_af_dict['community_entries']['memory_usage'] = community_memory_usage
                    except Exception:
                        pass
                continue

        return sum_dict


# =====================================================
# Parser for:
#   * 'show bgp summary'
#   * 'show bgp {address_family} summary'
#   * 'show bgp {address_family} vrf {vrf} summary'
#   * 'show bgp {address_family} rd {rd} summary'
# =====================================================
class ShowBgpSummary(ShowBgpSummarySuperParser, ShowBgpSummarySchema):

    ''' Parser for:
        * 'show bgp summary'
        * 'show bgp {address_family} summary'
        * 'show bgp {address_family} vrf {vrf} summary'
        * 'show bgp {address_family} rd {rd} summary'
    '''

    cli_command = ['show bgp {address_family} vrf {vrf} summary',
                   'show bgp {address_family} rd {rd} summary',
                   'show bgp {address_family} summary',
                   'show bgp summary'
                   ]
    exclude = ['msg_rcvd', 'msg_sent', 'up_down']

    def cli(self, address_family='', vrf='', rd='', output=None):

        cmd = ''
        if output is None:
            # Build command
            if vrf:
                if address_family:
                    cmd = self.cli_command[0].format(address_family=address_family,
                                                 vrf=vrf)
            elif rd:
                if address_family:
                    cmd = self.cli_command[1].format(address_family=address_family,
                                                 rd=rd)
            elif address_family:
                cmd = self.cli_command[2].format(address_family=address_family)

            else:
                cmd = self.cli_command[3]
            # Execute command
            show_output = self.device.execute(cmd)
        else:
            show_output = output

        # Call super
        return super().cli(output=show_output, vrf=vrf, rd=rd,
                           address_family=address_family, cmd=cmd)


class ShowBgpL2vpnEvpnSummary(ShowBgpSummarySuperParser):

    ''' Parser for:
        * 'show bgp l2vpn evpn summary'
    '''

    cli_command = 'show bgp l2vpn evpn summary'

    def cli(self, output=None):

        if output is None:
            output = self.device.execute(self.cli_command)

        # Call super
        return super().cli(output=output)


# ============================================
# Parser for:
#   * 'show bgp all summary'
#   * 'show bgp {address_family} all summary'
#   * 'show bgp vrf {vrf} all summary'
# ============================================
class ShowBgpAllSummary(ShowBgpSummarySuperParser, ShowBgpSummarySchema):

    ''' Parser for:
        * 'show bgp all summary'
        * 'show bgp {address_family} all summary'
        * 'show bgp vrf {vrf} all summary'
    '''

    cli_command = ['show bgp {address_family} all summary',
                   'show bgp all summary',
                   'show bgp vrf {vrf} all summary'
                   ]
    exclude = ['msg_sent', 'msg_rcvd', 'activity_paths', 'activity_prefixes',
        'bgp_table_version', 'routing_table_version', 'tbl_ver', 'up_down',
        'attribute_entries', 'dropped', 'established', 'input_queue',
        'output_queue']


    def cli(self, address_family='', vrf='',output=None):

        if output is None:
            # Build command
            if address_family and not vrf:
                cmd = self.cli_command[0].format(address_family=address_family)
            elif vrf and not address_family:
                cmd = self.cli_command[2].format(vrf=vrf)
            else:
                cmd = self.cli_command[1]
            # Execute command
            show_output = self.device.execute(cmd)
        else:
            show_output = output

        # Call super
        return super().cli(output=show_output, address_family=address_family, 
                          vrf=vrf)

#-------------------------------------------------------------------------------


# ==================================================================
# Schema for:
#   * 'show bgp all neighbors'
#   * 'show bgp all neighbors {neighbor}'
#   * 'show bgp {address_family} all neighbors'
#   * 'show bgp {address_family} all neighbors {neighbor}'
#   * 'show bgp neighbors'
#   * 'show bgp neighbors {neighbor}'
#   * 'show bgp {address_family} neighbors'
#   * 'show bgp {address_family} neighbors {neighbor}'
#   * 'show bgp {address_family} vrf {vrf} neighbors'
#   * 'show bgp {address_family} vrf {vrf} neighbors {neighbor}'
#   * 'show ip bgp all neighbors',
#   * 'show ip bgp all neighbors {neighbor}'
#   * 'show ip bgp {address_family} all neighbors'
#   * 'show ip bgp {address_family} all neighbors {neighbor}'
#   * 'show ip bgp neighbors'
#   * 'show ip bgp neighbors {neighbor}'
#   * 'show ip bgp {address_family} neighbors'
#   * 'show ip bgp {address_family} neighbors {neighbor}'
#   * 'show ip bgp {address_family} vrf {vrf} neighbors'
#   * 'show ip bgp {address_family} vrf {vrf} neighbors {neighbor}'
# ==================================================================
class ShowBgpAllNeighborsSchema(MetaParser):

    ''' Schema for
        * 'show bgp all neighbors'
        * 'show bgp all neighbors {neighbor}'
        * 'show bgp {address_family} all neighbors'
        * 'show bgp {address_family} all neighbors {neighbor}'
        * 'show bgp neighbors'
        * 'show bgp neighbors {neighbor}'
        * 'show bgp {address_family} neighbors'
        * 'show bgp {address_family} neighbors {neighbor}'
        * 'show bgp {address_family} vrf {vrf} neighbors'
        * 'show bgp {address_family} vrf {vrf} neighbors {neighbor}'
        * 'show ip bgp all neighbors',
        * 'show ip bgp all neighbors {neighbor}'
        * 'show ip bgp {address_family} all neighbors'
        * 'show ip bgp {address_family} all neighbors {neighbor}'
        * 'show ip bgp neighbors'
        * 'show ip bgp neighbors {neighbor}'
        * 'show ip bgp {address_family} neighbors'
        * 'show ip bgp {address_family} neighbors {neighbor}'
        * 'show ip bgp {address_family} vrf {vrf} neighbors'
        * 'show ip bgp {address_family} vrf {vrf} neighbors {neighbor}'
    '''

    schema = {
        Optional('list_of_neighbors'): list,
        'vrf':
            {Any():
                 {'neighbor':
                    {Any():
                        {'remote_as': Or(int, str),
                        'link': str,
                        Optional('local_as'): Or(int, str),
                        Optional('description'): str,
                        'shutdown': bool,
                        Optional('bgp_version'): int,
                        Optional('peer_group'): str,
                        Optional('router_id'): str,
                        Optional('session_state'): str,
                        Optional('no_prepend'): bool,
                        Optional('replace_as'): bool,
                        Optional('address_family'):
                            {Any():
                                {Optional('session_state'): str,
                                Optional('up_time'): str,
                                Optional('down_time'): str,
                                Optional('last_read'): str,
                                Optional('last_write'): str,
                                Optional('current_time'): str,
                                Optional('bgp_table_version'): int,
                                Optional('neighbor_version'): str,
                                Optional('output_queue_size'): int,
                                Optional('index'): int,
                                Optional('advertise_bit'): int,
                                Optional('route_reflector_client'): bool,
                                Optional('update_group_member'): int,
                                Optional('community_attribute_sent'): bool,
                                Optional('extended_community_attribute_sent'): bool,
                                Optional('suppress_ldp_signaling'): bool,
                                Optional('slow_peer_detection'): bool,
                                Optional('slow_peer_split_update_group_dynamic'): bool,
                                Optional('refresh_epoch'): int,
                                Optional('max_nlri'): int,
                                Optional('min_nlri'): int,
                                Optional('last_detected_dynamic_slow_peer'): str,
                                Optional('dynamic_slow_peer_recovered'): str,
                                Optional('last_sent_refresh_start_of_rib'): str,
                                Optional('last_received_refresh_start_of_rib'): str,
                                Optional('last_sent_refresh_end_of_rib'): str,
                                Optional('last_received_refresh_end_of_rib'): str,
                                Optional('refresh_out'): int,
                                Optional('refresh_in'): int,
                                Optional('prefix_activity_counters'):
                                    {'sent':
                                        {Any(): Any(),
                                        },
                                    'received':
                                        {Any(): Any(),
                                        },
                                    },
                                Optional('local_policy_denied_prefixes_counters'):
                                    {'outbound':
                                        {Any(): Any(),
                                        },
                                    'inbound':
                                        {Any(): Any(),
                                        },
                                    },
                                Optional('refresh_activity_counters'):
                                    {'sent':
                                        {Any(): int,
                                        },
                                    'received':
                                        {Any(): int,
                                        },
                                    },
                                },
                            },
                        Optional('bgp_negotiated_keepalive_timers'):
                            {'keepalive_interval': int,
                            'hold_time': int,
                            Optional('min_holdtime'): int,
                            },
                        Optional('bgp_negotiated_capabilities'):
                            {
                            Optional('remote_restart_timer'): int,
                            Optional('graceful_restart_af_advertised_by_peer'): list,
                            Any(): str,
                            },
                            Optional('bgp_neighbor_session'): {
                             Optional('sessions'): int,
                            Optional('stateful_switchover'): str,
                        },
                        Optional('bgp_neighbor_counters'):
                            {
                            Optional('messages'):
                                {'sent':
                                    {'opens': int,
                                    'updates': int,
                                    'notifications': int,
                                    'keepalives': int,
                                    'route_refresh': int,
                                    'total': int,
                                    },
                                'received':
                                    {'opens': int,
                                    'updates': int,
                                    'notifications': int,
                                    'keepalives': int,
                                    'route_refresh': int,
                                    'total': int,
                                    },
                                'in_queue_depth': int,
                                'out_queue_depth': int,
                                },
                            Optional('multisession_messages'): {
                                Any(): 
                                    {'sent':
                                        {'opens': int,
                                        'updates': int,
                                        'notifications': int,
                                        'keepalives': int,
                                        'route_refresh': int,
                                        'total': int,
                                        },
                                    'received':
                                        {'opens': int,
                                        'updates': int,
                                        'notifications': int,
                                        'keepalives': int,
                                        'route_refresh': int,
                                        'total': int,
                                        },
                                    'in_queue_depth': int,
                                    'out_queue_depth': int,
                                    },
                                },
                            },
                        Optional('bgp_session_transport'):
                            {'min_time_between_advertisement_runs': int,
                            Optional('address_tracking_status'): str,
                            Optional('rib_route_ip'): str,
                            Optional('tcp_path_mtu_discovery'): str,
                            'connection':
                                {'established': int,
                                'dropped': int,
                                'last_reset': str,
                                Optional('reset_reason'): str,
                                },
                            Optional('transport'):
                                {'local_port': str,
                                'local_host': str,
                                'foreign_port': str,
                                'foreign_host': str,
                                Optional('mss'): int,
                                },
                            Optional('graceful_restart'): str,
                            Optional('gr_restart_time'): int,
                            Optional('gr_stalepath_time'): int,
                            Optional('connection_state'): str,
                            Optional('io_status'): int,
                            Optional('unread_input_bytes'): int,
                            Optional('ecn_connection'): str,
                            Optional('minimum_incoming_ttl'): int,
                            Optional('outgoing_ttl'): int,
                            Optional('connection_tableid'): int,
                            Optional('maximum_output_segment_queue_size'): int,
                            Optional('enqueued_packets'):
                                {'retransmit_packet': int,
                                'input_packet': int,
                                'mis_ordered_packet': int,
                                },
                            Optional('iss'): int,
                            Optional('snduna'): int,
                            Optional('sndnxt'): int,
                            Optional('irs'): int,
                            Optional('rcvnxt'): int,
                            Optional('sndwnd'): int,
                            Optional('snd_scale'): int,
                            Optional('maxrcvwnd'): int,
                            Optional('rcvwnd'): int,
                            Optional('rcv_scale'): int,
                            Optional('delrcvwnd'): int,
                            Optional('srtt'): int,
                            Optional('rtto'): int,
                            Optional('rtv'): int,
                            Optional('krtt'): int,
                            Optional('min_rtt'): int,
                            Optional('max_rtt'): int,
                            Optional('ack_hold'): int,
                            Optional('uptime'): int,
                            Optional('sent_idletime'): int,
                            Optional('receive_idletime'): int,
                            Optional('status_flags'): str,
                            Optional('option_flags'): str,
                            Optional('ip_precedence_value'): int,
                            Optional('datagram'):
                                {Optional('datagram_sent'):
                                    {'value': int,
                                    'retransmit': int,
                                    'fastretransmit': int,
                                    'partialack': int,
                                    'second_congestion': int,
                                    'with_data': int,
                                    'total_data': int,
                                    },
                                'datagram_received':
                                    {'value': int,
                                    'out_of_order': int,
                                    'with_data': int,
                                    'total_data': int,
                                    },
                                },
                            Optional('packet_fast_path'): int,
                            Optional('packet_fast_processed'): int,
                            Optional('packet_slow_path'): int,
                            Optional('fast_lock_acquisition_failures'): int,
                            Optional('lock_slow_path'): int,
                            Optional('tcp_semaphore'): str,
                            Optional('tcp_semaphore_status'): str,
                            Optional('sso'): bool,
                            Optional('tcp_connection'): bool,
                            },
                        Optional('bgp_event_timer'):
                            {'starts':
                                {Any(): int,
                                },
                            'wakeups':
                                {Any(): int,
                                },
                            'next':
                                {Any(): str,
                                },
                            },
                        },
                    },
                },
            },
        }


# ==================================================================
# Super Parser:
#   * 'show bgp all neighbors'
#   * 'show bgp all neighbors {neighbor}'
#   * 'show bgp {address_family} all neighbors'
#   * 'show bgp {address_family} all neighbors {neighbor}'
#   * 'show bgp neighbors'
#   * 'show bgp neighbors {neighbor}'
#   * 'show bgp {address_family} neighbors'
#   * 'show bgp {address_family} neighbors {neighbor}'
#   * 'show bgp {address_family} vrf {vrf} neighbors'
#   * 'show bgp {address_family} vrf {vrf} neighbors {neighbor}'
#   * 'show ip bgp all neighbors',
#   * 'show ip bgp all neighbors {neighbor}'
#   * 'show ip bgp {address_family} all neighbors'
#   * 'show ip bgp {address_family} all neighbors {neighbor}'
#   * 'show ip bgp neighbors'
#   * 'show ip bgp neighbors {neighbor}'
#   * 'show ip bgp {address_family} neighbors'
#   * 'show ip bgp {address_family} neighbors {neighbor}'
#   * 'show ip bgp {address_family} vrf {vrf} neighbors'
#   * 'show ip bgp {address_family} vrf {vrf} neighbors {neighbor}'
# ==================================================================
class ShowBgpNeighborSuperParser(MetaParser):

    ''' Super parser for:
        * 'show bgp all neighbors'
        * 'show bgp all neighbors {neighbor}'
        * 'show bgp {address_family} all neighbors'
        * 'show bgp {address_family} all neighbors {neighbor}'
        * 'show bgp neighbors'
        * 'show bgp neighbors {neighbor}'
        * 'show bgp {address_family} neighbors'
        * 'show bgp {address_family} neighbors {neighbor}'
        * 'show bgp {address_family} vrf {vrf} neighbors'
        * 'show bgp {address_family} vrf {vrf} neighbors {neighbor}'
        * 'show ip bgp all neighbors',
        * 'show ip bgp all neighbors {neighbor}'
        * 'show ip bgp {address_family} all neighbors'
        * 'show ip bgp {address_family} all neighbors {neighbor}'
        * 'show ip bgp neighbors'
        * 'show ip bgp neighbors {neighbor}'
        * 'show ip bgp {address_family} neighbors'
        * 'show ip bgp {address_family} neighbors {neighbor}'
        * 'show ip bgp {address_family} vrf {vrf} neighbors'
        * 'show ip bgp {address_family} vrf {vrf} neighbors {neighbor}'
    '''

    def cli(self, neighbor='', address_family='', vrf='', output=None):

        # Init vars
        ret_dict = {}
        list_of_neighbors = []
        af_name = None ; af_dict = {} ; nbr_dict = {}
        message_statistics = False
        prefix_activity = True
        local_prefix = False
        refresh_activity = False

        # For address family: IPv4 Unicast
        # For address family: L2VPN E-VPN
        p1 = re.compile(r'^For +address +family: +(?P<af>[a-zA-Z0-9\-\s]+)$')

        # BGP neighbor is 10.16.2.2,  remote AS 100, internal link
        p2_1 = re.compile(r'^BGP +neighbor +is +(?P<neighbor>(\S+)), +remote +AS'
                         r' +(?P<remote_as>([\d\.]+)), +(?P<link>[a-zA-Z]+) +link$')

        # BGP neighbor is 10.66.6.6,  vrf VRF2,  remote AS 400, external link
        # BGP neighbor is 172.17.111.1,  vrf SH_BGP_VRF100,  remote AS 65000, external link
        p2_2 = re.compile(r'^BGP +neighbor +is +(?P<neighbor>(\S+)), +vrf'
                           r' +(?P<vrf>(\S+)), +remote +AS +(?P<remote_as>([\d\.]+)),'
                           r' +(?P<link>[a-zA-Z]+) +link$')

        # IOS output
        # BGP neighbor is 10.51.1.101,  remote AS 300,  local AS 101, external link
        # BGP neighbor is 10.51.1.101,  remote AS 300,  local AS 101 no-prepend replace-as, external link
        # BGP neighbor is 10.4.11.2, remote AS 101.101, external link
        # BGP neighbor is 10.10.11.1, vrf CustA-VPN1, remote AS 4200000001, local AS 4200000101 no-prepend replace-as, external link
        p2_3 = re.compile(r'^BGP +neighbor +is +(?P<neighbor>(\S+)),'
                           r'(?: +vrf +(?P<vrf>(\S+)),)?'
                           r' +remote +AS +(?P<remote_as>([\d\.]+)),'
                           r'( +local +AS +(?P<local_as>[\d\.]+))?(?P<no_prepend> no-prepend)?'
                           r'(?P<replace_as> replace-as)?,? +(?P<link>(\S+)) +link$')

        # Description: router22222222
        p3 = re.compile(r'^Description: +(?P<description>(\S+))$')

        # Administratively shut down
        p4 = re.compile(r'^Administratively shut down$')

        # BGP version 4, remote router ID 10.16.2.2
        p5 = re.compile(r'^BGP +version +(?P<bgp_version>(\d+)), +remote'
                         r' +router +ID +(?P<router_id>(\S+))$')

        # BGP state = Established, up for 01:10:35
        # BGP state = Idle, down for 01:10:35
        # BGP state = Idle
        # BGP state = Established, up for 1w2d
        # Session state = Closing
        p6 = re.compile(r'^(BGP|Session) +state += +(?P<session_state>(\S+))'
                         r'(?:, +(?P<state>(up|down)) +for +(?P<time>(\S+)))?$')

        # Last read 00:00:04, last write 00:00:09, hold time is 180, keepalive interval is 60 seconds
        p7_1 = re.compile(r'^Last +read +(?P<last_read>(\S+)), +last +write'
                           r' +(?P<last_write>(\S+)), +hold +time +is'
                           r' +(?P<hold_time>(\d+)), +keepalive +interval +is'
                           r' +(?P<keepalive>(\d+)) +seconds$')

        # Configured hold time is 90, keepalive interval is 30 seconds
        p7_2 = re.compile(r'^Configured +hold +time +is (?P<holdtime>(\d+)),'
                           r' +keepalive +interval +is +(?P<keepalive>(\d+))'
                           r' +seconds$')

        # Minimum holdtime from neighbor is 0 seconds
        p7_3 = re.compile(r'^Minimum +holdtime +from +neighbor +is'
                           r' +(?P<min_holdtime>(\d+)) +seconds$')

        # Neighbor sessions:
        p7_4 = re.compile(r'^Neighbor +sessions:+$')

        # Neighbor sessions:
        #  1 active, is not multisession capable (disabled)
        p8 = re.compile(r'^(?P<sessions>(\d+)) active,(?: +is +not +multisession'
                         r' +capable( +\(disabled\))?)?$')

        # Neighbor capabilities:
        p9 = re.compile(r'^Neighbor +capabilities:$')

        #  Route refresh: advertised and received(new)
        p10 = re.compile(r'^Route +refresh: +(?P<route_refresh>(.*))$')

        #  Four-octets ASN Capability: advertised and received
        p11 = re.compile(r'^Four-octets +ASN +Capability: +(?P<cap>(.*))$')

        # Address family VPNv4 Unicast: advertised and received
        # Address family VPNv6 Unicast: advertised and received
        # Address family link-state link-state: advertised
        p12 = re.compile(r'^Address +family +(?P<af_type>([a-zA-Z0-9\s\-]+)) *:'
                          r' +(?P<val>(.*))$')

        #  Graceful Restart Capability: received
        p13 = re.compile(r'^Graceful +Restart +Capability: +(?P<gr>(.*))$')

        #   Remote Restart timer is 120 seconds
        p14 = re.compile(r'^Remote +Restart +timer +is +(?P<timer>(\d+))'
                          r' +seconds$')

        #   Address families advertised by peer:
        #    VPNv4 Unicast (was not preserved, VPNv6 Unicast (was not preserved
        p15 = re.compile(r'^(?P<af_type1>([a-zA-Z0-9\s]+)) +\(was +not'
                          r' +preserved, +(?P<af_type2>([a-zA-Z0-9\s]+))'
                          r' +\(was +not +preserved$')

        # Address families advertised by peer before restart:
        #   IPv4 Unicast, VPNv4 Unicast, L2VPN Vpls

        #  Enhanced Refresh Capability: advertised
        p16 = re.compile(r'^Enhanced +Refresh +Capability: +(?P<erc>(.*))$')


        #  Multisession Capability:
        #  Multisession Capability: advertised
        p17 = re.compile(r'^Multisession +Capability: +(?P<multisession>(.*))$')

        #  Stateful switchover support enabled: NO for session 1
        p18 = re.compile(r'^Stateful +switchover +support +(?P<state>(\S+)):'
                         ' +(?P<value>(.*))$')

        # Message statistics:
        # Message statistics for 192.168.10.253 active:
        # Message statistics, state Established:
        p19 = re.compile(r'^Message +statistics(( +for +(?P<state>[\w. ]+))|'
                         r'(, +state +Established))?:$')

        #  InQ depth is 0
        #  OutQ depth is 0
        p20 = re.compile(r'^(?P<qtype>(InQ|OutQ)) +depth +is +(?P<val>(\d+))$')

        # Prefix activity:               ----       ----
        # Local Policy Denied Prefixes:    --------    -------
        # Refresh activity:          ----   ----
        p21 = re.compile(r'^(?P<table_type>(Prefix activity|'
                          r'Local Policy Denied Prefixes|Refresh activity)) *:'
                          r' +(.*)$')

        #  Opens:                  1          1
        #  Notifications:          0          0
        #  Updates:               11          6
        #  Keepalives:            75         74
        #  Route Refresh:          0          0
        #  Total:                 87         81
        #  Prefixes Current:     403        201 (Consumes 27336 bytes)
        #  Used as bestpath:     n/a          0
        #  Used as multipath:    n/a          0
        p22 = re.compile(r'^(?P<item>([a-zA-Z\s\-]+)):? +(?P<sent>(n/a|\d+))'
                         r' +(?P<recv>(n/a|\d+))(?:\s+\(Consumes +(?P<bytes>(\d+))'
                         r' +bytes\))?$')

        # Do log neighbor state changes (via global configuration)

        # Default minimum time between advertisement runs is 0 seconds
        p23 = re.compile(r'^Default +minimum +time +between +advertisement'
                          r' +runs +is +(?P<time>(\d+)) +seconds$')

        # Address tracking is enabled, the RIB does have a route to 10.16.2.2
        # Address tracking is enabled, the RIB does not have a route to 10.16.2.2
        p24 = re.compile(r'^Address +tracking +is +(?P<status>(\S+)), +the +RIB'
                          r' +does( +(?P<rip_has_route>(not)+))? +have +a +route +to +(?P<route>(\S+))$')

        # Connections established 1; dropped 0
        p25 = re.compile(r'^Connections +established +(?P<established>(\d+));'
                          r' +dropped +(?P<dropped>(\d+))$')

        # Last reset never
        # Last reset 01:05:09, due to Active open failed
        p26 = re.compile(r'^Last +reset +(?P<reset>(\S+))(?:, +due +to'
                          r' +(?P<reason>(.*)))?$')

        # Transport(tcp) path-mtu-discovery is enabled
        p27 = re.compile(r'^Transport\(tcp\) +path-mtu-discovery +is'
                          r' +(?P<status>(\S+))$')

        # Graceful-Restart is disabled
        # Graceful-Restart is enabled, restart-time 120 seconds, stalepath-time 360 seconds
        p28 = re.compile(r'^Graceful-Restart +is +(?P<gr>(enabled|disabled))'
                          r'(?:, +restart-time +(?P<restart>(\d+)) +seconds,'
                          r' +stalepath-time +(?P<stalepath>(\d+)) +seconds)?$')

        # Connection state is ESTAB, I/O status: 1, unread input bytes: 0
        p29 = re.compile(r'^Connection +state +is +(?P<state>(\S+)), +I/O'
                          r' +status: (?P<io>(\d+)), +unread +input +bytes:'
                          r' +(?P<bytes>(\d+))$')

        # Connection is ECN Disabled, Mininum incoming TTL 0, Outgoing TTL 255
        p30 = re.compile(r'^Connection +is +ECN +(?P<ecn_state>(\S+)),'
                          r' +Mininum +incoming +TTL +(?P<incoming_ttl>(\d+)),'
                          r' +Outgoing +TTL +(?P<outgoing_ttl>(\d+))$')

        # Local host: 10.64.4.4, Local port: 35281
        p31 = re.compile(r'^Local +host: +(?P<local_host>(\S+)), +Local +port:'
                          r' +(?P<local_port>(\d+))$')

        # Foreign host: 10.16.2.2, Foreign port: 179
        p32 = re.compile(r'^Foreign +host: +(?P<foreign_host>(\S+)), +Foreign'
                          r' +port: +(?P<foreign_port>(\d+))$')

        # Connection tableid (VRF): 0
        p33 = re.compile(r'^Connection +tableid +\(VRF\): +(?P<val>(\d+))$')

        # Maximum output segment queue size: 50
        p34 = re.compile(r'^Maximum +output +segment +queue +size:'
                          r' +(?P<size>(\d+))$')

        # Enqueued packets for retransmit: 0, input: 0  mis-ordered: 0 (0 bytes)
        p35 = re.compile(r'^Enqueued +packets +for +retransmit:'
                          r' +(?P<retransmit>(\d+)), +input: +(?P<input>(\d+))'
                          r' +mis-ordered: +(?P<misordered>(\d+))'
                          r' +\((?P<bytes>(\d+)) +bytes+\)$')

        # Event Timers (current time is 0x530449):
        p36 = re.compile(r'^Event +Timers +\(+current +time +is'
                          r' +(?P<time>(\S+))+\):$')

        # Timer          Starts    Wakeups            Next
        # Retrans            86          0             0x0
        # TimeWait            0          0             0x0
        # AckHold            80         72             0x0
        # SendWnd             0          0             0x0
        # KeepAlive           0          0             0x0
        # GiveUp              0          0             0x0
        # PmtuAger            1          1             0x0
        # DeadWait            0          0             0x0
        # Linger              0          0             0x0
        # ProcessQ            0          0             0x0
        p37 = re.compile(r'^(?P<item>(\S+)) +(?P<starts>(\d+))'
                          r' +(?P<wakeups>(\d+)) +(?P<next>0x[0-9a-f]+)$')

        # iss:   55023811  snduna:   55027115  sndnxt:   55027115
        p38 = re.compile(r'^iss: +(?P<iss>(\d+)) +snduna: +(?P<snduna>(\d+))'
                          r' +sndnxt: +(?P<sndnxt>(\d+))$')

        # irs:  109992783  rcvnxt:  109995158
        p39 = re.compile(r'^irs: +(?P<irs>(\d+)) +rcvnxt: +(?P<rcvnxt>(\d+))$')


        # sndwnd:  16616  scale:      0  maxrcvwnd:  16384
        p40 = re.compile(r'^sndwnd: +(?P<sndwnd>(\d+)) +scale: +(?P<scale>(\d+))'
                          r' +maxrcvwnd: +(?P<maxrcvwnd>(\d+))$')

        # rcvwnd:  16327  scale:      0  delrcvwnd:     57
        p41 = re.compile(r'^rcvwnd: +(?P<rcvwnd>(\d+)) +scale: +(?P<scale>(\d+))'
                          r' +delrcvwnd: +(?P<delrcvwnd>(\d+))$')

        # SRTT: 1000 ms, RTTO: 1003 ms, RTV: 3 ms, KRTT: 0 ms
        p42 = re.compile(r'^SRTT: +(?P<srtt>(\d+)) +ms, +RTTO: +(?P<rtto>(\d+))'
                          r' +ms, +RTV: +(?P<rtv>(\d+)) +ms, +KRTT:'
                          r' +(?P<krtt>(\d+)) +ms$')

        # minRTT: 4 ms, maxRTT: 1000 ms, ACK hold: 200 ms
        p43 = re.compile(r'^minRTT: +(?P<min_rtt>(\d+)) +ms, +maxRTT:'
                          r' +(?P<max_rtt>(\d+)) +ms, +ACK +hold:'
                          r' +(?P<ack_hold>(\d+)) +ms$')


        # uptime: 4236258 ms, Sent idletime: 4349 ms, Receive idletime: 4549 ms
        p44 = re.compile(r'^uptime: +(?P<uptime>(\d+)) +ms, +Sent +idletime:'
                          r' +(?P<sent>(\d+)) +ms, +Receive +idletime:'
                          r' +(?P<receive>(\d+)) +ms$')

        # Status Flags: active open
        p45 = re.compile(r'^Status +Flags: +(?P<flags>(.*))$')

        # Option Flags: nagle, path mtu capable
        p46 = re.compile(r'^Option +Flags: +(?P<flags>(.*))$')

        # IP Precedence value : 6
        p47 = re.compile(r'^IP +Precedence +value : +(?P<value>(\d+))$')

        # Datagrams (max data segment is 536 bytes):
        p48 = re.compile(r'^Datagrams +\(max +data +segment +is'
                          r' +(?P<bytes>(\d+)) +bytes\):$')

        # Rcvd: 164 (out of order: 0), with data: 80, total data bytes: 2374
        p49 = re.compile(r'^Rcvd: +(?P<received>(\d+)) +\(out +of +order:'
                          r' +(?P<out_of_order>(\d+))\), +with +data:'
                          r' (?P<with_data>(\d+)), +total +data +bytes:'
                          r' (?P<total_data>(\d+))$')

        # Sent: 166 (retransmit: 0, fastretransmit: 0, partialack: 0, Second Congestion: 0), with data: 87, total data bytes: 3303
        p50 = re.compile(r'^Sent: (?P<sent>(\d+)) +\(retransmit:'
                          r' +(?P<retransmit>(\d+)), +fastretransmit:'
                          r' +(?P<fastretransmit>(\d+)), +partialack:'
                          r' +(?P<partialack>(\d+)), +Second +Congestion:'
                          r' +(?P<second_congestion>(\d+))\), +with +data:'
                          r' (?P<sent_with_data>(\d+)), +total +data +bytes:'
                          r' +(?P<sent_total_data>(\d+))$')


        # Packets received in fast path: 0, fast processed: 0, slow path: 0
        p51 = re.compile(r'^Packets +received +in +fast +path: +(?P<rcv>(\d+)),'
                          r' +fast +processed: +(?P<processed>(\d+)),'
                          r' +slow +path: +(?P<path>(\d+))$')

        # fast lock acquisition failures: 0, slow path: 0
        p52 = re.compile(r'^fast +lock +acquisition +failures:'
                          r' +(?P<failures>(\d+)), +slow +path: +(?P<path>(\d+))$')


        # TCP Semaphore      0x1286E7EC  FREE
        p53 = re.compile(r'^TCP +Semaphore +(?P<semaphore>0x[0-9a-fA-F]+)'
                          r' +(?P<status>(\S+))$')

        # BGP table version 9431, neighbor version 9431/0
        p54 = re.compile(r'^BGP +table +version +(?P<bgp_table_version>(\d+)),'
                          r' +neighbor +version +(?P<nbr_version>(\S+))$')

        # Output queue size : 0
        p55 = re.compile(r'^Output +queue +size *: +(?P<size>(\d+))$')

        # Index 38, Advertise bit 1
        p56 = re.compile(r'^Index +(?P<index>(\d+)), +Advertise +bit'
                        r' +(?P<adv_bit>(\d+))$')

        # Route-Reflector Client
        p57 = re.compile(r'^Route-Reflector +Client$')

        # 38 update-group member
        p58 = re.compile(r'^(?P<num>(\d+)) +update-group +member$')

        # Community attribute sent to this neighbor
        p59 = re.compile(r'^Community +attribute +sent +to +this +neighbor$')

        # Extended-community attribute sent to this neighbor
        p60 = re.compile(r'^Extended-community +attribute +sent +to +this'
                        r' +neighbor$')

        # Suppress LDP signaling protocol
        p61 = re.compile(r'^Suppress +LDP +signaling +protocol$')

        # Slow-peer detection is disabled
        p62 = re.compile(r'^Slow-peer +detection +is'
                          r' +(?P<state>(enabled|disabled))$')

        # Slow-peer split-update-group dynamic is disabled
        p63 = re.compile(r'^Slow-peer +split-update-group +dynamic +is'
                          r' +(?P<state>(enabled|disabled))$')

        # Number of NLRIs in the update sent: max 199, min 0
        p64 = re.compile(r'^Number +of +NLRIs +in +the +update +sent: +max'
                        r' +(?P<max>(\d+)), +min +(?P<min>(\d+))$')

        # Last detected as dynamic slow peer: never
        p65 = re.compile(r'^Last +detected +as +dynamic +slow +peer:'
                          r' +(?P<val>(\S+))$')

        # Dynamic slow peer recovered: never
        p66 = re.compile(r'^Dynamic +slow +peer +recovered: +(?P<val>(\S+))$')

        # Refresh Epoch: 3
        p67 = re.compile(r'^Refresh +Epoch: +(?P<num>(\d+))$')

        # Last Sent Refresh Start-of-rib: 02:41:38
        # Last Received Refresh Start-of-rib: 02:01:36
        p68 = re.compile(r'^Last +(Sent|Received) +Refresh +Start-of-rib:'
                          r' +(?P<val>(\S+))$')

        # Last Sent Refresh End-of-rib: 02:41:38
        # Last Received Refresh End-of-rib: 02:01:32
        p69 = re.compile(r'^Last +(Sent|Received) +Refresh +End-of-rib:'
                          r' +(?P<val>(\S+))$')

        # Refresh-Out took 0 seconds
        # Refresh-In took 4 seconds
        p70 = re.compile(r'^Refresh-(?P<type>(In|Out)) +took +(?P<val>(\d+))'
                          r' +seconds$')

        # SSO is disabled
        p71 = re.compile(r'^SSO +is +(?P<state>(enabled|disabled))$')

        # No active TCP connection
        p72 = re.compile(r'^No +active +TCP +connection$')

        # Member of peer-group T2-ASN1.1 for session parameters
        p73 = re.compile(r'^Member +of +peer-group +(?P<peer_group>(.*)) +for +session +parameters$')

        for line in output.splitlines():

            line = line.strip()

            # For address family: IPv4 Unicast
            m = p1.match(line)
            if m:
                af_name = m.groupdict()['af'].lower().replace("-", "")
                # af_dict
                if nbr_dict:
                    af_dict = nbr_dict.setdefault('address_family', {}).\
                                       setdefault(af_name, {})
                continue

            # BGP neighbor is 10.16.2.2,  remote AS 100, internal link
            m = p2_1.match(line)
            if m:
                group = m.groupdict()
                neighbor = group['neighbor']
                vrf = 'default'

                # Add to neighbors list
                if neighbor not in list_of_neighbors:
                    list_of_neighbors.append(neighbor)
                ret_dict['list_of_neighbors'] = list_of_neighbors

                # nbr_dict
                nbr_dict = ret_dict.setdefault('vrf', {}).setdefault(vrf, {}).\
                           setdefault('neighbor', {}).setdefault(neighbor, {})

                # Set keys
                try:
                    nbr_dict['remote_as'] = int(group['remote_as'])
                except:
                    nbr_dict['remote_as'] = group['remote_as']
                nbr_dict['link'] = group['link']
                nbr_dict['shutdown'] = False

                # af_dict
                if af_name:
                    af_dict = nbr_dict.setdefault('address_family', {}).\
                                       setdefault(af_name, {})
                continue

            # BGP neighbor is 10.66.6.6,  vrf VRF2,  remote AS 400, external link
            # BGP neighbor is 172.17.111.1,  vrf SH_BGP_VRF100,  remote AS 65000, external link
            m = p2_2.match(line)
            if m:
                group = m.groupdict()
                neighbor = group['neighbor']
                vrf = group['vrf']

                # Add to neighbors list
                list_of_neighbors.append(neighbor)
                ret_dict['list_of_neighbors'] = list_of_neighbors

                # nbr_dict
                nbr_dict = ret_dict.setdefault('vrf', {}).setdefault(vrf, {}).\
                           setdefault('neighbor', {}).setdefault(neighbor, {})

                # Set keys
                try:
                    nbr_dict['remote_as'] = int(group['remote_as'])
                except:
                    nbr_dict['remote_as'] = group['remote_as']
                nbr_dict['link'] = group['link']
                nbr_dict['shutdown'] = False

                # af_dict
                if af_name:
                    af_dict = nbr_dict.setdefault('address_family', {}).\
                                       setdefault(af_name, {})
                continue

            # BGP neighbor is 10.51.1.101,  remote AS 300,  local AS 101, external link
            # BGP neighbor is 10.51.1.101,  remote AS 300,  local AS 101 no-prepend replace-as, external link
            # BGP neighbor is 10.4.11.2, remote AS 101.101, external link
            # BGP neighbor is 10.10.11.1, vrf CustA-VPN1, remote AS 4200000001, local AS 4200000101 no-prepend replace-as, external link
            m = p2_3.match(line)
            if m:
                group = m.groupdict()
                neighbor = group['neighbor']
                vrf = group['vrf']
                # if no vrf is configured - set vrf to 'default'
                if not vrf:
                    vrf = 'default'

                # Add to neighbors list
                list_of_neighbors.append(neighbor)
                ret_dict['list_of_neighbors'] = list_of_neighbors

                # nbr_dict
                nbr_dict = ret_dict.setdefault('vrf', {}).setdefault(vrf, {}).\
                           setdefault('neighbor', {}).setdefault(neighbor, {})

                # Set keys
                try:
                    nbr_dict['remote_as'] = int(group['remote_as'])
                except:
                    nbr_dict['remote_as'] = group['remote_as']
                nbr_dict['link'] = group['link']
                nbr_dict['shutdown'] = False
                if group['local_as']:
                    try:
                        nbr_dict['local_as'] = int(group['local_as'])
                    except:
                        nbr_dict['local_as'] = group['local_as']
                if group['replace_as']:
                    nbr_dict['replace_as'] = True
                else:
                    nbr_dict['replace_as'] = False
                if group['no_prepend']:
                    nbr_dict['no_prepend'] = True
                else:
                    nbr_dict['no_prepend'] = False

                # af_dict
                if af_name:
                    af_dict = nbr_dict.setdefault('address_family', {}).\
                                       setdefault(af_name, {})
                continue

            # Description: router22222222
            m = p3.match(line)
            if m:
                nbr_dict['description'] = m.groupdict()['description']
                continue

            # Administratively shut down
            m = p4.match(line)
            if m:
                nbr_dict['shutdown'] = True
                continue

            # BGP version 4, remote router ID 10.16.2.2
            m = p5.match(line)
            if m:
                group = m.groupdict()
                nbr_dict['bgp_version'] = int(group['bgp_version'])
                nbr_dict['router_id'] = group['router_id']
                continue

            # BGP state = Established, up for 01:10:35
            # BGP state = Idle, down for 01:10:35
            # BGP state = Idle
            # BGP state = Established, up for 1w2d
            m = p6.match(line)
            if m:
                group = m.groupdict()
                nbr_dict['session_state'] = group['session_state']
                if af_name:
                    af_dict['session_state'] = group['session_state']
                    if group['state']:
                        if 'down' in group['state']:
                            af_dict['down_time'] = group['time']
                        elif 'up' in group['state']:
                            af_dict['up_time'] = group['time']
                continue

            # Last read 00:00:04, last write 00:00:09, hold time is 180, keepalive interval is 60 seconds
            m = p7_1.match(line)
            if m:
                group = m.groupdict()
                timers_dict = nbr_dict.\
                                setdefault('bgp_negotiated_keepalive_timers', {})
                timers_dict['hold_time'] = int(group['hold_time'])
                timers_dict['keepalive_interval'] = int(group['keepalive'])
                if af_name:
                    af_dict['last_read'] = group['last_read']
                    af_dict['last_write'] = group['last_write']
                continue

            # Configured hold time is 90, keepalive interval is 30 seconds
            m = p7_2.match(line)
            if m:
                group = m.groupdict()
                timers_dict = nbr_dict.\
                                setdefault('bgp_negotiated_keepalive_timers', {})
                timers_dict['hold_time'] = int(group['holdtime'])
                timers_dict['keepalive_interval'] = int(group['keepalive'])
                continue

            # Minimum holdtime from neighbor is 0 seconds
            m = p7_3.match(line)
            if m:
                timers_dict['min_holdtime'] = int(m.groupdict()['min_holdtime'])
                continue

            # Neighbor sessions:
            m = p7_4.match(line)
            if m:
                neighbor_type = 'neighbor_session'
                nbr_session_dict = nbr_dict.\
                                setdefault('bgp_neighbor_session', {})
                continue

            #  1 active, is not multisession capable (disabled)
            m = p8.match(line)
            if m:
                neighbor_active_sessions = int(m.groupdict()['sessions'])
                if neighbor_type == 'neighbor_session':
                    nbr_session_dict.update({'sessions': neighbor_active_sessions})
                continue


            # Neighbor capabilities:
            m = p9.match(line)
            if m:
                neighbor_type = 'neighbor_capabilities'
                nbr_cap_dict = nbr_dict.\
                                setdefault('bgp_negotiated_capabilities', {})
                continue

            #  Route refresh: advertised and received(new)
            m = p10.match(line)
            if m:
                nbr_cap_dict['route_refresh'] = m.groupdict()['route_refresh']
                continue

            #  Four-octets ASN Capability: advertised and received
            m = p11.match(line)
            if m:
                nbr_cap_dict['four_octets_asn'] = m.groupdict()['cap']
                continue

            # Address family VPNv4 Unicast: advertised and received
            # Address family VPNv6 Unicast: advertised and received
            # Address family IPv4 Unicast: advertised and received
            # Address family IPv6 Unicast: advertised and received
            # Address family link-state link-state: advertised
            m = p12.match(line)
            if m:
                group = m.groupdict()
                af_type = group['af_type'].lower().replace(" ", "_")
                nbr_cap_dict[af_type] = group['val']
                continue

            #  Graceful Restart Capability: received
            m = p13.match(line)
            if m:
                nbr_cap_dict['graceful_restart'] = m.groupdict()['gr']
                continue

            #   Remote Restart timer is 120 seconds
            m = p14.match(line)
            if m:
                nbr_cap_dict['remote_restart_timer'] = int(m.groupdict()['timer'])
                continue

            #   Address families advertised by peer:
            #    VPNv4 Unicast (was not preserved, VPNv6 Unicast (was not preserved
            m = p15.match(line)
            if m:
                af_list = []
                group = m.groupdict()
                af_list.append(group['af_type1'].lower())
                af_list.append(group['af_type2'].lower())
                nbr_cap_dict['graceful_restart_af_advertised_by_peer'] = af_list
                continue

            #  Enhanced Refresh Capability: advertised
            m = p16.match(line)
            if m:
                nbr_cap_dict['enhanced_refresh'] = m.groupdict()['erc']
                continue

            #  Multisession Capability:
            #  Multisession Capability: advertised
            m = p17.match(line)
            if m:
                nbr_cap_dict['multisession'] = m.groupdict()['multisession']
                continue

            # Stateful switchover support enabled: NO for session 1
            m = p18.match(line)
            if m:
                if neighbor_type == 'neighbor_session':
                    nbr_session_dict['stateful_switchover'] = m.groupdict()['value']
                else:
                    nbr_cap_dict['stateful_switchover'] = m.groupdict()['value']
                continue

            # Message statistics:
            # Message statistics for 192.168.10.253 active:
            # Message statistics, state Established:
            m = p19.match(line)
            if m:
                message_statistics = True
                prefix_activity = False
                local_prefix = False
                refresh_activity = False
                state = m.groupdict()['state']
                if state:
                    nbr_counters_dict = nbr_dict.\
                                        setdefault('bgp_neighbor_counters', {}).\
                                        setdefault('multisession_messages', {}).\
                                        setdefault(state, {})
                else:
                    nbr_counters_dict = nbr_dict.\
                                        setdefault('bgp_neighbor_counters', {}).\
                                        setdefault('messages', {})
                nbr_counters_sent_dict = nbr_counters_dict.\
                                                    setdefault('sent', {})
                nbr_counters_recv_dict = nbr_counters_dict.\
                                                    setdefault('received', {})
                continue

            #  InQ depth is 0
            #  OutQ depth is 0
            m = p20.match(line)
            if m:
                group = m.groupdict()
                key = '{}_depth'.format(group['qtype'].lower().\
                                        replace("q", "_queue"))
                nbr_counters_dict[key] = int(group['val'])
                continue

            # Prefix activity:               ----       ----
            # Local Policy Denied Prefixes:    --------    -------
            # Refresh activity:          ----   ----
            m = p21.match(line)
            if m:
                table_type = m.groupdict()['table_type'].lower()
                if table_type == 'prefix activity':
                    message_statistics = False
                    prefix_activity = True
                    local_prefix = False
                    refresh_activity = False
                    pfx_act_dict = af_dict.\
                                    setdefault('prefix_activity_counters', {})
                    pfx_act_sent_dict = pfx_act_dict.setdefault('sent', {})
                    pfx_act_recv_dict = pfx_act_dict.setdefault('received', {})
                elif table_type == 'local policy denied prefixes':
                    message_statistics = False
                    prefix_activity = False
                    local_prefix = True
                    refresh_activity = False
                    local_pfx_dict = af_dict.setdefault(
                                    'local_policy_denied_prefixes_counters', {})
                    local_pfx_sent_dict = local_pfx_dict.setdefault('outbound', {})
                    local_pfx_recv_dict = local_pfx_dict.\
                                                    setdefault('inbound', {})
                elif table_type == 'refresh activity':
                    message_statistics = False
                    prefix_activity = False
                    local_prefix = False
                    refresh_activity = True
                    refresh_act_dict = af_dict.\
                                    setdefault('refresh_activity_counters', {})
                    refresh_act_sent_dict = refresh_act_dict.setdefault('sent', {})
                    refresh_act_recv_dict = refresh_act_dict.\
                                                    setdefault('received', {})
                continue

            #  Opens:                  1          1
            #  Notifications:          0          0
            #  Updates:               11          6
            #  Keepalives:            75         74
            #  Route Refresh:          0          0
            #  Total:                 87         81
            #  Prefixes Current:     403        201 (Consumes 27336 bytes)
            m = p22.match(line)
            if m:
                group = m.groupdict()
                item = group['item'].strip().lower().replace(" ", "_").\
                                                     replace("-", "_")
                if message_statistics:
                    sdict = nbr_counters_sent_dict
                    rdict = nbr_counters_recv_dict
                elif prefix_activity:
                    sdict = pfx_act_sent_dict
                    rdict = pfx_act_recv_dict
                elif local_prefix:
                    sdict = local_pfx_sent_dict
                    rdict = local_pfx_recv_dict
                elif refresh_activity:
                    sdict = refresh_act_sent_dict
                    rdict = refresh_act_recv_dict
                else:
                    continue
                try:
                    sdict[item] = int(group['sent'])
                except:
                    sdict[item] = group['sent']
                try:
                    rdict[item] = int(group['recv'])
                except:
                    rdict[item] = group['recv']
                continue

            # Default minimum time between advertisement runs is 0 seconds
            m = p23.match(line)
            if m:
                session_transport_dict = nbr_dict.\
                                        setdefault('bgp_session_transport', {})
                session_transport_dict['min_time_between_advertisement_runs'] =\
                        int(m.groupdict()['time'])
                continue

            # Address tracking is enabled, the RIB does have a route to 10.16.2.2
            # Address tracking is enabled, the RIB does not have a route to 10.16.2.2
            m = p24.match(line)
            if m:
                group = m.groupdict()
                session_transport_dict['address_tracking_status'] = group['status']
                if not group['rip_has_route']:
                    session_transport_dict['rib_route_ip'] = group['route']
                continue

            # Connections established 1; dropped 0
            m = p25.match(line)
            if m:
                group = m.groupdict()
                conn_dict = session_transport_dict.setdefault('connection', {})
                conn_dict['established'] = int(group['established'])
                conn_dict['dropped'] = int(group['dropped'])
                continue

            # Last reset never
            m = p26.match(line)
            if m:
                group = m.groupdict()
                conn_dict['last_reset'] = group['reset']
                if group['reason']:
                    conn_dict['reset_reason'] = group['reason']
                continue

            # Transport(tcp) path-mtu-discovery is enabled
            m = p27.match(line)
            if m:
                session_transport_dict['tcp_path_mtu_discovery'] = \
                                                        m.groupdict()['status']
                continue

            # Graceful-Restart is disabled
            # Graceful-Restart is enabled, restart-time 120 seconds, stalepath-time 360 seconds
            m = p28.match(line)
            if m:
                group = m.groupdict()
                session_transport_dict['graceful_restart'] = group['gr']
                if group['restart']:
                    session_transport_dict['gr_restart_time'] = \
                                                        int(group['restart'])
                if group['stalepath']:
                    session_transport_dict['gr_stalepath_time'] = \
                                                        int(group['stalepath'])
                continue

            # Connection state is ESTAB, I/O status: 1, unread input bytes: 0
            m = p29.match(line)
            if m:
                group = m.groupdict()
                session_transport_dict['connection_state'] = \
                                                        group['state'].lower()
                session_transport_dict['io_status'] = int(group['io'])
                session_transport_dict['unread_input_bytes'] = int(group['bytes'])
                continue

            # Connection is ECN Disabled, Mininum incoming TTL 0, Outgoing TTL 255
            m = p30.match(line)
            if m:
                group = m.groupdict()
                session_transport_dict['ecn_connection'] = \
                                                    group['ecn_state'].lower()
                session_transport_dict['minimum_incoming_ttl'] = \
                                                    int(group['incoming_ttl'])
                session_transport_dict['outgoing_ttl'] = \
                                                    int(group['outgoing_ttl'])
                continue

            # Local host: 10.64.4.4, Local port: 35281
            m = p31.match(line)
            if m:
                group = m.groupdict()
                transport_dict = session_transport_dict.\
                                                    setdefault('transport', {})
                transport_dict['local_host'] = group['local_host']
                transport_dict['local_port'] = group['local_port']
                continue

            # Foreign host: 10.16.2.2, Foreign port: 179
            m = p32.match(line)
            if m:
                group = m.groupdict()
                transport_dict['foreign_host'] = group['foreign_host']
                transport_dict['foreign_port'] = group['foreign_port']
                continue

            # Connection tableid (VRF): 0
            m = p33.match(line)
            if m:
                session_transport_dict['connection_tableid'] = \
                                                    int(m.groupdict()['val'])
                continue

            # Maximum output segment queue size: 50
            m = p34.match(line)
            if m:
                session_transport_dict['maximum_output_segment_queue_size'] = \
                                                    int(m.groupdict()['size'])
                continue

            # Enqueued packets for retransmit: 0, input: 0  mis-ordered: 0 (0 bytes)
            m = p35.match(line)
            if m:
                group = m.groupdict()
                enq_dict = session_transport_dict.setdefault('enqueued_packets', {})
                enq_dict['retransmit_packet'] = int(group['retransmit'])
                enq_dict['input_packet'] = int(group['input'])
                enq_dict['mis_ordered_packet'] = int(group['misordered'])
                continue

            # Event Timers (current time is 0x530449):
            m = p36.match(line)
            if m:
                af_dict['current_time'] = m.groupdict()['time']
                event_timers_dict = nbr_dict.setdefault('bgp_event_timer', {})
                starts_dict = event_timers_dict.setdefault('starts', {})
                wakeups_dict = event_timers_dict.setdefault('wakeups', {})
                next_dict = event_timers_dict.setdefault('next', {})
                continue

            # Timer          Starts    Wakeups            Next
            # Retrans            86          0             0x0
            # TimeWait            0          0             0x0
            # AckHold            80         72             0x0
            # SendWnd             0          0             0x0
            # KeepAlive           0          0             0x0
            # GiveUp              0          0             0x0
            # PmtuAger            1          1             0x0
            # DeadWait            0          0             0x0
            # Linger              0          0             0x0
            # ProcessQ            0          0             0x0
            m = p37.match(line)
            if m:
                group = m.groupdict()
                item = group['item'].lower()
                starts_dict[item] = int(group['starts'])
                wakeups_dict[item] = int(group['wakeups'])
                next_dict[item] = group['next']
                continue

            # iss:   55023811  snduna:   55027115  sndnxt:   55027115
            m = p38.match(line)
            if m:
                group = m.groupdict()
                session_transport_dict['iss'] = int(group['iss'])
                session_transport_dict['snduna'] = int(group['snduna'])
                session_transport_dict['sndnxt'] = int(group['sndnxt'])
                continue

            # irs:  109992783  rcvnxt:  109995158
            m = p39.match(line)
            if m:
                group = m.groupdict()
                session_transport_dict['irs'] = int(group['irs'])
                session_transport_dict['rcvnxt'] = int(group['rcvnxt'])
                continue

            # sndwnd:  16616  scale:      0  maxrcvwnd:  16384
            m = p40.match(line)
            if m:
                group = m.groupdict()
                session_transport_dict['sndwnd'] = int(group['sndwnd'])
                session_transport_dict['snd_scale'] = int(group['scale'])
                session_transport_dict['maxrcvwnd'] = int(group['maxrcvwnd'])
                continue

            # rcvwnd:  16327  scale:      0  delrcvwnd:     57
            m = p41.match(line)
            if m:
                group = m.groupdict()
                session_transport_dict['rcvwnd'] = int(group['rcvwnd'])
                session_transport_dict['rcv_scale'] = int(group['scale'])
                session_transport_dict['delrcvwnd'] = int(group['delrcvwnd'])
                continue

            # SRTT: 1000 ms, RTTO: 1003 ms, RTV: 3 ms, KRTT: 0 ms
            m = p42.match(line)
            if m:
                group = m.groupdict()
                session_transport_dict['srtt'] = int(group['srtt'])
                session_transport_dict['rtto'] = int(group['rtto'])
                session_transport_dict['rtv'] = int(group['rtv'])
                session_transport_dict['krtt'] = int(group['krtt'])
                continue

            # minRTT: 4 ms, maxRTT: 1000 ms, ACK hold: 200 ms
            m = p43.match(line)
            if m:
                group = m.groupdict()
                session_transport_dict['min_rtt'] = int(group['min_rtt'])
                session_transport_dict['max_rtt'] = int(group['max_rtt'])
                session_transport_dict['ack_hold'] = int(group['ack_hold'])
                continue

            # uptime: 4236258 ms, Sent idletime: 4349 ms, Receive idletime: 4549 ms
            m = p44.match(line)
            if m:
                group = m.groupdict()
                session_transport_dict['uptime'] = int(group['uptime'])
                session_transport_dict['sent_idletime'] = int(group['sent'])
                session_transport_dict['receive_idletime'] = int(group['receive'])
                continue

            # Status Flags: active open
            m = p45.match(line)
            if m:
                session_transport_dict['status_flags'] = m.groupdict()['flags']
                continue

            # Option Flags: nagle, path mtu capable
            m = p46.match(line)
            if m:
                session_transport_dict['option_flags'] = m.groupdict()['flags']
                continue

            # IP Precedence value : 6
            m = p47.match(line)
            if m:
                session_transport_dict['ip_precedence_value'] = \
                                                    int(m.groupdict()['value'])
                continue

            # Datagrams (max data segment is 536 bytes):
            m = p48.match(line)
            if m:
                session_transport_dict['transport']['mss'] = \
                                                    int(m.groupdict()['bytes'])
                datagram_dict = session_transport_dict.setdefault('datagram', {})
                continue

            # Rcvd: 164 (out of order: 0), with data: 80, total data bytes: 2374
            m = p49.match(line)
            if m:
                group = m.groupdict()
                datagram_rcv_dict = datagram_dict.\
                                            setdefault('datagram_received', {})
                datagram_rcv_dict['value'] = int(group['received'])
                datagram_rcv_dict['out_of_order'] = int(group['out_of_order'])
                datagram_rcv_dict['with_data'] = int(group['with_data'])
                datagram_rcv_dict['total_data'] = int(group['total_data'])
                continue

            # Sent: 166 (retransmit: 0, fastretransmit: 0, partialack: 0, Second Congestion: 0),
            #       with data: 87, total data bytes: 3303
            m = p50.match(line)
            if m:
                group = m.groupdict()
                datagram_sent_dict = datagram_dict.\
                                            setdefault('datagram_sent', {})
                datagram_sent_dict['value'] = int(group['sent'])
                datagram_sent_dict['retransmit'] = int(group['retransmit'])
                datagram_sent_dict['fastretransmit'] = int(group['fastretransmit'])
                datagram_sent_dict['partialack'] = int(group['partialack'])
                datagram_sent_dict['second_congestion'] = int(group['second_congestion'])
                datagram_sent_dict['with_data'] = int(group['sent_with_data'])
                datagram_sent_dict['total_data'] = int(group['sent_total_data'])
                continue

            # Packets received in fast path: 0, fast processed: 0, slow path: 0
            m = p51.match(line)
            if m:
                group = m.groupdict()
                session_transport_dict['packet_fast_path'] = int(group['rcv'])
                session_transport_dict['packet_fast_processed'] = \
                                                        int(group['processed'])
                session_transport_dict['packet_slow_path'] = int(group['path'])
                continue

            # fast lock acquisition failures: 0, slow path: 0
            m = p52.match(line)
            if m:
                group = m.groupdict()
                session_transport_dict['fast_lock_acquisition_failures'] = \
                                                        int(group['failures'])
                session_transport_dict['lock_slow_path'] = int(group['path'])
                continue

            # TCP Semaphore      0x1286E7EC  FREE
            m = p53.match(line)
            if m:
                group = m.groupdict()
                session_transport_dict['tcp_semaphore'] = group['semaphore']
                session_transport_dict['tcp_semaphore_status'] = group['status']
                continue

            # Session: 192.168.197.254
            # BGP table version 9431, neighbor version 9431/0
            m = p54.match(line)
            if m:
                group = m.groupdict()
                af_dict['bgp_table_version'] = int(group['bgp_table_version'])
                af_dict['neighbor_version'] = group['nbr_version']
                continue

            # Output queue size : 0
            m = p55.match(line)
            if m:
                af_dict['output_queue_size'] = int(m.groupdict()['size'])
                continue

            # Index 38, Advertise bit 1
            m = p56.match(line)
            if m:
                group = m.groupdict()
                af_dict['index'] = int(group['index'])
                af_dict['advertise_bit'] = int(group['adv_bit'])
                continue

            # Route-Reflector Client
            m = p57.match(line)
            if m:
                af_dict['route_reflector_client'] = True
                continue

            # 38 update-group member
            m = p58.match(line)
            if m:
                af_dict['update_group_member'] = int(m.groupdict()['num'])
                continue

            # Community attribute sent to this neighbor
            m = p59.match(line)
            if m:
                af_dict['community_attribute_sent'] = True
                continue

            # Extended-community attribute sent to this neighbor
            m = p60.match(line)
            if m:
                af_dict['extended_community_attribute_sent'] = True
                continue

            # Suppress LDP signaling protocol
            m = p61.match(line)
            if m:
                af_dict['suppress_ldp_signaling'] = True
                continue

            # Slow-peer detection is disabled
            m = p62.match(line)
            if m:
                if m.groupdict()['state'] == 'disabled':
                    af_dict['slow_peer_detection'] = False
                else:
                    af_dict['slow_peer_detection'] = True
                continue

            # Slow-peer split-update-group dynamic is disabled
            m = p63.match(line)
            if m:
                if m.groupdict()['state'] == 'disabled':
                    af_dict['slow_peer_split_update_group_dynamic'] = False
                else:
                    af_dict['slow_peer_split_update_group_dynamic'] = True
                continue

            # Number of NLRIs in the update sent: max 199, min 0
            m = p64.match(line)
            if m:
                group = m.groupdict()
                af_dict['max_nlri'] = int(group['max'])
                af_dict['min_nlri'] = int(group['min'])
                continue

            # Last detected as dynamic slow peer: never
            m = p65.match(line)
            if m:
                af_dict['last_detected_dynamic_slow_peer'] = m.groupdict()['val']
                continue

            # Dynamic slow peer recovered: never
            m = p66.match(line)
            if m:
                af_dict['dynamic_slow_peer_recovered'] = m.groupdict()['val']
                continue

            # Refresh Epoch: 3
            m = p67.match(line)
            if m:
                af_dict['refresh_epoch'] = int(m.groupdict()['num'])
                continue

            # Last Sent Refresh Start-of-rib: 02:41:38
            # Last Received Refresh Start-of-rib: 02:01:36
            m = p68.match(line)
            if m:
                if 'Sent' in line:
                    af_dict['last_sent_refresh_start_of_rib'] = \
                                                            m.groupdict()['val']
                else:
                    af_dict['last_received_refresh_start_of_rib'] = \
                                                            m.groupdict()['val']
                continue

            # Last Sent Refresh End-of-rib: 02:41:38
            # Last Received Refresh End-of-rib: 02:01:32
            m = p69.match(line)
            if m:
                if 'Sent' in line:
                    af_dict['last_sent_refresh_end_of_rib'] = \
                                                            m.groupdict()['val']
                else:
                    af_dict['last_received_refresh_end_of_rib'] = \
                                                            m.groupdict()['val']
                continue

            # Refresh-Out took 0 seconds
            # Refresh-In took 4 seconds
            m = p70.match(line)
            if m:
                if m.groupdict()['type'] == 'Out':
                    af_dict['refresh_out'] = int(m.groupdict()['val'])
                else:
                    af_dict['refresh_in'] = int(m.groupdict()['val'])
                continue

            # SSO is disabled
            m = p71.match(line)
            if m:
                if m.groupdict()['state'] == 'disabled':
                    session_transport_dict['sso'] = False
                else:
                    session_transport_dict['sso'] = True
                continue

            # No active TCP connection
            m = p72.match(line)
            if m:
                session_transport_dict['tcp_connection'] = False
                continue

            # Member of peer-group T2-ASN1.1 for session parameters
            m = p73.match(line)
            if m:
                nbr_dict['peer_group'] = m.groupdict()['peer_group']
                continue

        return ret_dict


# =========================================================
# Parser for:
#   * 'show bgp all neighbors'
#   * 'show bgp all neighbors {neighbor}'
#   * 'show bgp {address_family} all neighbors'
#   * 'show bgp {address_family} all neighbors {neighbor}'
# =========================================================
class ShowBgpAllNeighbors(ShowBgpNeighborSuperParser, ShowBgpAllNeighborsSchema):

    ''' Parser for:
        * 'show bgp all neighbors'
        * 'show bgp all neighbors {neighbor}'
        * 'show bgp {address_family} all neighbors'
        * 'show bgp {address_family} all neighbors {neighbor}'
    '''

    cli_command = ['show bgp all neighbors',
                   'show bgp all neighbors {neighbor}',
                   'show bgp {address_family} all neighbors',
                   'show bgp {address_family} all neighbors {neighbor}',
                   ]
    exclude = ['current_time', 'last_read', 'last_write', 'retrans', 'keepalives',
        'total', 'value', 'retransmit', 'total_data', 'with_data', 'krtt', 'receive_idletime',
        'sent_idletime', 'sndnxt', 'snduna', 'sndwnd', 'uptime', 'ackhold', 'delrcvwnd', 'rcvnxt',
        'receive_idletime', 'rcvwnd', 'updates', 'down_time', 'last_reset', 'notifications',
        'opens', 'route_refresh', 'total', 'updates', 'up_time', 'rtto', 'rtv', 'srtt',
        'pmtuager', 'min_rtt', 'irs', 'iss', 'tcp_semaphore', 'foreign_port', 'local_port',
        'reset_reason', 'status_flags', 'dropped', 'established', 'out_of_order',
        'keepalive', 'retransmit_packet', 'max_rtt', 'mss', 'rcv_scale', 'ack_hold', 'fastretransmit']


    def cli(self, neighbor='', address_family='', output=None):

        # Restricted address families
        restricted_list = ['ipv4 unicast', 'ipv6 unicast','l2vpn evpn']

        # Init vars
        ret_dict = {}

        if output is None:
            # Select the command
            if address_family and neighbor:
                if address_family not in restricted_list:
                    cmd = self.cli_command[3].format(address_family=address_family,
                                                     neighbor=neighbor)
                else:
                    return ret_dict
            elif address_family:
                if address_family not in restricted_list:
                    cmd = self.cli_command[2].format(address_family=address_family)
                else:
                    return ret_dict
            elif neighbor:
                cmd = self.cli_command[1].format(neighbor=neighbor)
            else:
                cmd = self.cli_command[0]
            # Execute command
            show_output = self.device.execute(cmd)
        else:
            show_output = output

        # Call super
        return super().cli(output=show_output, neighbor=neighbor,
                           address_family=address_family)


# ===============================================================
# Parser for:
#   * 'show bgp neighbors'
#   * 'show bgp neighbors {neighbor}'
#   * 'show bgp {address_family} neighbors'
#   * 'show bgp {address_family} neighbors {neighbor}'
#   * 'show bgp {address_family} vrf {vrf} neighbors'
#   * 'show bgp {address_family} vrf {vrf} neighbors {neighbor}'
# ===============================================================
class ShowBgpNeighbors(ShowBgpNeighborSuperParser, ShowBgpAllNeighborsSchema):

    ''' Parser for:
        * 'show bgp neighbors'
        * 'show bgp neighbors {neighbor}'
        * 'show bgp {address_family} neighbors'
        * 'show bgp {address_family} neighbors {neighbor}'
        * 'show bgp {address_family} vrf {vrf} neighbors'
        * 'show bgp {address_family} vrf {vrf} neighbors {neighbor}'
    '''

    cli_command = ['show bgp {address_family} vrf {vrf} neighbors {neighbor}',
                   'show bgp {address_family} vrf {vrf} neighbors',
                   'show bgp {address_family} neighbors {neighbor}',
                   'show bgp {address_family} neighbors',
                   'show bgp neighbors {neighbor}',
                   'show bgp neighbors',
                   ]

    exclude = ['current_time','last_read', 'last_write', 'up_time', 'ackhold', 'retrans',
                'keepalives', 'total', 'total_data', 'value', 'with_data', 'delrcvwnd', 'rcvnxt',
                'rcvwnd', 'receive_idletime' , 'sent_idletime', 'sndnxt' , 'snduna', 'uptime']
    def cli(self, neighbor='', address_family='', vrf='', output=None):

        # Restricted address families
        restricted_list = ['ipv4 unicast', 'ipv6 unicast']

        # Init vars
        ret_dict = {}

        if output is None:
            # Select the command
            if address_family and vrf and neighbor:
                if address_family not in restricted_list:
                    cmd = self.cli_command[0].\
                                        format(address_family=address_family,
                                               vrf=vrf, neighbor=neighbor)
                else:
                    return ret_dict
            elif address_family and vrf:
                if address_family not in restricted_list:
                    cmd = self.cli_command[1].\
                                        format(address_family=address_family,
                                               vrf=vrf)
                else:
                    return ret_dict
            elif address_family and neighbor:
                if address_family in restricted_list:
                    cmd = self.cli_command[2].format(address_family=address_family,
                                                     neighbor=neighbor)
                else:
                    return ret_dict
            elif address_family:
                if address_family in restricted_list:
                    cmd = self.cli_command[3].format(address_family=address_family)
                else:
                    return ret_dict
            elif neighbor:
                cmd = self.cli_command[4].format(neighbor=neighbor)
            else:
                cmd = self.cli_command[5]
            # Execute command
            show_output = self.device.execute(cmd)
        else:
            show_output = output

        # Call super
        return super().cli(output=show_output, neighbor=neighbor, vrf=vrf,
                           address_family=address_family)




# ==============================================================================
# Schema for:
#   * 'show bgp all neighbors {neighbor} advertised-routes'
#   * 'show bgp {address_family} all neighbors {neighbor} advertised-routes'
#   * 'show bgp neighbors {neighbor} advertised-routes'
#   * 'show bgp {address_family} neighbors {neighbor} advertised-routes'
#   * 'show ip bgp all neighbors {neighbor} advertised-routes'
#   * 'show ip bgp {address_family} all neighbors {neighbor} advertised-routes'
#   * 'show ip bgp neighbors {neighbor} advertised-routes'
#   * 'show ip bgp {address_family} neighbors {neighbor} advertised-routes'
# ==============================================================================
class ShowBgpNeighborsAdvertisedRoutesSchema(MetaParser):

    ''' Schema for:
        * 'show bgp all neighbors {neighbor} advertised-routes'
        * 'show bgp {address_family} all neighbors {neighbor} advertised-routes'
        * 'show bgp neighbors {neighbor} advertised-routes'
        * 'show bgp {address_family} neighbors {neighbor} advertised-routes'
        * 'show ip bgp all neighbors {neighbor} advertised-routes'
        * 'show ip bgp {address_family} all neighbors {neighbor} advertised-routes'
        * 'show ip bgp neighbors {neighbor} advertised-routes'
        * 'show ip bgp {address_family} neighbors {neighbor} advertised-routes'
    '''

    schema = {
        'vrf':
            {Any():
                {'neighbor':
                    {Any():
                        {'address_family':
                            {Any():
                                {Optional('bgp_table_version'): int,
                                Optional('local_router_id'): str,
                                Optional('route_distinguisher'): str,
                                Optional('default_vrf'): str,
                                Optional('advertised'):
                                    {Optional(Any()):
                                        {Optional('index'):
                                            {Optional(Any()):
                                                {Optional('next_hop'): str,
                                                Optional('status_codes'): str,
                                                Optional('path_type'): str,
                                                Optional('metric'): int,
                                                Optional('localprf'): int,
                                                Optional('weight'): int,
                                                Optional('path'): str,
                                                Optional('origin_codes'): str,
                                                },
                                            },
                                        },
                                    },
                                },
                            },
                        },
                    },
                },
            },
        }


# ==============================================================================
# Super Parser for:
#   * 'show bgp all neighbors {neighbor} advertised-routes'
#   * 'show bgp {address_family} all neighbors {neighbor} advertised-routes'
#   * 'show bgp neighbors {neighbor} advertised-routes'
#   * 'show bgp {address_family} neighbors {neighbor} advertised-routes'
#   * 'show ip bgp all neighbors {neighbor} advertised-routes'
#   * 'show ip bgp {address_family} all neighbors {neighbor} advertised-routes'
#   * 'show ip bgp neighbors {neighbor} advertised-routes'
#   * 'show ip bgp {address_family} neighbors {neighbor} advertised-routes'
#   * 'show ip bgp {address_family} rd {rd} neighbors {neighbor} advertised-routes'
#   * 'show ip bgp {address_family} vrf {vrf} neighbors {neighbor} advertised-routes'
# ==============================================================================
class ShowBgpNeighborsAdvertisedRoutesSuperParser(ShowBgpNeighborsAdvertisedRoutesSchema):

    ''' Parser for:
        * 'show bgp all neighbors {neighbor} advertised-routes'
        * 'show bgp {address_family} all neighbors {neighbor} advertised-routes'
        * 'show bgp neighbors {neighbor} advertised-routes'
        * 'show bgp {address_family} neighbors {neighbor} advertised-routes'
        * 'show ip bgp all neighbors {neighbor} advertised-routes'
        * 'show ip bgp {address_family} all neighbors {neighbor} advertised-routes'
        * 'show ip bgp neighbors {neighbor} advertised-routes'
        * 'show ip bgp {address_family} neighbors {neighbor} advertised-routes'
        * 'show ip bgp {address_family} rd {rd} neighbors {neighbor} advertised-routes'
        * 'show ip bgp {address_family} vrf {vrf} neighbors {neighbor} advertised-routes'
    '''

    def cli(self, neighbor, address_family='', vrf='', output=None):

        p1 = re.compile(r'^\s*For +address +family:'
                            r' +(?P<address_family>[a-zA-Z0-9\s\-\_]+)$')

        p3_1 = re.compile(r'^\s*(?P<status_codes>(s|d|h|\*|\>|i|r|S|m|b|f|x|a|c|t|L|\s)+)?(?=[\d|\[])'
                            r'(?P<path_type>(i|e|c|l|a|r|I))?(\s)?'
                            r'(?P<prefix>[a-zA-Z0-9\.\:\/\[\]\,]+)'
                            r'(?: *(?P<next_hop>[a-zA-Z0-9\.\:\/\[\]\,]+))?$')

        p3_2 = re.compile(r'^\s*(?P<status_codes>(s|d|h|\*|\>|i|r|S|m|b|f|x|a|c|t|L|\s)+)'
                            r'(?P<path_type>(i|e|c|l|a|r|I))?(\s)?'
                            r'(?P<prefix>(([0-9]+[\.][0-9]+[\.][0-9]+'
                            r'[\.][0-9]+[\/]?[0-9]*)|([a-zA-Z0-9]+[\:]'
                            r'[a-zA-Z0-9]+[\:][a-zA-Z0-9]+[\:]'
                            r'[a-zA-Z0-9]+[\:][\:][\/][0-9]+)|'
                            r'([a-zA-Z0-9]+[\:][a-zA-Z0-9]+[\:]'
                            r'[a-zA-Z0-9]+[\:][\:][\/][0-9]+)))'
                            r' +(?P<next_hop>[a-zA-Z0-9\.\:]+)'
                            r' +(?P<numbers>[a-zA-Z0-9\s\(\)\{\}]+)'
                            r' +(?P<origin_codes>(i|e|\?|\&|\|))$')

        p3_3 = re.compile(r'^\s*(?P<status_codes>(s|d|h|\*|\>|i|r|S|m|b|f|x|a|c|t|L|\s)+)?'
                            r'(?P<path_type>(i|e|c|l|a|r|I))?'
                            r' +(?P<next_hop>(([0-9]+[\.][0-9]+[\.][0-9]'
                            r'+[\.][0-9]+)|([a-zA-Z0-9]+[\:][a-zA-Z0-9]+'
                            r'[\:][a-zA-Z0-9]+[\:][a-zA-Z0-9]+[\:]'
                            r'[a-zA-Z0-9]+[\:][\:][a-zA-Z0-9])|'
                            r'([a-zA-Z0-9]+[\:][a-zA-Z0-9]+[\:][a-zA-Z0-9]+'
                            r'[\:][a-zA-Z0-9]+[\:][\:][a-zA-Z0-9])))?'
                            r'(?: +(?P<numbers>[a-zA-Z0-9\s\(\)\{\}\.]+))?'
                            r' +(?P<origin_codes>(i|e|\?|\|))$')

        p4 = re.compile(r'^\s*Route +Distinguisher *: '
                            r'+(?P<route_distinguisher>(\S+))'
                            r'( +\(default for vrf +(?P<default_vrf>(\S+))\))?'
                            r'( +VRF Router ID (?P<vrf_router_id>(\S+)))?$')

        if not vrf:
            vrf = 'default'
        # Get VRF name by executing 'show bgp all neighbors | i BGP neighbor'
        out_vrf = self.device.execute('show bgp all neighbors | i BGP neighbor')
        bgp_neighbor_re = re.compile(r'^BGP +neighbor +is +(?P<bgp_neighbor>[0-9A-Z\:\.]+)'
                            r'(, +vrf +(?P<vrf>\S+))?, +remote AS '
                            r'+(?P<remote_as_id>[0-9]+), '
                            r'+(?P<internal_external_link>[a-z\s]+)$')
        for line in out_vrf.splitlines():
            line = line.strip()
            # BGP neighbor is 10.16.2.2,  remote AS 100, internal link
            # BGP neighbor is 10.225.10.253,  vrf CE1test,  remote AS 60000, external link
            # BGP neighbor is 192.168.0.254,  vrf L3VPN_1001,  remote AS 60001, external link
            m = bgp_neighbor_re.match(line)
            if m:
                if m.groupdict()['bgp_neighbor'] == neighbor:
                    if m.groupdict()['vrf']:
                        vrf = m.groupdict()['vrf']
                        break
                else:
                    continue

        # Init vars
        route_dict = {}
        af_dict = {}
        data_on_nextline = False
        index = 1
        bgp_table_version = local_router_id = ''
        neighbor_id = neighbor
        if address_family:
            original_address_family = address_family

        # For address family: IPv4 Unicast

        # BGP table version is 25, Local Router ID is 10.186.101.1
        p2 = re.compile(r'^\s*BGP +table +version +is'
                         r' +(?P<bgp_table_version>[0-9]+), +[Ll]ocal +[Rr]outer'
                         r' +ID +is +(?P<local_router_id>(\S+))$')

        # Status: s-suppressed, x-deleted, S-stale, d-dampened, h-history, *-valid, >-best
        # Path type: i-internal, e-external, c-confed, l-local, a-aggregate, r-redist, I-injected
        # Origin codes: i - IGP, e - EGP, ? - incomplete, | - multipath, & - backup

        # *>i[2]:[77][7,0][10.69.9.9,1,151587081][10.135.1.1,22][10.106.101.1,10.76.1.30]/616
        # *>i2001:db8:aaaa:1::/113       ::ffff:10.106.101.1
        # *>  2001:db8:a69:484::/64   2001:DB8:20:4:6::6

        # Network            Next Hop            Metric     LocPrf     Weight Path
        # *>i 10.1.2.0/24      10.4.1.1               2219    100      0 200 33299 51178 47751 {27016} e
        # *>l10.4.1.0/24         0.0.0.0                           100      32768 i
        # *>r10.16.1.0/24         0.0.0.0               4444        100      32768 ?
        # *>r10.16.1.0           0.0.0.0               4444        100      32768 ?
        # *>r10.16.2.0/24         0.0.0.0               4444        100      32768 ?
        # *>i10.49.0.0/16         10.106.101.1                        100          0 10 20 30 40 50 60 70 80 90 i
        # *>i10.4.2.0/24         10.106.102.4                        100          0 {62112 33492 4872 41787 13166 50081 21461 58376 29755 1135} i
        # *>i  172.16.51.0/24    192.168.36.220          0    100      0 ?
        # r>i 0.0.0.0          10.250.6.1               0    300      0 65000 i
        # r>i 0.0.0.0          10.250.6.1               0    300      0 65000.1 i
        # r>i 0.0.0.0          10.250.6.1               0    300      0 65000.1 65000.1 i
        p3_2 = re.compile(r'^\s*(?P<status_codes>(s|d|h|\*|\>|i|r|S|m|b|f|x|a|c|t|L|\s)+)'
            r'(?P<path_type>(i|e|c|l|a|r|I))?(\s+)?(?P<prefix>\S+) +(?P<next_hop>'
            r'[a-zA-Z0-9\.\:]+) +(?P<numbers>[a-zA-Z0-9\s\(\)\{\}\.]+) +'
            r'(?P<origin_codes>(i|e|\?|\&|\|))$')

        #                     0.0.0.0               100      32768 i
        #                     10.106.101.1            4444       100 0 3 10 20 30 40 50 60 70 80 90 i
        #*>i                  10.4.1.1               2219    100      0 200 33299 51178 47751 {27016} e
        #                                           2219             0 400 33299 51178 47751 {27016} e

        # Route Distinguisher: 200:1
        # Route Distinguisher: 300:1 (default for vrf VRF1) VRF Router ID 10.94.44.44


        for line in output.splitlines():
            line = line.rstrip()

            # For address family: IPv4 Unicast
            m = p1.match(line)
            if m:
                address_family = m.groupdict()['address_family'].lower()
                original_address_family = address_family
                continue

            # BGP table version is 25, Local Router ID is 10.186.101.1
            m = p2.match(line)
            if m:
                bgp_table_version = int(m.groupdict()['bgp_table_version'])
                local_router_id = str(m.groupdict()['local_router_id'])

                # Init dict
                if 'vrf' not in route_dict:
                    route_dict['vrf'] = {}
                if vrf not in route_dict['vrf']:
                    route_dict['vrf'][vrf] = {}
                if 'neighbor' not in route_dict['vrf'][vrf]:
                    route_dict['vrf'][vrf]['neighbor'] = {}
                if neighbor_id not in route_dict['vrf'][vrf]['neighbor']:
                    route_dict['vrf'][vrf]['neighbor'][neighbor_id] = {}
                if 'address_family' not in route_dict['vrf'][vrf]['neighbor']\
                    [neighbor_id]:
                    route_dict['vrf'][vrf]['neighbor'][neighbor_id]\
                        ['address_family'] = {}
                if address_family not in route_dict['vrf'][vrf]['neighbor']\
                    [neighbor_id]['address_family']:
                    route_dict['vrf'][vrf]['neighbor'][neighbor_id]\
                        ['address_family'][address_family] = {}

                # Set af_dict
                af_dict = route_dict['vrf'][vrf]['neighbor'][neighbor_id]\
                    ['address_family'][address_family]

                # Init advertised dict
                if 'advertised' not in af_dict:
                    af_dict['advertised'] = {}

                route_dict['vrf'][vrf]['neighbor'][neighbor_id]\
                    ['address_family'][address_family]['bgp_table_version'] = \
                        bgp_table_version
                route_dict['vrf'][vrf]['neighbor'][neighbor_id]\
                    ['address_family'][address_family]['local_router_id'] = \
                        local_router_id
                continue

            # Status: s-suppressed, x-deleted, S-stale, d-dampened, h-history, *-valid, >-best
            # Path type: i-internal, e-external, c-confed, l-local, a-aggregate, r-redist, I-injected
            # Origin codes: i - IGP, e - EGP, ? - incomplete, | - multipath, & - backup

            # *>i[2]:[77][7,0][10.69.9.9,1,151587081][10.135.1.1,22][10.106.101.1,10.76.1.30]/616
            # *>i2001:db8:aaaa:1::/113       ::ffff:10.106.101.1
            # *>  2001:db8:a69:484::/64   2001:DB8:20:4:6::6
            # *>i 10.100.248.128/26
            m = p3_1.match(line)
            if m:
                # New prefix, reset index count
                index = 1
                data_on_nextline = True

                # Get keys
                if m.groupdict()['status_codes']:
                    status_codes = str(m.groupdict()['status_codes'].rstrip())
                if m.groupdict()['path_type']:
                    path_type = str(m.groupdict()['path_type'])
                if m.groupdict()['prefix']:
                    prefix = str(m.groupdict()['prefix'])

                # Init dict
                if 'advertised' not in af_dict:
                    af_dict['advertised'] = {}
                if prefix not in af_dict['advertised']:
                    af_dict['advertised'][prefix] = {}
                if 'index' not in af_dict['advertised'][prefix]:
                    af_dict['advertised'][prefix]['index'] = {}
                if index not in af_dict['advertised'][prefix]['index']:
                    af_dict['advertised'][prefix]['index'][index] = {}

                # Set keys
                if m.groupdict()['status_codes']:
                    af_dict['advertised'][prefix]['index'][index]['status_codes'] = status_codes
                if m.groupdict()['path_type']:
                    af_dict['advertised'][prefix]['index'][index]['path_type'] = path_type
                if m.groupdict()['next_hop']:
                    af_dict['advertised'][prefix]['index'][index]['next_hop'] = str(m.groupdict()['next_hop'])
                continue

            # Network            Next Hop            Metric     LocPrf     Weight Path
            # *>i 10.1.2.0/24      10.4.1.1               2219    100      0 200 33299 51178 47751 {27016} e
            # *>l10.4.1.0/24         0.0.0.0                           100      32768 i
            # *>r10.16.1.0/24         0.0.0.0               4444        100      32768 ?
            # *>r10.16.2.0/24         0.0.0.0               4444        100      32768 ?
            # *>r10.16.2.0         0.0.0.0               4444        100      32768 ?
            # *>i10.49.0.0/16         10.106.101.1                        100          0 10 20 30 40 50 60 70 80 90 i
            # *>i10.4.2.0/24         10.106.102.4                        100          0 {62112 33492 4872 41787 13166 50081 21461 58376 29755 1135} i
            # r>i 0.0.0.0          10.250.6.1               0    300      0 65000 i
            # r>i 0.0.0.0          10.250.6.1               0    300      0 65000.1 i
            # r>i 0.0.0.0          10.250.6.1               0    300      0 65000.1 65000.1 i
            # Condition placed to handle the situation of a long line that is
            # divided nto two lines while actually it is not another index.
            if not data_on_nextline:
                m = p3_2.match(line.strip())

                if m:
                    # Get keys
                    if m.groupdict()['status_codes']:
                        status_codes = str(m.groupdict()['status_codes'].rstrip())
                    if m.groupdict()['path_type']:
                        path_type = str(m.groupdict()['path_type'])
                    if m.groupdict()['prefix']:
                        prefix = str(m.groupdict()['prefix'])
                    if m.groupdict()['next_hop']:
                        next_hop = str(m.groupdict()['next_hop'])
                    if m.groupdict()['origin_codes']:
                        origin_codes = str(m.groupdict()['origin_codes'])

                    # Init dict
                    if 'advertised' not in af_dict:
                        af_dict['advertised'] = {}
                    if prefix not in af_dict['advertised']:
                        af_dict['advertised'][prefix] = {}
                        # New prefix, reset index count
                        index = 1
                    else:
                        # get last index for prefix to prevent overwriting
                        index = list(af_dict['advertised'][prefix]['index'].keys())[-1]
                        index += 1
                    if 'index' not in af_dict['advertised'][prefix]:
                        af_dict['advertised'][prefix]['index'] = {}
                    if index not in af_dict['advertised'][prefix]['index']:
                        af_dict['advertised'][prefix]['index'][index] = {}
                    if index not in af_dict['advertised'][prefix]['index']:
                        af_dict['advertised'][prefix]['index'][index] = {}

                    # Set keys
                    if m.groupdict()['status_codes']:
                        af_dict['advertised'][prefix]['index'][index]['status_codes'] = status_codes
                    if m.groupdict()['path_type']:
                        af_dict['advertised'][prefix]['index'][index]['path_type'] = path_type
                    if m.groupdict()['next_hop']:
                        af_dict['advertised'][prefix]['index'][index]['next_hop'] = next_hop
                    if m.groupdict()['origin_codes']:
                        af_dict['advertised'][prefix]['index'][index]['origin_codes'] = origin_codes

                    # Parse numbers
                    numbers = m.groupdict()['numbers']

                    # Metric     LocPrf     Weight Path
                    #    4444       100          0  10 3 10 20 30 40 50 60 70 80 90
                    m1 = re.compile(r'^(?P<metric>[0-9]+)'
                                     r'(?P<space1>\s{4,10})'
                                     r'(?P<localprf>[0-9]+)'
                                     r'(?P<space2>\s{5,10})'
                                     r'(?P<weight>[0-9]+)'
                                     r'(?: *(?P<path>[0-9\{\}\s\.]+))?$').match(numbers)

                    #    100        ---          0 10 20 30 40 50 60 70 80 90
                    #    ---        100          0 10 20 30 40 50 60 70 80 90
                    #    100        ---      32788 ---
                    #    ---        100      32788 ---
                    m2 = re.compile(r'^(?P<value>[0-9]+)'
                                     r'(?P<space>\s{2,21})'
                                     r'(?P<weight>[0-9]+)'
                                     r'(?: *(?P<path>[0-9\{\}\s\.]+))?$').match(numbers)

                    #    ---        ---      32788 200 33299 51178 47751 {27016}
                    m3 = re.compile(r'^(?P<weight>[0-9]+)'
                                     r' +(?P<path>[0-9\{\}\s\.]+)$').match(numbers)

                    if m1:
                        af_dict['advertised'][prefix]['index'][index]['metric'] = int(m1.groupdict()['metric'])
                        af_dict['advertised'][prefix]['index'][index]['localprf'] = int(m1.groupdict()['localprf'])
                        af_dict['advertised'][prefix]['index'][index]['weight'] = int(m1.groupdict()['weight'])
                        # Set path
                        if m1.groupdict()['path']:
                            af_dict['advertised'][prefix]['index'][index]['path'] = m1.groupdict()['path'].strip()
                            continue
                    elif m2:
                        af_dict['advertised'][prefix]['index'][index]['weight'] = int(m2.groupdict()['weight'])
                        # Set metric or localprf
                        if len(m2.groupdict()['space']) > 10:
                            af_dict['advertised'][prefix]['index'][index]['metric'] = int(m2.groupdict()['value'])
                        else:
                            af_dict['advertised'][prefix]['index'][index]['localprf'] = int(m2.groupdict()['value'])
                        # Set path
                        if m2.groupdict()['path']:
                            af_dict['advertised'][prefix]['index'][index]['path'] = m2.groupdict()['path'].strip()
                        continue
                    elif m3:
                        af_dict['advertised'][prefix]['index'][index]['weight'] = int(m3.groupdict()['weight'])
                        af_dict['advertised'][prefix]['index'][index]['path'] = m3.groupdict()['path'].strip()
                        continue

            #                     0.0.0.0               100      32768 i
            #                     10.106.101.1            4444       100 0 3 10 20 30 40 50 60 70 80 90 i
            #*>i                  10.4.1.1               2219    100      0 200 33299 51178 47751 {27016} e
            #                                           2219             0 400 33299 51178 47751 {27016} e
            #                                           2219             0 400 33299 51178 47751 27016.1 e
            m = p3_3.match(line)
            if m:
                # Get keys
                if m.groupdict()['next_hop']:
                    next_hop = str(m.groupdict()['next_hop'])
                if m.groupdict()['origin_codes']:
                    origin_codes = str(m.groupdict()['origin_codes'])

                if data_on_nextline:
                    data_on_nextline =  False
                else:
                    index += 1

                # Init dict
                if 'advertised' not in af_dict:
                    af_dict['advertised'] = {}
                if prefix not in af_dict['advertised']:
                    af_dict['advertised'][prefix] = {}
                if 'index' not in af_dict['advertised'][prefix]:
                    af_dict['advertised'][prefix]['index'] = {}
                if index not in af_dict['advertised'][prefix]['index']:
                    af_dict['advertised'][prefix]['index'][index] = {}

                # Set keys
                if m.groupdict()['next_hop']:
                    af_dict['advertised'][prefix]['index'][index]['next_hop'] = next_hop
                if m.groupdict()['origin_codes']:
                    af_dict['advertised'][prefix]['index'][index]['origin_codes'] = origin_codes
                try:
                    # Set values of status_codes and path_type from prefix line
                    af_dict['advertised'][prefix]['index'][index]['status_codes'] = status_codes
                    af_dict['advertised'][prefix]['index'][index]['path_type'] = path_type
                except Exception:
                    pass

                # Parse numbers
                numbers = m.groupdict()['numbers']

                # Metric     LocPrf     Weight Path
                #    4444       100          0  10 3 10 20 30 40 50 60 70 80 90
                m1 = re.compile(r'^(?P<metric>[0-9]+)'
                                 r'(?P<space1>\s{4,10})'
                                 r'(?P<localprf>[0-9]+)'
                                 r'(?P<space2>\s{5,10})'
                                 r'(?P<weight>[0-9]+)'
                                 r'(?: *(?P<path>[0-9\{\}\s\.]+))?$').match(numbers)

                #    100        ---          0 10 20 30 40 50 60 70 80 90
                #    ---        100          0 10 20 30 40 50 60 70 80 90
                #    100        ---      32788 ---
                #    ---        100      32788 ---
                m2 = re.compile(r'^(?P<value>[0-9]+)'
                                 r'(?P<space>\s{2,21})'
                                 r'(?P<weight>[0-9]+)'
                                 r'(?: *(?P<path>[0-9\{\}\s\.]+))?$').match(numbers)

                #    ---        ---      32788 200 33299 51178 47751 {27016}
                m3 = re.compile(r'^(?P<weight>[0-9]+)'
                                 r' +(?P<path>[0-9\{\}\s\.]+)$').match(numbers)

                if m1:
                    af_dict['advertised'][prefix]['index'][index]['metric'] = int(m1.groupdict()['metric'])
                    af_dict['advertised'][prefix]['index'][index]['localprf'] = int(m1.groupdict()['localprf'])
                    af_dict['advertised'][prefix]['index'][index]['weight'] = int(m1.groupdict()['weight'])
                    # Set path
                    if m1.groupdict()['path']:
                        af_dict['advertised'][prefix]['index'][index]['path'] = m1.groupdict()['path'].strip()
                        continue
                elif m2:
                    af_dict['advertised'][prefix]['index'][index]['weight'] = int(m2.groupdict()['weight'])
                    # Set metric or localprf
                    if len(m2.groupdict()['space']) > 10:
                        af_dict['advertised'][prefix]['index'][index]['metric'] = int(m2.groupdict()['value'])
                    else:
                        af_dict['advertised'][prefix]['index'][index]['localprf'] = int(m2.groupdict()['value'])
                    # Set path
                    if m2.groupdict()['path']:
                        af_dict['advertised'][prefix]['index'][index]['path'] = m2.groupdict()['path'].strip()
                        continue
                elif m3:
                    af_dict['advertised'][prefix]['index'][index]['weight'] = int(m3.groupdict()['weight'])
                    af_dict['advertised'][prefix]['index'][index]['path'] = m3.groupdict()['path'].strip()
                    continue

            # Route Distinguisher: 200:1
            # Route Distinguisher: 300:1 (default for vrf VRF1) VRF Router ID 10.94.44.44
            m = p4.match(line)
            if m:
                route_distinguisher = str(m.groupdict()['route_distinguisher'])
                new_address_family = original_address_family + ' RD ' + route_distinguisher

                # Init dict
                if 'address_family' not in route_dict['vrf'][vrf]['neighbor']\
                        [neighbor_id]:
                    route_dict['vrf'][vrf]['neighbor'][neighbor_id]\
                        ['address_family'] = {}
                if new_address_family not in route_dict['vrf'][vrf]['neighbor']\
                    [neighbor_id]['address_family']:
                    route_dict['vrf'][vrf]['neighbor'][neighbor_id]\
                        ['address_family'][new_address_family] = {}

                # Set keys
                route_dict['vrf'][vrf]['neighbor'][neighbor_id]\
                    ['address_family'][new_address_family]['bgp_table_version'] = bgp_table_version
                route_dict['vrf'][vrf]['neighbor'][neighbor_id]\
                    ['address_family'][new_address_family]['local_router_id'] = local_router_id
                route_dict['vrf'][vrf]['neighbor'][neighbor_id]\
                    ['address_family'][new_address_family]['route_distinguisher'] = route_distinguisher
                if m.groupdict()['default_vrf']:
                    route_dict['vrf'][vrf]['neighbor'][neighbor_id]\
                        ['address_family'][new_address_family]['default_vrf'] = \
                            str(m.groupdict()['default_vrf'])

                # Reset address_family key and af_dict for use in other regex
                address_family = new_address_family
                af_dict = route_dict['vrf'][vrf]['neighbor'][neighbor_id]\
                    ['address_family'][address_family]

                # Init advertised dict
                if 'advertised' not in af_dict:
                    af_dict['advertised'] = {}
                    continue

        return route_dict


# ===========================================================================
# Parser for:
#   * 'show bgp all neighbors {neighbor} advertised-routes'
#   * 'show bgp {address_family} all neighbors {neighbor} advertised-routes'
# ===========================================================================
class ShowBgpAllNeighborsAdvertisedRoutes(ShowBgpNeighborsAdvertisedRoutesSuperParser, ShowBgpNeighborsAdvertisedRoutesSchema):

    ''' Parser for:
        * 'show bgp all neighbors {neighbor} advertised-routes'
        * 'show bgp {address_family} all neighbors {neighbor} advertised-routes'
    '''

    cli_command = ['show bgp {address_family} all neighbors {neighbor} advertised-routes',
                   'show bgp all neighbors {neighbor} advertised-routes',
                   ]

    def cli(self, neighbor, address_family='', output=None):

        if output is None:
            # Build command
            if address_family and neighbor:
                cmd = self.cli_command[0].format(address_family=address_family,
                                                 neighbor=neighbor)
            else:
                cmd = self.cli_command[1].format(neighbor=neighbor)
            # Execute command
            show_output = self.device.execute(cmd)
        else:
            show_output = output

        # Call super
        return super().cli(output=show_output, neighbor=neighbor,
                           address_family=address_family)


# ===========================================================================
# Parser for:
#   * 'show bgp neighbors {neighbor} advertised-routes'
#   * 'show bgp {address_family} neighbors {neighbor} advertised-routes'
# ===========================================================================
class ShowBgpNeighborsAdvertisedRoutes(ShowBgpNeighborsAdvertisedRoutesSuperParser, ShowBgpNeighborsAdvertisedRoutesSchema):

    ''' Parser for:
        * 'show bgp {address_family} neighbors {neighbor} advertised-routes'
        * 'show bgp neighbors {neighbor} advertised-routes'
    '''

    cli_command = ['show bgp {address_family} vrf {vrf} neighbors {neighbor} advertised-routes',
                   'show bgp {address_family} neighbors {neighbor} advertised-routes',
                   'show bgp neighbors {neighbor} advertised-routes',
                   ]

    def cli(self, neighbor, address_family='', vrf='',output=None):
        if output is None:
            # Build command
            if address_family and vrf and neighbor:
                cmd = self.cli_command[0].format(address_family=address_family,
                                                 vrf=vrf,
                                                 neighbor=neighbor)
            elif address_family and neighbor:
                cmd = self.cli_command[1].format(address_family=address_family,
                                                 neighbor=neighbor)
            elif neighbor:
                cmd = self.cli_command[2].format(neighbor=neighbor)
            # Execute command
            show_output = self.device.execute(cmd)
        else:
            show_output = output
        # Call super
        return super().cli(output=show_output, neighbor=neighbor,
                           address_family=address_family,vrf=vrf)


# ===========================================================================
# Schema for:
#   * 'show bgp all neighbors {neighbor} received-routes'
#   * 'show bgp {address_family} all neighbors {neighbor} received-routes'
#   * 'show bgp neighbors {neighbor} received-routes'
#   * 'show bgp {address_family} neighbors {neighbor} received-routes'
#   * 'show ip bgp all neighbors {neighbor} received-routes'
#   * 'show ip bgp {address_family} all neighbors {neighbor} received-routes'
#   * 'show ip bgp neighbors {neighbor} received-routes'
#   * 'show ip bgp {address_family} neighbors {neighbor} received-routes'
# ===========================================================================
class ShowBgpNeighborsReceivedRoutesSchema(MetaParser):

    ''' Schema for:
        * 'show bgp all neighbors {neighbor} received-routes'
        * 'show bgp {address_family} all neighbors {neighbor} received-routes'
        * 'show bgp neighbors {neighbor} received-routes'
        * 'show bgp {address_family} neighbors {neighbor} received-routes'
        * 'show ip bgp all neighbors {neighbor} received-routes'
        * 'show ip bgp {address_family} all neighbors {neighbor} received-routes'
        * 'show ip bgp neighbors {neighbor} received-routes'
        * 'show ip bgp {address_family} neighbors {neighbor} received-routes'
    '''

    schema = {
        'vrf':
            {Any():
                {'neighbor':
                    {Any():
                        {'address_family':
                            {Any():
                                {Optional('bgp_table_version'): int,
                                 Optional('local_router_id'): str,
                                 Optional('route_distinguisher'): str,
                                 Optional('default_vrf'): str,
                                 Optional('received_routes'):
                                    {Optional(Any()):
                                        {Optional('index'):
                                            {Optional(Any()):
                                                {Optional('next_hop'): str,
                                                 Optional('status_codes'): str,
                                                 Optional('path_type'): str,
                                                 Optional('metric'): int,
                                                 Optional('localprf'): int,
                                                 Optional('weight'): int,
                                                 Optional('path'): str,
                                                 Optional('origin_codes'): str,
                                                },
                                            },
                                        },
                                    },
                                },
                            },
                        },
                    },
                },
            },
        }


# ===========================================================================
# Super Parser for:
#   * 'show bgp all neighbors {neighbor} received-routes'
#   * 'show bgp {address_family} all neighbors {neighbor} received-routes'
#   * 'show bgp neighbors {neighbor} received-routes'
#   * 'show bgp {address_family} neighbors {neighbor} received-routes'
#   * 'show ip bgp all neighbors {neighbor} received-routes'
#   * 'show ip bgp {address_family} all neighbors {neighbor} received-routes'
#   * 'show ip bgp neighbors {neighbor} received-routes'
#   * 'show ip bgp {address_family} neighbors {neighbor} received-routes'
# ===========================================================================
class ShowBgpNeighborsReceivedRoutesSuperParser(ShowBgpNeighborsReceivedRoutesSchema):

    ''' Super Parser for:
        * 'show bgp all neighbors {neighbor} received-routes'
        * 'show bgp {address_family} all neighbors {neighbor} received-routes'
        * 'show bgp neighbors {neighbor} received-routes'
        * 'show bgp {address_family} neighbors {neighbor} received-routes'
        * 'show ip bgp all neighbors {neighbor} received-routes'
        * 'show ip bgp {address_family} all neighbors {neighbor} received-routes'
        * 'show ip bgp neighbors {neighbor} received-routes'
        * 'show ip bgp {address_family} neighbors {neighbor} received-routes'
    '''

    def cli(self, neighbor, address_family='', output=None):
        p = re.compile(r'^BGP +neighbor +is +(?P<bgp_neighbor>[0-9A-Z\:\.]+)'
                        r'(, +vrf +(?P<vrf>[0-9A-Za-z]+))?, +remote AS '
                        r'+(?P<remote_as_id>[0-9]+), '
                        r'+(?P<internal_external_link>[a-z\s]+)$')
        p1 = re.compile(r'^\s*For +address +family:'
                            r' +(?P<address_family>[a-zA-Z0-9\s\-\_]+)$')
        p2 = re.compile(r'^\s*BGP +table +version +is'
                            r' +(?P<bgp_table_version>[0-9]+), +[Ll]ocal +[Rr]outer'
                            r' +ID +is +(?P<local_router_id>(\S+))$')
        p3_1 = re.compile(r'^\s*(?P<status_codes>(s|x|S|d|h|\*|\>|\s)+)?'
                            r'(?P<path_type>(i|e|c|l|a|r|I))?'
                            r'(?P<prefix>[a-zA-Z0-9\.\:\/\[\]\,]+)'
                        r'(?: *(?P<next_hop>[a-zA-Z0-9\.\:\/\[\]\,]+))?$')
        p3_2 = re.compile(r'^\s*(?P<status_codes>(s|x|S|d|h|\*|\>|\s)+)'
                            r'(?P<path_type>(i|e|c|l|a|r|I))?(\s)?'
                            r'(?P<prefix>(([0-9]+[\.][0-9]+[\.][0-9]+'
                            r'[\.][0-9]+([\/][0-9]+)?)|([a-zA-Z0-9]+[\:]'
                            r'[a-zA-Z0-9]+[\:][a-zA-Z0-9]+[\:]'
                            r'[a-zA-Z0-9]+[\:][\:][\/][0-9]+)|'
                            r'([a-zA-Z0-9]+[\:][a-zA-Z0-9]+[\:]'
                            r'[a-zA-Z0-9]+[\:][\:][\/][0-9]+)))'
                            r' +(?P<next_hop>[a-zA-Z0-9\.\:]+)'
                            r' +(?P<numbers>[a-zA-Z0-9\s\(\)\{\}]+)'
                            r' +(?P<origin_codes>(i|e|\?|\&|\|))$')
        p3_3 = re.compile(r'^\s*(?P<next_hop>[a-zA-Z0-9\.\:]+)'
                            r'(?: +(?P<numbers>[a-zA-Z0-9\s\(\)\{\}]+))?'
                            r' +(?P<origin_codes>(i|e|\?|\|))$')
        p4 = re.compile(r'^\s*Route +Distinguisher *: '
                            r'+(?P<route_distinguisher>(\S+))'
                            r'( +\(default for vrf +(?P<default_vrf>(\S+))\))?'
                            r'( +VRF Router ID (?P<vrf_router_id>(\S+)))?$')

        # Get VRF name by executing 'show bgp all neighbors | i BGP neighbor'
        out_vrf = self.device.execute('show bgp all neighbors | i BGP neighbor')
        vrf = 'default'
        for line in out_vrf.splitlines():
            line = line.strip()
            # BGP neighbor is 10.16.2.2,  remote AS 100, internal link
            m = p.match(line)
            if m:
                if m.groupdict()['bgp_neighbor'] == neighbor:
                    if m.groupdict()['vrf']:
                        vrf = str(m.groupdict()['vrf'])
                        break
                else:
                    continue

        # Init dictionary
        route_dict = {}
        af_dict = {}

        # Init vars
        data_on_nextline =  False
        index = 1
        bgp_table_version = local_router_id = ''
        neighbor_id = str(neighbor)
        original_address_family = address_family

        for line in output.splitlines():
            line = line.rstrip()

            # For address family: IPv4 Unicast
            m = p1.match(line)
            if m:
                address_family = str(m.groupdict()['address_family']).lower()
                original_address_family = address_family
                continue

            # BGP table version is 25, Local Router ID is 10.186.101.1
            m = p2.match(line)
            if m:
                bgp_table_version = int(m.groupdict()['bgp_table_version'])
                local_router_id = str(m.groupdict()['local_router_id'])

                # Init dict
                if 'vrf' not in route_dict:
                    route_dict['vrf'] = {}
                if vrf not in route_dict['vrf']:
                    route_dict['vrf'][vrf] = {}
                if 'neighbor' not in route_dict['vrf'][vrf]:
                    route_dict['vrf'][vrf]['neighbor'] = {}
                if neighbor_id not in route_dict['vrf'][vrf]['neighbor']:
                    route_dict['vrf'][vrf]['neighbor'][neighbor_id] = {}
                if 'address_family' not in route_dict['vrf'][vrf]['neighbor']\
                    [neighbor_id]:
                    route_dict['vrf'][vrf]['neighbor'][neighbor_id]\
                        ['address_family'] = {}
                if address_family not in route_dict['vrf'][vrf]['neighbor']\
                    [neighbor_id]['address_family']:
                    route_dict['vrf'][vrf]['neighbor'][neighbor_id]\
                        ['address_family'][address_family] = {}

                # Set af_dict
                af_dict = route_dict['vrf'][vrf]['neighbor'][neighbor_id]\
                    ['address_family'][address_family]

                # Init received_routes dict
                if 'received_routes' not in af_dict:
                    af_dict['received_routes'] = {}

                route_dict['vrf'][vrf]['neighbor'][neighbor_id]\
                    ['address_family'][address_family]['bgp_table_version'] = \
                        bgp_table_version
                route_dict['vrf'][vrf]['neighbor'][neighbor_id]\
                    ['address_family'][address_family]['local_router_id'] = \
                        local_router_id
                continue

            # Status codes: s suppressed, d damped, h history, * valid, > best, i - internal,
            #   r RIB-failure, S Stale, m multipath, b backup-path, f RT-Filter,
            #   x best-external, a additional-path, c RIB-compressed,
            # Origin codes: i - IGP, e - EGP, ? - incomplete
            # RPKI validation codes: V valid, I invalid, N Not found

            # *>i[2]:[77][7,0][10.69.9.9,1,151587081][10.135.1.1,22][10.106.101.1,10.76.1.30]/616
            # *>i2001:db8:aaaa:1::/113       ::ffff:10.106.101.1
            # *>  2001:db8:a69:484::/64   2001:DB8:20:4:6::6
            m = p3_1.match(line)
            if m:
                # New prefix, reset index count
                index = 1
                data_on_nextline = True

                # Get keys
                if m.groupdict()['status_codes']:
                    status_codes = str(m.groupdict()['status_codes'].rstrip())
                if m.groupdict()['path_type']:
                    path_type = str(m.groupdict()['path_type'])
                if m.groupdict()['prefix']:
                    prefix = str(m.groupdict()['prefix'])

                # Init dict
                if 'received_routes' not in af_dict:
                    af_dict['received_routes'] = {}
                if prefix not in af_dict['received_routes']:
                    af_dict['received_routes'][prefix] = {}
                if 'index' not in af_dict['received_routes'][prefix]:
                    af_dict['received_routes'][prefix]['index'] = {}
                if index not in af_dict['received_routes'][prefix]['index']:
                    af_dict['received_routes'][prefix]['index'][index] = {}

                # Set keys
                if m.groupdict()['status_codes']:
                    af_dict['received_routes'][prefix]['index'][index]['status_codes'] = status_codes
                if m.groupdict()['path_type']:
                    af_dict['received_routes'][prefix]['index'][index]['path_type'] = path_type
                if m.groupdict()['next_hop']:
                    af_dict['received_routes'][prefix]['index'][index]['next_hop'] = str(m.groupdict()['next_hop'])
                continue

            # Network            Next Hop            Metric     LocPrf     Weight Path
            # *   10.169.1.0/24      10.4.6.6              2219             0 300 33299 51178 47751 {27016} e
            # *>l10.4.1.0/24         0.0.0.0                           100      32768 i
            # *>r10.16.1.0/24         0.0.0.0               4444        100      32768 ?
            # *>r10.16.2.0/24         0.0.0.0               4444        100      32768 ?
            # *>i10.49.0.0/16         10.106.101.1                        100          0 10 20 30 40 50 60 70 80 90 i
            # *>i10.4.2.0/24         10.106.102.4                        100          0 {62112 33492 4872 41787 13166 50081 21461 58376 29755 1135} i
            # Condition placed to handle the situation of a long line that is
            # divided nto two lines while actually it is not another index.
            if not data_on_nextline:
                m = p3_2.match(line)
                if m:
                    # New prefix, reset index count
                    index = 1

                    # Get keys
                    if m.groupdict()['status_codes']:
                        status_codes = str(m.groupdict()['status_codes'].rstrip())
                    if m.groupdict()['path_type']:
                        path_type = str(m.groupdict()['path_type'])
                    if m.groupdict()['prefix']:
                        prefix = str(m.groupdict()['prefix'])
                    if m.groupdict()['next_hop']:
                        next_hop = str(m.groupdict()['next_hop'])
                    if m.groupdict()['origin_codes']:
                        origin_codes = str(m.groupdict()['origin_codes'])

                    # Init dict
                    if 'received_routes' not in af_dict:
                        af_dict['received_routes'] = {}
                    if prefix not in af_dict['received_routes']:
                        af_dict['received_routes'][prefix] = {}
                    if 'index' not in af_dict['received_routes'][prefix]:
                        af_dict['received_routes'][prefix]['index'] = {}
                    if index not in af_dict['received_routes'][prefix]['index']:
                        af_dict['received_routes'][prefix]['index'][index] = {}
                    if index not in af_dict['received_routes'][prefix]['index']:
                        af_dict['received_routes'][prefix]['index'][index] = {}

                    # Set keys
                    if m.groupdict()['status_codes']:
                        af_dict['received_routes'][prefix]['index'][index]['status_codes'] = status_codes
                    if m.groupdict()['path_type']:
                        af_dict['received_routes'][prefix]['index'][index]['path_type'] = path_type
                    if m.groupdict()['next_hop']:
                        af_dict['received_routes'][prefix]['index'][index]['next_hop'] = next_hop
                    if m.groupdict()['origin_codes']:
                        af_dict['received_routes'][prefix]['index'][index]['origin_codes'] = origin_codes

                    # Parse numbers
                    numbers = m.groupdict()['numbers']

                    # Metric     LocPrf     Weight Path
                    #    4444       100          0  10 3 10 20 30 40 50 60 70 80 90
                    m1 = re.compile(r'^(?P<metric>[0-9]+)'
                                     r'(?P<space1>\s{5,10})'
                                     r'(?P<localprf>[0-9]+)'
                                     r'(?P<space2>\s{5,10})'
                                     r'(?P<weight>[0-9]+)'
                                     r'(?: *(?P<path>[0-9\{\}\s]+))?$').match(numbers)

                    #    100        ---          0 10 20 30 40 50 60 70 80 90
                    #    ---        100          0 10 20 30 40 50 60 70 80 90
                    #    100        ---      32788 ---
                    #    ---        100      32788 ---
                    m2 = re.compile(r'^(?P<value>[0-9]+)'
                                     r'(?P<space>\s{2,21})'
                                     r'(?P<weight>[0-9]+)'
                                     r'(?: *(?P<path>[0-9\{\}\s]+))?$').match(numbers)

                    #    ---        ---      32788 200 33299 51178 47751 {27016}
                    m3 = re.compile(r'^(?P<weight>[0-9]+)'
                                     r' +(?P<path>[0-9\{\}\s]+)$').match(numbers)

                    if m1:
                        af_dict['received_routes'][prefix]['index'][index]['metric'] = int(m1.groupdict()['metric'])
                        af_dict['received_routes'][prefix]['index'][index]['localprf'] = int(m1.groupdict()['localprf'])
                        af_dict['received_routes'][prefix]['index'][index]['weight'] = int(m1.groupdict()['weight'])
                        # Set path
                        if m1.groupdict()['path']:
                            af_dict['received_routes'][prefix]['index'][index]['path'] = m1.groupdict()['path'].strip()
                            continue
                    elif m2:
                        af_dict['received_routes'][prefix]['index'][index]['weight'] = int(m2.groupdict()['weight'])
                        # Set metric or localprf
                        if len(m2.groupdict()['space']) > 10:
                            af_dict['received_routes'][prefix]['index'][index]['metric'] = int(m2.groupdict()['value'])
                        else:
                            af_dict['received_routes'][prefix]['index'][index]['localprf'] = int(m2.groupdict()['value'])
                        # Set path
                        if m2.groupdict()['path']:
                            af_dict['received_routes'][prefix]['index'][index]['path'] = m2.groupdict()['path'].strip()
                            continue
                    elif m3:
                        af_dict['received_routes'][prefix]['index'][index]['weight'] = int(m3.groupdict()['weight'])
                        af_dict['received_routes'][prefix]['index'][index]['path'] = m3.groupdict()['path'].strip()
                        continue

            #                     0.0.0.0               100      32768 i
            #                     10.106.101.1            4444       100 0 3 10 20 30 40 50 60 70 80 90 i
            m = p3_3.match(line)
            if m:
                # Get keys
                next_hop = str(m.groupdict()['next_hop'])
                origin_codes = str(m.groupdict()['origin_codes'])

                if data_on_nextline:
                    data_on_nextline =  False
                else:
                    index += 1

                # Init dict
                if 'received_routes' not in af_dict:
                    af_dict['received_routes'] = {}
                if prefix not in af_dict['received_routes']:
                    af_dict['received_routes'][prefix] = {}
                if 'index' not in af_dict['received_routes'][prefix]:
                    af_dict['received_routes'][prefix]['index'] = {}
                if index not in af_dict['received_routes'][prefix]['index']:
                    af_dict['received_routes'][prefix]['index'][index] = {}

                # Set keys
                af_dict['received_routes'][prefix]['index'][index]['next_hop'] = next_hop
                af_dict['received_routes'][prefix]['index'][index]['origin_codes'] = origin_codes
                try:
                    # Set values of status_codes and path_type from prefix line
                    af_dict['received_routes'][prefix]['index'][index]['status_codes'] = status_codes
                    af_dict['received_routes'][prefix]['index'][index]['path_type'] = path_type
                except Exception:
                    pass

                # Parse numbers
                numbers = m.groupdict()['numbers']

                # Metric     LocPrf     Weight Path
                #    4444       100          0  10 3 10 20 30 40 50 60 70 80 90
                m1 = re.compile(r'^(?P<metric>[0-9]+)'
                                 r'(?P<space1>\s{5,10})'
                                 r'(?P<localprf>[0-9]+)'
                                 r'(?P<space2>\s{5,10})'
                                 r'(?P<weight>[0-9]+)'
                                 r'(?: *(?P<path>[0-9\{\}\s]+))?$').match(numbers)

                #    100        ---          0 10 20 30 40 50 60 70 80 90
                #    ---        100          0 10 20 30 40 50 60 70 80 90
                #    100        ---      32788 ---
                #    ---        100      32788 ---
                m2 = re.compile(r'^(?P<value>[0-9]+)'
                                 r'(?P<space>\s{2,21})'
                                 r'(?P<weight>[0-9]+)'
                                 r'(?: *(?P<path>[0-9\{\}\s]+))?$').match(numbers)

                #    ---        ---      32788 200 33299 51178 47751 {27016}
                m3 = re.compile(r'^(?P<weight>[0-9]+)'
                                 r' +(?P<path>[0-9\{\}\s]+)$').match(numbers)

                if m1:
                    af_dict['received_routes'][prefix]['index'][index]['metric'] = int(m1.groupdict()['metric'])
                    af_dict['received_routes'][prefix]['index'][index]['localprf'] = int(m1.groupdict()['localprf'])
                    af_dict['received_routes'][prefix]['index'][index]['weight'] = int(m1.groupdict()['weight'])
                    # Set path
                    if m1.groupdict()['path']:
                        af_dict['received_routes'][prefix]['index'][index]['path'] = m1.groupdict()['path'].strip()
                        continue
                elif m2:
                    af_dict['received_routes'][prefix]['index'][index]['weight'] = int(m2.groupdict()['weight'])
                    # Set metric or localprf
                    if len(m2.groupdict()['space']) > 10:
                        af_dict['received_routes'][prefix]['index'][index]['metric'] = int(m2.groupdict()['value'])
                    else:
                        af_dict['received_routes'][prefix]['index'][index]['localprf'] = int(m2.groupdict()['value'])
                    # Set path
                    if m2.groupdict()['path']:
                        af_dict['received_routes'][prefix]['index'][index]['path'] = m2.groupdict()['path'].strip()
                        continue
                elif m3:
                    af_dict['received_routes'][prefix]['index'][index]['weight'] = int(m3.groupdict()['weight'])
                    af_dict['received_routes'][prefix]['index'][index]['path'] = m3.groupdict()['path'].strip()
                    continue

            # Route Distinguisher: 200:1
            # Route Distinguisher: 300:1 (default for vrf VRF1) VRF Router ID 10.94.44.44
            m = p4.match(line)
            if m:
                route_distinguisher = str(m.groupdict()['route_distinguisher'])
                new_address_family = original_address_family + ' RD ' + route_distinguisher

                # Init dict
                if 'address_family' not in route_dict['vrf'][vrf]['neighbor']\
                        [neighbor_id]:
                    route_dict['vrf'][vrf]['neighbor'][neighbor_id]\
                        ['address_family'] = {}
                if new_address_family not in route_dict['vrf'][vrf]['neighbor']\
                    [neighbor_id]['address_family']:
                    route_dict['vrf'][vrf]['neighbor'][neighbor_id]\
                        ['address_family'][new_address_family] = {}

                # Set keys
                route_dict['vrf'][vrf]['neighbor'][neighbor_id]\
                    ['address_family'][new_address_family]['bgp_table_version'] = bgp_table_version
                route_dict['vrf'][vrf]['neighbor'][neighbor_id]\
                    ['address_family'][new_address_family]['local_router_id'] = local_router_id
                route_dict['vrf'][vrf]['neighbor'][neighbor_id]\
                    ['address_family'][new_address_family]['route_distinguisher'] = route_distinguisher
                if m.groupdict()['default_vrf']:
                    route_dict['vrf'][vrf]['neighbor'][neighbor_id]\
                        ['address_family'][new_address_family]['default_vrf'] = \
                            str(m.groupdict()['default_vrf'])

                # Reset address_family key and af_dict for use in other regex
                address_family = new_address_family
                af_dict = route_dict['vrf'][vrf]['neighbor'][neighbor_id]\
                    ['address_family'][address_family]

                # Init received_routes dict
                if 'received_routes' not in af_dict:
                    af_dict['received_routes'] = {}
                    continue

        return route_dict


# ========================================================================
# Parser for:
#   * 'show bgp all neighbors {neighbor} received-routes'
#   * 'show bgp {address_family} all neighbors {neighbor} received-routes'
# ========================================================================
class ShowBgpAllNeighborsReceivedRoutes(ShowBgpNeighborsReceivedRoutesSuperParser, ShowBgpNeighborsReceivedRoutesSchema):

    ''' Parser for:
        * 'show bgp all neighbors {neighbor} received-routes'
        * 'show bgp {address_family} all neighbors {neighbor} received-routes'
    '''

    cli_command = ['show bgp {address_family} all neighbors {neighbor} received-routes',
                   'show bgp all neighbors {neighbor} received-routes',
                   ]

    def cli(self, neighbor, address_family='', output=None):

        if output is None:
            # Build command
            if address_family and neighbor:
                cmd = self.cli_command[0].format(address_family=address_family,
                                                 neighbor=neighbor)
            else:
                cmd = self.cli_command[1].format(neighbor=neighbor)
            # Execute command
            show_output = self.device.execute(cmd)
        else:
            show_output = output

        # Call super
        return super().cli(output=show_output, neighbor=neighbor,
                           address_family=address_family)


# ====================================================================
# Parser for:
#   * 'show bgp {address_family} vrf {vrf} neighbors {neighbor} received-routes'
#   * 'show bgp {address_family} neighbors {neighbor} received-routes'
#   * 'show bgp neighbors {neighbor} received-routes'
# ====================================================================
class ShowBgpNeighborsReceivedRoutes(ShowBgpNeighborsReceivedRoutesSuperParser, ShowBgpNeighborsReceivedRoutesSchema):

    ''' Parser for:
        * 'show bgp {address_family} vrf {vrf} neighbors {neighbor} received-routes'
        * 'show bgp {address_family} neighbors {neighbor} received-routes'
        * 'show bgp neighbors {neighbor} received-routes'
    '''

    cli_command = [
        'show bgp neighbors {neighbor} received-routes',
        'show bgp {address_family} neighbors {neighbor} received-routes',
        'show bgp {address_family} vrf {vrf} neighbors {neighbor} received-routes',
    ]

    def cli(self, neighbor, address_family='', vrf='', output=None):

        if output is None:
            # Build command
            if address_family and vrf and neighbor:
                cmd = self.cli_command[2].format(address_family=address_family,
                                                 vrf=vrf,
                                                 neighbor=neighbor)
            elif address_family and neighbor:
                cmd = self.cli_command[1].format(address_family=address_family,
                                                 neighbor=neighbor)
            elif neighbor:
                cmd = self.cli_command[0].format(neighbor=neighbor)
            # Execute command
            show_output = self.device.execute(cmd)
        else:
            show_output = output

        # Call super
        return super().cli(output=show_output, neighbor=neighbor,
                           address_family=address_family)




# ===================================================================
# Schema for:
#   * 'show bgp all neighbors {neighbor} routes'
#   * 'show bgp {address_family} all neighbors {neighbor} routes'
#   * 'show bgp neighbors {neighbor} routes'
#   * 'show bgp {address_family} neighbors {neighbor} routes'
#   * 'show ip bgp all neighbors {neighbor} routes'
#   * 'show ip bgp {address_family} all neighbors {neighbor} routes'
#   * 'show ip bgp neighbors {neighbor} routes'
#   * 'show ip bgp {address_family} neighbors {neighbor} routes'
# ===================================================================
class ShowBgpAllNeighborsRoutesSchema(MetaParser):

    ''' Schema for
        * 'show bgp all neighbors {neighbor} routes'
        * 'show bgp {address_family} neighbors {neighbor} routes'
        * 'show bgp {address_family} all neighbors {neighbor} routes'
        * 'show ip bgp neighbors {neighbor} routes'
        * 'show ip bgp all neighbors {neighbor} routes'
    '''

    schema = {
        Optional('total_num_of_prefixes'): int,
        Optional('vrf'):
            {Any():
                {'neighbor':
                    {Any():
                        {'address_family':
                            {Any():
                                {Optional('bgp_table_version'): int,
                                Optional('local_router_id'): str,
                                Optional('route_distinguisher'): str,
                                Optional('default_vrf'): str,
                                Optional('routes'):
                                    {Optional(Any()):
                                        {Optional('index'):
                                            {Optional(Any()):
                                                {Optional('next_hop'): str,
                                                Optional('status_codes'): str,
                                                Optional('path_type'): str,
                                                Optional('metric'): int,
                                                Optional('localprf'): int,
                                                Optional('weight'): int,
                                                Optional('path'): str,
                                                Optional('origin_codes'): str,
                                                },
                                            },
                                        },
                                    },
                                },
                            },
                        },
                    },
                },
            },
        }


# ===================================================================
# Parser for:
#   * 'show bgp all neighbors {neighbor} routes'
#   * 'show bgp {address_family} all neighbors {neighbor} routes'
#   * 'show bgp neighbors {neighbor} routes'
#   * 'show bgp {address_family} vrf {vrf} neighbors {neighbor} routes'
#   * 'show bgp {address_family} neighbors {neighbor} routes'
#   * 'show ip bgp all neighbors {neighbor} routes'
#   * 'show ip bgp {address_family} all neighbors {neighbor} routes'
#   * 'show ip bgp neighbors {neighbor} routes'
#   * 'show ip bgp {address_family} neighbors {neighbor} routes'
# ===================================================================
class ShowBgpAllNeighborsRoutesSuperParser(ShowBgpAllNeighborsRoutesSchema):

    ''' Parser for
        * 'show bgp all neighbors {neighbor} routes'
        * 'show bgp {address_family} all neighbors {neighbor} routes'
        * 'show bgp neighbors {neighbor} routes'
        * 'show bgp {address_family} neighbors {neighbor} routes'
        * 'show bgp {address_family} vrf {vrf} neighbors {neighbor} routes'
        * 'show ip bgp all neighbors {neighbor} routes'
        * 'show ip bgp {address_family} all neighbors {neighbor} routes'
        * 'show ip bgp neighbors {neighbor} routes'
        * 'show ip bgp {address_family} neighbors {neighbor} routes'
    '''

    def cli(self, neighbor, address_family='', vrf='', output=None):

        if not vrf:
            # Get VRF name by executing 'show bgp all neighbors | i BGP neighbor'
            out_vrf = self.device.execute('show bgp all neighbors | i BGP neighbor')
            vrf='default'
            p = re.compile(r'^BGP +neighbor +is +(?P<bgp_neighbor>[0-9A-Z\:\.]+)'
                            r'(, +vrf +(?P<vrf>[0-9A-Za-z]+))?, +remote AS '
                            r'+(?P<remote_as_id>[0-9]+), '
                            r'+(?P<internal_external_link>[a-z\s]+)$')
            for line in out_vrf.splitlines():
                line = line.strip()
                # BGP neighbor is 10.16.2.2,  remote AS 100, internal link
                m = p.match(line)
                if m:
                    if m.groupdict()['bgp_neighbor'] == neighbor:
                        if m.groupdict()['vrf']:
                            vrf = str(m.groupdict()['vrf'])
                            break
                    else:
                        continue

        # Init dictionary
        route_dict = {}
        af_dict = {}
        data_on_nextline = False
        index = 1
        bgp_table_version = local_router_id = ''
        neighbor_id = neighbor
        if address_family:
            original_address_family = address_family

        # For address family: IPv4 Unicast
        p1 = re.compile(r'^\s*For +address +family:'
                         r' +(?P<address_family>[a-zA-Z0-9\s\-\_]+)$')

        # BGP table version is 25, Local Router ID is 10.186.101.1
        p2 = re.compile(r'^\s*BGP +table +version +is'
                         r' +(?P<bgp_table_version>[0-9]+), +[Ll]ocal +[Rr]outer'
                         r' +ID +is +(?P<local_router_id>(\S+))$')

        # *>i[2]:[77][7,0][10.69.9.9,1,151587081][10.135.1.1,22][10.106.101.1,10.76.1.30]/616
        # *>i2001:db8:aaaa:1::/113       ::ffff:10.106.101.1
        # *>i  2001:db8:400::/64          ::FFFF:192.168.51.1
        # r>i  2001:2:2:2::2/128
        p3 = re.compile(r'^\s*(?P<status_codes>(b|s|x|S|d|h|r|\*|\>|\s)+)?'
                         r'(?P<path_type>(i|e|c|l|a|r|I))? *'
                         r'(?P<prefix>[a-zA-Z0-9\.\:\/\[\]\,]+)'
                         r'(?: *(?P<next_hop>[a-zA-Z0-9\.\:\/\[\]\,]+))?$')

        # 4444        100          0 i
        p4 = re.compile(r'^(?P<metric>(\d+)) +(?P<locprf>(\d+))'
                         r' +(?P<weight>(\d+)) +(?P<origin_codes>(i|e|\?|\|))$')

        #                     0.0.0.0               100     32768 i
        #                     10.106.101.1            4444    100 0 3 10 20 30 40 50 60 70 80 90 i
        # *>i                 10.4.1.1               2219    100      0 200 33299 51178 47751 {27016} e
        p5 = re.compile(r'^\s*(?P<status_codes>(s|x|S|d|h|\*|\>|\s)+)?'
                         r'(?P<path_type>(i|e|c|l|a|r|I))?'
                         r' +(?P<next_hop>[a-zA-Z0-9\.\:]+)'
                         r'(?: +(?P<numbers>[a-zA-Z0-9\s\(\)\{\}]+))? +'
                         r'(?P<origin_codes>(i|e|\?|\|))$')

        # Network            Next Hop            Metric     LocPrf     Weight Path
        # *>i 10.1.2.0/24      10.4.1.1               2219    100      0 200 33299 51178 47751 {27016} e
        # *>l10.4.1.0/24         0.0.0.0                           100      32768 i
        # *>r10.16.1.0/24         0.0.0.0               4444        100      32768 ?
        # *>r10.16.2.0/24         0.0.0.0               4444        100      32768 ?
        # *>i  10.145.0.0/24      192.168.51.1                1    100      0 ?
        # *>i10.49.0.0/16         10.106.101.1                        100          0 10 20 30 40 50 60 70 80 90 i
        # *>i10.4.2.0/24         10.106.102.4                        100          0 {62112 33492 4872 41787 13166 50081 21461 58376 29755 1135} i
        # Condition placed to handle the situation of a long line that is
        # divided nto two lines while actually it is not another index.
        p6 = re.compile(r'^\s*(?P<status_codes>(s|x|S|d|r|h|\*|\>|\s)+)'
                         r'(?P<path_type>(i|e|c|l|a|r|I))? *'
                         r'(?P<prefix>(([0-9]+[\.][0-9]+[\.][0-9]+'
                         r'[\.][0-9]+[\/][0-9]+)|([a-zA-Z0-9]+[\:]'
                         r'[a-zA-Z0-9]+[\:][a-zA-Z0-9]+[\:]'
                         r'[a-zA-Z0-9]+[\:][\:][\/][0-9]+)|'
                         r'([a-zA-Z0-9]+[\:][a-zA-Z0-9]+[\:]'
                         r'[a-zA-Z0-9]+[\:][\:][\/][0-9]+)|'
                         r'([a-zA-Z0-9\.\:]+)))'
                         r' +(?P<next_hop>[a-zA-Z0-9\.\:]+)'
                         r' +(?P<numbers>[a-zA-Z0-9\s\(\)\{\}]+)'
                         r' +(?P<origin_codes>(i|e|\?|\&|\|))$')

        # Route Distinguisher: 200:1
        # Route Distinguisher: 300:1 (default for vrf VRF1) VRF Router ID 10.94.44.44
        p7 = re.compile(r'^\s*Route +Distinguisher *: '
                         r'+(?P<route_distinguisher>(\S+))'
                         r'( +\(default for vrf +(?P<default_vrf>(\S+))\))?'
                         r'( +VRF Router ID (?P<vrf_router_id>(\S+)))?$')

        # Total number of prefixes 32
        p8 = re.compile(r'^Total number of prefixes (?P<total_num_of_prefixes>\d+)$')

        for line in output.splitlines():
            line = line.rstrip()

            # For address family: IPv4 Unicast
            m = p1.match(line)
            if m:
                address_family = str(m.groupdict()['address_family']).lower()
                original_address_family = address_family
                continue

            # BGP table version is 25, Local Router ID is 10.186.101.1
            m = p2.match(line)
            if m:
                bgp_table_version = int(m.groupdict()['bgp_table_version'])
                local_router_id = str(m.groupdict()['local_router_id'])

                # Init dict
                if 'vrf' not in route_dict:
                    route_dict['vrf'] = {}
                if vrf not in route_dict['vrf']:
                    route_dict['vrf'][vrf] = {}
                if 'neighbor' not in route_dict['vrf'][vrf]:
                    route_dict['vrf'][vrf]['neighbor'] = {}
                if neighbor_id not in route_dict['vrf'][vrf]['neighbor']:
                    route_dict['vrf'][vrf]['neighbor'][neighbor_id] = {}
                if 'address_family' not in route_dict['vrf'][vrf]['neighbor']\
                    [neighbor_id]:
                    route_dict['vrf'][vrf]['neighbor'][neighbor_id]\
                        ['address_family'] = {}
                if address_family not in route_dict['vrf'][vrf]['neighbor']\
                    [neighbor_id]['address_family']:
                    route_dict['vrf'][vrf]['neighbor'][neighbor_id]\
                        ['address_family'][address_family] = {}

                # Set af_dict
                af_dict = route_dict['vrf'][vrf]['neighbor'][neighbor_id]\
                    ['address_family'][address_family]

                # Init routes dict
                if 'routes' not in af_dict:
                    af_dict['routes'] = {}

                route_dict['vrf'][vrf]['neighbor'][neighbor_id]\
                    ['address_family'][address_family]['bgp_table_version'] = \
                        bgp_table_version
                route_dict['vrf'][vrf]['neighbor'][neighbor_id]\
                    ['address_family'][address_family]['local_router_id'] = \
                        local_router_id
                continue

            # *>i[2]:[77][7,0][10.69.9.9,1,151587081][10.135.1.1,22][10.106.101.1,10.76.1.30]/616
            # *>i2001:db8:aaaa:1::/113       ::ffff:10.106.101.1
            # *>i  2001:db8:400::/64          ::FFFF:192.168.51.1
            m = p3.match(line)
            if m:
                # New prefix, reset index count
                index = 1
                data_on_nextline = True

                # Get keys
                if m.groupdict()['status_codes']:
                    status_codes = str(m.groupdict()['status_codes'].rstrip())
                if m.groupdict()['path_type']:
                    path_type = str(m.groupdict()['path_type'])
                if m.groupdict()['prefix']:
                    prefix = str(m.groupdict()['prefix'])

                # Init dict
                if 'routes' not in af_dict:
                    af_dict['routes'] = {}
                if prefix not in af_dict['routes']:
                    af_dict['routes'][prefix] = {}
                if 'index' not in af_dict['routes'][prefix]:
                    af_dict['routes'][prefix]['index'] = {}
                if index not in af_dict['routes'][prefix]['index']:
                    af_dict['routes'][prefix]['index'][index] = {}

                # Set keys
                if m.groupdict()['status_codes']:
                    af_dict['routes'][prefix]['index'][index]['status_codes'] = status_codes
                if m.groupdict()['path_type']:
                    af_dict['routes'][prefix]['index'][index]['path_type'] = path_type
                if m.groupdict()['next_hop']:
                    af_dict['routes'][prefix]['index'][index]['next_hop'] = str(m.groupdict()['next_hop'])
                continue

            # 4444        100          0 i
            m = p4.match(line)
            if m:
                group = m.groupdict()
                af_dict['routes'][prefix]['index'][index]['metric'] = int(group['metric'])
                af_dict['routes'][prefix]['index'][index]['locprf'] = int(group['locprf'])
                af_dict['routes'][prefix]['index'][index]['weight'] = int(group['weight'])
                af_dict['routes'][prefix]['index'][index]['origin_codes'] = group['origin_codes']
                continue

            #                     0.0.0.0               100     32768 i
            #                     10.81.101.1            4444     100 0 3 10 20 30 40 50 60 70 80 90 i
            # *>i                 10.4.1.1               2219    100      0 200 33299 51178 47751 {27016} e
            # *>i                 ::FFFF:10.4.1.1        2219    100      0 200 33299 51178 47751 {27016} e
            m = p5.match(line)
            if m:
                # Get keys
                next_hop = str(m.groupdict()['next_hop'])
                origin_codes = str(m.groupdict()['origin_codes'])

                if data_on_nextline:
                    data_on_nextline =  False
                else:
                    index += 1

                # Init dict
                if 'routes' not in af_dict:
                    af_dict['routes'] = {}
                if prefix not in af_dict['routes']:
                    af_dict['routes'][prefix] = {}
                if 'index' not in af_dict['routes'][prefix]:
                    af_dict['routes'][prefix]['index'] = {}
                if index not in af_dict['routes'][prefix]['index']:
                    af_dict['routes'][prefix]['index'][index] = {}

                # Set keys
                af_dict['routes'][prefix]['index'][index]['next_hop'] = next_hop
                af_dict['routes'][prefix]['index'][index]['origin_codes'] = origin_codes
                try:
                    # Set values of status_codes and path_type from prefix line
                    af_dict['routes'][prefix]['index'][index]['status_codes'] = status_codes
                    af_dict['routes'][prefix]['index'][index]['path_type'] = path_type
                except Exception:
                    pass

                # Parse numbers
                numbers = m.groupdict()['numbers']

                # Metric     LocPrf     Weight Path
                #    4444       100          0  10 3 10 20 30 40 50 60 70 80 90
                m1 = re.compile(r'^(?P<metric>[0-9]+)'
                                 r'(?P<space1>\s{4,10})'
                                 r'(?P<localprf>[0-9]+)'
                                 r'(?P<space2>\s{5,10})'
                                 r'(?P<weight>[0-9]+)'
                                 r'(?: *(?P<path>[0-9\{\}\s]+))?$').match(numbers)

                #    100        ---          0 10 20 30 40 50 60 70 80 90
                #    ---        100          0 10 20 30 40 50 60 70 80 90
                #    100        ---      32788 ---
                #    ---        100      32788 ---
                m2 = re.compile(r'^(?P<value>[0-9]+)'
                                 r'(?P<space>\s{2,21})'
                                 r'(?P<weight>[0-9]+)'
                                 r'(?: *(?P<path>[0-9\{\}\s]+))?$').match(numbers)

                #    ---        ---      32788 200 33299 51178 47751 {27016}
                m3 = re.compile(r'^(?P<weight>[0-9]+)'
                                 r' +(?P<path>[0-9\{\}\s]+)$').match(numbers)

                if m1:
                    af_dict['routes'][prefix]['index'][index]['metric'] = int(m1.groupdict()['metric'])
                    af_dict['routes'][prefix]['index'][index]['localprf'] = int(m1.groupdict()['localprf'])
                    af_dict['routes'][prefix]['index'][index]['weight'] = int(m1.groupdict()['weight'])
                    # Set path
                    if m1.groupdict()['path']:
                        af_dict['routes'][prefix]['index'][index]['path'] = m1.groupdict()['path'].strip()
                        continue
                elif m2:
                    af_dict['routes'][prefix]['index'][index]['weight'] = int(m2.groupdict()['weight'])
                    # Set metric or localprf
                    if len(m2.groupdict()['space']) > 10:
                        af_dict['routes'][prefix]['index'][index]['metric'] = int(m2.groupdict()['value'])
                    else:
                        af_dict['routes'][prefix]['index'][index]['localprf'] = int(m2.groupdict()['value'])
                    # Set path
                    if m2.groupdict()['path']:
                        af_dict['routes'][prefix]['index'][index]['path'] = m2.groupdict()['path'].strip()
                        continue
                elif m3:
                    af_dict['routes'][prefix]['index'][index]['weight'] = int(m3.groupdict()['weight'])
                    af_dict['routes'][prefix]['index'][index]['path'] = m3.groupdict()['path'].strip()
                continue

            # Network            Next Hop            Metric     LocPrf     Weight Path
            # *>i 10.1.2.0/24      10.4.1.1               2219    100      0 200 33299 51178 47751 {27016} e
            # *>l10.4.1.0/24         0.0.0.0                           100      32768 i
            # *>r10.16.1.0/24         0.0.0.0               4444        100      32768 ?
            # *>r10.16.2.0/24         0.0.0.0               4444        100      32768 ?
            # *>i  10.145.0.0/24      192.168.51.1                1    100      0 ?
            # *>i10.49.0.0/16         10.106.101.1                        100          0 10 20 30 40 50 60 70 80 90 i
            # *>i10.4.2.0/24         10.106.102.4                        100          0 {62112 33492 4872 41787 13166 50081 21461 58376 29755 1135} i
            m = p6.match(line)
            if m and not data_on_nextline:
                # New prefix, reset index count
                index = 1

                # Get keys
                if m.groupdict()['status_codes']:
                    status_codes = str(m.groupdict()['status_codes'].rstrip())
                if m.groupdict()['path_type']:
                    path_type = str(m.groupdict()['path_type'])
                if m.groupdict()['prefix']:
                    prefix = str(m.groupdict()['prefix'])
                if m.groupdict()['next_hop']:
                    next_hop = str(m.groupdict()['next_hop'])
                if m.groupdict()['origin_codes']:
                    origin_codes = str(m.groupdict()['origin_codes'])

                # Init dict
                if 'routes' not in af_dict:
                    af_dict['routes'] = {}
                if prefix not in af_dict['routes']:
                    af_dict['routes'][prefix] = {}
                if 'index' not in af_dict['routes'][prefix]:
                    af_dict['routes'][prefix]['index'] = {}
                if index not in af_dict['routes'][prefix]['index']:
                    af_dict['routes'][prefix]['index'][index] = {}
                if index not in af_dict['routes'][prefix]['index']:
                    af_dict['routes'][prefix]['index'][index] = {}

                # Set keys
                if m.groupdict()['status_codes']:
                    af_dict['routes'][prefix]['index'][index]['status_codes'] = status_codes
                if m.groupdict()['path_type']:
                    af_dict['routes'][prefix]['index'][index]['path_type'] = path_type
                if m.groupdict()['next_hop']:
                    af_dict['routes'][prefix]['index'][index]['next_hop'] = next_hop
                if m.groupdict()['origin_codes']:
                    af_dict['routes'][prefix]['index'][index]['origin_codes'] = origin_codes

                # Parse numbers
                numbers = m.groupdict()['numbers']

                # Metric     LocPrf     Weight Path
                #    4444       100          0  10 3 10 20 30 40 50 60 70 80 90
                m1 = re.compile(r'^(?P<metric>[0-9]+)'
                                 r'(?P<space1>\s{4,10})'
                                 r'(?P<localprf>[0-9]+)'
                                 r'(?P<space2>\s{5,10})'
                                 r'(?P<weight>[0-9]+)'
                                 r'(?: *(?P<path>[0-9\{\}\s]+))?$').match(numbers)

                #    100        ---          0 10 20 30 40 50 60 70 80 90
                #    ---        100          0 10 20 30 40 50 60 70 80 90
                #    100        ---      32788 ---
                #    ---        100      32788 ---
                m2 = re.compile(r'^(?P<value>[0-9]+)'
                                 r'(?P<space>\s{2,21})'
                                 r'(?P<weight>[0-9]+)'
                                 r'(?: *(?P<path>[0-9\{\}\s]+))?$').match(numbers)

                #    ---        ---      32788 200 33299 51178 47751 {27016}
                m3 = re.compile(r'^(?P<weight>[0-9]+)'
                                 r' +(?P<path>[0-9\{\}\s]+)$').match(numbers)

                if m1:
                    af_dict['routes'][prefix]['index'][index]['metric'] = int(m1.groupdict()['metric'])
                    af_dict['routes'][prefix]['index'][index]['localprf'] = int(m1.groupdict()['localprf'])
                    af_dict['routes'][prefix]['index'][index]['weight'] = int(m1.groupdict()['weight'])
                    # Set path
                    if m1.groupdict()['path']:
                        af_dict['routes'][prefix]['index'][index]['path'] = m1.groupdict()['path'].strip()
                        continue
                elif m2:
                    af_dict['routes'][prefix]['index'][index]['weight'] = int(m2.groupdict()['weight'])
                    # Set metric or localprf
                    if len(m2.groupdict()['space']) > 10:
                        af_dict['routes'][prefix]['index'][index]['metric'] = int(m2.groupdict()['value'])
                    else:
                        af_dict['routes'][prefix]['index'][index]['localprf'] = int(m2.groupdict()['value'])
                    # Set path
                    if m2.groupdict()['path']:
                        af_dict['routes'][prefix]['index'][index]['path'] = m2.groupdict()['path'].strip()
                        continue
                elif m3:
                    af_dict['routes'][prefix]['index'][index]['weight'] = int(m3.groupdict()['weight'])
                    af_dict['routes'][prefix]['index'][index]['path'] = m3.groupdict()['path'].strip()
                continue

            # Route Distinguisher: 200:1
            # Route Distinguisher: 300:1 (default for vrf VRF1) VRF Router ID 10.94.44.44
            m = p7.match(line)
            if m:
                route_distinguisher = str(m.groupdict()['route_distinguisher'])
                new_address_family = original_address_family + ' RD ' + route_distinguisher

                # Init dict
                if 'address_family' not in route_dict['vrf'][vrf]['neighbor']\
                        [neighbor_id]:
                    route_dict['vrf'][vrf]['neighbor'][neighbor_id]\
                        ['address_family'] = {}
                if new_address_family not in route_dict['vrf'][vrf]['neighbor']\
                    [neighbor_id]['address_family']:
                    route_dict['vrf'][vrf]['neighbor'][neighbor_id]\
                        ['address_family'][new_address_family] = {}

                # Set keys
                route_dict['vrf'][vrf]['neighbor'][neighbor_id]\
                    ['address_family'][new_address_family]['bgp_table_version'] = bgp_table_version
                route_dict['vrf'][vrf]['neighbor'][neighbor_id]\
                    ['address_family'][new_address_family]['local_router_id'] = local_router_id
                route_dict['vrf'][vrf]['neighbor'][neighbor_id]\
                    ['address_family'][new_address_family]['route_distinguisher'] = route_distinguisher
                if m.groupdict()['default_vrf']:
                    route_dict['vrf'][vrf]['neighbor'][neighbor_id]\
                        ['address_family'][new_address_family]['default_vrf'] = \
                            str(m.groupdict()['default_vrf'])

                # Reset address_family key and af_dict for use in other regex
                address_family = new_address_family
                af_dict = route_dict['vrf'][vrf]['neighbor'][neighbor_id]\
                    ['address_family'][address_family]

                # Init routes dict
                if 'routes' not in af_dict:
                    af_dict['routes'] = {}
                    continue

            # Total number of prefixes 32
            m = p8.match(line.strip())
            if m:
                if 'total_num_of_prefixes' in route_dict:
                    # key already exists, add to it
                    route_dict['total_num_of_prefixes'] += int(m.groupdict()['total_num_of_prefixes'])
                else:
                    # key doesnt exist, create it
                    route_dict['total_num_of_prefixes'] = int(m.groupdict()['total_num_of_prefixes'])
                continue

        return route_dict


# ===============================================================
# Parser for:
#   * 'show bgp all neighbors {neighbor} routes'
#   * 'show bgp {address_family} all neighbors {neighbor} routes'
# ===============================================================
class ShowBgpAllNeighborsRoutes(ShowBgpAllNeighborsRoutesSuperParser, ShowBgpAllNeighborsRoutesSchema):

    ''' Parser for:
        * 'show bgp all neighbors {neighbor} routes'
        * 'show bgp {address_family} all neighbors {neighbor} routes'
    '''

    cli_command = ['show bgp {address_family} all neighbors {neighbor} routes',
                   'show bgp all neighbors {neighbor} routes',
                   ]

    def cli(self, neighbor, address_family='', output=None):

        if output is None:
            # Build command
            if address_family and neighbor:
                cmd = self.cli_command[0].format(address_family=address_family,
                                                 neighbor=neighbor)
            else:
                cmd = self.cli_command[1].format(neighbor=neighbor)
            # Execute command
            show_output = self.device.execute(cmd)
        else:
            show_output = output

        # Call super
        return super().cli(output=show_output, neighbor=neighbor,
                           address_family=address_family)


# ===========================================================
# Parser for:
#   * 'show bgp neighbors {neighbor} routes'
#   * 'show bgp {address_family} vrf {vrf} neighbors {neighbor} routes'
#   * 'show bgp {address_family} neighbors {neighbor} routes'
# ===========================================================
class ShowBgpNeighborsRoutes(ShowBgpAllNeighborsRoutesSuperParser, ShowBgpAllNeighborsRoutesSchema):

    ''' Parser for:
        * 'show bgp {address_family} vrf {vrf} neighbors {neighbor} routes'
        * 'show bgp {address_family} neighbors {neighbor} routes'
        * 'show bgp neighbors {neighbor} routes'
    '''

    cli_command = ['show bgp {address_family} vrf {vrf} neighbors {neighbor} routes',
                   'show bgp {address_family} neighbors {neighbor} routes',
                   'show bgp neighbors {neighbor} routes',
                   ]

    def cli(self, neighbor, address_family='', vrf='', output=None):

        if output is None:
            # Build command
            if address_family and neighbor and vrf:
                cmd = self.cli_command[0].format(address_family=address_family,
                                                 neighbor=neighbor,
                                                 vrf=vrf)
            elif address_family and neighbor:
                cmd = self.cli_command[1].format(address_family=address_family,
                                                 neighbor=neighbor)
            elif neighbor:
                cmd = self.cli_command[2].format(neighbor=neighbor)
            # Execute command
            show_output = self.device.execute(cmd)
        else:
            show_output = output

        # Call super
        return super().cli(output=show_output, neighbor=neighbor,
                           address_family=address_family, vrf=vrf)




# ==============================
# Schema for:
#   * 'show bgp all cluster-ids'
# ==============================
class ShowBgpAllClusterIdsSchema(MetaParser):

    ''' Schema for "show bgp all cluster-ids" '''

    schema = {
        'vrf':
            {Any():
                {Optional('cluster_id'): str,
                Optional('configured_id'): str,
                Optional('reflection_all_configured'): str,
                Optional('reflection_intra_cluster_configured'): str,
                Optional('reflection_intra_cluster_used'): str,
                Optional('list_of_cluster_ids'):
                    {Any():
                        {Optional('num_neighbors'): int,
                        Optional('client_to_client_reflection_configured'): str,
                        Optional('client_to_client_reflection_used'): str,
                        },
                    },
                },
            },
        }


# ==============================
# Parser for:
#   * 'show bgp all cluster-ids'
# ==============================
class ShowBgpAllClusterIds(ShowBgpAllClusterIdsSchema):

    ''' 
        Parser for "show bgp all cluster-ids"
        Note: this parser executes 'show vrf detail | inc \\(VRF' to collect vrf names.
    '''

    cli_command = 'show bgp all cluster-ids'

    def cli(self, output=None):
        # find vrf names
        # show vrf detail | inc \(VRF
        cmd_vrfs = r'show vrf detail | inc \(VRF'
        out_vrf = self.device.execute(cmd_vrfs)
        vrf_dict = {'0':'default'}
        p = re.compile(r'^\s*VRF +(?P<vrf_name>[0-9a-zA-Z]+)'
                        r' +\(+VRF +Id += +(?P<vrf_id>[0-9]+)+\)+;'
                        r' +default +(?P<other_data>.+)$')
        p1 = re.compile(r'^\s*Global +cluster-id: +(?P<cluster_id>[0-9\.]+)'
                        r' +\(+configured: +(?P<configured>[0-9\.]+)+\)$')
        p3 = re.compile(r'^\s*all +\(+inter-cluster +and +intra-cluster+\):'
                        r' +(?P<all_configured>[a-zA-Z]+)$')
        p4 = re.compile(r'^\s*intra-cluster:\s+(?P<intra_cluster_configured>[a-zA-Z]+)'
                        r' +(?P<intra_cluster_used>[a-zA-Z]+)$')
        p5 = re.compile(r'^\s*(?P<cluster_ids>[0-9\.]+)'
                    r' +(?P<num_neighbors>[0-9]+)'
                    r' +(?P<client_to_client_ref_configured>[a-zA-Z]+)'
                    r' +(?P<client_to_client_ref_used>[a-zA-Z]+)$')

        for line in out_vrf.splitlines():
            if not line:
                continue
            else:
                line = line.rstrip()

            # VRF VRF1 (VRF Id = 1); default RD 300:1; default VPNID <not set>
            m = p.match(line)
            if m:
                # Save variables for use later
                vrf_name = str(m.groupdict()['vrf_name'])
                vrf_id = str(m.groupdict()['vrf_id'])
                vrf_dict[vrf_id] = vrf_name
                continue


        # show bgp all cluster-ids
        cmd = self.cli_command
        out = self.device.execute(cmd)

        # Init vars
        sum_dict = {}
        cluster_id = None
        list_of_cluster_ids = dict()
        configured_id = ""
        reflection_all_configured = ""
        reflection_intra_cluster_configured = ""
        reflection_intra_cluster_used = ""


        for line in out.splitlines():
            if line.strip():
                line = line.rstrip()
            else:
                continue

            # Global cluster-id: 10.64.4.4 (configured: 0.0.0.0)
            m = p1.match(line)
            if m:
                # Save variables for use later
                cluster_id = str(m.groupdict()['cluster_id'])
                configured_id = str(m.groupdict()['configured'])

                if 'vrf' not in sum_dict:
                    sum_dict['vrf'] = {}

                continue

            #   all (inter-cluster and intra-cluster): ENABLED
            m = p3.match(line)
            if m:
                reflection_all_configured = m.groupdict()['all_configured'].lower()
                continue

            # intra-cluster:                         ENABLED       ENABLED
            m = p4.match(line)
            if m:
                reflection_intra_cluster_configured = m.groupdict()['intra_cluster_configured'].lower()
                reflection_intra_cluster_used = m.groupdict()['intra_cluster_used'].lower()
                continue

            # List of cluster-ids
            # Cluster-id  #-neighbors C2C-rfl-CFG C2C-rfl-USE
            # 192.168.1.1                2 DISABLED    DISABLED
            m = p5.match(line)
            if m:
                cluster_ids = m.groupdict()['cluster_ids']
                list_of_cluster_ids[cluster_ids] = cluster_ids
                list_of_cluster_ids[cluster_ids] = {}
                list_of_cluster_ids[cluster_ids]['num_neighbors'] = int(m.groupdict()['num_neighbors'])
                list_of_cluster_ids[cluster_ids]['client_to_client_reflection_configured'] = \
                    m.groupdict()['client_to_client_ref_configured'].lower()
                list_of_cluster_ids[cluster_ids]['client_to_client_reflection_used'] = \
                    m.groupdict()['client_to_client_ref_used'].lower()

                continue

        for vrf_id, vrf_name in vrf_dict.items():
            if 'vrf' not in sum_dict:
                sum_dict['vrf'] = {}
            if vrf_name not in sum_dict['vrf']:
                sum_dict['vrf'][vrf_name] = {}
            if 'cluster_id' not in sum_dict['vrf'][vrf_name]:
                if not cluster_id:
                    del sum_dict['vrf']
                if cluster_id:
                    sum_dict['vrf'][vrf_name]['cluster_id'] = cluster_id
                if configured_id:
                    sum_dict['vrf'][vrf_name]['configured_id'] = configured_id
                if reflection_all_configured:
                    sum_dict['vrf'][vrf_name]['reflection_all_configured'] = \
                        reflection_all_configured
                if reflection_intra_cluster_configured:
                    sum_dict['vrf'][vrf_name]['reflection_intra_cluster_configured'] = \
                        reflection_intra_cluster_configured
                if reflection_intra_cluster_used:
                    sum_dict['vrf'][vrf_name]['reflection_intra_cluster_used'] = \
                        reflection_intra_cluster_used
                if list_of_cluster_ids:
                    sum_dict['vrf'][vrf_name]['list_of_cluster_ids'] = list_of_cluster_ids
        return sum_dict


#-------------------------------------------------------------------------------


# ==============================================
# Schema for:
#   * 'show bgp all neighbors {neighbor} policy'
# ==============================================
class ShowBgpAllNeighborsPolicySchema(MetaParser):

    ''' Schema for "show bgp all neighbors {neighbor} policy" '''

    schema = {
        'vrf':
            {Any():
                {'neighbor':
                    {Any():
                        {'address_family':
                            {Any():
                                {Optional('nbr_af_route_map_name_in'): str,
                                 Optional('nbr_af_route_map_name_out'): str,
                                }
                            },
                        }
                    },
                }
            },
        }


# ==============================================
# Parser for:
#   * 'show bgp all neighbors {neighbor} policy'
# ==============================================
class ShowBgpAllNeighborsPolicy(ShowBgpAllNeighborsPolicySchema):

    ''' Parser for "show bgp all neighbors {neighbor} policy" '''

    cli_command = 'show bgp all neighbors {neighbor} policy'

    def cli(self, neighbor, output=None):
        if output is None:
            out = self.device.execute(self.cli_command.format(neighbor=neighbor))
        else:
            out = output

        # Neighbor: 10.4.6.6, Address-Family: VPNv4 Unicast (VRF1)
        # Neighbor: 10.251.15.5, Address-Family: VPNv4 Unicast (LABDR_HoC_AZS_Transit)
        p1 = re.compile(r'^\s*Neighbor: +(?P<neighbor>[\S]+),'
                        r' +Address-Family: +(?P<address_family>[\w\s\-\_]+)'
                        r'( +\((?P<vrf>[\S]+)\))?$')

        # route-map test in
        p2 = re.compile(r'^\s*route-map +(?P<route_map_name>\S+)'
                            r' +(?P<route_map_direction>[a-zA-Z]+)$')

        # Init dictionary
        policy_dict = {}

        for line in out.splitlines():
            line = line.rstrip()

            # Neighbor: 10.4.6.6, Address-Family: VPNv4 Unicast (VRF1)
            m = p1.match(line)
            if m:
                neighbor_id = str(m.groupdict()['neighbor'])
                address_family = str(m.groupdict()['address_family']).lower()
                if m.groupdict()['vrf']:
                    vrf = str(m.groupdict()['vrf'])
                else:
                    vrf = 'default'
                continue

            # route-map test in
            # route-map test out
            m = p2.match(line)
            if m:
                route_map_name = str(m.groupdict()['route_map_name'])
                route_map_direction = str(m.groupdict()['route_map_direction'])

                # Init dict
                sub_dict = policy_dict.setdefault('vrf', {}).setdefault(vrf, {}).\
                    setdefault('neighbor', {}).setdefault(neighbor_id, {}).\
                    setdefault('address_family', {}).setdefault(address_family, {})

                if route_map_direction == 'in':
                    sub_dict['nbr_af_route_map_name_in'] = route_map_name
                else:
                    sub_dict['nbr_af_route_map_name_out'] = route_map_name

                continue

        return policy_dict


#-------------------------------------------------------------------------------


# ======================================================
# Parser for 'show bgp l2vpn evpn evi {evi_id} route-type {route_type} '
# ======================================================

class ShowBgpL2vpnEvpnEviRouteTypeSchema(MetaParser):
    """Schema for show bgp l2vpn evpn evi {evi_id} route-type {route_type}"""

    schema = {
        'bgp_routing_table': str,
	'version': {
            Any():{
                'evi_num': str,
                'advertise': str,
                'refresh': str,
                Optional('import_path'): str,
                'vtep_loopback': str,
                'dist_loopback': str,
                Optional('origin'): str,
                Optional('metric'): int,
                Optional('local_pref'): int,
                Optional('community'): str,
                'extended_community': str,
                'encap': int,
                Optional('originator'): str,
                Optional('cluster_list'): str,
                'pmsi_flags': str,
                'tunnel_type': str,
                'length': int,
                'vni_id': int,
                'tunnel_id': str,
                Optional('vrf'): str,
                Optional('l3_vni'): int,
                Optional('local_router_mac'): str,
                Optional('core_irb_intf'): str,
                Optional('vtep_ip'): str,
                'rx_path_id': str,
                'tx_path_id': str,
                'date_time': str,
            },
        }
    }

class ShowBgpL2vpnEvpnEviRouteType(ShowBgpL2vpnEvpnEviRouteTypeSchema):
    """Parser for show bgp l2vpn evpn evi {evi_id} route-type {route_type}"""

    cli_command = 'show bgp l2vpn evpn evi {evi_id} route-type {route_type}'

    def cli(self, evi_id, route_type, output=None):
        if output is None:
            output = self.device.execute(self.cli_command.format(evi_id=evi_id, route_type=route_type))

        # BGP routing table entry for [3][172.11.1.22:99][0][32][172.11.1.1]/17, version 264
        p1 = re.compile(r"^BGP\s+routing\s+table\s+entry\s+for\s+\[+\d+\]+\[+(?P<bgp_routing_table>(\d{1,3}\.){3}\d{1,3}\:\d+)+\]+\S+\s+version+\s(?P<version>\S+)$")

        # Paths: (1 available, best #1, table evi_99)
        p2 = re.compile(r"^Paths:\s+\(1\s+available,\s+best\s+#1,\s+table\s+(?P<evi_num>\S+)\)$")

        # Not advertised to any peer
        p3_1 = re.compile(r"^(?P<advertise>\S+\s+\S+)\s+to\s+any\s+peer$")

        # Advertised to update-groups:
        p3_2 = re.compile(r"^(?P<advertise>\S+)\s+to\s+update-+groups:$")

        # Refresh Epoch 1
        p4 = re.compile(r"^Refresh\s+(?P<refresh>\S+\s+\d+)$")

        # Local, imported path from [3][172.11.1.2:99][0][32][172.11.1.2]/17 (global)
        p5 = re.compile(r"^Local,+\s+imported\s+path\s+from\s+(?P<import_path>\S+)+\s+\(+global\)$")

        # 172.11.1.2 (metric 30) (via default) from 172.11.1.11 (172.11.1.11)
        p6 = re.compile(
            r"^(?P<vtep_loopback>\S+)\s+\(+metric\s+\d+\)+\s+\(via\s+default+\)+\s+from+\s+(?P<dist_loopback>\S+)\s+\S+$")

        # 0.0.0.0 (via default) from 0.0.0.0 (172.11.1.22)
        p6_1 = re.compile(r"^(?P<vtep_loopback>(\d{1,3}\.){3}\d{1,3})+\s+\(+via\s+default\)+\s+from\s+(?P<dist_loopback>(\d{1,3}\.){3}\d{1,3})\s+\S+$")

        #      Origin incomplete, metric 0, localpref 100, valid, internal, best
        p7 = re.compile(
            r"^Origin\s+(?P<origin>\w+),\s+metric\s+(?P<metric>\d+),\s+localpref\s+(?P<local_pref>\d+),\s+valid,\s+internal,\s+best$")

        # Community: 999:999
        p7_1 = re.compile(r"^Community:\s+(?P<community>\S+)$")

        #      Extended Community: RT:9999:99 ENCAP:8
        p8 = re.compile(r"^Extended\s+Community:\s+(?P<extended_community>\S+)\s+ENCAP:(?P<encap>\d+)$")

        #      Originator: 172.11.2.1, Cluster list: 172.11.1.11
        p9 = re.compile(
            r"^Originator:\s+(?P<originator>(\d{1,3}\.){3}\d{1,3}),\s+Cluster\s+list:\s+(?P<cluster_list>(\d{1,3}\.){3}\d{1,3})$")

        #      PMSI Attribute: Flags:0x0, Tunnel type:IR, length 4, vni:200199, tunnel identifier: < Tunnel Endpoint: 172.11.1.1 >
        p10 = re.compile(
            r"PMSI\s+Attribute:\s+Flags:(?P<pmsi_flags>\S+),\s+Tunnel\s+type:+(?P<tunnel_type>\w+),\s+length\s+(?P<length>\d+),\s+vni:+(?P<vni_id>\d+),\s+tunnel\s+identifier:\s+(?P<tunnel_id>.*)$")

        # Local irb vxlan vtep:
        p11 = re.compile(r"^Local\s+irb\s+(?P<vxlan_vtep>\w+\s+\w+)$")

        #        vrf:not found, l3-vni:0
        p12 = re.compile(r"^vrf:+(?P<vrf>\w+\s+\w+),\s+l3-vni:+(?P<l3_vni>\d+)$")

        #        local router mac:0000.0000.0000
        p13 = re.compile(r"^local\s+router\s+mac:+(?P<local_router_mac>\S+)$")

        #        core-irb interface:(not found)
        p14 = re.compile(r"^core-irb\s+interface:+(?P<core_irb_intf>\S+\s+\S+)$")

        #        vtep-ip:172.11.1.22
        p15 = re.compile(r"^vtep-ip:+(?P<vtep_ip>\S+)$")

        #      rx pathid: 0, tx pathid: 0x0
        p16 = re.compile(r"^rx\s+pathid:\s+(?P<rx_path_id>\S+),\s+tx\s+pathid:\s+(?P<tx_path_id>\S+)$")

        #      Updated on Jan 22 2023 07:59:46 UTC
        p17 = re.compile(r"^Updated\s+on\s+(?P<date_time>\S+\s+\S+\s+\S+\s+\S+\s+\S+)$")

        ret_dict = {}

        for line in output.splitlines():
            line = line.strip()

            # BGP routing table entry for [3][172.11.1.22:99][0][32][172.11.1.1]/17, version 264
            m = p1.match(line)
            if m:
                group = m.groupdict()
                ret_dict.update({'bgp_routing_table': group['bgp_routing_table']})
                version = int(group['version'])
                bgp_dict = ret_dict.setdefault('version', {})
                version_dict = bgp_dict.setdefault(version, {})
                continue

            # Paths: (1 available, best #1, table evi_99)
            m = p2.match(line)
            if m:
                group = m.groupdict()
                version_dict.update({'evi_num': group['evi_num']})
                continue

            # Not advertised to any peer
            m = p3_1.match(line)
            if m:
                group = m.groupdict()
                version_dict['advertise'] = group['advertise']
                continue

            # Advertised to update-groups:
            m = p3_2.match(line)
            if m:
                group = m.groupdict()
                version_dict['advertise'] = group['advertise']
                continue

            # Refresh Epoch 1
            m = p4.match(line)
            if m:
                group = m.groupdict()
                version_dict['refresh'] = group['refresh']
                continue

            # Local, imported path from [3][172.11.1.2:99][0][32][172.11.1.2]/17 (global)
            m = p5.match(line)
            if m:
                group = m.groupdict()
                version_dict['import_path'] = group['import_path']
                continue

            # 172.11.1.2 (metric 30) (via default) from 172.11.1.11 (172.11.1.11)
            m = p6.match(line)
            if m:
                group = m.groupdict()
                version_dict['vtep_loopback'] = group['vtep_loopback']
                version_dict['dist_loopback'] = group['dist_loopback']
                continue

            # 0.0.0.0 (via default) from 0.0.0.0 (172.11.1.22)
            m = p6_1.match(line)
            if m:
                group = m.groupdict()
                version_dict['vtep_loopback'] = group['vtep_loopback']
                version_dict['dist_loopback'] = group['dist_loopback']
                continue

            #      Origin incomplete, metric 0, localpref 100, valid, internal, best
            m = p7.match(line)
            if m:
                group = m.groupdict()
                version_dict['origin'] = group['origin']
                version_dict['metric'] = int(group['metric'])
                version_dict['local_pref'] = int(group['local_pref'])
                continue

            #  Community: 999:999
            m = p7_1.match(line)
            if m:
                group = m.groupdict()
                version_dict['community'] = group['community']
                continue

            #      Extended Community: RT:9999:99 ENCAP:8
            m = p8.match(line)
            if m:
                group = m.groupdict()
                version_dict['extended_community'] = group['extended_community']
                version_dict['encap'] = int(group['encap'])
                continue

            #      Originator: 172.11.2.1, Cluster list: 172.11.1.11
            m = p9.match(line)
            if m:
                group = m.groupdict()
                version_dict['originator'] = group['originator']
                version_dict['cluster_list'] = group['cluster_list']
                continue

            #      PMSI Attribute: Flags:0x0, Tunnel type:IR, length 4, vni:200199, tunnel identifier: < Tunnel Endpoint: 172.11.1.1 >
            m = p10.match(line)
            if m:
                group = m.groupdict()
                version_dict['pmsi_flags'] = group['pmsi_flags']
                version_dict['tunnel_type'] = group['tunnel_type']
                version_dict['length'] = int(group['length'])
                version_dict['vni_id'] = int(group['vni_id'])
                version_dict['tunnel_id'] = group['tunnel_id']
                continue

            #        vrf:not found, l3-vni:0
            m = p12.match(line)
            if m:
                group = m.groupdict()
                version_dict['vrf'] = group['vrf']
                version_dict['l3_vni'] = int(group['l3_vni'])
                continue

            #        local router mac:0000.0000.0000
            m = p13.match(line)
            if m:
                group = m.groupdict()
                version_dict['local_router_mac'] = group['local_router_mac']
                continue

            #        core-irb interface:(not found)
            m = p14.match(line)
            if m:
                group = m.groupdict()
                version_dict['core_irb_intf'] = group['core_irb_intf']
                continue

            #        vtep-ip:172.11.1.22
            m = p15.match(line)
            if m:
                group = m.groupdict()
                version_dict['vtep_ip'] = group['vtep_ip']
                continue

            #      rx pathid: 0, tx pathid: 0x0
            m = p16.match(line)
            if m:
                group = m.groupdict()
                version_dict['rx_path_id'] = group['rx_path_id']
                version_dict['tx_path_id'] = group['tx_path_id']
                continue

            #      Updated on Jan 22 2023 07:59:46 UTC
            m = p17.match(line)
            if m:
                group = m.groupdict()
                version_dict['date_time'] = group['date_time']
                continue

        return ret_dict

class ShowBgpAllSummaryNetworkSchema(MetaParser):
    """Schema for show bgp * all summary | include network"""
    schema = {
        'network_entries': {
            'total_network_entries': int,
            'memory_usage_bytes': int,
            'total_network_peaked': int,
            'peaked_at': str,
            'peaked_duration': str,
        }
    }

class ShowBgpAllSummaryNetwork(ShowBgpAllSummaryNetworkSchema):
    """Parser for show bgp * all summary | include network"""

    cli_command = 'show bgp * all summary'
    include = ['network']

    def cli(self, output=None):
        if output is None:
            output = self.device.execute(self.cli_command)

        # Initialize the parsed dictionary
        parsed_dict = {}

        # Regular expressions for parsing the output
        # 2049580 network entries using 590279040 bytes of memory
        p1 = re.compile(r'^(?P<total_network_entries>\d+) network entries using (?P<memory_usage_bytes>\d+) bytes of memory$')
        # 2049580 networks peaked at 15:32:57 Jan 16 2024 EST (00:00:27.974 ago)
        p2 = re.compile(r'^(?P<total_network_peaked>\d+) networks peaked at (?P<peaked_time>\d{2}:\d{2}:\d{2} [A-Za-z]{3} \d{1,2} \d{4} [A-Z]{3}) (?P<peaked_duration>\(\d{2}:\d{2}:\d{2}\.\d{3} ago\))')

        for line in output.splitlines():
            line = line.strip()

            # 2049580 network entries using 590279040 bytes of memory
            m = p1.match(line)
            if m:
                group = m.groupdict()
                network_entries = parsed_dict.setdefault('network_entries', {})
                network_entries['total_network_entries'] = int(group['total_network_entries'])
                network_entries['memory_usage_bytes'] = int(group['memory_usage_bytes'])
                continue

            # 2049580 networks peaked at 15:32:57 Jan 16 2024 EST (00:00:27.974 ago)
            m = p2.match(line)
            if m:
                group = m.groupdict()
                network_entries = parsed_dict.setdefault('network_entries', {})
                network_entries['total_network_peaked'] = int(group['total_network_peaked'])
                network_entries['peaked_at'] = group['peaked_time']
                network_entries['peaked_duration'] = group['peaked_duration']
                continue

        return parsed_dict
