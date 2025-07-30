from dataclasses import dataclass
from typing import Any, Dict, List


@dataclass
class Note:
    start: float
    end: float
    frequency: float


@dataclass
class NoteList:
    notes: List[Note]

    def __init__(self, notes: List[Note]):
        self.notes = notes

    def __len__(self):
        return len(self.notes)

    def __getitem__(self, index: int) -> Note:
        return self.notes[index]

    def __setitem__(self, index: int, note: Note):
        self.notes[index] = note

    def __iter__(self):
        return iter(self.notes)

    def __next__(self):
        return next(self.notes)

    @classmethod
    def from_json(cls, json_data: List[Dict[str, Any]]) -> "NoteList":
        return cls([Note(**note) for note in json_data])
