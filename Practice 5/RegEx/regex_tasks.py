import re


def main():
    # 1. An 'a' followed by zero or more 'b's.
    pattern1 = r"ab*"
    print("1:", re.findall(pattern1, "a ab abb abbb ac"))

    # 2. An 'a' followed by two or three 'b's.
    pattern2 = r"ab{2,3}"
    print("2:", re.findall(pattern2, "ab abb abbb abbbb"))

    # 3. Lowercase letter sequences joined by underscores.
    pattern3 = r"[a-z]+(?:_[a-z]+)+"
    print("3:", re.findall(pattern3, "first_name user_id Hello_world one_two_three"))

    # 4. One uppercase letter followed by one or more lowercase letters.
    pattern4 = r"\b[A-Z][a-z]+\b"
    print("4:", re.findall(pattern4, "Alice met Bob and McKay"))

    # 5. An 'a', followed by any characters, ending in 'b'.
    pattern5 = r"a.*b"
    print("5:", re.findall(pattern5, "a12b and acb, but not ax"))

    # 6. Replace every space, comma, or dot with a colon.
    text6 = "Hello, world. How are you?"
    print("6:", re.sub(r"[ ,. ]", ":", text6))

    # 7. Convert snake_case to camelCase.
    def snake_to_camel(text):
        words = text.split("_")
        return words[0] + "".join(word.capitalize() for word in words[1:])

    print("7:", snake_to_camel("this_is_snake_case"))

    # 8. Split a string at uppercase letters.
    text8 = "SplitAtUppercaseLetters"
    print("8:", re.findall(r"[A-Z]?[a-z]+|[A-Z]+(?=[A-Z]|$)", text8))

    # 9. Insert spaces before capitalized words in a PascalCase string.
    text9 = "InsertSpacesBetweenWords"
    print("9:", re.sub(r"(?<!^)(?=[A-Z])", " ", text9))

    # 10. Convert camelCase to snake_case, including acronym boundaries.
    def camel_to_snake(text):
        text = re.sub(r"([A-Z]+)([A-Z][a-z])", r"\1_\2", text)
        text = re.sub(r"([a-z0-9])([A-Z])", r"\1_\2", text)
        return text.lower()

    print("10:", camel_to_snake("camelCase and HTTPResponse"))


if __name__ == "__main__":
    main()
