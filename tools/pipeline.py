"""
📌 PARA QUE SERVE ESTE CÓDIGO?

Este arquivo gera um mini-relatório automático do Bitcoin.

Em termos simples, ele:
- Busca preços reais do Bitcoin na internet (CoinGecko)
- Organiza os dados em listas (preço e data)
- Calcula estatísticas básicas (ganhos e perdas)
- Identifica valores fora do padrão (outliers)
- Faz uma “previsão” simples (repete o último preço como referência)
- Cria um gráfico em PNG para visualizar

⚠️ Importante:
- NÃO é recomendação financeira.
- A previsão é bem simples e serve só como “ponto de comparação” (baseline).
"""

from __future__ import annotations

from typing import Any, Dict

from tools.market_data import (
    fetch_crypto_prices,   # Busca dados reais do Bitcoin na internet
    extract_prices,        # Pega só os preços do retorno da API
    extract_timestamps,    # Pega só as datas (em milissegundos)
)

from tools.analysis import (
    summarize_returns,     # Resume como o preço variou (retornos)
    detect_outliers_iqr,   # Acha pontos muito fora do padrão
    forecast_naive_last,   # Previsão simples: repete o último valor
    plot_prices_png,       # Cria e salva o gráfico em PNG
)


def bitcoin_report(days: int = 7, horizon: int = 3) -> Dict[str, Any]:
    """
    Gera um relatório simples do Bitcoin.

    Parâmetros:
    - days: quantos dias de histórico buscar
    - horizon: quantos “passos” no futuro a previsão simples vai repetir

    Retorno:
    - Um dicionário (tipo JSON) com estatísticas, outliers, previsão e gráfico.
    """

    # 1) Busca os dados reais do Bitcoin (em dólar) na CoinGecko
    payload = fetch_crypto_prices(coin_id="bitcoin", vs_currency="usd", days=days)

    # 2) Separa os dados em duas listas simples:
    #    - prices: lista de preços
    #    - ts: lista de datas (timestamps)
    prices = extract_prices(payload)
    ts = extract_timestamps(payload)

    # 3) Checagem simples: sem dados, não tem relatório
    if len(prices) < 3:
        return {
            "coin": "bitcoin",
            "days": int(days),
            "horizon": int(horizon),
            "n_prices": int(len(prices)),
            "reason": "Poucos dados para gerar o relatório (mínimo: 3 preços).",
        }

    # 4) Estatísticas básicas de variação (retornos)
    stats = summarize_returns(prices)

    # 5) Outliers: pontos que ficaram “fora do normal”
    outliers = detect_outliers_iqr(prices)

    # 6) Previsão simples (baseline): repete o último preço
    forecast = forecast_naive_last(prices, horizon=int(horizon))

    # 7) Gera o gráfico em PNG e salva na pasta "artifacts"
    chart = plot_prices_png(
        timestamps_ms=ts,
        prices=prices,
        title=f"Bitcoin - últimos {days} dias",
        out_dir="artifacts",
    )

    # 8) Link opcional para ver o PNG no navegador (só funciona localmente)
    #    Para funcionar, você precisa rodar o servidor local:
    #    python -m http.server 9000
    if chart.get("filename"):
        chart_url = f"http://127.0.0.1:9000/artifacts/{chart['filename']}"
    else:
        chart_url = None

    # 9) Monta e devolve o relatório completo
    return {
        "coin": "bitcoin",
        "days": int(days),
        "horizon": int(horizon),
        "n_prices": int(len(prices)),

        # Resultados da análise
        "stats": stats,
        "outliers": outliers,
        "forecast": forecast,

        # Informações do gráfico
        "chart_filename": chart.get("filename"),
        "chart_path": chart.get("path"),
        "chart_url": chart_url,

        # Dica para quem estiver usando o projeto localmente
        "note": (
            "Para ver o gráfico no navegador, rode "
            "'python -m http.server 9000' na raiz do projeto "
            "e abra o link em chart_url."
        ),
    }
