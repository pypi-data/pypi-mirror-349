from noteforge.structures.note.note import Note
from noteforge.data.note import chromatic_scale,inverted_chromatic_scale
from typing import Tuple
from noteforge.data.freqs.validation_handlers import handle_range_validation
def get_transposed_note_attrs(note : Note,semitones : int) -> Tuple[str,int] :
    '''
    This function return `note name` and `octave`
        '''
    chromatic_len = len(chromatic_scale) 
    new_absolute_position = note.get_absolute_position() + semitones
    new_name = inverted_chromatic_scale[new_absolute_position % chromatic_len]

    new_octave = int(new_absolute_position / chromatic_len)
    try :
        handle_range_validation(new_absolute_position)
    except ValueError :
        raise ValueError(f"result of transposition is {new_name}{new_octave}, this note is out of range -> [A0 - C8]")
    return new_name,new_octave

def transpose_note (note : Note,semitones : str) -> Note :
    name,octave = get_transposed_note_attrs(note,semitones)
    return Note(name, octave)