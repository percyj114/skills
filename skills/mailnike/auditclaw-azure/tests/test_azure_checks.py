"""Tests for Azure compliance check modules (14 tests with mocked Azure SDK)."""

import os
import sys
from unittest.mock import MagicMock, patch

import pytest

sys.path.insert(0, os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "scripts"))


# ---------------------------------------------------------------------------
# Helper: mock credential
# ---------------------------------------------------------------------------

def _mock_credential():
    """Create a mock Azure credential."""
    return MagicMock()


# ---------------------------------------------------------------------------
# Storage Tests (2)
# ---------------------------------------------------------------------------

class TestStorageChecks:
    @patch("checks.storage.StorageManagementClient", create=True)
    def test_storage_all_compliant(self, MockStorageClient):
        from checks.storage import run_storage_checks

        acct = MagicMock()
        acct.name = "securesa"
        acct.enable_https_traffic_only = True
        acct.minimum_tls_version = "TLS1_2"
        acct.allow_blob_public_access = False
        acct.network_rule_set.default_action = "Deny"

        client = MockStorageClient.return_value
        client.storage_accounts.list.return_value = [acct]

        result = run_storage_checks(_mock_credential(), subscription_id="sub-123")
        assert result["check"] == "storage"
        assert result["provider"] == "azure"
        assert result["status"] == "pass"
        assert result["passed"] == 4
        assert result["failed"] == 0

    @patch("checks.storage.StorageManagementClient", create=True)
    def test_storage_non_compliant(self, MockStorageClient):
        from checks.storage import run_storage_checks

        acct = MagicMock()
        acct.name = "insecuresa"
        acct.enable_https_traffic_only = False
        acct.minimum_tls_version = "TLS1_0"
        acct.allow_blob_public_access = True
        acct.network_rule_set.default_action = "Allow"

        client = MockStorageClient.return_value
        client.storage_accounts.list.return_value = [acct]

        result = run_storage_checks(_mock_credential(), subscription_id="sub-123")
        assert result["status"] == "fail"
        assert result["failed"] == 4
        assert result["passed"] == 0


# ---------------------------------------------------------------------------
# Network Tests (2)
# ---------------------------------------------------------------------------

class TestNetworkChecks:
    @patch("checks.network.NetworkManagementClient", create=True)
    def test_network_no_open_rules(self, MockNetClient):
        from checks.network import run_network_checks

        nsg = MagicMock()
        nsg.name = "secure-nsg"
        rule = MagicMock()
        rule.direction = "Inbound"
        rule.access = "Allow"
        rule.source_address_prefix = "10.0.0.0/8"
        rule.destination_port_range = "22"
        nsg.security_rules = [rule]

        client = MockNetClient.return_value
        client.network_security_groups.list_all.return_value = [nsg]

        result = run_network_checks(_mock_credential(), subscription_id="sub-123")
        assert result["check"] == "network"
        assert result["status"] == "pass"
        assert result["passed"] == 2
        assert result["failed"] == 0

    @patch("checks.network.NetworkManagementClient", create=True)
    def test_network_ssh_rdp_open(self, MockNetClient):
        from checks.network import run_network_checks

        nsg = MagicMock()
        nsg.name = "open-nsg"

        ssh_rule = MagicMock()
        ssh_rule.direction = "Inbound"
        ssh_rule.access = "Allow"
        ssh_rule.source_address_prefix = "0.0.0.0/0"
        ssh_rule.destination_port_range = "22"

        rdp_rule = MagicMock()
        rdp_rule.direction = "Inbound"
        rdp_rule.access = "Allow"
        rdp_rule.source_address_prefix = "*"
        rdp_rule.destination_port_range = "3389"

        nsg.security_rules = [ssh_rule, rdp_rule]

        client = MockNetClient.return_value
        client.network_security_groups.list_all.return_value = [nsg]

        result = run_network_checks(_mock_credential(), subscription_id="sub-123")
        assert result["status"] == "fail"
        assert result["failed"] == 2


# ---------------------------------------------------------------------------
# Key Vault Tests (2)
# ---------------------------------------------------------------------------

