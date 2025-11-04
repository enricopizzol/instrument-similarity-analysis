# Ata da Reunião

- **Data**: 30/10/2025
- **Tema**: Alinhamento sobre apresentação e próximos passos do projeto de análise de similaridade de instrumentos

## Resumo
- **Principal**: A apresentação foi confusa; fala desconectada dos slides.
- **Diretriz**: Próxima versão deve ser mais clara, direta e com sinergia entre narrativa e slides.
- **Foco técnico**: Definições de domínio, correção de granularidade/frequência e plano de experimentos por frequência.

## Problemas Identificados
- **Desconexão fala-slides**.
- **Escopo pouco claro**: o que está sendo feito, ambiente, como testar, objetivo.
- **Baixa especificidade**: poucos exemplos e visualizações.

## Recomendações para os Próximos Slides
- **Domínio**: O que é instrumento, ticker, papel (ex.: VALE3, PETR4). Revisitar o conceito de trade.
- **Séries temporais**: Explicar variação de preço no tempo e ilustrar com gráficos (efeito do número de pontos).
- **Granularidade**: Deixar claro o conceito e relação com frequência amostral.
- **Correção conceitual**:
  - Baixa granularidade → janelas maiores (menor frequência).
  - Alta granularidade → janelas menores (alta frequência, ex.: ms).

## Plano de Experimentos
- **Etapa 2 — Correlação por frequência**:
  - Fixar dois instrumentos: VALE3 e PETR4.
  - Frequências: 1ms, 5ms, 100ms, 1s, 5min, 15min, 1h.
  - Objetivo: identificar a partir de qual janela a correlação diminui.
- **Etapa 3 — Automação/Execução (PCAD/Draco)**:
  - Script para rodar no PCAD e distribuir nas máquinas Draco.
  - Gerar input aleatório com tuplas:
    - `inst1, inst2, period, freq, correlation, repeat`
  - Repetir N=10. Período: 1 ano. Frequências: 1ms, 1s, 1min, 1h, 1d.
  - Focar na métrica de tempo de execução (load, transform, correlação).
  - Rodar em partes (lotes).

## Itens Técnicos a Ajustar
- **Scripts**: Corrigir/otimizar load e transform.
- **Medições**: Coletar tempos por etapa.
- **Reprodutibilidade**: Semente para geração aleatória.
- **Ambiente**: Documentar (PCAD/Draco), versões e dependências.

## Decisões
- **Instrumentos**: VALE3 e PETR4 na Etapa 2.
- **Métrica foco**: Tempo de execução.
- **Visualizações**: Gráficos de séries e de correlação por granularidade.

## Entregáveis
- **Slides revisados**.
- **Notebook/Script**: Correlações multi-frequência para VALE3×PETR4.
- **Pipeline**: Geração de inputs, execução (PCAD/Draco) e medição de tempos.
- **Relatório**: Queda de correlação vs granularidade.

## Pendências
- **Confirmar frequências**.
- **Padronizar conceito**: granularidade vs frequência.
- **Definir responsáveis e prazos.**

## Próximas Ações
- **[Slides]**: Reestruturar com foco em domínio, método, objetivos, resultados esperados.
- **[Experimentos]**: Rodar correlação VALE3×PETR4 nas frequências definidas e plotar.
- **[Infra]**: Preparar scripts para PCAD/Draco (lotes, logging de tempos).
- **[Dados]**: Ajustar load/transform.

---

## O que foi feito até agora

- **Coleta de dados (MT5)**  
  - `data_retrieval.py`: carrega credenciais (`.env`), inicializa MT5, coleta ticks de 5 instrumentos exemplo (PETR4, VALE3, ITUB4, BBDC4, WEGE3) no período de 1 ano e salva CSVs (`instrument_series/`) com `instrument,time,last`.

- **Transformação e limpeza**  
  - `correlation_analysis.py`:
    - `load_and_transform_file`: converte `time_msc`→`datetime`, filtra horário de pregão (10:00–17:00), `ffill/bfill`, mantém `instrument,last`, indexa por `datetime`.
    - `transform_all_files`: processa todos os CSVs de `dataset/` e salva em `clean_dataset/instrument_series/`.

- **Reamostragem e correlação**  
  - `resample_and_fill`: 1ms/1S/1T/1H/1D (agrega duplicados para 1ms, `last()` e `ffill` nas demais).
  - `calculate_correlation_with_timing`: Pearson/Spearman/Kendall com medição de tempo e sincronização por índice.

- **Geração de combinações**  
  - `generate_combinations.py`: gera `instrument_combinations_shuffled.csv` com tuplas `(inst1, inst2, period=1Year, freq in [1ms,1S,1T,1H,1D], correlation in [pearson,kendall,spearman], repeat=1..10)` embaralhadas.

- **Execução em lote**  
  - `run_correlations.sh`: processa o CSV de combinações (todas ou primeiras N linhas) chamando `python correlation_analysis.py "<linha>"`.

- **Exploração e validação em notebook**  
  - `script_correlation_pipeline.ipynb`: pipeline end-to-end
    - Lista e transforma um instrumento; plota séries em múltiplas frequências (1ms, 1S, 1T, 1H, 1D).
    - Executa testes de correlação em par de instrumentos e reporta `time_sec`.

- **Todo**  
  - `README.md`: melhorar doc 
  