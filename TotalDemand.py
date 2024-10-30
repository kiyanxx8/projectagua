def totaldemand(inhabitants):
    Wpriv = 0.073  # L/person/year, water demand for private use
    Wrest = 0.0456  # L/industry/year, water demand for industry

    return inhabitants * Wpriv + inhabitants * Wrest