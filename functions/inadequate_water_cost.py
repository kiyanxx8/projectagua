def Cwr(waterpump, Inhabitants, totaldemand):

    Wpriv = 0.089  # ML/person/year, water demand for private use per person
    Wrest = 0.049  # ML/person/year, water demand for industry per person

    Cpriv = 730 # CHF/ person/year Private Cost per person
    Crest = 199 # CHF/ person/year Rest Cost per person
    if totaldemand > waterpump:
        excessdemand = totaldemand - waterpump

        if Inhabitants * Wpriv > excessdemand:
            return excessdemand / Wpriv * Cpriv
        if Inhabitants * Wpriv < excessdemand:
            return Inhabitants * Cpriv + (excessdemand - Inhabitants * Wpriv) / Wrest * Crest

    else:
        return 0    
    
