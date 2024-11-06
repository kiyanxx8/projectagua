def totaldemand(inhabitants):
    Wpriv = 0.073  # ML/person/year, water demand for private use
    Wrest = 0.073  # ML/per/year, water demand for industry

    return inhabitants * Wpriv + inhabitants * Wrest