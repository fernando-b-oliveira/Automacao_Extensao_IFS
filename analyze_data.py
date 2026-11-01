import pandas as pd
import re
import sys

# Load manual sheets
file_acomp = r"C:\Automacao\Codigosf\0800 e acompanhamento\Controle Acompanhamento 2026_Copia.xlsx"
file_0800 = r"C:\Automacao\Codigosf\0800 e acompanhamento\Registro 0800 e Incidentes RDGN - 2026_Copia.xlsx"

try:
    df_acomp = pd.read_excel(file_acomp, sheet_name=0)
    print("Acompanhamento columns:", list(df_acomp.columns))
    for col in df_acomp.columns:
        if "diret" in str(col).lower() or "descri" in str(col).lower():
            print(f"\nSample Acompanhamento {col}:")
            print(df_acomp[col].dropna().head(10).tolist())
except Exception as e:
    print(f"Error reading Acompanhamento: {e}")

try:
    df_0800 = pd.read_excel(file_0800, sheet_name=0)
    print("\n0800 columns:", list(df_0800.columns))
    for col in df_0800.columns:
        if "diret" in str(col).lower() or "descri" in str(col).lower():
            print(f"\nSample 0800 {col}:")
            print(df_0800[col].dropna().head(10).tolist())
except Exception as e:
    print(f"Error reading 0800: {e}")


