expected_output = {
    'policy_map': {
        'policy-cbwfq-1': {'class': {
            'class-gold': {'bandwidth_percent': '40',
                           'random_detect': ['dscp-based', 'ecn']},
            'class-silver': {'bandwidth_percent': '20',
                             'random_detect': ['dscp-based', 'ecn']},
            'class-bronze': {'bandwidth_percent': '10',
                             'random_detect': ['dscp-based', 'ecn']},
            'management-traffic': {'bandwidth_percent': '1',
                                   'random_detect': ['dscp-based', 'ecn'],
                                   'qos_set': {'dscp': 'af21'}},
            'class-default': {'bandwidth_percent': '29',
                              'random_detect': ['dscp-based', 'ecn'],
                              'qos_set': {'dscp': 'default'}}}}
    }
}
