from typing import Dict,List,Literal

IntervalSymbol = Literal[
    "T", "b2", "2", "b3", "3", "4", "#4", "b5", "5", "#5", "b6", "6", "bb7",
    "b7", "7", "8", "b9", "9", "#9", "11", "#11", "b13", "13"
]
Intervaldegree = Literal["T","2","3","4","5","6","7","8","9","#9","11","13"]

interval_and_semitone : Dict[IntervalSymbol,int] = {
    "T" : 0,
    "b2": 1,
    "2": 2,
    "b3": 3,
    "3": 4,
    "4": 5,
    "#4": 6,
    "b5": 6,
    "5": 7,
    "#5": 8,
    "b6": 8,
    "6": 9,
    "bb7" : 9,
    "b7": 10,
    "7": 11,
    "8": 12,
    "b9": 1 + 12,
    "9": 2 + 12,
    "#9": 3 + 12,
    "11": 5 + 12,
    "#11": 6 + 12,
    "b13": 8 + 12,
    "13": 9 + 12 
}
def gen_semitone_interval_dict () : 
    global interval_semitone_dict
    
    d : Dict[int,List[str]] = {}

    for k in interval_and_semitone : 
        semitones = interval_and_semitone[k]
        if semitones in d : 
            d[semitones].append(k)
        else :
            d[semitones] = [k]
            
    return d

semitone_and_interval : Dict[int,List[IntervalSymbol]] = gen_semitone_interval_dict()

interval_degree_and_symbols : Dict[Intervaldegree,List[IntervalSymbol]] = {
    "T" : ["T"],
    "2" : ["2","b2"],
    "3" : ["3","b3"],
    "4" : ["4","#4"],
    "5" : ["5","b5","#5"],
    "6" : ["6","b6"],
    "7" : ["7","b7"],
    "8" : ["8"],
    "9" : ["9","b9"],
    "#9" : ["#9"],
    "11" : ["11","#11"],
    "13" : ["13","b13"]
    }

symbol_and_interval_degree: Dict[IntervalSymbol, Intervaldegree] = {
    "T": "T",
    "2": "2",
    "b2": "2",
    "3": "3",
    "b3": "3",
    "4": "4",
    "#4": "4",
    "5": "5",
    "b5": "5",
    "#5": "5",
    "6": "6",
    "b6": "6",
    "7": "7",
    "b7": "7",
    "8": "8",
    "9": "9",
    "b9": "9",
    "#9": "#9",
    "11": "11",
    "#11": "11",
    "13": "13",
    "b13": "13"
}

interval_degree_and_value : Dict[Intervaldegree,int] = {
    "T" : 1,
    "2" : 2,
    "3" : 3,
    "4" : 4,
    "5" : 5,
    "6" : 6,
    "7" : 7,
    "8" : 8,
    "9" : 2,
    "#9" : 2,
    "11" : 4,
    "13" : 6
    }

value_and_interval_degrees : Dict[int,List[Intervaldegree]] = {
    1: ["T"],
    2: ["2", "9", "#9"],
    3: ["3"],
    4: ["4", "11"],
    5: ["5"],
    6: ["6", "13"],
    7: ["7"],
    8: ["8"]
}

interval_degree_equivalences : Dict[Intervaldegree,Intervaldegree] = {
    "2" : "9",
    "4" : "11",
    "6" : "13",
    "9" : "2",
    "11" : "4",
    "13" : "6"
}

interval_symbol_equivalences : Dict[IntervalSymbol,IntervalSymbol] = {
    "b3" : "#9",
    "#9" : "b3",
    "#4" : "b5",
    "b5" : "#4",
    "#5" : "b6",
    "b6" : "#5",
    "6" : "bb7",
    "bb7" : "6",
    "13" : "6"
}

no_quality_interval_degrees : List[Intervaldegree] = ["#9","T","8"]
unextended_tensions : List[IntervalSymbol] = ["b2","#2","#4","b6"]

interval_coexistence_restrictions : Dict[Intervaldegree,List[Intervaldegree]] = {
    "4" : ["3","2"],
    "2" : ["3","4"],
    "3" : ["2","4"] 
}

interval_harmonic_weights : Dict[IntervalSymbol,int] = { 
    "b2" : 1,
    "2" : 2,
    "b3" : 7,
    "3" : 7,
    "4" : 2,
    "5" : 15,
    "b7" : 5,
    "7" : 5,
    "8" : 7
}