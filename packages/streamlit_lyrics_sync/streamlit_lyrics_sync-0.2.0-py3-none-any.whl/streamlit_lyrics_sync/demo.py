def run_demo():
    import json
    from pathlib import Path

    import streamlit as st
    from phrase import build_lyrics
    from streamlit_wavesurfer import (
        OverlayPluginOptions,
        RegionsPluginOptions,
        WaveSurferOptions,
        WaveSurferPluginConfiguration,
        ZoomPluginOptions,
        image_to_base64,
        wavesurfer,
    )

    from streamlit_lyrics_sync import lyrics_sync

    # early exit if data directory doesn't exist
    if not Path(Path(__file__).parent.parent / "data").exists():
        st.error("Data directory not found")
        return
    with open(Path(__file__).parent.parent / "data" / "suzanne.srt", "r") as f:
        lyrics = f.read()
    with open(Path(__file__).parent.parent / "data" / "suzanne.word.srt", "r") as f:
        word_lyrics = f.read()

    with open(Path(__file__).parent.parent / "data" / "suzanne_notes.json", "r") as f:
        notes = json.load(f)
    with open(Path(__file__).parent.parent / "data" / "suzanne.mp3", "rb") as f:
        audio_src = f.read()
    with open(
        Path(__file__).parent.parent / "data" / "suzanne_piano_roll.png", "rb"
    ) as f:
        image_data = f.read()
        # convert to base64
        image_url = image_to_base64(image_data)
        overlay_options = OverlayPluginOptions(
            imageUrl=image_url,
            position="overlay",
            opacity=0.5,
            hideWaveform=False,
            imageRendering="pixelated",
        )
        overlay_plugin_config = WaveSurferPluginConfiguration(
            name="overlay",
            options=overlay_options,
        )

        zoom_plugin_configuration = WaveSurferPluginConfiguration(
            name="zoom",
            options=ZoomPluginOptions().__default_options__(),
        )

        region_plugin_configuration = WaveSurferPluginConfiguration(
            name="regions",
            options=RegionsPluginOptions(),
        )
        plugins = [
            region_plugin_configuration,
            zoom_plugin_configuration,
            overlay_plugin_config,
        ]

    with st.container(border=False):
        ws_state = wavesurfer(
            audio_src=audio_src,
            key="wavesurfer",
            plugins=plugins,
            show_controls=False,
            wave_options=WaveSurferOptions(
                hideScrollbar=True,
                # wavecolor light blue
                height=300,
                waveColor="#cccccc",
                # progress color gray
                progressColor="#3b82f6",
                minPxPerSec=201,
            ),
        )
    if ws_state:
        sync_channel_id = ws_state["syncChannelId"]
        phrases = build_lyrics(lyrics, word_lyrics)
        if sync_channel_id:
            lyrics_sync(
                "lyrics_sync",
                key="lyrics_sync",
                phrases=phrases,
                notes=notes,
                channel=sync_channel_id,
            )
