import re


examples = {
    "dot": re.findall(r"c.t", "cat cot cut coat"),
    "star": re.findall(r"ab*c", "ac abc abbc abbbc"),
    "plus": re.findall(r"ab+c", "ac abc abbc"),
    "optional": re.findall(r"colou?r", "color colour"),
    "start_end": bool(re.search(r"^Python$", "Python")),
    "set": re.findall(r"[aeiou]", "regular expressions"),
    "alternation": re.findall(r"cat|dog", "cat, dog, bird"),
    "group": re.findall(r"(ha)+", "haha hahaha"),
    "digit_word_space": re.findall(r"\d+|\w+|\s", "A7 B"),
    "non_digit": re.findall(r"\D+", "Room 204"),
    "non_word": re.findall(r"\W", "a+b = c"),
    "non_space": re.findall(r"\S+", "one two"),
    "absolute_start": bool(re.search(r"\APython", "Python 3")),
    "absolute_end": bool(re.search(r"3\Z", "Python 3")),
}

for name, result in examples.items():
    print(f"{name}: {result}")
