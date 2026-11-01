﻿import pandas as pd
import sys
import warnings
warnings.filterwarnings("ignore")

try:
    df_gen_0800 = pd.read_excel(r"C:\Users\UsuarioPadrao\Downloads\Relatorio_Separado_SISTEMA_ERP_EXEMPLO (7).xlsx", sheet_name="0800")
    df_gen_acomp = pd.read_excel(r"C:\Users\UsuarioPadrao\Downloads\Relatorio_Separado_SISTEMA_ERP_EXEMPLO (7).xlsx", sheet_name="Acompanhamento")
    
    print(f"Generated 0800 count: {len(df_gen_0800)}")
    print(f"Generated Acomp count: {len(df_gen_acomp)}")
except Exception as e:
    print(f"Could not read generated file: {e}")

try:
    df_tgt_0800 = pd.read_excel(r"C:\Automacao\Codigosf\0800 e acompanhamento\Registro 0800 e Incidentes RDGN - 2026_Copia.xlsx")
    print(f"Target 0800 rows: {len(df_tgt_0800)}")
    print("Target 0800 sample OSs:", df_tgt_0800['Nº Ordem'].dropna().head(5).tolist())
except Exception as e:
    print(f"Could not read tgt 0800: {e}")

try:
    df_tgt_acomp = pd.read_excel(r"C:\Automacao\Codigosf\0800 e acompanhamento\Controle Acompanhamento 2026_Copia.xlsx")
    print(f"Target Acomp rows: {len(df_tgt_acomp)}")
    print("Target Acomp sample OSs:", df_tgt_acomp['Nº Ordem'].dropna().head(5).tolist())
except Exception as e:
    print(f"Could not read tgt acomp: {e}")



