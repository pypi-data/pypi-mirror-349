"""
streamlit_lyrics_sync
=====================

A component for syncing lyrics to a timecode source over the Broadcast Channel API.

Requires a master component that emits timeUpdate events.

"""

__all__ = ["lyrics_sync", "NoteList", "Phrase", "srt_to_lyrics"]

from os import getenv
from pathlib import Path
from typing import Any, Dict, List

import streamlit as st
import streamlit.components.v1 as components
from dotenv import load_dotenv
from notes import NoteList
from phrase import Phrase, srt_to_lyrics

load_dotenv()

_RELEASE = getenv("RELEASE", False) in (True, "True")
if not _RELEASE:
    _component_func = components.declare_component(
        "lyrics_sync",
        url="http://localhost:5173",
    )
else:
    parent_dir = Path(__file__).parent
    build_dir = parent_dir / "frontend" / "dist"
    if not build_dir.exists():
        raise FileNotFoundError(f"Build directory not found: {build_dir}")
    _component_func = components.declare_component("lyrics_sync", path=build_dir)


def lyrics_sync(
    name: str,
    key: str = None,
    phrases: List[Phrase] | List[Dict[str, Any]] = None,
    notes: NoteList | List[Dict[str, Any]] = None,
    channel: str = None,
) -> None:
    """
    Displays a list of phrases with nested words with an animated display of the current word
    Used for displaying aligned lyrics alongside an audio waveform -- can also be used for speech subtitling.

    Arguments:
        name: The name of the component
        key: The key of the component
        phrases: A list of phrases with nested words to render
        notes: A list of notes to assist with word animation rendering
        channel: The broadcast channel to sync to for timeUpdate events

    Example:
        ```python

        # make up upstream master component that emits timeUpdate events
        # this could be a video player or audio player component
        state = timecode_master(channel="sync_channel")
        phrases = [
        {"start": 0, "end": 10, "text": "Hello, world!"},
        {"start": 10, "end": 20, "text": "This is a test."},
        ]
        notes = [
        {"start": 0, "end": 10, "frequency": 220},
        {"start": 10, "end": 20, "frequency": 440},
        ]
        lyrics_sync(name="lyrics_sync", key="lyrics_sync", phrases=phrases, notes=notes, channel="sync_channel")
        ```
    """
    component_value = _component_func(
        name=name,
        key=key,
        phrases=phrases,
        notes=notes,
        channel=channel,
    )
    return component_value


if __name__ == "__main__":
    if getenv("DEBUG", False) in (True, "True"):
        from demo import run_demo

        run_demo()
