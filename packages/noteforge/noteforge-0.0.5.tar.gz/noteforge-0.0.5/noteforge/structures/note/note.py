from noteforge.data.alterations import handle_alteration_validation,alteration_and_value
from noteforge.data.note import chromatic_scale,natural_note_and_value,NaturalNote
from noteforge.data.freqs import freq_list,handle_range_validation
from copy import copy
from noteforge.data.note import *
class Note : 
    def __init__ (self,name: str,octave = 3) : 
        '''
        name format must be "note|alteration|octave"
        note : A B C D E F G 
        alteration : #, b, ##, bb or nothing,
        octave : values between or equal at 0 and 8
        input examples : A#, Ab, A#4, Ab4, Bb3, C5
        '''
        self._init = False
        self.set_note(name,octave)
        
    def copy (self) : 
        return copy(self)    
    
    def set_note (self,name,octave) : 
        proper_name,alteration = name[0],name[1:]
        self._init = False
        self.alteration = alteration  
        self.proper_name = proper_name
        self.octave = octave
        self._init = True
        handle_range_validation(self.get_absolute_position())
        return self
    
    @property
    def octave (self) : 
        return self.__octave 
    
    @octave.setter
    def octave (self,new_octave: int|None) : 
        if self._init :
            handle_range_validation(self.get_absolute_position())
            
        self.__octave = new_octave
    
    @property
    def alteration (self,) :  
        return self.__alteration  
    
    @alteration.setter
    def alteration (self,value : str) :
        if self._init :
            handle_range_validation(self.get_absolute_position())
            
        self.__alteration = handle_alteration_validation(value)
    
    @property
    def proper_name (self) : 
        return self.__proper_name
    
    @proper_name.setter
    def proper_name(self,value: str) :
        if self._init :
            handle_range_validation(self.get_absolute_position())
            
        self.__proper_name = handle_natural_note_validation(value)
   
    def get_full_name (self) : 
        return f"{self.proper_name}{self.alteration or ''}{self.octave}"
    
    def get_name (self) : 
        return f"{self.proper_name}{self.alteration or ''}"        
    
    def get_alteration_contribution (self) -> int : 
        return alteration_and_value[self.alteration] if self.alteration in alteration_and_value else 0
    
    def get_absolute_position (self) ->int : 
        alt_contribution = self.get_alteration_contribution()
        return ((self.octave * len(chromatic_scale)) + chromatic_scale[self.proper_name] + alt_contribution)
    
    def get_freq (self) : 
        return freq_list[self.get_absolute_position() - chromatic_scale["A"]]
    
    def get_chromatic_position (self) : 
        return self.get_absolute_position() % len(chromatic_scale)
    
    def get_natural_position (self) : 
        return natural_note_and_value[self.proper_name]

    def transpose (self,semitones:int) -> "Note" :
        from .morphers import get_transposed_note_attrs
        name,octave = get_transposed_note_attrs(self,semitones)
        self.set_note(name,octave)
        return self
    