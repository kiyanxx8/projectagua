def totwater(water_currently, rainfall, leakage, waterpump, totaldemand):
    
    if totaldemand > waterpump:
        return water_currently + rainfall - leakage - waterpump
    if totaldemand < waterpump:
        return water_currently + rainfall - leakage - totaldemand