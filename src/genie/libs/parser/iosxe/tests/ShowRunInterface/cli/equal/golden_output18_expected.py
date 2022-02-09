expected_output = {
    "interfaces": {
        "Vlan10": {
            "fhrps": {
                "1": {
                    "group_id": "1",
                    'ips': ['1.1.1.2', '11.11.11.11 secondary', '111.111.111.111 secondary'],
                    "priority": "90",
                    "timers": "msec 150 160",
                    "encryption_level": "7",
                    "encryption_string": "070C285F4D06"
                },
                "2": {
                    "group_id": "2",
                    "encryption_level": "7",
                    "encryption_string": "070C285F4D06",
                    "ips": ["2.2.2.2"],
                    "preempt": True,
                    "timers": "msec 150 msec 160",
                    "priority": "200"
                },
                "20": {
                    "group_id": "20",
                    'ips': ['20.20.20.20', '22.22.22.22 secondary', '222.222.222.222 secondary'],
                    "priority": "100",
                    "timers": "150 160",
                    "encryption_string": "cisco"
                }
            },
            "ipv4": {
                "ip": "1.1.1.1",
                "netmask": "255.255.255.0"
            }
        }
    }
}
