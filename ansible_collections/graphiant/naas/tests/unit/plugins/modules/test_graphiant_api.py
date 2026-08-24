# -*- coding: utf-8 -*-
# Copyright (c) Graphiant, Inc. | GNU General Public License v3.0+ (see LICENSES/GPL-3.0-or-later.txt)
"""Unit tests for graphiant_api module (mocked Ansible + connection)."""

from __future__ import annotations

from unittest.mock import MagicMock, patch

from ansible_collections.graphiant.naas.plugins.modules import graphiant_api

MODULE = "ansible_collections.graphiant.naas.plugins.modules.graphiant_api"


def _params(**overrides):
    params = {
        "host": "https://api.example.com",
        "username": "u",
        "password": "p",
        "access_token": None,
        "method": "get_bearer_token",
        "kwargs": None,
        "detailed_logs": False,
    }
    params.update(overrides)
    return params


def _module(**overrides):
    module = MagicMock()
    module.params = _params(**overrides)
    module.check_mode = overrides.pop("check_mode", False)
    return module


def _client(mock_conn):
    client = MagicMock()
    mock_conn.return_value.graphiant_config.config_utils.gsdk = client
    return client


@patch(f"{MODULE}.get_graphiant_connection")
@patch(f"{MODULE}.AnsibleModule")
def test_read_only_method_reports_unchanged(mock_module_cls, mock_conn) -> None:
    module = _module(method="get_bearer_token")
    mock_module_cls.return_value = module
    _client(mock_conn).get_bearer_token.return_value = "Bearer abc123"

    graphiant_api.main()

    module.exit_json.assert_called_once()
    kwargs = module.exit_json.call_args.kwargs
    assert kwargs["changed"] is False
    assert kwargs["method"] == "get_bearer_token"
    assert kwargs["response_data"] == "Bearer abc123"


@patch(f"{MODULE}.get_graphiant_connection")
@patch(f"{MODULE}.AnsibleModule")
def test_write_method_reports_changed(mock_module_cls, mock_conn) -> None:
    module = _module(method="put_devices_bringup", kwargs={"device_ids": [1], "status": "Allowed"})
    mock_module_cls.return_value = module
    client = _client(mock_conn)
    client.put_devices_bringup.return_value = True

    graphiant_api.main()

    client.put_devices_bringup.assert_called_once_with(device_ids=[1], status="Allowed")
    assert module.exit_json.call_args.kwargs["changed"] is True


@patch(f"{MODULE}.get_graphiant_connection")
@patch(f"{MODULE}.AnsibleModule")
def test_kwargs_are_forwarded(mock_module_cls, mock_conn) -> None:
    module = _module(method="get_edges_summary", kwargs={"hostname": "gateway-1"})
    mock_module_cls.return_value = module
    client = _client(mock_conn)
    client.get_edges_summary.return_value = None

    graphiant_api.main()

    client.get_edges_summary.assert_called_once_with(hostname="gateway-1")


@patch(f"{MODULE}.get_graphiant_connection")
@patch(f"{MODULE}.AnsibleModule")
def test_write_method_skipped_in_check_mode(mock_module_cls, mock_conn) -> None:
    module = _module(method="put_device_config", kwargs={"device_id": 1})
    module.check_mode = True
    mock_module_cls.return_value = module

    graphiant_api.main()

    mock_conn.assert_not_called()
    assert module.exit_json.call_args.kwargs["changed"] is True


@patch(f"{MODULE}.get_graphiant_connection")
@patch(f"{MODULE}.AnsibleModule")
def test_failure_omits_response_data(mock_module_cls, mock_conn) -> None:
    """Callers poll on `response_data is not none`, so a failure must not set it."""
    module = _module(method="get_edges_summary", kwargs={"device_id": "42"})
    mock_module_cls.return_value = module
    _client(mock_conn).get_edges_summary.side_effect = RuntimeError("boom")

    graphiant_api.main()

    module.fail_json.assert_called_once()
    assert "response_data" not in module.fail_json.call_args.kwargs


def test_every_supported_method_declares_change_semantics() -> None:
    """The argspec choices and the dispatch table must not drift apart."""
    assert graphiant_api.SUPPORTED_METHODS
    for name, modifies in graphiant_api.SUPPORTED_METHODS.items():
        assert isinstance(modifies, bool), name
    # Read-only names must be non-mutating; the bringup-token POST does create state.
    for name, modifies in graphiant_api.SUPPORTED_METHODS.items():
        if name.startswith("get_"):
            assert modifies is False, name
        if name.startswith("put_"):
            assert modifies is True, name


def test_convert_to_serializable_handles_pydantic_and_nesting() -> None:
    module = MagicMock()

    class Model:
        def model_dump(self):
            return {"a": 1}

    class Plain:
        def __init__(self):
            self.visible = "x"
            self._hidden = "y"

    assert graphiant_api.convert_to_serializable(module, Model()) == {"a": 1}
    assert graphiant_api.convert_to_serializable(module, Plain()) == {"visible": "x"}
    assert graphiant_api.convert_to_serializable(module, [Model()]) == [{"a": 1}]
    assert graphiant_api.convert_to_serializable(module, {"k": Model()}) == {"k": {"a": 1}}
    assert graphiant_api.convert_to_serializable(module, "Bearer abc") == "Bearer abc"
