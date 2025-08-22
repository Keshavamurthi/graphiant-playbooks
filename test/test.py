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
        enterprise_id = edge.get_enterprise_id()
        LOG.info(f"Enterprise ID: {enterprise_id}")

    def test_configure_interfaces(self):
        """
        Configure Interfaces.
        """
        base_url, username, password = read_config()
        edge = Edge(base_url=base_url, username=username, password=password)
        edge.configure_interfaces("sample_interface_config.yaml")

    def test_deconfigure_interfaces(self):
        """
        Deconfigure Interfaces (i.e Reset to default lan)
        """
        base_url, username, password = read_config()
        edge = Edge(base_url=base_url, username=username, password=password)
        edge.deconfigure_interfaces("sample_interface_config.yaml")

    def test_configure_global_config_prefix_lists(self):
        """
        Configure Global Config Prefix Lists.
        """
        base_url, username, password = read_config()
        edge = Edge(base_url=base_url, username=username, password=password)
        edge.configure_global_config_prefix_lists("sample_global_routing_policies.yaml")

    def test_deconfigure_global_config_prefix_lists(self):
        """
        Deconfigure Global Config Prefix Lists.
        """
        base_url, username, password = read_config()
        edge = Edge(base_url=base_url, username=username, password=password)
        edge.deconfigure_global_config_prefix_lists("sample_global_routing_policies.yaml")

    def test_configure_global_config_routing_policies(self):
        """
        Configure Global Routing Policies.
        """
        base_url, username, password = read_config()
        edge = Edge(base_url=base_url, username=username, password=password)
        edge.configure_global_config_routing_policies("sample_global_routing_policies.yaml")

    def test_deconfigure_global_config_routing_policies(self):
        """
        Deconfigure Global Config Routing Policies.
        """
        base_url, username, password = read_config()
        edge = Edge(base_url=base_url, username=username, password=password)
        edge.deconfigure_global_config_routing_policies("sample_global_routing_policies.yaml")

    def test_configure_bgp_peering(self):
        """
        Configure BGP Peering.
        """
        base_url, username, password = read_config()
        edge = Edge(base_url=base_url, username=username, password=password)
        edge.configure_bgp_peers("sample_bgp_peering.yaml")

    def test_deconfigure_bgp_peering(self):
        """
        Deconfigure BGP Peering.
        """
        base_url, username, password = read_config()
        edge = Edge(base_url=base_url, username=username, password=password)
        edge.deconfigure_bgp_peers("sample_bgp_peering.yaml")

    def test_detach_policies_from_bgp_peers(self):
        """
        Detach policies from BGP peers.
        """
        base_url, username, password = read_config()
        edge = Edge(base_url=base_url, username=username, password=password)
        edge.detach_policies_from_bgp_peers("sample_bgp_peering.yaml")

    def test_configure_snmp_service(self):
        """
        Configure Global SNMP Service.
        """
        base_url, username, password = read_config()
        edge = Edge(base_url=base_url, username=username, password=password)
        edge.configure_global_snmp_service("sample_global_system_services.yaml")

    def test_deconfigure_snmp_service(self):
        """
        Deconfigure Global SNMP Service.
        """
        base_url, username, password = read_config()
        edge = Edge(base_url=base_url, username=username, password=password)
        edge.deconfigure_global_snmp_service("sample_global_system_services.yaml")


if __name__ == '__main__':
    suite = unittest.TestSuite()

    suite.addTest(TestGraphiantPlaybooks('test_get_login_token'))

    # suite.addTest(TestGraphiantPlaybooks('test_get_enterprise_id'))

    # suite.addTest(TestGraphiantPlaybooks('test_configure_interfaces'))
    # suite.addTest(TestGraphiantPlaybooks('test_configure_global_config_prefix_lists'))
    # suite.addTest(TestGraphiantPlaybooks('test_configure_global_config_routing_policies'))
    # suite.addTest(TestGraphiantPlaybooks('test_configure_bgp_peering'))

    # suite.addTest(TestGraphiantPlaybooks('test_detach_policies_from_bgp_peers'))
    # suite.addTest(TestGraphiantPlaybooks('test_deconfigure_bgp_peering'))
    # suite.addTest(TestGraphiantPlaybooks('test_deconfigure_global_config_routing_policies'))
    # suite.addTest(TestGraphiantPlaybooks('test_deconfigure_global_config_prefix_lists'))
    # suite.addTest(TestGraphiantPlaybooks('test_deconfigure_interfaces'))
    # suite.addTest(TestGraphiantPlaybooks('test_configure_snmp_service'))
    # suite.addTest(TestGraphiantPlaybooks('test_deconfigure_snmp_service'))

    runner = unittest.TextTestRunner(verbosity=2).run(suite)
