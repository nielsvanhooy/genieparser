expected_output = {
    'ip_routes': {
        1: {'vrf': '3rdParty', 'vrf_global': '', 'subnet': '139.156.202.96',
            'subnet_mask': '255.255.255.240', 'next_hop': '10.194.48.110',
            'forward_address': '', 'route_name': '', 'metric': '',
            'track_object': '', 'permanent': '', 'tag': '',
            'parsing_leftovers': ''},
        2: {'vrf': '3rdParty', 'vrf_global': '', 'subnet': '139.156.202.96',
            'subnet_mask': '255.255.255.240', 'next_hop': '10.194.48.110',
            'forward_address': '', 'route_name': 'Management', 'metric': '',
            'track_object': '', 'permanent': '', 'tag': '',
            'parsing_leftovers': ''},
        3: {'vrf': '', 'vrf_global': '', 'subnet': '139.156.202.96',
            'subnet_mask': '255.255.255.240', 'next_hop': '10.194.48.110',
            'forward_address': '', 'route_name': '', 'metric': '',
            'track_object': '', 'permanent': '', 'tag': '',
            'parsing_leftovers': ''},
        4: {'vrf': '', 'vrf_global': '', 'subnet': '139.156.202.96',
            'subnet_mask': '255.255.255.251', 'next_hop': 'Vlan100',
            'forward_address': '', 'route_name': '', 'metric': '',
            'track_object': '', 'permanent': '', 'tag': '',
            'parsing_leftovers': ''},
        5: {'vrf': '', 'vrf_global': '', 'subnet': '139.156.202.96',
            'subnet_mask': '255.255.255.240', 'next_hop': 'Vlan100',
            'forward_address': '10.194.48.110', 'route_name': '', 'metric': '',
            'track_object': '', 'permanent': '', 'tag': '',
            'parsing_leftovers': ''},
        6: {'vrf': '', 'vrf_global': '', 'subnet': '139.156.202.96',
            'subnet_mask': '255.255.255.240',
            'next_hop': 'GigabitEthernet0/1/1',
            'forward_address': '', 'route_name': '', 'metric': '',
            'track_object': '', 'permanent': '', 'tag': '',
            'parsing_leftovers': ''},
        7: {'vrf': '', 'vrf_global': '', 'subnet': '139.156.202.96',
            'subnet_mask': '255.255.255.240',
            'next_hop': 'GigabitEthernet0/1/1',
            'forward_address': '', 'route_name': '', 'metric': '240',
            'track_object': '', 'permanent': '', 'tag': '',
            'parsing_leftovers': ''},
        8: {'vrf': '', 'vrf_global': '', 'subnet': '139.156.202.96',
            'subnet_mask': '255.255.255.240',
            'next_hop': 'GigabitEthernet0/1/1',
            'forward_address': '10.194.48.110', 'route_name': '', 'metric': '',
            'track_object': '', 'permanent': '', 'tag': '',
            'parsing_leftovers': ''},
        9: {'vrf': '', 'vrf_global': '', 'subnet': '192.168.1.0',
            'subnet_mask': '255.255.255.0', 'next_hop': 'GigabitEthernet0/0/0',
            'forward_address': '213.162.171.193', 'route_name': 'Management',
            'metric': '', 'track_object': '100', 'permanent': '', 'tag': '',
            'parsing_leftovers': ''},
        10: {'vrf': '', 'vrf_global': '', 'subnet': '139.156.202.96',
             'subnet_mask': '255.255.255.240', 'next_hop': '10.194.48.110',
             'forward_address': '', 'route_name': 'Management', 'metric': '',
             'track_object': '', 'permanent': '', 'tag': '',
             'parsing_leftovers': ''},
        11: {'vrf': '', 'vrf_global': '', 'subnet': '139.156.202.96',
             'subnet_mask': '255.255.255.240', 'next_hop': '10.194.48.110',
             'forward_address': '', 'route_name': '', 'metric': '255',
             'track_object': '', 'permanent': '', 'tag': '',
             'parsing_leftovers': ''},
        12: {'vrf': '', 'vrf_global': '', 'subnet': '139.156.202.96',
             'subnet_mask': '255.255.255.240', 'next_hop': 'Vlan100',
             'forward_address': '', 'route_name': '', 'metric': '255',
             'track_object': '', 'permanent': '', 'tag': '',
             'parsing_leftovers': ''},
        13: {'vrf': '', 'vrf_global': '', 'subnet': '139.156.202.96',
             'subnet_mask': '255.255.255.240', 'next_hop': 'Vlan100',
             'forward_address': '10.194.48.110', 'route_name': '',
             'metric': '255',
             'track_object': '', 'permanent': '', 'tag': '',
             'parsing_leftovers': ''},
        14: {'vrf': '', 'vrf_global': '', 'subnet': '139.156.202.96',
             'subnet_mask': '255.255.255.240', 'next_hop': '10.194.48.110',
             'forward_address': '', 'route_name': '', 'metric': '',
             'track_object': '100', 'permanent': '', 'tag': '',
             'parsing_leftovers': ''},
        15: {'vrf': '', 'vrf_global': '', 'subnet': '139.156.202.96',
             'subnet_mask': '255.255.255.240', 'next_hop': 'Vlan100',
             'forward_address': '', 'route_name': '', 'metric': '',
             'track_object': '100', 'permanent': '', 'tag': '',
             'parsing_leftovers': ''},
        16: {'vrf': '', 'vrf_global': '', 'subnet': '139.156.202.96',
             'subnet_mask': '255.255.255.240', 'next_hop': 'Vlan100',
             'forward_address': '10.194.48.110', 'route_name': '',
             'metric': '',
             'track_object': '100', 'permanent': '', 'tag': '',
             'parsing_leftovers': ''},
        17: {'vrf': '', 'vrf_global': '', 'subnet': '139.156.202.96',
             'subnet_mask': '255.255.255.240',
             'next_hop': 'GigabitEthernet0/1/1',
             'forward_address': '10.194.48.110', 'route_name': '',
             'metric': '',
             'track_object': '100', 'permanent': '', 'tag': '',
             'parsing_leftovers': ''},
        18: {'vrf': '', 'vrf_global': '', 'subnet': '139.156.202.96',
             'subnet_mask': '255.255.255.240', 'next_hop': '10.194.48.110',
             'forward_address': '', 'route_name': '', 'metric': '255',
             'track_object': '100', 'permanent': '', 'tag': '',
             'parsing_leftovers': ''},
        19: {'vrf': '', 'vrf_global': '', 'subnet': '139.156.202.96',
             'subnet_mask': '255.255.255.240', 'next_hop': 'Vlan100',
             'forward_address': '', 'route_name': '', 'metric': '255',
             'track_object': '100', 'permanent': '', 'tag': '',
             'parsing_leftovers': ''},
        20: {'vrf': '', 'vrf_global': '', 'subnet': '139.156.202.96',
             'subnet_mask': '255.255.255.240', 'next_hop': 'Vlan100',
             'forward_address': '10.194.48.110', 'route_name': '',
             'metric': '255',
             'track_object': '100', 'permanent': '', 'tag': '',
             'parsing_leftovers': ''},
        21: {'vrf': '', 'vrf_global': '', 'subnet': '139.156.202.96',
             'subnet_mask': '255.255.255.240',
             'next_hop': 'GigabitEthernet0/1/1',
             'forward_address': '10.194.48.110', 'route_name': '',
             'metric': '255',
             'track_object': '100', 'permanent': '', 'tag': '',
             'parsing_leftovers': ''},
        22: {'vrf': '', 'vrf_global': '', 'subnet': '10.73.238.0',
             'subnet_mask': '255.255.254.0', 'next_hop': '10.73.224.1',
             'forward_address': '', 'route_name': 'Dat"a`', 'metric': '',
             'track_object': '', 'permanent': '', 'tag': '',
             'parsing_leftovers': ''},
        23: {'vrf': '', 'vrf_global': '', 'subnet': '60.250.233.50',
             'subnet_mask': '255.255.255.255',
             'next_hop': 'GigabitEthernet0/0',
             'forward_address': '115.186.231.1',
             'route_name': 'Taiwan=Ware&house-TWTL-EP.10.1.1.1', 'metric': '',
             'track_object': '', 'permanent': '', 'tag': '',
             'parsing_leftovers': ''},
        24: {'vrf': 'wlvbnavpn-11495', 'vrf_global': '',
             'subnet': '10.122.230.176', 'subnet_mask': '255.255.255.255',
             'next_hop': 'Cellular0/2/0', 'forward_address': '',
             'route_name': 'Loopback0_WBLM1151', 'metric': '10',
             'track_object': '', 'permanent': 'permanent', 'tag': '',
             'parsing_leftovers': ''},
        25: {'vrf': '', 'vrf_global': '', 'subnet': '139.156.202.96',
             'subnet_mask': '255.255.255.240', 'next_hop': 'Serial0/0/0:0.110',
             'forward_address': '10.194.48.110', 'route_name': '',
             'metric': '255',
             'track_object': '100', 'permanent': '', 'tag': '',
             'parsing_leftovers': ''},
        26: {'vrf': 'infinity01', 'vrf_global': 'global',
             'subnet': '10.100.0.0',
             'subnet_mask': '255.255.0.0', 'next_hop': 'FastEthernet4',
             'forward_address': '222.229.224.185',
             'route_name': 'Lala3-VPN-Inifnity-ED', 'metric': '',
             'track_object': '', 'permanent': '', 'tag': '',
             'parsing_leftovers': ''}}}