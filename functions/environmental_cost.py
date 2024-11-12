def costenv(current_wateramount, water_min, Env_Cost):
    # This function returns the environmental cost of the product



    if current_wateramount <= water_min:
        return (water_min - current_wateramount) * Env_Cost
    else:
        return 0