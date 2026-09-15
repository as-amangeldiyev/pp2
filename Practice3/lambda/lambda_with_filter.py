"""Examples of selecting items with filter and lambda."""


# Here is a list of test scores from which passing scores are selected.
test_scores = [48, 72, 59, 88, 61]
passing_scores = list(filter(lambda score: score >= 60, test_scores))
print("Passing scores:", passing_scores)
