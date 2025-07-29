import unittest
import noteforge as nf

class NoteTest(unittest.TestCase): 
    def test_interval_between(self):
        param_groups = [
            (nf.Note("E",3), nf.Note("F",3), "b2"),
            (nf.Note("E",3), nf.Note("F",4), "b2"),
            (nf.Note("C",3), nf.Note("Ab",3), "b6"),
            (nf.Note("C",3), nf.Note("G#",3), "#5"),
        ]
        for root,target,expected in param_groups:
            result = nf.get_interval_between_notes(root, target)
            self.assertEqual(result, expected)

    def test_interval_between_invalid(self):
        param_groups = [
            (nf.Note("C#",3), nf.Note("Eb",3)),
        ]
        for root,target in param_groups:
            result = nf.get_interval_between_notes(root, target)
            self.assertEqual(result, None)
            
    def test_transpose_interval_type(self):
        param_groups = [
            ("3","5","5"),
            ("b2","9","b9"),
            ("b13","6","b6"),
            ("#9","5","#5"),
            ("#5","#6",None)
        ]
        for interval,target_type,expected in param_groups:
            result = nf.transpose_interval_degree(interval,target_type)
            self.assertEqual(result, expected)
            
    def test_interval_map_consistency (self) : 
        param_groups = [
            (
                nf.Note("C",3),
                [nf.Note("G",3),nf.Note("E",4)],
                ["T","3","5"]
            ),
            (
                nf.Note("G#",3),
                [nf.Note("B#",4),nf.Note("D",4)],
                ["T","3","b5"]
            ),
            (
                nf.Note("Eb",3),
                [nf.Note("Bb",2),nf.Note("Ab",3)],
                ["T","4","5"]
            ),
            (
                nf.Note("Eb",3),
                [nf.Note("Bb",2),nf.Note("Ab",3),nf.Note("G")],
                ["T","3","5","11"]
            ),
            (
                nf.Note("Bb",3),
                [nf.Note("D",5),nf.Note("F#",4),nf.Note("Ab",4)],
                ["T","3","#5","b7"]
            ), 
            (
                nf.Note("E",3),
                [nf.Note("G#",5),nf.Note("A#",5),nf.Note("D",4)],
                ["T","3","b7","#11"]
            ), 
            (
                nf.Note("E",3),
                [nf.Note("F",3),nf.Note("A",3),nf.Note("B",3)],
                ["T","4","5","b9"]
            ), 
            (
                nf.Note("Ab",3),
                [nf.Note("C",4),nf.Note("Ebb",4),nf.Note("Gb",5),nf.Note("Bbb"),nf.Note("B")],
                ["T","3","b5","b7","b9","#9"]
            )
        ]
        
        for root,notes,expected_list in param_groups : 
            mapping = nf.HarmonicMap(root)
            for note in notes : 
                mapping.add_note(note)
            mapping_list = mapping.to_list()    
            self.assertEqual(mapping_list,expected_list,f"result: {mapping_list}")
            
