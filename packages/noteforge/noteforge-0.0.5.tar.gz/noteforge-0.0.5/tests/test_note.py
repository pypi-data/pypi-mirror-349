import unittest
from noteforge.structures.note import Note

class NoteTest(unittest.TestCase): 
    def test_valid_constructor(self): 
        param_groups = [
            ("F", 4, "F4"),
            ("Ab", 3, "Ab3"),
            ("C#", 5, "C#5"),
            ("Abb", 7, "Abb7"),
            ("Ax", 4, "Ax4"),
            ("E#", 4, "E#4"),
            ("Cb", 5, "Cb5")
        ]
        for note_name, octave, target in param_groups:
            note = Note(note_name, octave)
            self.assertEqual(note.get_full_name(), target) 
            
    def test_invalid_constructor(self):
        param_groups = [
            ("a", 4),
            ("H", 5),
            ("C##", 4),
            ("Cxx", 4),
            ("C", 9),
            ("C", -1),
            ("Ab",0),
            ("C#",8)
        ]
        for note_name, octave in param_groups:
            with self.assertRaises(Exception):
                Note(note_name, octave)

    def test_get_alteration_contribution(self):
        param_groups = [
            ("F", 4, 0),
            ("Ab", 3, -1),
            ("C#", 5, 1),
            ("Abb", 7, -2),
            ("Ax", 4, 2),
            ("E#", 4, 1),
            ("Cb", 5, -1)
        ]
        for note_name, octave, expected in param_groups:
            note = Note(note_name, octave)
            self.assertEqual(note.get_alteration_contribution(), expected)

    def test_transpose(self):
        param_groups = [
            ("C", 4, 2, "D4"),
            ("G", 3, 5, "C4"),
            ("A", 4, -3, "F#4"),
            ("E", 4, 7, "B4")
        ]
        for note_name, octave, semitones, target in param_groups:
            note = Note(note_name, octave)
            transposed = note.transpose(semitones)
            self.assertEqual(transposed.get_full_name(), target)
            
    def test_position(self):
        param_groups = [
            (Note("C",4),0,0),
            (Note("B",4),6,11),
        ]
        for note, natural, chroma in param_groups:
            self.assertEqual(note.get_natural_position(),natural)
            self.assertEqual(note.get_chromatic_position(),chroma)
            
    def test_freq (self) :
        param_groups = [
            (Note("A",0),27.5),
            (Note("C",8),4186.0),
        ]
        for note, expected in param_groups:
            self.assertEqual(round(note.get_freq(),1),round(expected,1))