class TestKeyVaultChecks:
    @patch("checks.keyvault.KeyVaultManagementClient", create=True)
    def test_keyvault_compliant(self, MockKVClient):
        from checks.keyvault import run_keyvault_checks

        vault = MagicMock()
        vault.name = "prod-vault"
        vault.properties.enable_soft_delete = True
        vault.properties.enable_purge_protection = True

        client = MockKVClient.return_value
        client.vaults.list_by_subscription.return_value = [vault]

        result = run_keyvault_checks(_mock_credential(), subscription_id="sub-123")
        assert result["check"] == "keyvault"
        assert result["status"] == "pass"
        assert result["passed"] == 1

    @patch("checks.keyvault.KeyVaultManagementClient", create=True)
    def test_keyvault_purge_protection_off(self, MockKVClient):
        from checks.keyvault import run_keyvault_checks

        vault = MagicMock()
        vault.name = "weak-vault"
        vault.properties.enable_soft_delete = True
        vault.properties.enable_purge_protection = False

        client = MockKVClient.return_value
        client.vaults.list_by_subscription.return_value = [vault]

        result = run_keyvault_checks(_mock_credential(), subscription_id="sub-123")
        assert result["status"] == "fail"
        assert result["failed"] == 1


# ---------------------------------------------------------------------------
# SQL Tests (2)
# ---------------------------------------------------------------------------

class TestSQLChecks:
    @patch("checks.sql.SqlManagementClient", create=True)
    def test_sql_auditing_tde_on(self, MockSqlClient):
        from checks.sql import run_sql_checks

        server = MagicMock()
        server.name = "prod-sql"
        server.id = "/subscriptions/sub-123/resourceGroups/rg-prod/providers/Microsoft.Sql/servers/prod-sql"

        db = MagicMock()
        db.name = "appdb"

        policy = MagicMock()
        policy.state = "Enabled"

        tde = MagicMock()
        tde.state = "Enabled"

        client = MockSqlClient.return_value
        client.servers.list.return_value = [server]
        client.server_blob_auditing_policies.get.return_value = policy
        client.databases.list_by_server.return_value = [db]
        client.transparent_data_encryptions.get.return_value = tde

        result = run_sql_checks(_mock_credential(), subscription_id="sub-123")
        assert result["check"] == "sql"
        assert result["status"] == "pass"
        assert result["passed"] == 2
        assert result["failed"] == 0

    @patch("checks.sql.SqlManagementClient", create=True)
    def test_sql_auditing_off_tde_disabled(self, MockSqlClient):
        from checks.sql import run_sql_checks

        server = MagicMock()
        server.name = "test-sql"
        server.id = "/subscriptions/sub-123/resourceGroups/rg-test/providers/Microsoft.Sql/servers/test-sql"

        db = MagicMock()
        db.name = "testdb"

        policy = MagicMock()
        policy.state = "Disabled"

        tde = MagicMock()
        tde.state = "Disabled"

        client = MockSqlClient.return_value
        client.servers.list.return_value = [server]
        client.server_blob_auditing_policies.get.return_value = policy
        client.databases.list_by_server.return_value = [db]
        client.transparent_data_encryptions.get.return_value = tde

        result = run_sql_checks(_mock_credential(), subscription_id="sub-123")
        assert result["status"] == "fail"
        assert result["failed"] == 2


# ---------------------------------------------------------------------------
# Compute Tests (2)
# ---------------------------------------------------------------------------

class TestComputeChecks:
    @patch("checks.compute.ComputeManagementClient", create=True)
    def test_compute_encryption_at_host(self, MockComputeClient):
        from checks.compute import run_compute_checks

        vm = MagicMock()
        vm.name = "secure-vm"
        vm.security_profile.encryption_at_host = True

        client = MockComputeClient.return_value
        client.virtual_machines.list_all.return_value = [vm]

        result = run_compute_checks(_mock_credential(), subscription_id="sub-123")
        assert result["check"] == "compute"
        assert result["status"] == "pass"
        assert result["passed"] == 1

    @patch("checks.compute.ComputeManagementClient", create=True)
    def test_compute_no_encryption(self, MockComputeClient):
        from checks.compute import run_compute_checks

        vm = MagicMock()
        vm.name = "unencrypted-vm"
        vm.security_profile = None

        client = MockComputeClient.return_value
        client.virtual_machines.list_all.return_value = [vm]

        result = run_compute_checks(_mock_credential(), subscription_id="sub-123")
        assert result["status"] == "fail"
        assert result["failed"] == 1


