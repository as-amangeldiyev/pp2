"""Examples of returning values and passing a list to a function."""


# Here is a function that receives a list and returns its average.
def average_score(scores):
    if not scores:
        return 0
    return sum(scores) / len(scores)


# Here is a list passed as an argument and the returned result stored in a variable.
exam_scores = [86, 91, 78, 95]
class_average = average_score(exam_scores)
print(f"Average score: {class_average:.2f}")
