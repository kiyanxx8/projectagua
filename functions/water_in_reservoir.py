def totwater(water_currently, rainfall, leakage, waterpump, totaldemand):
    water_min_constraint = 72000  # ML

    if water_currently <= water_min_constraint:
        return water_currently + rainfall - leakage
    
    if totaldemand >= waterpump:
        return water_currently + rainfall - leakage - waterpump
    else:
        return water_currently + rainfall - leakage - totaldemand