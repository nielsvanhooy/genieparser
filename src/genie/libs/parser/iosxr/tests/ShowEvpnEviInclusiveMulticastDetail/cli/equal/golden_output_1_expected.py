

expected_output = {
    'vpn_id':{
        1:{
            'originating_ip':{
                '1.1.1.1':{
                    'encap':'SRv6',
                    'ethertag':0,
                    'tepid':'0xffffffff',
                    'pmsi_type':6,
                    'nexthop':'::',
                    'sr_te_info':'N/A',
                    'sid':'cafe:0:128:e1aa::',
                    'source':'Local',
                    'e_tree':'Root'
                },
                '2.2.2.2':{
                    'encap':'SRv6',
                    'ethertag':0,
                    'tepid':'0x05000001',
                    'pmsi_type':6,
                    'nexthop':'2.2.2.2',
                    'sr_te_info':'N/A',
                    'sid':'cafe:0:200:e001::',
                    'source':'Remote',
                    'e_tree':'Root'
                },
                '3.3.3.3':{
                    'encap':'SRv6',
                    'ethertag':0,
                    'tepid':'0x05000003',
                    'pmsi_type':6,
                    'nexthop':'3.3.3.3',
                    'sr_te_info':'N/A',
                    'sid':'cafe:0:300:e001::',
                    'source':'Remote',
                    'e_tree':'Root'
                },
                '4.4.4.4':{
                    'encap':'SRv6',
                    'ethertag':0,
                    'tepid':'0x05000002',
                    'pmsi_type':6,
                    'nexthop':'4.4.4.4',
                    'sr_te_info':'N/A',
                    'sid':'cafe:0:400:e001::',
                    'source':'Remote',
                    'e_tree':'Root'
                }
            }
        }
    }
}