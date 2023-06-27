expected_output={
   "vrf_name":{
      "Default":{
         "process_type":{
            "route":{
               "gateway":{
                  "11.1.6.1":{
                     "mask":"255.255.255.0"
                  }
               }
            },
            "cef":{
               "gateway":{
                  "11.1.6.1":{
                     "mask":"255.255.255.0"
                  }
               }
            },
            "rp":{
               "gateway":{
                  "11.1.6.1":{
                     "mask_number":"24"
                  }
               }
            },
            "fp":{
               "gateway":{
                  "11.1.6.1":{
                     "mask_number":"24"
                  }
               }
            }
         }
      },
      "Mgmt-vrf":{
         "process_type":{
            "route":{
               "gateway":{
                  "11.1.6.1":{
                     "mask":"255.255.255.0"
                  }
               }
            },
            "cef":{
               "gateway":{
                  "11.1.6.1":{
                     "mask":"255.255.255.0"
                  }
               }
            },
            "rp":{
               "gateway":{
                  "11.1.6.1":{
                     "mask_number":"24"
                  }
               }
            },
            "fp":{
               "gateway":{
                  "11.1.6.1":{
                     "mask_number":"24"
                  }
               }
            }
         }
      },
      "vrf1000":{
         "process_type":{
            "route":{
               "gateway":{
                  "11.1.6.1":{
                     "mask":"255.255.255.0",
                     "route_vrf_name":"vrf1000",
                     "route_ip_address":"11.1.6.0",
                     "route_mask_num":"24",
                     "stage":"connected",
                     "distance":"0",
                     "metric":"0",
                     "interface":"HundredGigE1/0/3",
                     "route_metric":"0",
                     "traffic_share":"1"
                  }
               }
            },
            "cef":{
               "gateway":{
                  "11.1.6.1":{
                     "mask":"255.255.255.0"
                  }
               }
            },
            "rp":{
               "gateway":{
                  "11.1.6.1":{
                     "mask_number":"24"
                  }
               }
            },
            "fp":{
               "gateway":{
                  "11.1.6.1":{
                     "mask_number":"24"
                  }
               }
            }
         }
      },
      "vrf1001":{
         "process_type":{
            "route":{
               "gateway":{
                  "11.1.6.1":{
                     "mask":"255.255.255.0",
                     "route_vrf_name":"vrf1001"
                  }
               }
            },
            "cef":{
               "gateway":{
                  "11.1.6.1":{
                     "mask":"255.255.255.0"
                  }
               }
            },
            "rp":{
               "gateway":{
                  "11.1.6.1":{
                     "mask_number":"24"
                  }
               }
            },
            "fp":{
               "gateway":{
                  "11.1.6.1":{
                     "mask_number":"24"
                  }
               }
            }
         }
      }
   }
}