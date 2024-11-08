def totaldemand(inhabitants):
    Wpriv = 0.09  # ML/person/year, water demand for private use
    Wrest = 0.06  # ML/per/year, water demand for industry

    return inhabitants * Wpriv + inhabitants * Wrest