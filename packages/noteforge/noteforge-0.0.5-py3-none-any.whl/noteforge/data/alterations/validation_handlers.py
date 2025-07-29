from .mappings import alteration_and_value

def handle_alteration_validation (value) : 
    if value in alteration_and_value : 
        return value
    
    raise ValueError(f"{value} is a invalid alteration") 
