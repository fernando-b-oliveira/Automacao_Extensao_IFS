﻿import pandas as pd
df_tgt_acomp = pd.read_excel(r"C:\Automacao\Codigosf\0800 e acompanhamento\Controle Acompanhamento 2026_Copia.xlsx", header=2)
print("Acomp columns (header=2):", df_tgt_acomp.columns.tolist()[:15])

df_tgt_0800 = pd.read_excel(r"C:\Automacao\Codigosf\0800 e acompanhamento\Registro 0800 e Incidentes RDGN - 2026_Copia.xlsx", header=1)
print("0800 columns (header=1):", df_tgt_0800.columns.tolist()[:15])


