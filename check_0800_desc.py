﻿import pandas as pd
df = pd.read_excel(r"C:\Automacao\Codigosf\0800 e acompanhamento\Registro 0800 e Incidentes RDGN - 2026_Copia.xlsx", header=2)
print(df.iloc[:20, 9].dropna().head(10).tolist())


