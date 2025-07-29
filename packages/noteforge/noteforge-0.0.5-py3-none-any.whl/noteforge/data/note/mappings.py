from typing import Literal,Dict

NaturalNote = Literal["A","B","C","D","E","F","G"]

natural_note_and_value : Dict[NaturalNote,int] = {
    "C": 0,
    "D": 1,
    "E": 2,
    "F": 3,
    "G": 4,
    "A": 5,
    "B": 6
}

chromatic_scale : Dict[str,int] = {
    "C": 0,
    "C#": 1,
    "D": 2,
    "D#": 3,
    "E": 4,
    "F": 5,
    "F#": 6,
    "G": 7,
    "G#": 8,
    "A": 9,
    "A#": 10,
    "B": 11
}

sharp_swapping : Dict[str,str] = {
    "C#" : "Db",
    "D#" : "Eb",
    "F#" : "Gb",
    "G#" : "Ab",
    "A#" : "Bb"
}

bemol_swapping : Dict[str,str] = {v: k for k,v in sharp_swapping.items()}
value_and_natural_note : Dict[int,NaturalNote] = {v: k for k, v in natural_note_and_value.items()}
inverted_chromatic_scale : Dict[int,str] = {v: k for k, v in chromatic_scale.items()}