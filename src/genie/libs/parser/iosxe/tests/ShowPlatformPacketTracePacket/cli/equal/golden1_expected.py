
expected_output = \
{'packets': {11: {'cbug_id': 115,
                  'iosd_flow': {'infra': {'packet_rcvd_from': 'DATAPLANE',
                                          'pkt_direction': 'IN'},
                                'ip': {'destination': '172.20.2.54',
                                       'interface': 'GigabitEthernet1',
                                       'packet_enqueued_in': 'IP layer',
                                       'pkt_direction': 'IN',
                                       'source': '172.20.2.55'},
                                'tcp': {'pkt_direction': 'IN',
                                        'tcp0': 'I NoTCB 172.20.2.55:43520 '
                                                '172.20.2.54:22 seq 1565917747 '
                                                'ACK 140303057  WIN 63840'}},
                  'path_trace': {'cft': {'api': 'cft_handle_pkt',
                                         'calling_feature': 'STILE',
                                         'cft_bucket_number': '206290',
                                         'cft_l3_payload_size': '20',
                                         'cft_pkt_ind_flags': '0x00000002',
                                         'cft_pkt_ind_valid': '0x00009bff',
                                         'direction': 'Input',
                                         'input_vrf_idx': '0',
                                         'packet_capabilities': '0x000000af',
                                         'pkt_sb_num_flows': '0',
                                         'pkt_sb_state': '0',
                                         'pkt_sb_tuple_epoch': '0',
                                         'returned_cft_error': '0',
                                         'returned_fid': '0xe9328b50',
                                         'triplet_counter': '0',
                                         'triplet_network_start': '0x00000000',
                                         'triplet_triplet_flags': '0x00000000',
                                         'triplet_vrf_idx': '0',
                                         'tuple_dst_ip': '172.20.2.54',
                                         'tuple_dst_port': '22',
                                         'tuple_l3_protocol': 'IPV4',
                                         'tuple_l4_protocol': 'TCP',
                                         'tuple_src_ip': '172.20.2.55',
                                         'tuple_src_port': '43520',
                                         'tuple_vrfid': '0'},
                                 'ipv4_input': {'destination': '172.20.2.54',
                                                'dst_port': '22',
                                                'input': 'GigabitEthernet1',
                                                'output': '<unknown>',
                                                'protocol': '6 (TCP)',
                                                'source': '172.20.2.55',
                                                'src_port': '43520'},
                                 'nbar': {'classification_id': '[IANA-L4:22]',
                                          'classification_name': 'ssh',
                                          'classification_source': 'Unknown',
                                          'classification_state': 'Final',
                                          'is_pa_split_packet': 'False',
                                          'number_of_extracted_fields': '0',
                                          'number_of_matched_sub_classifications': '0',
                                          'packet_number_in_flow': 'N/A',
                                          'tph_mqc_bitmask_value': '0x0'},
                                 'qos': {'action': 'SET',
                                         'direction': 'Ingress',
                                         'fields': 'DSCP'}},
                  'summary': {'input': 'GigabitEthernet1',
                              'output': 'internal0/0/rp:0',
                              'start_timestamp': '07/27/2021 09:34:28.261898',
                              'start_timestamp_ns': 19591546248064016,
                              'state': 'PUNT 11  (For-us data)',
                              'stop_timestamp': '07/27/2021 09:34:28.261921',
                              'stop_timestamp_ns': 19591546248087028}}}}
