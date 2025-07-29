from noteforge.data.intervals.mappings import *
from noteforge.data.note.mappings import * 
from noteforge.data.alterations.mappings import *
from noteforge.data import handle_interval_degree_validation,handle_interval_symbol_validation
from noteforge.structures.note.note import Note
from typing import Union

def get_interval_between_notes(root : Note, target : Note) -> Union[IntervalSymbol,None] : 

    if root.get_name() == target.get_name() :  
        if root.get_absolute_position() == target.get_absolute_position() : return "T"
        else : return "8"
    
    natural_difference = None
    semitone_relative_difference = None

    root_ntaural_value,target_natural_value = root.get_natural_position(),target.get_natural_position()
    if root_ntaural_value > target_natural_value :
        natural_difference = (7-root_ntaural_value + target_natural_value) + 1
        semitone_relative_difference = (12-root.get_chromatic_position()+target.get_chromatic_position())
    else : 
        natural_difference = (target_natural_value-root_ntaural_value)+1
        semitone_relative_difference = (target.get_chromatic_position()-root.get_chromatic_position())

    if semitone_relative_difference < 0 : 
        semitone_relative_difference = semitone_relative_difference + len(chromatic_scale)
        
    interval_type_choices = value_and_interval_degrees[natural_difference]
    result = None
    
    for interval_type in interval_type_choices :
        choices = interval_degree_and_symbols[interval_type]
        for interval in choices : 
            if interval_and_semitone[interval] % 12 == semitone_relative_difference:
                result = interval
                break 
        if result is not None : break
        
    return result
    
def get_interval_weight (interval : IntervalSymbol) -> int : 
    if interval in interval_harmonic_weights : 
        return interval_harmonic_weights[interval]
    return 0

def get_interval_degree (interval : IntervalSymbol) -> Intervaldegree : 
    handle_interval_symbol_validation(interval)
    return symbol_and_interval_degree[interval]

def get_interval_degree_value (interval_degree : Intervaldegree) -> int : 
    handle_interval_degree_validation(interval_degree)
    return interval_degree_and_value[interval_degree]
    
def get_interval_semitones (interval : IntervalSymbol) -> int :
    return interval_and_semitone[handle_interval_symbol_validation(interval)]

def get_note_name_by_interval (root : Note,interval :IntervalSymbol) -> str : 
    interval_semitones = get_interval_semitones(interval)
    target_chromatic_value = (interval_semitones + root.get_chromatic_position()) % len(chromatic_scale)
    degree_value = interval_degree_and_value[get_interval_degree(interval)] - 1
    base_note_value = root.get_natural_position() + degree_value
    base_note = value_and_natural_note[base_note_value % len(natural_note_and_value)]

    if target_chromatic_value == chromatic_scale[base_note] : 
        return base_note
    else : 
        for k in alteration_and_value : 
            if target_chromatic_value == (alteration_and_value[k] + chromatic_scale[base_note]) : 
                return base_note+k
            
def get_note_by_interval (root : Note,interval : IntervalSymbol) : 
    note_name = get_note_name_by_interval(root,interval)
    c_distance = root.get_natural_position() + get_interval_degree_value(get_interval_degree(interval))
    
    if c_distance > len(natural_note_and_value) : 
        return Note(note_name, root.octave + 1)
    
    return Note(note_name, root.octave)
    
    
    
    

    
    