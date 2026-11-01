﻿import pandas as pd
df_tgt_acomp = pd.read_excel(r"C:\Automacao\Codigosf\0800 e acompanhamento\Controle Acompanhamento 2026_Copia.xlsx")
print("Acomp columns:", df_tgt_acomp.columns.tolist())
df_tgt_0800 = pd.read_excel(r"C:\Automacao\Codigosf\0800 e acompanhamento\Registro 0800 e Incidentes RDGN - 2026_Copia.xlsx")
print("0800 columns:", df_tgt_0800.columns.tolist())


