from typing import Literal,Dict

AlterationSymbol = Literal["#","b","x","bb",""]

alteration_and_value : Dict[AlterationSymbol,int] = {
    "#" : 1,
    "b" : -1,
    "x" : 2,
    "bb" : -2,
    "" : 0
}

value_and_alteration : Dict[int,AlterationSymbol] = {b:a for a,b in alteration_and_value.items()}