from __future__ import annotations

import importlib
import os
import sys
from pathlib import Path

import pytest

FAKES = Path(__file__).resolve().parent / 'fakes'


def load_module(monkeypatch):
    monkeypatch.syspath_prepend(str(FAKES))
    for name in ('numpy', 'sounddevice', 'deepgram'):
        if name in sys.modules:
            del sys.modules[name]
    if 'livetranscriber.livetranscriber' in sys.modules:
        del sys.modules['livetranscriber.livetranscriber']
    return importlib.import_module('livetranscriber.livetranscriber')


def test_valid_construction(monkeypatch):
    lt_mod = load_module(monkeypatch)
    monkeypatch.setenv('DEEPGRAM_API_KEY', 'token')
    obj = lt_mod.LiveTranscriber(callback=lambda text: None)
    assert obj._api_key == 'token'


def test_missing_callback(monkeypatch):
    lt_mod = load_module(monkeypatch)
    monkeypatch.setenv('DEEPGRAM_API_KEY', 'token')
    with pytest.raises(TypeError):
        lt_mod.LiveTranscriber(callback=None)


def test_missing_api_key(monkeypatch):
    lt_mod = load_module(monkeypatch)
    monkeypatch.delenv('DEEPGRAM_API_KEY', raising=False)
    with pytest.raises(RuntimeError):
        lt_mod.LiveTranscriber(callback=lambda _: None)
