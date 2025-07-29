from __future__ import annotations

import importlib
import sys
from pathlib import Path

import pytest

FAKES = Path(__file__).resolve().parent / "fakes"


class FakeTranscriber:
    def __init__(self, *a, **k):
        self.connect_calls = 0
        self.close_calls = 0
        self.sent = []

    def connect(self):
        self.connect_calls += 1

    def send(self, data: bytes):
        self.sent.append(data)

    def close(self):
        self.close_calls += 1


class FakeDeepgramTranscriber(FakeTranscriber):
    pass


class FakeWhisperTranscriber(FakeTranscriber):
    pass


def load_module(monkeypatch):
    monkeypatch.syspath_prepend(str(FAKES))
    for name in ("numpy", "sounddevice", "deepgram", "whisper"):
        if name in sys.modules:
            del sys.modules[name]
    # Patch transcriber classes before importing LiveTranscriber
    trans_mod = importlib.import_module("livetranscriber.transcribers")
    monkeypatch.setattr(trans_mod, "DeepgramTranscriber", FakeDeepgramTranscriber)
    monkeypatch.setattr(trans_mod, "WhisperTranscriber", FakeWhisperTranscriber)
    if "livetranscriber.livetranscriber" in sys.modules:
        del sys.modules["livetranscriber.livetranscriber"]
    return importlib.import_module("livetranscriber.livetranscriber")


def test_pause_resume(monkeypatch):
    lt_mod = load_module(monkeypatch)
    monkeypatch.setenv("DEEPGRAM_API_KEY", "token")
    lt = lt_mod.LiveTranscriber(callback=lambda _: None)

    dg = lt._dg_transcriber
    wh = lt._whisper_transcriber

    # Initially active transcriber is Deepgram
    lt._active_transcriber.send(b"a1")

    # Pause switches to Whisper
    lt.pause()
    lt._active_transcriber.send(b"w1")

    assert dg.close_calls == 1
    assert wh.connect_calls == 1
    assert lt.paused is True

    # Resume switches back to Deepgram
    lt.resume()
    lt._active_transcriber.send(b"a2")

    assert wh.close_calls == 1
    assert dg.connect_calls == 1
    assert lt.paused is False

    assert dg.sent == [b"a1", b"a2"]
    assert wh.sent == [b"w1"]

