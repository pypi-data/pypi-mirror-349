from effspm import PrefixProjection, BTMiner

data = [[1, 2, 3], [1, 2], [2, 3]]

# Test PrefixProjection
result1 = PrefixProjection(data, minsup=0.5)
print("PrefixProjection Patterns:", result1["patterns"])

# Test BTMiner
result2 = BTMiner(data, minsup=0.5)
print("BTMiner Patterns:", result2["patterns"])
