expected_output = {
    'interfaces': {
        'GigabitEthernet0/5/6': {
            'cdp': 'enable',
            'description': 'wan_pyats',
            'ipv4': {
                '192.168.168.1': {
                    'ip': '192.168.168.1',
                    'netmask': '255.255.255.252',
                    'primary': True,
                },
            },
            'load_interval': '30',
            'mpls_ip': "enabled",
            'mtu': '9198',
            'negotiation_auto': True,
            'output_policy': 'PYATS_TEST'
        }
    }
}
