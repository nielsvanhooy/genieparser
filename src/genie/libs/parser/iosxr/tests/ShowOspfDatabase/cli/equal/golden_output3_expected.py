expected_output= {
   "vrf":{
      "default":{
         "address_family":{
            "ipv4":{
               "instance":{
                  "1":{
                     "router_id":"10.0.0.11",
                     "area":{
                        "0.0.0.0":{
                           "area_id":0,
                           "database":{
                              "lsa_types":{
                                 1:{
                                    "lsa_type":1,
                                    "lsas":{
                                       "10.0.0.1 10.0.0.1":{
                                          "adv_router":"10.0.0.1",
                                          "link_id":"10.0.0.1",
                                          "ospf":{
                                             "header":{
                                                "age":1820,
                                                "seq_num":"0x80000189",
                                                "checksum":"0x00d66f",
                                                "link_count":2
                                             }
                                          }
                                       },
                                       "10.0.0.11 10.0.0.11":{
                                          "adv_router":"10.0.0.11",
                                          "link_id":"10.0.0.11",
                                          "ospf":{
                                             "header":{
                                                "age":1519,
                                                "seq_num":"0x8000018a",
                                                "checksum":"0x00af77",
                                                "link_count":2
                                             }
                                          }
                                       }
                                    }
                                 },
                                 2:{
                                    "lsa_type":2,
                                    "lsas":{
                                       "10.1.11.2 10.0.0.11":{
                                          "adv_router":"10.0.0.11",
                                          "link_id":"10.1.11.2",
                                          "ospf":{
                                             "header":{
                                                "age":1519,
                                                "seq_num":"0x80000183",
                                                "checksum":"0x002646"
                                             }
                                          }
                                       }
                                    }
                                 },
                                 3:{
                                    "lsa_type":3,
                                    "lsas":{
                                       "10.0.0.13 10.0.0.11":{
                                          "adv_router":"10.0.0.11",
                                          "link_id":"10.0.0.13",
                                          "ospf":{
                                             "header":{
                                                "age":1519,
                                                "seq_num":"0x80000166",
                                                "checksum":"0x002e7a"
                                             }
                                          }
                                       },
                                       "10.11.13.0 10.0.0.11":{
                                          "adv_router":"10.0.0.11",
                                          "link_id":"10.11.13.0",
                                          "ospf":{
                                             "header":{
                                                "age":1519,
                                                "seq_num":"0x80000186",
                                                "checksum":"0x004041"
                                             }
                                          }
                                       }
                                    }
                                 }
                              }
                           }
                        },
                        "0.0.0.1":{
                           "area_id":1,
                           "database":{
                              "lsa_types":{
                                 1:{
                                    "lsa_type":1,
                                    "lsas":{
                                       "10.0.0.11 10.0.0.11":{
                                          "adv_router":"10.0.0.11",
                                          "link_id":"10.0.0.11",
                                          "ospf":{
                                             "header":{
                                                "age":1519,
                                                "seq_num":"0x80000187",
                                                "checksum":"0x001a20",
                                                "link_count":1
                                             }
                                          }
                                       },
                                       "10.0.0.13 10.0.0.13":{
                                          "adv_router":"10.0.0.13",
                                          "link_id":"10.0.0.13",
                                          "ospf":{
                                             "header":{
                                                "age":1716,
                                                "seq_num":"0x80000187",
                                                "checksum":"0x00a667",
                                                "link_count":2
                                             }
                                          }
                                       }
                                    }
                                 },
                                 2:{
                                    "lsa_type":2,
                                    "lsas":{
                                       "10.11.13.1 10.0.0.11":{
                                          "adv_router":"10.0.0.11",
                                          "link_id":"10.11.13.1",
                                          "ospf":{
                                             "header":{
                                                "age":1519,
                                                "seq_num":"0x80000183",
                                                "checksum":"0x002233"
                                             }
                                          }
                                       }
                                    }
                                 },
                                 3:{
                                    "lsa_type":3,
                                    "lsas":{
                                       "10.0.0.1 10.0.0.11":{
                                          "adv_router":"10.0.0.11",
                                          "link_id":"10.0.0.1",
                                          "ospf":{
                                             "header":{
                                                "age":1519,
                                                "seq_num":"0x80000166",
                                                "checksum":"0x00a60e"
                                             }
                                          }
                                       },
                                       "10.0.0.11 10.0.0.11":{
                                          "adv_router":"10.0.0.11",
                                          "link_id":"10.0.0.11",
                                          "ospf":{
                                             "header":{
                                                "age":1519,
                                                "seq_num":"0x80000163",
                                                "checksum":"0x003e70"
                                             }
                                          }
                                       },
                                       "10.1.11.0 10.0.0.11":{
                                          "adv_router":"10.0.0.11",
                                          "link_id":"10.1.11.0",
                                          "ospf":{
                                             "header":{
                                                "age":1519,
                                                "seq_num":"0x80000186",
                                                "checksum":"0x00cebe"
                                             }
                                          }
                                       }
                                    }
                                 },
                                 4:{
                                    "lsa_type":4,
                                    "lsas":{
                                       "10.0.0.1 10.0.0.11":{
                                          "adv_router":"10.0.0.11",
                                          "link_id":"10.0.0.1",
                                          "ospf":{
                                             "header":{
                                                "age":1519,
                                                "seq_num":"0x80000186",
                                                "checksum":"0x004e46"
                                             }
                                          }
                                       }
                                    }
                                 }
                              }
                           }
                        }
                     },
                     "database":{
                        "lsa_types":{
                           5:{
                              "lsa_type":5,
                              "lsas":{
                                 "1.1.1.1 10.0.0.1":{
                                    "adv_router":"10.0.0.1",
                                    "link_id":"1.1.1.1",
                                    "ospf":{
                                       "header":{
                                          "age":1820,
                                          "seq_num":"0x80000163",
                                          "checksum":"0x00919c",
                                          "tag":0
                                       }
                                    }
                                 },
                                 "2.2.2.2 10.0.0.1":{
                                    "adv_router":"10.0.0.1",
                                    "link_id":"2.2.2.2",
                                    "ospf":{
                                       "header":{
                                          "age":1820,
                                          "seq_num":"0x80000163",
                                          "checksum":"0x0063c6",
                                          "tag":0
                                       }
                                    }
                                 },
                                 "10.0.0.1 10.0.0.1":{
                                    "adv_router":"10.0.0.1",
                                    "link_id":"10.0.0.1",
                                    "ospf":{
                                       "header":{
                                          "age":1820,
                                          "seq_num":"0x80000183",
                                          "checksum":"0x00f214",
                                          "tag":0
                                       }
                                    }
                                 },
                                 "10.1.11.0 10.0.0.1":{
                                    "adv_router":"10.0.0.1",
                                    "link_id":"10.1.11.0",
                                    "ospf":{
                                       "header":{
                                          "age":1820,
                                          "seq_num":"0x80000183",
                                          "checksum":"0x006599",
                                          "tag":0
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
