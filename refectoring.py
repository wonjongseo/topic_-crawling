import json


fileName = "TOKIC12data.json"

words = []

with open(fileName, "r", encoding="utf-8") as f:
    words = json.load(f)






for word in words:
    print(word)


