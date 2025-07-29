from __future__ import annotations

import importlib
import sys
from pathlib import Path

import numpy as np

FAKES = Path(__file__).resolve().parent / "fakes"


def load_whisper_transcriber(monkeypatch):
    # Ensure real numpy is used even if previous tests replaced it
    if "numpy" in sys.modules:
        del sys.modules["numpy"]
    import numpy as _np  # noqa: F401
    import importlib.util
    monkeypatch.syspath_prepend(str(FAKES))

    def _load_fake(name: str):
        path = FAKES / f"{name}.py"
        spec = importlib.util.spec_from_file_location(name, path)
        mod = importlib.util.module_from_spec(spec)
        assert spec and spec.loader
        spec.loader.exec_module(mod)  # type: ignore[attr-defined]
        monkeypatch.setitem(sys.modules, name, mod)

    _load_fake("deepgram")
    _load_fake("whisper")

    if "livetranscriber.transcribers" in sys.modules:
        del sys.modules["livetranscriber.transcribers"]
    trans_mod = importlib.import_module("livetranscriber.transcribers")
    return trans_mod.WhisperTranscriber


def test_flush_on_silence(monkeypatch):
    WhisperTranscriber = load_whisper_transcriber(monkeypatch)
    outputs = []
    wt = WhisperTranscriber(sample_rate=16000, callback=outputs.append)
    wt.connect()
    speech = (np.ones(1600, dtype=np.int16) * 1000).tobytes()
    wt.send(speech)
    silence = (np.zeros(16000, dtype=np.int16)).tobytes()
    wt.send(silence)
    assert outputs == ["test"]
