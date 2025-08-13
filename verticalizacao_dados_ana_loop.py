import pandas as pd
import io

estacoes_escolhidas =['46520000', '46530000']
for estacao in range (len(estacoes_escolhidas)):
    file_path = ""+ estacoes_escolhidas[estacao]+"_Vazoes.csv"

    print(estacoes_escolhidas[estacao])
    # Passo 1: Encontrar o número da linha do cabeçalho dinamicamente
    # Usar a codificação 'latin-1' para ler o arquivo corretamente
    skip_rows = 0
    with open(file_path, "r", encoding="latin-1") as f:
        for i, line in enumerate(f):
            if "EstacaoCodigo" in line:
                skip_rows = i
                break
    print(f"O cabeçalho foi encontrado na linha {skip_rows+1}. O skiprows será {skip_rows}.")


    # Passo 2: Ler o arquivo com o número de linhas a pular dinâmico
    # Usar a codificação 'latin-1' para ler o arquivo corretamente
    df = pd.read_csv(file_path, sep=";", skiprows=skip_rows, encoding="latin-1" , decimal=',')

    # Passo 3: Limpeza Inicial e Identificação Dinâmica de Colunas
    df = df.iloc[:, :-1]
    df.columns = [col.strip() for col in df.columns]

    vazao_cols = [col for col in df.columns if col.startswith("Vazao") and col[5:].isdigit()]
    id_vars = [col for col in df.columns if col not in vazao_cols]

    # Passo 4: Transformar a estrutura dos dados (melt)
    df_long = df.melt(
        id_vars=id_vars,
        value_vars=vazao_cols,
        var_name="Dia_do_mes",
        value_name="Vazao_m3s",)
    # Passo 5: Limpeza e Conversão de Dados
    df_long["Vazao_m3s"] = df_long["Vazao_m3s"].fillna(0.0)

    df_long["Dia_do_mes"] = pd.to_numeric(
        df_long["Dia_do_mes"].astype(str).str.extract("(\d+)").iloc[:, 0], errors='coerce'
    ).astype('Int64')

    # --- CORREÇÃO: Tratar datas inválidas de forma mais robusta ---
    df_long["Data"] = pd.to_datetime(df_long["Data"], format="%d/%m/%Y")
    df_long["DataCompleta"] = pd.to_datetime(
        df_long["Data"].dt.strftime("%Y-%m-") + df_long["Dia_do_mes"].astype(str),
        errors='coerce'
    )
    # Remover as linhas com datas inválidas (ex: 30 de fevereiro)
    df_long = df_long.dropna(subset=['DataCompleta'])

    # Passo 6: Organizar as colunas finais
    df_final = df_long[
        [
            "EstacaoCodigo",
            "DataCompleta",
            "Vazao_m3s",
            
        ]
    ].rename(columns={"DataCompleta": "Data", "Vazao_m3s": "Vazao (m3/s)"})

    # --- SUGESTÃO: Ordenar por data de forma decrescente ---
    df_final = df_final.sort_values(by='Data', ascending=False).reset_index(drop=True)

    # # Passo 7: Salvar o DataFrame final em um novo arquivo CSV
   
    print(estacoes_escolhidas[estacao])
    df_final.to_csv(str(estacoes_escolhidas[estacao])+'_Vazoes_vertical.csv', sep=";", decimal=",", index=False, encoding="latin-1")
    