# ---------------------------------------------------------------------------
# App Service Tests (2)
# ---------------------------------------------------------------------------

class TestAppServiceChecks:
    @patch("checks.appservice.WebSiteManagementClient", create=True)
    def test_appservice_https_tls12(self, MockWebClient):
        from checks.appservice import run_appservice_checks

        app = MagicMock()
        app.name = "secure-app"
        app.resource_group = "rg-prod"
        app.https_only = True

        config = MagicMock()
        config.min_tls_version = "1.2"

        client = MockWebClient.return_value
        client.web_apps.list.return_value = [app]
        client.web_apps.get_configuration.return_value = config

        result = run_appservice_checks(_mock_credential(), subscription_id="sub-123")
        assert result["check"] == "appservice"
        assert result["status"] == "pass"
        assert result["passed"] == 1

    @patch("checks.appservice.WebSiteManagementClient", create=True)
    def test_appservice_http_old_tls(self, MockWebClient):
        from checks.appservice import run_appservice_checks

        app = MagicMock()
        app.name = "insecure-app"
        app.resource_group = "rg-test"
        app.https_only = False

        config = MagicMock()
        config.min_tls_version = "1.0"

        client = MockWebClient.return_value
        client.web_apps.list.return_value = [app]
        client.web_apps.get_configuration.return_value = config

        result = run_appservice_checks(_mock_credential(), subscription_id="sub-123")
        assert result["status"] == "fail"
        assert result["failed"] == 1


# ---------------------------------------------------------------------------
# Defender Tests (2)
# ---------------------------------------------------------------------------

class TestDefenderChecks:
    @patch("checks.defender.SecurityCenter", create=True)
    def test_defender_all_standard(self, MockSecClient):
        from checks.defender import run_defender_checks, CRITICAL_PLANS

        pricings = []
        for plan_name in CRITICAL_PLANS:
            p = MagicMock()
            p.name = plan_name
            p.pricing_tier = "Standard"
            pricings.append(p)

        result_obj = MagicMock()
        result_obj.value = pricings

        client = MockSecClient.return_value
        client.pricings.list.return_value = result_obj

        result = run_defender_checks(_mock_credential(), subscription_id="sub-123")
        assert result["check"] == "defender"
        assert result["status"] == "pass"
        assert result["passed"] == 7
        assert result["failed"] == 0

    @patch("checks.defender.SecurityCenter", create=True)
    def test_defender_some_free(self, MockSecClient):
        from checks.defender import run_defender_checks, CRITICAL_PLANS

        pricings = []
        for i, plan_name in enumerate(sorted(CRITICAL_PLANS)):
            p = MagicMock()
            p.name = plan_name
            # Make first 3 Standard, rest Free
            p.pricing_tier = "Standard" if i < 3 else "Free"
            pricings.append(p)

        result_obj = MagicMock()
        result_obj.value = pricings

        client = MockSecClient.return_value
        client.pricings.list.return_value = result_obj

        result = run_defender_checks(_mock_credential(), subscription_id="sub-123")
        assert result["status"] == "fail"
        assert result["failed"] >= 1
        # At least some should be on Standard
        assert result["passed"] >= 1


# ---------------------------------------------------------------------------
# Orchestrator / Registry Test
# ---------------------------------------------------------------------------

class TestOrchestrator:
    def test_all_checks_registered(self):
        from checks import ALL_CHECKS
        expected = {"storage", "network", "keyvault", "sql", "compute", "appservice", "defender"}
        assert set(ALL_CHECKS.keys()) == expected
        assert len(ALL_CHECKS) == 7
