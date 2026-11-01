import pandas as pd

def read_and_find_header(file_path):
    print(f"\nAnalyzing: {file_path}")
    try:
        # Read first 10 rows to find header
        df_temp = pd.read_excel(file_path, sheet_name=0, nrows=10, header=None)
        header_row = -1
        for i, row in df_temp.iterrows():
            row_str = " ".join(str(x).lower() for x in row.dropna())
            if "diretriz" in row_str or "descri" in row_str or "tcnico" in row_str or "tecnico" in row_str:
                header_row = i
                break
        
        if header_row != -1:
            print(f"Found header at row {header_row}")
            df = pd.read_excel(file_path, sheet_name=0, header=header_row)
            print("Columns:", list(df.columns))
            for col in df.columns:
                if "diretriz" in str(col).lower() or "descri" in str(col).lower() or "tec" in str(col).lower() or "tc" in str(col).lower():
                    print(f"\nSample {col}:")
                    print(df[col].dropna().head(15).tolist())
        else:
            print("Could not find header row.")
    except Exception as e:
        print(f"Error: {e}")

file_acomp = r"C:\Automacao\Codigosf\0800 e acompanhamento\Controle Acompanhamento 2026_Copia.xlsx"
file_0800 = r"C:\Automacao\Codigosf\0800 e acompanhamento\Registro 0800 e Incidentes RDGN - 2026_Copia.xlsx"

read_and_find_header(file_acomp)
read_and_find_header(file_0800)


