expected_output = {
    'ip_routes': {
        1: {'forward_address': '',
            'metric': '',
            'next_hop': '10.194.48.110',
            'parsing_leftovers': '',
            'permanent': '',
            'route_name': '',
            'subnet': '139.156.202.96',
            'subnet_mask': '255.255.255.240',
            'track_object': '',
            'vrf': '3rdParty',
            'vrf_global': ''},
        2: {'forward_address': '',
            'metric': '',
            'next_hop': '10.194.48.110',
            'parsing_leftovers': '',
            'permanent': '',
            'route_name': 'Management',
            'subnet': '139.156.202.96',
            'subnet_mask': '255.255.255.240',
            'track_object': '',
            'vrf': '3rdParty',
            'vrf_global': ''},
        3: {'forward_address': '',
            'metric': '',
            'next_hop': '10.194.48.110',
            'parsing_leftovers': '',
            'permanent': '',
            'route_name': '',
            'subnet': '139.156.202.96',
            'subnet_mask': '255.255.255.240',
            'track_object': '',
            'vrf': '',
            'vrf_global': ''},
        4: {'forward_address': '',
            'metric': '',
            'next_hop': 'Vlan100',
            'parsing_leftovers': '',
            'permanent': '',
            'route_name': '',
            'subnet': '139.156.202.96',
            'subnet_mask': '255.255.255.251',
            'track_object': '',
            'vrf': '',
            'vrf_global': ''},
        5: {'forward_address': '10.194.48.110',
            'metric': '',
            'next_hop': 'Vlan100',
            'parsing_leftovers': '',
            'permanent': '',
            'route_name': '',
            'subnet': '139.156.202.96',
            'subnet_mask': '255.255.255.240',
            'track_object': '',
            'vrf': '',
            'vrf_global': ''},
        6: {'forward_address': '',
            'metric': '',
            'next_hop': 'GigabitEthernet0/1/1',
            'parsing_leftovers': '',
            'permanent': '',
            'route_name': '',
            'subnet': '139.156.202.96',
            'subnet_mask': '255.255.255.240',
            'track_object': '',
            'vrf': '',
            'vrf_global': ''},
        7: {'forward_address': '',
            'metric': '240',
            'next_hop': 'GigabitEthernet0/1/1',
            'parsing_leftovers': '',
            'permanent': '',
            'route_name': '',
            'subnet': '139.156.202.96',
            'subnet_mask': '255.255.255.240',
            'track_object': '',
            'vrf': '',
            'vrf_global': ''},
        8: {'forward_address': '10.194.48.110',
            'metric': '',
            'next_hop': 'GigabitEthernet0/1/1',
            'parsing_leftovers': '',
            'permanent': '',
            'route_name': '',
            'subnet': '139.156.202.96',
            'subnet_mask': '255.255.255.240',
            'track_object': '',
            'vrf': '',
            'vrf_global': ''},
        9: {'forward_address': '213.162.171.193',
            'metric': '',
            'next_hop': 'GigabitEthernet0/0/0',
            'parsing_leftovers': '',
            'permanent': '',
            'route_name': 'Management',
            'subnet': '192.168.1.0',
            'subnet_mask': '255.255.255.0',
            'track_object': '100',
            'vrf': '',
            'vrf_global': ''},
        10: {'forward_address': '',
             'metric': '',
             'next_hop': '10.194.48.110',
             'parsing_leftovers': '',
             'permanent': '',
             'route_name': 'Management',
             'subnet': '139.156.202.96',
             'subnet_mask': '255.255.255.240',
             'track_object': '',
             'vrf': '',
             'vrf_global': ''},
        11: {'forward_address': '',
             'metric': '255',
             'next_hop': '10.194.48.110',
             'parsing_leftovers': '',
             'permanent': '',
             'route_name': '',
             'subnet': '139.156.202.96',
             'subnet_mask': '255.255.255.240',
             'track_object': '',
             'vrf': '',
             'vrf_global': ''},
        12: {'forward_address': '',
             'metric': '255',
             'next_hop': 'Vlan100',
             'parsing_leftovers': '',
             'permanent': '',
             'route_name': '',
             'subnet': '139.156.202.96',
             'subnet_mask': '255.255.255.240',
             'track_object': '',
             'vrf': '',
             'vrf_global': ''},
        13: {'forward_address': '10.194.48.110',
             'metric': '255',
             'next_hop': 'Vlan100',
             'parsing_leftovers': '',
             'permanent': '',
             'route_name': '',
             'subnet': '139.156.202.96',
             'subnet_mask': '255.255.255.240',
             'track_object': '',
             'vrf': '',
             'vrf_global': ''},
        14: {'forward_address': '',
             'metric': '',
             'next_hop': '10.194.48.110',
             'parsing_leftovers': '',
             'permanent': '',
             'route_name': '',
             'subnet': '139.156.202.96',
             'subnet_mask': '255.255.255.240',
             'track_object': '100',
             'vrf': '',
             'vrf_global': ''},
        15: {'forward_address': '',
             'metric': '',
             'next_hop': 'Vlan100',
             'parsing_leftovers': '',
             'permanent': '',
             'route_name': '',
             'subnet': '139.156.202.96',
             'subnet_mask': '255.255.255.240',
             'track_object': '100',
             'vrf': '',
             'vrf_global': ''},

        16: {'forward_address': '10.194.48.110',
             'metric': '',
             'next_hop': 'Vlan100',
             'parsing_leftovers': '',
             'permanent': '',
             'route_name': '',
             'subnet': '139.156.202.96',
             'subnet_mask': '255.255.255.240',
             'track_object': '100',
             'vrf': '',
             'vrf_global': ''},
        17: {'forward_address': '10.194.48.110',
             'metric': '',
             'next_hop': 'GigabitEthernet0/1/1',
             'parsing_leftovers': '',
             'permanent': '',
             'route_name': '',
             'subnet': '139.156.202.96',
             'subnet_mask': '255.255.255.240',
             'track_object': '100',
             'vrf': '',
             'vrf_global': ''},
        18: {'forward_address': '',
             'metric': '255',
             'next_hop': '10.194.48.110',
             'parsing_leftovers': '',
             'permanent': '',
             'route_name': '',
             'subnet': '139.156.202.96',
             'subnet_mask': '255.255.255.240',
             'track_object': '100',
             'vrf': '',
             'vrf_global': ''},
        19: {'forward_address': '',
             'metric': '255',
             'next_hop': 'Vlan100',
             'parsing_leftovers': '',
             'permanent': '',
             'route_name': '',
             'subnet': '139.156.202.96',
             'subnet_mask': '255.255.255.240',
             'track_object': '100',
             'vrf': '',
             'vrf_global': ''},
        20: {'forward_address': '10.194.48.110',
             'metric': '255',
             'next_hop': 'Vlan100',
             'parsing_leftovers': '',
             'permanent': '',
             'route_name': '',
             'subnet': '139.156.202.96',
             'subnet_mask': '255.255.255.240',
             'track_object': '100',
             'vrf': '',
             'vrf_global': ''},
        21: {'forward_address': '10.194.48.110',
             'metric': '255',
             'next_hop': 'GigabitEthernet0/1/1',
             'parsing_leftovers': '',
             'permanent': '',
             'route_name': '',
             'subnet': '139.156.202.96',
             'subnet_mask': '255.255.255.240',
             'track_object': '100',
             'vrf': '',
             'vrf_global': ''},
        22: {'forward_address': '',
             'metric': '',
             'next_hop': '10.73.224.1',
             'parsing_leftovers': '',
             'permanent': '',
             'route_name': 'Dat"a`',
             'subnet': '10.73.238.0',
             'subnet_mask': '255.255.254.0',
             'track_object': '',
             'vrf': '',
             'vrf_global': ''},
        23: {'forward_address': '115.186.231.1',
             'metric': '',
             'next_hop': 'GigabitEthernet0/0',
             'parsing_leftovers': '',
             'permanent': '',
             'route_name': 'Taiwan=Ware&house-TWTL-EP.10.1.1.1',
             'subnet': '60.250.233.50',
             'subnet_mask': '255.255.255.255',
             'track_object': '',
             'vrf': '',
             'vrf_global': ''},
        24: {'forward_address': '',
             'metric': '10',
             'next_hop': 'Cellular0/2/0',
             'parsing_leftovers': '',
             'permanent': 'permanent',
             'route_name': 'Loopback0_WBLM1151',
             'subnet': '10.122.230.176',
             'subnet_mask': '255.255.255.255',
             'track_object': '',
             'vrf': 'wlvbnavpn-11495',
             'vrf_global': ''},
        25: {'forward_address': '10.194.48.110',
             'metric': '255',
             'next_hop': 'Serial0/0/0:0.110',
             'parsing_leftovers': '',
             'permanent': '',
             'route_name': '',
             'subnet': '139.156.202.96',
             'subnet_mask': '255.255.255.240',
             'track_object': '100',
             'vrf': '',
             'vrf_global': ''},
        26: {'forward_address': '222.229.224.185',
             'metric': '',
             'next_hop': 'FastEthernet4',
             'parsing_leftovers': '',
             'permanent': '',
             'route_name': 'Lala3-VPN-Inifnity-ED',
             'subnet': '10.100.0.0',
             'subnet_mask': '255.255.0.0',
             'track_object': '',
             'vrf': 'infinity01',
             'vrf_global': 'global'}
    }
}