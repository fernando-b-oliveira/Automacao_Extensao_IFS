﻿import pandas as pd
df = pd.read_excel(r"C:\Automacao\Codigosf\0800 e acompanhamento\Registro 0800 e Incidentes RDGN - 2026_Copia.xlsx", header=2)
# Look at the first column (Chamadas) or whatever has the descriptions
for i, col in enumerate(df.columns):
    print(f"Col {i}: {col}")


