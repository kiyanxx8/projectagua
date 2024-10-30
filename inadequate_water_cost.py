def Cwr(waterpump, Inhabitants, totaldemand):

    Wpriv = 0.073  # ML/person/year, water demand for private use per person
    Wrest = 0.0456  # ML/person/year, water demand for industry per person

    Cpriv = 730 # CHF/L Private residence Cost per person
    Crest = 1000 # CHF/L Industry Cost per person
    if totaldemand > waterpump:
        excessdemand = totaldemand - waterpump

        if Inhabitants * Wpriv > excessdemand:
            return excessdemand / Wpriv * Cpriv
        if Inhabitants * Wpriv < excessdemand:
            return Inhabitants * Cpriv + (excessdemand - Inhabitants * Wpriv) / Wrest * Crest

    else:
        return 0    
    
