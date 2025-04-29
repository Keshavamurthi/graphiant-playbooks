from libs.edge import Edge
import configparser

def read_config():
    config = configparser.ConfigParser()
    config.read('test.ini')
    username = config['credentials']['username']
    password = config['credentials']['password']
    host = config['host']['url']
    return host, username, password

def main():
    base_url, username, password = read_config()
    edge = Edge(base_url=base_url, username=username, password=password)
    print(f"Enterprise ID : {edge.get_enterprise_id()}")

    # To Configure the interfaces defined in sample_interface_config.yaml
    # edge.configure_interfaces("sample_interface_config.yaml")

    # To deconfigure all the interfaces defined in sample_interface_config.yaml
    # edge.deconfigure_interfaces("sample_interface_config.yaml")

    # To configure the Global Prefixes defined in sample_global_routing_policies.yaml
    #edge.configure_global_prefix("sample_global_routing_policies.yaml")

    # To Configure the Global Prefixes defined in sample_global_routing_policies.yaml
    #edge.configure_global_bgp_routing_policies("sample_global_routing_policies.yaml")

    # To Configure the BGP Peers defined in sample_bgp_peering.yaml
    #edge.configure_bgp_peers("sample_bgp_peering.yaml")

    # To Unlink and deconfigure the BGP Peers defined in sample_global_routing_policies.yaml
    #edge.unlink_bgp_peers("sample_bgp_peering.yaml")
    #edge.deconfigure_bgp_peers("sample_bgp_peering.yaml")

    # To Deconfigure the Global BGP Routing Policies
    #edge.deconfigure_global_bgp_routing_policies("sample_global_routing_policies.yaml")

    # To Deconfigure the Global Prefixes
    #edge.deconfigure_global_prefix("sample_global_routing_policies.yaml")

if __name__ == "__main__":
    main()