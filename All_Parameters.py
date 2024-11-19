water_min = 136800  # ML critical wateramount => when environmental costs get triggered
Env_Cost = 200 # CHF/ML
Wpriv = 0.089  # ML/person/year, water demand for private use per person
Wrest = 0.049  # ML/person/year, water demand for industry per person

Cpriv = 730 # CHF/ person/year Private Cost per person
Crest = 199 # CHF/ person/year Rest Cost per person

water_min_constraint = 72000  # ML, constraint water amount, this is the minimum amount of water that should be in the reservoir

cost_catchment_area_increase = 50  # Cost of increasing catchment area in $/m^2
cost_waterpump_capacity_increase = 100 # Cost of increasing water pump capacity in $/ML
operational_cost_waterpump_increase = 5 # Operational cost of the water pump capacity in $/ML