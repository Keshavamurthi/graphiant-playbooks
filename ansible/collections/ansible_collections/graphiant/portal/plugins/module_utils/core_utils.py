from edge_utils import PortalUtils

class Core(PortalUtils):

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

    def add_wan_interface(self, device_id, interface_name, circuit_name,
                          ipv4_address, gw_address, **kwargs):
        config = {
            "interfaces": {
                interface_name: {
                    "interface": {
                        "adminStatus": kwargs.get("admin_status", "true"),
                        "circuit": circuit_name,
                        "description": f"{device_id}_{circuit_name}",
                        "gw": {
                            "gw": {
                                "address": {
                                    "address": gw_address
                                }
                            }
                        },
                        "ipv4": {
                            "address": {
                                "address": ipv4_address
                            }
                        },
                        "ipv6": {
                            "address": {}
                        },
                        "maxTransmissionUnit": kwargs.get("mtu", 1500)
                    }
                }
            }
        }
        output = self.gcsdk.put_device_config(device_id=device_id, core=config)
        result = True if output.job_id else False
        return result

    def add_core_interface(self, device_id, interface_name, ipv6_address, 
                           peer_hostname, ospf_cost, **kwargs):
        config = {
            "interfaces": {        
                interface_name: {
                    "interface": {
                        "lan": "graphiant-core",
                        "description": f"Towards {peer_hostname}",
                        "ipv6": {
                            "address": {
                                "address": ipv6_address
                            }
                        },
                        "peerHostname": peer_hostname,
                        "static": ospf_cost,
                        "maxTransmissionUnit": kwargs.get("mtu", 9200)
                    }
                }
            }
        }
        if kwargs.get("ipv4_address"):
            config["interfaces"][interface_name]["interface"].update(
                    {
                        "ipv4": {
                                "address": {
                                    "address": kwargs.get("ipv4_address")
                                }
                            }
                    })
        result = self.gcsdk.put_device_config(device_id=device_id, core=config)
        return result

    def move_interface_to_default_lan(self, device_id, interface_name, default_lan):
        config = {
                "interfaces": {
                    interface_name: {
                        "interface": {
                            "lan": default_lan
                        }
                    }
                }
            }
        output = self.gcsdk.put_device_config(device_id=device_id, core=config)
        result = True if output.job_id else False
        return result      

    def delete_interface(self, device_id, interface_name, default_lan, **kwargs):
        config = {
                "interfaces": {
                    interface_name: {
                        "interface": {
                            "adminStatus": "false",
                            "description": "",
                            "ipv4": {
                                "address": {}
                            },
                            "ipv6": {
                                "address": {}
                            },
                            "maxTransmissionUnit": 1500
                        }
                    }
                }
            }
        result = self.move_interface_to_default_lan(device_id, interface_name, default_lan)
        output = self.gcsdk.put_device_config(device_id=device_id, core=config)
        result = result if output.job_id else False
        return result

core = Core()
result = core.add_core_interface(device_id=30000049005, interface_name="TenGigabitEthernet7/5", ipv4_address="92.93.94.97/30", gw_address="92.93.94.98",
                                 ipv6_address="fc01:2001::1/127", peer_name="uk-read-rc-et-0-6520", ospf_cost=100, circuit_name="isp-8")
result = core.delete_interface(device_id=30000049005, interface_name="TenGigabitEthernet7/5", default_lan="default-10000000000")

#core = Core()
#result = core.add_core_interface(device_id=30000049005, interface_name="TenGigabitEthernet7/5", ipv4_address="92.93.94.97/30", 
#                                 ipv6_address="fc01:2001::1/127", peer_name="uk-read-rc-et-0-6520", ospf_cost=100)
#result = core.delete_interface(device_id=30000049005, interface_name="TenGigabitEthernet7/5", default_lan="default-10000000000")
#result = core.add_wan_interface(device_id=30000049005, interface_name="TenGigabitEthernet7/5", ipv4_address="92.93.94.97/30", gw_address="92.93.94.98", circuit_name="isp-8")
#result = core.delete_interface(device_id=30000049005, interface_name="TenGigabitEthernet7/5", default_lan="default-10000000000")
#print(result)