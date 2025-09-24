import configparser
import unittest
from libs.edge import Edge
from libs.logger import setup_logger

LOG = setup_logger()


def read_config():
    config = configparser.ConfigParser()
    config.read('test/test.ini')
    username = config['credentials']['username']
    password = config['credentials']['password']
    host = config['host']['url']
    return host, username, password


class TestGraphiantPlaybooks(unittest.TestCase):

    def test_get_login_token(self):
        """
        Test login and fetch token.
        """
        base_url, username, password = read_config()
        Edge(base_url=base_url, username=username, password=password)

    def test_get_enterprise_id(self):
        """
        Test login and fetch enterprise id.
        """
        base_url, username, password = read_config()
        edge = Edge(base_url=base_url, username=username, password=password)
        enterprise_id = edge.edge_utils.get_enterprise_id()
        LOG.info(f"Enterprise ID: {enterprise_id}")

    def test_get_lan_segments(self):
        """
        Test login and fetch Lan segments.
        """
        base_url, username, password = read_config()
        edge = Edge(base_url=base_url, username=username, password=password)
        lan_segments = edge.edge_utils.get_all_lan_segments()
        LOG.info(f"Lan Segments: {lan_segments}")

    def test_configure_wan_circuits_interfaces(self):
        """
        Configure WAN circuits and wan interfaces for multiple devices in a single operation.
        """
        base_url, username, password = read_config()
        edge = Edge(base_url=base_url, username=username, password=password)
        edge.interfaces.configure_wan_circuits_interfaces(
            circuit_config_file="sample_circuit_config.yaml",
            interface_config_file="sample_interface_config.yaml"
        )

    def test_configure_circuits(self):
        """
        Configure Circuits for multiple devices.
        """
        base_url, username, password = read_config()
        edge = Edge(base_url=base_url, username=username, password=password)
        edge.interfaces.configure_circuits(
            circuit_config_file="sample_circuit_config.yaml",
            interface_config_file="sample_interface_config.yaml")

    def test_deconfigure_circuits(self):
        """
        Deconfigure Circuits staticRoutes for multiple devices.
        """
        base_url, username, password = read_config()
        edge = Edge(base_url=base_url, username=username, password=password)
        edge.interfaces.deconfigure_circuits(
            interface_config_file="sample_interface_config.yaml",
            circuit_config_file="sample_circuit_config.yaml")

    def test_deconfigure_wan_circuits_interfaces(self):
        """
        Deconfigure WAN circuits and interfaces for multiple devices in a single operation.
        """
        base_url, username, password = read_config()
        edge = Edge(base_url=base_url, username=username, password=password)
        edge.interfaces.deconfigure_wan_circuits_interfaces(
            interface_config_file="sample_interface_config.yaml",
            circuit_config_file="sample_circuit_config.yaml"
        )

    def test_configure_lan_interfaces(self):
        """
        Configure LAN interfaces for multiple devices.
        """
        base_url, username, password = read_config()
        edge = Edge(base_url=base_url, username=username, password=password)
        edge.interfaces.configure_lan_interfaces("sample_interface_config.yaml")

    def test_deconfigure_lan_interfaces(self):
        """
        Deconfigure LAN interfaces for multiple devices.
        """
        base_url, username, password = read_config()
        edge = Edge(base_url=base_url, username=username, password=password)
        edge.interfaces.deconfigure_lan_interfaces("sample_interface_config.yaml")

    def test_configure_interfaces(self):
        """
        Configure Interfaces of all types.
        """
        base_url, username, password = read_config()
        edge = Edge(base_url=base_url, username=username, password=password)
        edge.interfaces.configure_interfaces(
            interface_config_file="sample_interface_config.yaml",
            circuit_config_file="sample_circuit_config.yaml")

    def test_deconfigure_interfaces(self):
        """
        Deconfigure Interfaces (i.e Reset parent interface to default lan and delete subinterfaces)
        """
        base_url, username, password = read_config()
        edge = Edge(base_url=base_url, username=username, password=password)
        edge.interfaces.deconfigure_interfaces(
            interface_config_file="sample_interface_config.yaml",
            circuit_config_file="sample_circuit_config.yaml")

    def test_configure_global_config_prefix_lists(self):
        """
        Configure Global Config Prefix Lists.
        """
        base_url, username, password = read_config()
        edge = Edge(base_url=base_url, username=username, password=password)
        # edge.global_config.configure_prefix_sets(prefix_sets)
        edge.global_config.configure("sample_global_prefix_lists.yaml")

    def test_deconfigure_global_config_prefix_lists(self):
        """
        Deconfigure Global Config Prefix Lists.
        """
        base_url, username, password = read_config()
        edge = Edge(base_url=base_url, username=username, password=password)
        # edge.global_config.deconfigure_prefix_sets(prefix_sets)
        edge.global_config.deconfigure("sample_global_prefix_lists.yaml")

    def test_configure_global_config_bgp_filters(self):
        """
        Configure Global BGP Filters.
        """
        base_url, username, password = read_config()
        edge = Edge(base_url=base_url, username=username, password=password)
        # edge.global_config.configure_bgp_filters(routing_policies)
        edge.global_config.configure("sample_global_bgp_filters.yaml")

    def test_deconfigure_global_config_bgp_filters(self):
        """
        Deconfigure Global Config BGP Filters.
        """
        base_url, username, password = read_config()
        edge = Edge(base_url=base_url, username=username, password=password)
        # edge.global_config.deconfigure_bgp_filters(routing_policies)
        edge.global_config.deconfigure("sample_global_bgp_filters.yaml")

    def test_configure_bgp_peering(self):
        """
        Configure BGP Peering.
        """
        base_url, username, password = read_config()
        edge = Edge(base_url=base_url, username=username, password=password)
        edge.bgp.configure("sample_bgp_peering.yaml")

    def test_deconfigure_bgp_peering(self):
        """
        Deconfigure BGP Peering.
        """
        base_url, username, password = read_config()
        edge = Edge(base_url=base_url, username=username, password=password)
        edge.bgp.deconfigure("sample_bgp_peering.yaml")

    def test_detach_policies_from_bgp_peers(self):
        """
        Detach policies from BGP peers.
        """
        base_url, username, password = read_config()
        edge = Edge(base_url=base_url, username=username, password=password)
        edge.bgp.detach_policies("sample_bgp_peering.yaml")

    def test_configure_snmp_service(self):
        """
        Configure Global SNMP Objects.
        """
        base_url, username, password = read_config()
        edge = Edge(base_url=base_url, username=username, password=password)
        # edge.global_config.configure_snmp_services(snmp_services)
        edge.global_config.configure("sample_global_snmp_services.yaml")

    def test_deconfigure_snmp_service(self):
        """
        Deconfigure Global SNMP Objects.
        """
        base_url, username, password = read_config()
        edge = Edge(base_url=base_url, username=username, password=password)
        # edge.global_config.deconfigure_snmp_services(snmp_services)
        edge.global_config.deconfigure("sample_global_snmp_services.yaml")

    def test_configure_syslog_service(self):
        """
        Configure Global Syslog Objects.
        """
        base_url, username, password = read_config()
        edge = Edge(base_url=base_url, username=username, password=password)
        # edge.global_config.configure_syslog_services(syslog_services)
        edge.global_config.configure("sample_global_syslog_servers.yaml")

    def test_deconfigure_syslog_service(self):
        """
        Deconfigure Global Syslog Objects.
        """
        base_url, username, password = read_config()
        edge = Edge(base_url=base_url, username=username, password=password)
        # edge.global_config.deconfigure_syslog_services(syslog_services)
        edge.global_config.deconfigure("sample_global_syslog_servers.yaml")

    def test_configure_ipfix_service(self):
        """
        Configure Global IPFIX Objects.
        """
        base_url, username, password = read_config()
        edge = Edge(base_url=base_url, username=username, password=password)
        # edge.global_config.configure_ipfix_services(ipfix_services)
        edge.global_config.configure("sample_global_ipfix_exporters.yaml")

    def test_deconfigure_ipfix_service(self):
        """
        Deconfigure Global IPFIX Objects.
        """
        base_url, username, password = read_config()
        edge = Edge(base_url=base_url, username=username, password=password)
        # edge.global_config.deconfigure_ipfix_services(ipfix_services)
        edge.global_config.deconfigure("sample_global_ipfix_exporters.yaml")

    def test_configure_vpn_profiles(self):
        """
        Configure Global VPN Profile Objects.
        """
        base_url, username, password = read_config()
        edge = Edge(base_url=base_url, username=username, password=password)
        # edge.global_config.configure_vpn_profiles(vpn_profiles)
        edge.global_config.configure("sample_global_vpn_profiles.yaml")

    def test_deconfigure_vpn_profiles(self):
        """
        Deconfigure Global VPN Profile Objects.
        """
        base_url, username, password = read_config()
        edge = Edge(base_url=base_url, username=username, password=password)
        # edge.global_config.deconfigure_vpn_profiles(vpn_profiles)
        edge.global_config.deconfigure("sample_global_vpn_profiles.yaml")

    def test_attach_global_system_objects_to_site(self):
        """
      syslog_servers:
        Attach Global System Objects (SNMP, Syslog, IPFIX etc) to Sites.
        """
        base_url, username, password = read_config()
        edge = Edge(base_url=base_url, username=username, password=password)
        edge.sites.manage_global_system_objects_on_site("sample_site_attachments.yaml", "attach")

    def test_detach_global_system_objects_from_site(self):
        """
        Detach Global System Objects (SNMP, Syslog, IPFIX etc) from Sites.
        """
        base_url, username, password = read_config()
        edge = Edge(base_url=base_url, username=username, password=password)
        edge.sites.manage_global_system_objects_on_site("sample_site_attachments.yaml", "detach")


