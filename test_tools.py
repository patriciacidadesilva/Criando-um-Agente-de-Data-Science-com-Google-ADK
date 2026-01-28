"""
📌 PARA QUE SERVE ESTE CÓDIGO?

Este script é um “teste rápido” das tools do projeto (SEM ADK).

Ele:
- Busca preços reais do Bitcoin na internet (CoinGecko)
- Extrai preços e timestamps do payload retornado
- Calcula estatísticas de retorno (média, volatilidade, min/max)
- Detecta outliers usando IQR
- Gera uma previsão simples (baseline: último valor repetido)
- Gera um gráfico em PNG e salva em ./artifacts

⚠️ Importante:
- NÃO é recomendação financeira.
- A previsão é apenas baseline (referência simples).
"""

from __future__ import annotations

from tools.market_data import (
    fetch_crypto_prices,
    extract_prices,
    extract_timestamps,
)

from tools.analysis import (
    summarize_returns,
    detect_outliers_iqr,
    forecast_naive_last,
    plot_prices_png,
)


def main() -> None:
    """
    Ponto de entrada do script.
    Roda o pipeline mínimo e imprime resultados no terminal.
    """

    days = 90
    horizon = 7

    # 1) Busca dados reais do Bitcoin (em USD) na CoinGecko
    payload = fetch_crypto_prices(coin_id="bitcoin", vs_currency="usd", days=days)

    # 2) Extrai listas simples de preços e timestamps
    prices = extract_prices(payload)
    ts = extract_timestamps(payload)

    # 3) Validação mínima: sem dados, não continua
    print(f"\n✅ Total de preços retornados: {len(prices)}")
    if len(prices) < 3:
        print("⚠️ Poucos dados para análise (mínimo: 3 preços). Encerrando.")
        return

    # 4) Estatísticas de retorno
    print("\n📈 Estatísticas de retorno:")
    stats = summarize_returns(prices)
    print(stats)

    # 5) Outliers (IQR)
    print("\n🚨 Outliers (IQR):")
    outliers = detect_outliers_iqr(prices)
    print(outliers)

    # 6) Previsão simples (baseline)
    print("\n🔮 Previsão simples (baseline):")
    forecast = forecast_naive_last(prices, horizon=horizon)
    print(forecast)

    # 7) Gráfico PNG (salvo em ./artifacts)
    print("\n🖼️ Gerando gráfico PNG...")
    chart = plot_prices_png(
        timestamps_ms=ts,
        prices=prices,
        title=f"Bitcoin - últimos {days} dias",
        out_dir="artifacts",
    )
    print(chart)

    if chart.get("path"):
        print(f"\n✅ Gráfico gerado em: {chart['path']}")
        print("💡 Para ver no navegador, suba um servidor local:")
        print("   python -m http.server 9000")
        print(f"   http://127.0.0.1:9000/{chart['path'].replace('\\\\', '/')}")
    else:
        print("\n⚠️ Não foi possível gerar o gráfico:", chart.get("reason"))

    print("\n✅ Finalizado.")


if __name__ == "__main__":
    main()