﻿with open("test.js", "r", encoding="utf-8") as f:
    lines = f.readlines()

for i in range(10, 30):
    print(f"{i+1}: {repr(lines[i])}")


