from noteforge.data import interval_and_semitone,Intervaldegree,IntervalSymbol

def transpose_interval_degree (interval : IntervalSymbol, new_degree : Intervaldegree) : 
    new_interval = None
    if interval.startswith("#") : 
        new_interval = "#"+new_degree
    elif interval.startswith("b") :
        new_interval = "b"+new_degree
    else : 
        new_interval = new_degree
        
    if new_interval not in interval_and_semitone : return None
    return new_interval

