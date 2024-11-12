def Cwr(waterpump, Inhabitants, totaldemand, Wpriv, Wrest, Cpriv, Crest):


    if totaldemand > waterpump: # if total demand is greater than water pump capacity
        excessdemand = totaldemand - waterpump

        if Inhabitants * Wpriv > excessdemand: # if the water demand for private use per person is greater than the excess demand
            return excessdemand / Wpriv * Cpriv # return the cost of the excess demand
        if Inhabitants * Wpriv < excessdemand: # if the water demand for private use per person is less than the excess demand
            return Inhabitants * Cpriv + (excessdemand - Inhabitants * Wpriv) / Wrest * Crest # return the cost of the excess demand

    else:
        return 0    
    
