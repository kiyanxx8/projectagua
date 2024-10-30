def totsup(water_act, rainfall, leakage):
    water_min = 1000 #ML

    return water_act + rainfall - leakage - water_min