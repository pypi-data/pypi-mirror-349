from dataclasses import dataclass
from typing import Any, Dict, Iterator, List

SRTTimeString = str


@dataclass
class Word:
    start: float
    end: float
    text: str


@dataclass
class Phrase(Iterator[Word]):
    start: float
    end: float
    text: str
    words: List[Word]


@dataclass
class PhraseList:
    phrases: List[Phrase]

    def __iter__(self) -> Iterator[Phrase]:
        return iter(self.phrases)

    def __getitem__(self, item: int) -> Phrase:
        return self.phrases[item]

    def __len__(self) -> int:
        return len(self.phrases)

    @staticmethod
    def from_word_and_phrase_srt(word_srt: str, phrase_srt: str) -> "PhraseList":
        return PhraseList(srt_to_lyrics(word_srt, phrase_srt))


@dataclass
class LyricsSyncArgs:
    phrases: PhraseList
    channel: str
    show_timecode: bool = False


def srt_time_to_seconds(time: SRTTimeString):
    hours, minutes, seconds_milliseconds = time.split(":")
    seconds, milliseconds = seconds_milliseconds.split(",")
    return (
        int(hours) * 3600 + int(minutes) * 60 + int(seconds) + int(milliseconds) / 1000
    )


def srt_to_lyrics(srt: str) -> List[Phrase | Dict[str, Any]]:
    """
    Parses SRT format: index\ntiming\ntext\n\n...
    """
    blocks = srt.strip().split("\n\n")
    results = []
    for block in blocks:
        lines = block.strip().split("\n")
        if len(lines) >= 3:
            timing = lines[1]
            text = " ".join(line.strip() for line in lines[2:])
            if "-->" in timing:
                start, end = timing.split("-->")
                start = srt_time_to_seconds(start.strip())
                end = srt_time_to_seconds(end.strip())
                results.append(
                    {
                        "start": start,
                        "end": end,
                        "text": text,
                    }
                )
    return results


def build_lyrics(phrase_srt: str, word_srt: str = ""):
    """
    Builds a lyrics object from a phrase-level and word-level lyrics file
    Parses SRT format: index\ntiming\ntext\n\n...
    """
    # Split into blocks separated by blank lines
    phrases = srt_to_lyrics(phrase_srt)
    words = srt_to_lyrics(word_srt)
    # convert to a dict where the phrase contains any words that are within it
    for phrase in phrases:
        phrase["words"] = [
            word
            for word in words
            if word["start"] >= phrase["start"] and word["end"] <= phrase["end"]
        ]
    return phrases
