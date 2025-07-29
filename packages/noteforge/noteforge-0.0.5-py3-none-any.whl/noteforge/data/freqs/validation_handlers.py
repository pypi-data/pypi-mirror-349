from .mappings import freqs
from ..note import chromatic_scale

def handle_range_validation (value : int) : 
    if value >= len(freqs)+chromatic_scale["A"] or value < chromatic_scale["A"] :
        raise ValueError(f"note is out of range out of range -> [A0 - C8]")
    return value