#%%
import pandas as pd
import io

# Para fins de demonstração, vou simular o conteúdo do arquivo
# como se estivesse lendo-o diretamente.

file_path = ".csv"


# Passo 1: Encontrar o número da linha do cabeçalho dinamicamente
# Vamos ler o arquivo linha por linha até encontrar a linha com a coluna "EstacaoCodigo"
skip_rows = 0
with open(file_path, "r", encoding="utf-8") as f:
    for i, line in enumerate(f):
        # A primeira linha que contém 'EstacaoCodigo' é a que buscamos
        if "EstacaoCodigo" in line:
            # O skiprows deve ser o número da linha antes do cabeçalho,
            # então i é a linha do cabeçalho, e i+1 é o valor correto para pular
            skip_rows = i
            break
print(f"O cabeçalho foi encontrado na linha {skip_rows+1}. O skiprows será {skip_rows}.")


# Passo 2: Ler o arquivo com o número de linhas a pular dinâmico
# Usamos o valor de skip_rows encontrado
df = pd.read_csv(file_path, sep=";", skiprows=skip_rows, encoding="utf-8")


# Passo 3: Limpeza Inicial
# Remover a última coluna vazia e corrigir nomes
df = df.iloc[:, :-1]
df.columns = [col.strip() for col in df.columns]


# Passo 4: Transformar a estrutura dos dados
# Identificar as colunas de vazão
vazao_cols = [col for col in df.columns if col.startswith("Vazao")]


# Usar `melt` para transformar as colunas de vazão em linhas.
df_long = df.melt(
    id_vars=[
        "EstacaoCodigo",
        "NivelConsistencia",
        "Data",
        "Hora",
        "MediaDiaria",
    ],
    value_vars=vazao_cols,
    var_name="Dia_do_mes",
    value_name="Vazao_m3s",
)


# Passo 5: Limpeza e Conversão de Dados
# Remover linhas com valores ausentes ou vazios
df_long = df_long.dropna(subset=["Vazao_m3s"])
df_long = df_long[df_long["Vazao_m3s"].astype(str).str.strip() != ""]


# Substituir vírgulas por pontos e converter para float
df_long["Vazao_m3s"] = (
    df_long["Vazao_m3s"].astype(str).str.replace(",", ".").astype(float)
)


# Extrair o número do dia da coluna `Dia_do_mes`
df_long["Dia_do_mes"] = df_long["Dia_do_mes"].str.replace("Vazao", "").astype(int)


# Converter a coluna `Data` para o tipo datetime e combinar com o dia do mês
df_long["Data"] = pd.to_datetime(df_long["Data"], format="%d/%m/%Y")
df_long["DataCompleta"] = df_long["Data"] + pd.to_timedelta(
    df_long["Dia_do_mes"] - 1, unit="D"
)


# Passo 6: Organizar as colunas finais
df_final = df_long[
    [
        "EstacaoCodigo",
        "DataCompleta",
        "Vazao_m3s",
        "NivelConsistencia",
        "MediaDiaria",
    ]
].rename(columns={"DataCompleta": "Data", "Vazao_m3s": "Vazao (m3/s)"})


# Exibir o DataFrame final
print(df_final.head())

# Passo 7: Salvar o DataFrame final em um novo arquivo CSV
output_file_path = "_Vazoes_vertical.csv"
df_final.to_csv(
    output_file_path, sep=";", decimal=",", index=False, encoding="latin-1"
)
print(f"\nDataFrame salvo com sucesso em '{output_file_path}'")
# %%
