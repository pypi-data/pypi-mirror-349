from .mappings import *

def handle_interval_symbol_validation (value : IntervalSymbol) : 
    if value in interval_and_semitone : 
        return value
    
    raise ValueError(f"invalid IntervalSymbol '{value}',valid symbols are: {interval_and_semitone.keys()}")

def handle_interval_degree_validation (value : Intervaldegree) : 
    if value in interval_and_semitone : 
        return value
    
    raise ValueError(f"invalid Intervaldegree '{value}',valid degrees are: {interval_degree_and_value.keys()}")




