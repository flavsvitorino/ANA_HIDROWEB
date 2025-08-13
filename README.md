# ANA_HIDROWEB
Vertilização dos dados de vazão da Agência Nacional de Águas e Saneamento
Este repositório contém um script em Python para processar e verticalizar dados de vazão da Agência Nacional de Águas (ANA), obtidos através do portal HidroWeb. O objetivo principal é transformar o formato de dados "wide" (com colunas para cada dia do mês) em um formato "long", ideal para análises de séries temporais e visualização de dados.
Funcionalidades

    Leitura de Dados: O script lê o arquivo CSV, detectando o cabeçalho dinamicamente.

    Verticalização: Utiliza pandas.melt para converter as colunas de vazão (Vazao01 a Vazao31) em um formato de dados vertical, com uma coluna para a data e outra para a vazão.

    Tratamento de Datas: Valida as datas geradas, removendo entradas inválidas (como 30 de fevereiro) e garantindo a consistência.

    Limpeza de Dados: Preenche valores de vazão ausentes (NaN) com 0.0.

    Exportação: Salva o DataFrame final, ordenado pela data mais recente, em um novo arquivo CSV (vazoes_processado.csv)
    
    Certifique-se de ter a biblioteca pandas instalada
