﻿import re
text = " conservação de viatura"
acomp_rx = re.compile(r"acomp|águas guariroba|aguas guariroba|prefeitura|sisep|sanesul|empreiteira|escava[çc][ãa]o|implanta[çc][ãa]o|sondagem|drenagem|pavimenta[çc][ãa]o|concession[áa]ria|rede de [áa]gua|rede de esgoto|reparo na via", re.I)

is_acomp = acomp_rx.search(text)
print("Acomp match:", is_acomp)

rx0800 = re.compile(r"0800|800|0300|300|cheiro|vazamento|press[ãa]o|falta de g[áa]s|inc[ê]ndio|fogo|trote|emerg[ê]ncia|rompimento|cliente ligou", re.I)
is_0800 = rx0800.search(text)
print("0800 match:", is_0800)


