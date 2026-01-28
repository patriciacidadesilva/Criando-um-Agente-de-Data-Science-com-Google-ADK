"""
📌 PARA QUE SERVE ESTE CÓDIGO?

Este código analisa uma sequência de preços ao longo do tempo
(ex.: Bitcoin, ações, qualquer série histórica) de forma simples e explicável.

Ele faz 4 coisas:

1) Resume como os preços variaram (retornos)
2) Encontra pontos “fora do padrão” (outliers)
3) Faz uma previsão simples (baseline)
4) Gera um gráfico em PNG para usar em relatório/sistema

⚠️ Importante:
- Não é recomendação de investimento.
- É análise objetiva de dados históricos.
"""

from __future__ import annotations

import os
import uuid
from datetime import datetime
from typing import Any, Dict, List, Optional

import numpy as np
import matplotlib

# Modo “sem tela” (útil para rodar em servidor, API, automação, agente)
matplotlib.use("Agg")
import matplotlib.pyplot as plt


def _to_float_array(values: List[float]) -> np.ndarray:
    """
    Converte lista para array numérico e remove valores inválidos (NaN/inf).
    """
    x = np.array(values, dtype=float)
    x = x[np.isfinite(x)]
    return x


def summarize_returns(prices: List[float]) -> Dict[str, Any]:
    """
    Calcula estatísticas simples sobre a variação (retorno) entre preços.
    Retorno aqui é: (preço_atual / preço_anterior) - 1
    """

    x = _to_float_array(prices)

    # Precisa de pelo menos 3 preços para ter um mínimo de informação útil
    if len(x) < 3:
        return {"n": 0, "reason": "Poucos dados para calcular retornos."}

    # Evita divisão por zero (se algum preço anterior for 0, ignora aquele ponto)
    prev = x[:-1]
    curr = x[1:]
    valid = prev != 0

    if valid.sum() < 2:
        return {"n": 0, "reason": "Dados insuficientes (muitos zeros) para calcular retornos."}

    rets = (curr[valid] / prev[valid]) - 1.0

    # Se ainda assim ficou curto, devolve “sem dados suficientes”
    if len(rets) < 2:
        return {"n": 0, "reason": "Retornos insuficientes para gerar estatísticas."}

    return {
        "n": int(rets.shape[0]),
        "mean_return": float(np.mean(rets)),
        "volatility": float(np.std(rets, ddof=1)),  # ddof=1 = variação “mais justa” para amostra
        "min_return": float(np.min(rets)),
        "max_return": float(np.max(rets)),
    }


def detect_outliers_iqr(series: List[float]) -> Dict[str, Any]:
    """
    Encontra valores fora do padrão usando IQR (um método simples e confiável).
    """

    x = _to_float_array(series)

    # Com poucos pontos, a detecção vira chute
    if len(x) < 10:
        return {"outliers_idx": [], "reason": "Poucos pontos para detectar outliers."}

    q1, q3 = np.percentile(x, [25, 75])
    iqr = q3 - q1

    # Se todos os valores forem praticamente iguais, não faz sentido procurar outlier
    if iqr == 0:
        return {
            "q1": float(q1),
            "q3": float(q3),
            "iqr": float(iqr),
            "lo": float(q1),
            "hi": float(q3),
            "outliers_idx": [],
            "outliers_count": 0,
            "reason": "Sem variação suficiente para detectar outliers.",
        }

    lo = q1 - 1.5 * iqr
    hi = q3 + 1.5 * iqr

    # Índices (posições) onde o valor está fora do intervalo normal
    idx = np.where((x < lo) | (x > hi))[0].tolist()

    return {
        "q1": float(q1),
        "q3": float(q3),
        "iqr": float(iqr),
        "lo": float(lo),
        "hi": float(hi),
        "outliers_idx": idx,
        "outliers_count": int(len(idx)),
    }


def forecast_naive_last(series: List[float], horizon: int = 7) -> Dict[str, Any]:
    """
    Previsão simples (baseline):
    repete o último valor conhecido por 'horizon' passos.
    """

    x = _to_float_array(series)

    if len(x) == 0:
        return {"forecast": [], "reason": "Série vazia ou inválida."}

    horizon = int(max(1, horizon))
    last = float(x[-1])

    return {
        "model": "naive_last_value",
        "horizon": horizon,
        "last_value": last,
        "forecast": [last] * horizon,
    }


def plot_prices_png(
    timestamps_ms: Optional[List[int]],
    prices: List[float],
    title: str = "Preço histórico",
    out_dir: str = "artifacts",
) -> Dict[str, Any]:
    """
    Gera um gráfico e salva em PNG.

    - Se timestamps_ms vier preenchido, o eixo X vira “datas”.
    - Se timestamps_ms vier vazio ou None, o eixo X vira “posição na lista”.
    """

    os.makedirs(out_dir, exist_ok=True)

    x_prices = _to_float_array(prices)
    if len(x_prices) < 2:
        return {"filename": None, "path": None, "reason": "Poucos dados para gerar gráfico."}

    # Garante que o gráfico não quebre se timestamps vier com tamanho diferente
    use_dates = bool(timestamps_ms) and len(timestamps_ms) == len(prices)

    if use_dates:
        x_axis = [datetime.fromtimestamp(t / 1000.0) for t in timestamps_ms]  # ms -> segundos
        x_label = "Data"
    else:
        x_axis = list(range(len(x_prices)))
        x_label = "Tempo (posição)"

    filename = f"price_chart_{uuid.uuid4().hex[:8]}.png"
    path = os.path.join(out_dir, filename)

    plt.figure(figsize=(10, 4))
    plt.plot(x_axis, x_prices)

    plt.title(title)
    plt.xlabel(x_label)
    plt.ylabel("Preço")
    plt.tight_layout()

    plt.savefig(path, dpi=150)
    plt.close()

    return {"filename": filename, "path": path}
