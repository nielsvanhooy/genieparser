expected_output = {
   "vrf":{
      "default":{
         "address_family":{
            "l2vpn_evpn":{
               "prefix":"[1][0000.0000.0000.0001.0500][10001]/120",
               "rd":"10.0.0.1:1001",
               "last_modified":"Jan 29 05:22:58.696 for 1d04h",
               "paths":{
                  "total_available_paths":2,
                  "best_path":1,
                  "path":{
                     "1":{
                        "as_path":{
                           "Local":{
                              "bgp_peer_neighbor_ip":{
                                 "fc00:a000:1000::1":{
                                    "metric":20,
                                    "bgp_peer_neighbor_ip":"fc00:a000:1000::1",
                                    "origin_neighbors_ip":"fc00:a000:2000::13",
                                    "origin_router_id":"10.0.0.1",
                                    "if_handle":"0x00000000",
                                    "received_label":"0xe00200",
                                    "localpref":100,
                                    "origin_codes":"i",
                                    "group_best":"group-best",
                                    "import_candidate":"import-candidate",
                                    "not_in_vrf":"not-in-vrf",
                                    "status_codes":"*>i",
                                    "received_path_id":1,
                                    "local_path_id":1,
                                    "version":6620,
                                    "extended_community":"EVPN L2 ATTRS:0x02:0 RT:100:1001",
                                    "originator":"10.0.0.1",
                                    "cluster_list":"10.0.0.13, 10.0.0.15, 10.0.0.11",
                                    "psid_type":{
                                       "L2":{
                                          "psid_type":"L2",
                                          "subtlv_count":1,
                                          "r_value":"0x00",
                                          "subtlv":{
                                             "t_value":"1",
                                             "sid_value":"fc00:c000:1001::",
                                             "f_value":"0x00",
                                             "r2_value":"0x00",
                                             "behaviour":"65",
                                             "r3_value":"0x00",
                                             "sstlv_count":1,
                                             "subsubtlv":{
                                                "t":{
                                                   "1":{
                                                      "loc_blk":"32",
                                                      "loc_node":"16",
                                                      "func":"16",
                                                      "arg":"0",
                                                      "tpose_len":"16",
                                                      "tpose_offset":"48"
                                                   }
                                                }
                                             }
                                          }
                                       }
                                    }
                                 }
                              }
                           }
                        }
                     },
                     "2":{
                        "as_path":{
                           "Local":{
                              "bgp_peer_neighbor_ip":{
                                 "fc00:a000:1000::1":{
                                    "metric":20,
                                    "bgp_peer_neighbor_ip":"fc00:a000:1000::1",
                                    "origin_neighbors_ip":"fc00:a000:2000::14",
                                    "origin_router_id":"10.0.0.1",
                                    "if_handle":"0x00000000",
                                    "received_label":"0xe00200",
                                    "localpref":100,
                                    "origin_codes":"i",
                                    "not_in_vrf":"not-in-vrf",
                                    "status_codes":"*i",
                                    "received_path_id":1,
                                    "local_path_id":0,
                                    "version":0,
                                    "extended_community":"EVPN L2 ATTRS:0x02:0 RT:100:1001",
                                    "originator":"10.0.0.1",
                                    "cluster_list":"10.0.0.14, 10.0.0.15, 10.0.0.11",
                                    "psid_type":{
                                       "L2":{
                                          "psid_type":"L2",
                                          "subtlv_count":1,
                                          "r_value":"0x00",
                                          "subtlv":{
                                             "t_value":"1",
                                             "sid_value":"fc00:c000:1001::",
                                             "f_value":"0x00",
                                             "r2_value":"0x00",
                                             "behaviour":"65",
                                             "r3_value":"0x00",
                                             "sstlv_count":1,
                                             "subsubtlv":{
                                                "t":{
                                                   "1":{
                                                      "loc_blk":"32",
                                                      "loc_node":"16",
                                                      "func":"16",
                                                      "arg":"0",
                                                      "tpose_len":"16",
                                                      "tpose_offset":"48"
                                                   }
                                                }
                                             }
                                          }
                                       }
                                    }
                                 }
                              }
                           }
                        }
                     }
                  }
               }
            }
         }
      }
   }
}
