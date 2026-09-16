"""Examples of returning values and passing a list to a function."""


def average_score(scores):
    if not scores:
        return 0
    return sum(scores) / len(scores)


exam_scores = [86, 91, 78, 95]
class_average = average_score(exam_scores)
print(f"Average score: {class_average:.2f}")
