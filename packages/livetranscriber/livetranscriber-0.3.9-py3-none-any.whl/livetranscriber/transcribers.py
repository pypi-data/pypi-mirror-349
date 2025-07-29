from __future__ import annotations

import asyncio
import json
from abc import ABC, abstractmethod
from typing import Callable, Any

from deepgram import (
    DeepgramClient,
    DeepgramClientOptions,
    LiveOptions,
    LiveTranscriptionEvents,
)
import vosk


class BaseTranscriber(ABC):
    """Abstract audio transcriber interface."""

    def __init__(self, callback: Callable[[str], Any]) -> None:
        self._callback = callback

    @abstractmethod
    def connect(self) -> None:
        """Establish underlying transcription connection."""

    @abstractmethod
    def send(self, data: bytes) -> None:
        """Send raw audio bytes to the recogniser."""

    @abstractmethod
    def close(self) -> None:
        """Terminate the transcription session."""


class DeepgramTranscriber(BaseTranscriber):
    """Transcriber implementation backed by Deepgram WebSocket API."""

    def __init__(
        self,
        api_key: str,
        options: LiveOptions,
        callback: Callable[[str], Any],
        *,
        keepalive: bool = True,
    ) -> None:
        super().__init__(callback)
        client_opts = (
            DeepgramClientOptions(options={"keepalive": "true"}) if keepalive else None
        )
        self._dg_client = DeepgramClient(api_key, client_opts)
        self._ws = self._dg_client.listen.websocket.v("1")
        self._options = options

    def connect(self) -> None:
        self._ws.on(LiveTranscriptionEvents.Open, self._on_open)
        self._ws.on(LiveTranscriptionEvents.Transcript, self._on_transcript)
        self._ws.on(LiveTranscriptionEvents.Error, self._on_error)
        self._ws.on(LiveTranscriptionEvents.Close, self._on_close)
        self._ws.start(self._options)

    def send(self, data: bytes) -> None:
        self._ws.send(data)

    def close(self) -> None:
        self._ws.finish()

    # Event handlers -------------------------------------------------
    def _on_open(self, *_):
        print("🟢  Deepgram connection established")

    def _on_transcript(self, _client, result, **_):
        text = result.channel.alternatives[0].transcript.strip()
        if text:
            maybe_coro = self._callback(text)
            if asyncio.iscoroutine(maybe_coro):
                asyncio.create_task(maybe_coro)

    def _on_error(self, _client, exc, **_):
        print(f"❌  Deepgram error: {exc}")

    def _on_close(self, *_):
        print("🔴  Deepgram connection closed")


class VoskTranscriber(BaseTranscriber):
    """Offline transcriber using the Vosk library."""

    def __init__(self, sample_rate: int, callback: Callable[[str], Any], model_path: str = "model") -> None:
        super().__init__(callback)
        self._recognizer = vosk.KaldiRecognizer(vosk.Model(model_path), sample_rate)

    def connect(self) -> None:
        pass  # Nothing to do for Vosk

    def send(self, data: bytes) -> None:
        if self._recognizer.AcceptWaveform(data):
            text = json.loads(self._recognizer.Result()).get("text", "").strip()
            if text:
                maybe_coro = self._callback(text)
                if asyncio.iscoroutine(maybe_coro):
                    asyncio.create_task(maybe_coro)

    def close(self) -> None:
        text = json.loads(self._recognizer.FinalResult()).get("text", "").strip()
        if text:
            maybe_coro = self._callback(text)
            if asyncio.iscoroutine(maybe_coro):
                asyncio.create_task(maybe_coro)

