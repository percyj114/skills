"""Test configuration for auditclaw-azure tests."""

import os
import sys
from unittest.mock import MagicMock

# Add scripts directory to path
sys.path.insert(0, os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "scripts"))

# Pre-populate sys.modules with mock Azure SDK modules so that
# check modules can do top-level imports without requiring the real SDK.
_AZURE_MODULES = [
    "azure",
    "azure.identity",
    "azure.mgmt",
    "azure.mgmt.storage",
    "azure.mgmt.network",
    "azure.mgmt.compute",
    "azure.mgmt.keyvault",
    "azure.mgmt.sql",
    "azure.mgmt.web",
    "azure.mgmt.security",
    "azure.mgmt.monitor",
    "azure.mgmt.resource",
]

for mod_name in _AZURE_MODULES:
    if mod_name not in sys.modules:
        sys.modules[mod_name] = MagicMock()
