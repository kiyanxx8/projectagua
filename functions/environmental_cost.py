def costenv(current_wateramount):
    # This function returns the environmental cost of the product
    water_min = 136800  # ML
    water_min_constraint = 72000  # ML
    Env_Cost = 200 # CHF/ML


    if current_wateramount <= water_min:
        return (water_min - current_wateramount) * Env_Cost
    else:
        return 0