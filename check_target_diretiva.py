﻿import pandas as pd

try:
    df_tgt_acomp = pd.read_excel(r"C:\Automacao\Codigosf\0800 e acompanhamento\Controle Acompanhamento 2026_Copia.xlsx")
    col_dir = [c for c in df_tgt_acomp.columns if 'Diretiva' in c or 'Diretriz' in c]
    if col_dir:
        print("Target Acomp Diretiva unique values:")
        print(df_tgt_acomp[col_dir[0]].value_counts().head(15))
    else:
        print("No Diretiva column found in Acomp target.")

    print("\n---")
    df_tgt_0800 = pd.read_excel(r"C:\Automacao\Codigosf\0800 e acompanhamento\Registro 0800 e Incidentes RDGN - 2026_Copia.xlsx")
    col_dir2 = [c for c in df_tgt_0800.columns if 'Diretiva' in c or 'Diretriz' in c]
    if col_dir2:
        print("Target 0800 Diretiva unique values:")
        print(df_tgt_0800[col_dir2[0]].value_counts().head(15))
    else:
        print("No Diretiva column found in 0800 target.")

except Exception as e:
    print(f"Error: {e}")



