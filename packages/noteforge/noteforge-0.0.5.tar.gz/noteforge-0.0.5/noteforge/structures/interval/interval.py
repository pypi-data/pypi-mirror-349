from typing import TypedDict,List
from ..note.note import Note

class Interval () :
    def __init__ (self,note : Note,interval : str) : 
        self.note = note
        self.name = interval
        
