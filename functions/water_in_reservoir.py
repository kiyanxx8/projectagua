def totwater(water_currently, rainfall, leakage, waterpump, totaldemand):
    water_min_constraint = 72000  # ML

    if water_currently <= water_min_constraint: # if water reserve is below minimum threshold
        return water_currently + rainfall - leakage
    else:
        if totaldemand >= waterpump:  # if total demand is greater than water pump capacity
            return water_currently + rainfall - leakage - waterpump
        else: 
            return water_currently + rainfall - leakage - totaldemand