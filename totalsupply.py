def totsup(water_act, rainfall, leakage):
    water_min = 1000 #ML, idk the real value

    return water_act + rainfall - leakage - water_min