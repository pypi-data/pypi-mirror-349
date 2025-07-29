from noteforge.data import interval_degree_and_value,IntervalSymbol,unextended_tensions,interval_degree_equivalences,interval_coexistence_restrictions,interval_and_semitone,no_quality_interval_degrees
from ..interval.transposers import transpose_interval_degree
from ..interval.interval import Interval
from typing import Dict,List
from ..note.note import Note
from ..interval.interval_getters import get_interval_between_notes,get_interval_degree

class HarmonicMap () : 
    def __init__(self, root: Note):
        if type(root) != Note : 
            raise TypeError("root param must be Note object")
        self.root: Note = root
        self.intervals: Dict[str,List[Interval]] = {k: [] for k in interval_degree_and_value}
        self.intervals["T"] = []
        self.add_note(self.root) 
    
    def __str__(self):
        for k in self.intervals : 
            interval_type_set : List[Interval] = self.intervals[k]
            if len(interval_type_set) <= 0 : continue
            for interval in interval_type_set :
                print(f"---- {interval.name}: {interval.note.get_full_name()}")
         
        return ">> MAP END"
    
    def to_list (self) : 
        result = []
        for k in self.intervals : 
            if len(self.intervals[k]) > 0 :
                result.append(self.intervals[k][0].name)
        return result
    
    def _add_interval (self,interval_type : str,interval_name:str,note:Note) -> bool :
        '''Avoid adding duplicate absolute positions. For example, if bb7 is already in the interval map, then 6 should not be added'''
        new_interval = Interval(note,interval_name)
        currents : List[Interval] = self.intervals[interval_type]
        if new_interval.note.get_absolute_position() not in [interval.note.get_absolute_position() for interval in currents] : 
            self.intervals[interval_type].append(new_interval)
            return True
        else:
            return False
    
    def add_note (self,note : Note) : 
        '''
        This function applies rules to find and add the interval, even if it requires making adjustments (applying extensions) to do so. 
        Examples:
        - If you try to add a <#4> interval, an extension will be applied if <3rd> is already present in the intervals.
        - If you try to add a <3> interval and the HarmonicMap contains <2> or <4>, they will be replaced with their extensions, which are <9> and <11>.
        '''
    
        interval = get_interval_between_notes(self.root,note)
        
        if interval is None : return False

        if self.try_to_add_self_referential_interval(interval,note) : return True
        if self.try_to_add_extension(interval,note) : return True
        if self.try_to_add_extensible(interval,note) : return True
        if self.try_to_add_unextensible(interval,note) : return True
        return False 
        
    def try_to_add_self_referential_interval (self,interval:IntervalSymbol,note:Note) -> bool : 
        interval_type = get_interval_degree(interval)
        if interval_type not in no_quality_interval_degrees : return False
   
        return self._add_interval(interval_type,interval,note)
        
    def try_to_add_extension (self,interval:IntervalSymbol,note:Note) -> bool : 
        interval_type = get_interval_degree(interval)
        if interval_type not in interval_degree_equivalences : return False
        if interval_and_semitone[interval] < 12 : return False
        
        return self._add_interval(interval_type,interval,note)
    
    def try_to_add_extensible (self,interval:IntervalSymbol,note:Note) -> bool : 
        interval_degree = get_interval_degree(interval)
        if interval_degree not in interval_degree_equivalences : return False
        if interval_and_semitone[interval] > 12 : return False
        restrictions = interval_coexistence_restrictions[interval_degree]
        extension_degree = interval_degree_equivalences[interval_degree]
        extension = transpose_interval_degree(interval,extension_degree)
        
        if any(len(self.intervals[avoid_type]) > 0 for avoid_type in restrictions) or interval in unextended_tensions : 
            return self._add_interval(extension_degree,extension,note)
        else : 
            return self._add_interval(interval_degree,interval,note)
     
    def try_to_add_unextensible (self,interval:IntervalSymbol,note:Note) -> bool : 
        interval_type = get_interval_degree(interval)
        if interval_type in interval_degree_equivalences : return False
        
        restrictions = interval_coexistence_restrictions[interval_type] if interval_type in interval_coexistence_restrictions else []
 
        for avoid_type in restrictions : 
            if len(self.intervals[avoid_type]) > 0 :
                extension_degree = interval_degree_equivalences[avoid_type]
                intervals = self.intervals[avoid_type]
                for avoid_interval in intervals : 
                    extension = transpose_interval_degree(avoid_interval.name,extension_degree)
                    self._add_interval(extension_degree,extension,note)

                self.intervals[avoid_type] = []
        
        self._add_interval(interval_type,interval,note)
        
        return True
        