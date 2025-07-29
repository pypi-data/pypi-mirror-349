from .mappings import *

def handle_natural_note_validation (value : NaturalNote) : 
    if value in natural_note_and_value : 
        return value
    
    raise ValueError(f"invalid natural note: {value}, valid notes are: {natural_note_and_value.keys()}")

def handle_chromatic_scale_validation (value) : 
    if value in chromatic_scale : 
        return value
    
    raise ValueError(f"invalid chromatic scale note: {value}, valid notes are: {chromatic_scale.keys()}")


