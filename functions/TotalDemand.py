def totaldemand(inhabitants):
    Wpriv = 0.089  # ML/person/year, water demand for private use per person
    Wrest = 0.049  # ML/person/year, water demand for industry per person

    return inhabitants * Wpriv + inhabitants * Wrest