if __name__ == '__main__':
    suite = unittest.TestSuite()
    suite.addTest(TestGraphiantPlaybooks('test_get_login_token'))
    suite.addTest(TestGraphiantPlaybooks('test_get_enterprise_id'))
    suite.addTest(TestGraphiantPlaybooks('test_get_lan_segments'))

    # Interface Management
    suite.addTest(TestGraphiantPlaybooks('test_configure_lan_interfaces'))
    suite.addTest(TestGraphiantPlaybooks('test_deconfigure_lan_interfaces'))
    suite.addTest(TestGraphiantPlaybooks('test_configure_wan_circuits_interfaces'))
    suite.addTest(TestGraphiantPlaybooks('test_configure_circuits'))
    suite.addTest(TestGraphiantPlaybooks('test_deconfigure_circuits'))
    suite.addTest(TestGraphiantPlaybooks('test_deconfigure_wan_circuits_interfaces'))
    # To configure all interfaces
    suite.addTest(TestGraphiantPlaybooks('test_configure_interfaces'))
    # To deconfigure all interfaces=
    # suite.addTest(TestGraphiantPlaybooks('test_deconfigure_interfaces'))

    # Global Configuration Management, BGP Peering and Sites Management
    suite.addTest(TestGraphiantPlaybooks('test_configure_global_config_prefix_lists'))
    suite.addTest(TestGraphiantPlaybooks('test_configure_global_config_bgp_filters'))
    suite.addTest(TestGraphiantPlaybooks('test_configure_bgp_peering'))
    suite.addTest(TestGraphiantPlaybooks('test_detach_policies_from_bgp_peers'))
    suite.addTest(TestGraphiantPlaybooks('test_deconfigure_bgp_peering'))
    suite.addTest(TestGraphiantPlaybooks('test_deconfigure_global_config_bgp_filters'))
    suite.addTest(TestGraphiantPlaybooks('test_deconfigure_global_config_prefix_lists'))

    suite.addTest(TestGraphiantPlaybooks('test_configure_vpn_profiles'))
    suite.addTest(TestGraphiantPlaybooks('test_deconfigure_vpn_profiles'))

    suite.addTest(TestGraphiantPlaybooks('test_configure_snmp_service'))
    suite.addTest(TestGraphiantPlaybooks('test_configure_syslog_service'))
    suite.addTest(TestGraphiantPlaybooks('test_configure_ipfix_service'))
    suite.addTest(TestGraphiantPlaybooks('test_attach_global_system_objects_to_site'))
    suite.addTest(TestGraphiantPlaybooks('test_detach_global_system_objects_from_site'))
    suite.addTest(TestGraphiantPlaybooks('test_deconfigure_snmp_service'))
    suite.addTest(TestGraphiantPlaybooks('test_deconfigure_syslog_service'))
    suite.addTest(TestGraphiantPlaybooks('test_deconfigure_ipfix_service'))

    # To deconfigure all interfaces
    suite.addTest(TestGraphiantPlaybooks('test_deconfigure_circuits'))
    suite.addTest(TestGraphiantPlaybooks('test_deconfigure_interfaces'))

    runner = unittest.TextTestRunner(verbosity=2).run(suite)
