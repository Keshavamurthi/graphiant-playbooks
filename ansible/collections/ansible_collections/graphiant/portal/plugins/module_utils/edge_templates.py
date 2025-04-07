from .logger import setup_logger

LOG = setup_logger()

class EdgeTemplates(object):

    @staticmethod
    def _wan_circuit_template(**kwargs):
        circuit_name = kwargs.get("circuit_name")
        config = {
            'circuits': {
                circuit_name: {
                    "name": circuit_name,
                    "description": kwargs.get("description", circuit_name),
                    "linkUpSpeedMbps": kwargs.get("upload_bandwidth", 50),
                    "linkDownSpeedMbps": kwargs.get("download_bandwidth", 100),
                    "connectionType": kwargs.get("connection_type", "internet_dia"),
                    "label": kwargs.get("label", "internet_dia_4"),
                    "qosProfile": kwargs.get("qos_profile", "gold25"),
                    "qosProfileType": kwargs.get("qos_profile_type", "balanced"),
                    "diaEnabled": kwargs.get("dia", False),
                    "patAddresses": [],
                    "interfaceName": "",
                    "snmpIndex": 0,
                    "coreLogicalInterfaces": [],
                    "staticRoutes": [],
                    "diaSnmpIndex": 0
                }
            }
        }
        return config

    @staticmethod
    def _wan_interface_template(**kwargs):
        interface_name = kwargs.get("interface_name")
        config = {
            "interfaces": {
                interface_name: {
                    "interface": {
                        "adminStatus": kwargs.get("admin_status", "true"),
                        "circuit": kwargs.get("circuit_name"),
                        "description": kwargs.get("description", kwargs.get("circuit_name")),
                        "ipv4": {
                            "address": {
                                "address": kwargs.get("ipv4_address"),
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
        return config

    @staticmethod
    def _lan_interface_template(**kwargs):
        interface_name = kwargs.get("interface_name")
        config = {
            "interfaces": {        
                interface_name: {
                    "interface": {
                        "lan": kwargs.get("lan"),
                        "description": kwargs.get("description", f"lan_{kwargs.get("lan")}"),
                        "ipv4": {
                            "address": {
                                "address": kwargs.get("ipv4_address")
                            }
                        },
                        "ipv6": {
                            "address": {
                                "address": kwargs.get("ipv6_address")
                            }
                        },
                        "maxTransmissionUnit": kwargs.get("mtu", 9000)
                    }
                }
            }
        }
        return config

    @staticmethod
    def _lan_subinterface_vlan_template(**kwargs):
        vlan = kwargs.get("vlan")
        config = {
            str(vlan): {
                "interface": {
                    "lan": kwargs.get("lan"),
                    "vlan": vlan,
                    "description": kwargs.get("description", f"{vlan}_{kwargs.get("lan")}"),
                    "adminStatus": "true",
                    "ipv4": {
                        "address": {
                            "address": kwargs.get("ipv4_address")
                        }
                    },
                    "ipv6": {
                        "address": {
                            "address": kwargs.get("ipv6_address")
                        }
                    },
                }
            }
        }
        return config

    @staticmethod
    def _lan_subinterface_template(**kwargs):
        interface_name = kwargs.get("interface_name")
        config = {
            "interfaces": {
                interface_name: {
                    "interface": {
                        "subinterfaces": {
                        }
                    }
                }
            }
        }
        vlan_config = EdgeTemplates._lan_subinterface_vlan_template(**kwargs)
        config["interfaces"][interface_name]["interface"]["subinterfaces"] = vlan_config
        return config

    @staticmethod
    def _default_lan_interface_template(**kwargs):
        interface_name = kwargs.get("interface_name")
        config = {
            "interfaces": {
                interface_name: {
                    "interface": {
                        "lan": kwargs.get("default_lan")
                    }
                }
            }
        }
        return config
    
    @staticmethod
    def _default_interface_template(**kwargs):
        interface_name = kwargs.get("interface_name")
        config = {
            "interfaces": {
                interface_name: {
                    "interface": {
                        "adminStatus": "false",
                        "description": "",
                        "maxTransmissionUnit": 1500
                    }
                }
            }
        }
        return config
    
    @staticmethod
    def _default_lan_subinterface_vlan_template(**kwargs):
        vlan = kwargs.get("vlan")
        config = {                  
            str(vlan): {
                "interface": {
                    "vlan": vlan,
                    "lan": kwargs.get("default_lan")
                }
            }
        }
        return config

    @staticmethod
    def _default_lan_subinterface_template(**kwargs):
        interface_name = kwargs.get("interface_name")
        config = {
            "interfaces": {
                interface_name: {
                    "interface": {
                        "subinterfaces": {
                        }
                    }
                }
            }
        }
        vlan_config = EdgeTemplates._default_lan_subinterface_vlan_template(**kwargs)
        config["interfaces"][interface_name]["interface"]["subinterfaces"] = vlan_config
        return config
    
    @staticmethod
    def _default_subinterface_vlan_template(**kwargs):
        vlan = kwargs.get("vlan")
        config = {
            str(vlan): {
                "interface": None
            }
        }
        return config

    @staticmethod
    def _default_subinterface_template(**kwargs):
        interface_name = kwargs.get("interface_name")
        config = {
            "interfaces": {
                interface_name: {
                    "interface": {
                        "subinterfaces": {
                        }
                    }
                }
            }
        }
        vlan_config = EdgeTemplates._default_subinterface_vlan_template(**kwargs)
        config["interfaces"][interface_name]["interface"]["subinterfaces"] = vlan_config
        return config