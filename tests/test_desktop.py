"""Unit coverage for the native desktop launcher's failure boundaries."""

from __future__ import annotations

import sys
from pathlib import Path

import pytest

from finops_cost_intelligence import desktop


class _Process:
    def __init__(self, return_code: int | None = None) -> None:
        self.return_code = return_code

    def poll(self) -> int | None:
        return self.return_code


class _Response:
    status = 200

    def __enter__(self) -> _Response:
        return self

    def __exit__(self, *_args: object) -> None:
        return None


def test_user_data_directory_honors_the_explicit_override(
    monkeypatch: pytest.MonkeyPatch,
    tmp_path: Path,
) -> None:
    requested = tmp_path / "Costavow data"
    monkeypatch.setenv("METRORA_USER_DATA_DIR", str(requested))

    assert desktop._user_data_directory() == requested.resolve()


def test_child_command_uses_module_mode_during_development(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    monkeypatch.delattr(sys, "frozen", raising=False)
    monkeypatch.setattr(sys, "executable", "python-test")

    assert desktop._child_command(8510) == [
        "python-test",
        "-m",
        "finops_cost_intelligence.desktop",
        "--streamlit-child",
        "8510",
    ]


def test_child_command_reuses_the_packaged_executable(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    monkeypatch.setattr(sys, "frozen", True, raising=False)
    monkeypatch.setattr(sys, "executable", "Costavow.exe")

    assert desktop._child_command(8511) == ["Costavow.exe", "--streamlit-child", "8511"]


def test_wait_until_ready_accepts_a_healthy_local_service(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    monkeypatch.setattr(desktop, "urlopen", lambda *_args, **_kwargs: _Response())

    desktop._wait_until_ready("http://127.0.0.1:8512", _Process(), timeout=0.1)


def test_wait_until_ready_reports_an_early_child_exit() -> None:
    with pytest.raises(RuntimeError, match="stopped before the window opened"):
        desktop._wait_until_ready("http://127.0.0.1:8513", _Process(1), timeout=0.1)


def test_rebrand_keeps_legacy_storage_and_supports_new_override(monkeypatch, tmp_path) -> None:
    monkeypatch.delenv("COSTAVOW_USER_DATA_DIR", raising=False)
    monkeypatch.delenv("METRORA_USER_DATA_DIR", raising=False)
    monkeypatch.setattr(sys, "platform", "win32")
    monkeypatch.setenv("LOCALAPPDATA", str(tmp_path))
    assert desktop._user_data_directory() == tmp_path / "Metrora"
    monkeypatch.setenv("METRORA_USER_DATA_DIR", str(tmp_path / "legacy"))
    monkeypatch.setenv("COSTAVOW_USER_DATA_DIR", str(tmp_path / "current"))
    assert desktop._user_data_directory() == (tmp_path / "current").resolve()


def test_native_launcher_allows_exports_and_stops_its_service(monkeypatch, tmp_path) -> None:
    from types import SimpleNamespace
    from unittest.mock import Mock

    settings = {}

    def start(**kwargs):
        assert settings["ALLOW_DOWNLOADS"] is True
        assert kwargs == {"debug": False, "private_mode": True}

    window = SimpleNamespace(settings=settings, create_window=Mock(), start=start)
    process = Mock()
    process.poll.return_value = None
    monkeypatch.setitem(sys.modules, "webview", window)
    monkeypatch.setattr(desktop, "_configure_desktop_environment", lambda: tmp_path)
    monkeypatch.setattr(desktop, "_available_port", lambda: 8530)
    monkeypatch.setattr(desktop, "_wait_until_ready", lambda *_args: None)
    monkeypatch.setattr(desktop.subprocess, "Popen", lambda *_args, **_kwargs: process)
    desktop._launch_desktop()
    process.terminate.assert_called_once()
    process.wait.assert_called_once_with(timeout=5)
