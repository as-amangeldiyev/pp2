import re


text = "Python 3 is fun. Regex makes text search useful!"

print(re.search(r"Python", text).group())
print(re.findall(r"\b\w+\b", text))
print(re.split(r"[.!?]\s*", text))
print(re.sub(r"Python", "Learning Python", text))
print(re.match(r"Python", text).group())

