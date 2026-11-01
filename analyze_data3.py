import pandas as pd

def print_first_rows(file_path):
    print(f"\nAnalyzing: {file_path}")
    try:
        df = pd.read_excel(file_path, sheet_name=0, nrows=15, header=None)
        print(df.to_string(index=False))
    except Exception as e:
        print(f"Error: {e}")

file_acomp = r"C:\Automacao\Codigosf\0800 e acompanhamento\Controle Acompanhamento 2026_Copia.xlsx"
file_0800 = r"C:\Automacao\Codigosf\0800 e acompanhamento\Registro 0800 e Incidentes RDGN - 2026_Copia.xlsx"

print_first_rows(file_acomp)
print_first_rows(file_0800)


