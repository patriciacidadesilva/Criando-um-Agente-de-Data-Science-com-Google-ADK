"""
📌 PARA QUE SERVE ESTE CÓDIGO?

Este código busca dados históricos de criptomoedas (ex.: Bitcoin)
diretamente da API pública do CoinGecko e organiza esses dados
para serem usados em análises e gráficos.

Ele faz 3 coisas:

1) Busca dados reais na internet (CoinGecko)
   - Preço ao longo do tempo
   - Volume negociado
   - Valor de mercado (market cap)

2) Extrai somente os preços do retorno da API
   - Converte o retorno “cru” em uma lista simples de números

3) Extrai as datas (timestamps) desses preços
   - Para permitir gráficos e análises no tempo

⚠️ Importante:
- Este código NÃO dá recomendação financeira.
- Ele apenas coleta e organiza dados de forma objetiva.
"""

from __future__ import annotations

from typing import Any, Dict, List

import httpx


def fetch_crypto_prices(
    coin_id: str,
    vs_currency: str = "usd",
    days: int = 90,
    timeout_s: float = 30.0,
) -> Dict[str, Any]:
    """
    Busca dados históricos de uma criptomoeda no CoinGecko.

    Parâmetros (bem simples):
    - coin_id: nome da moeda no CoinGecko (ex.: "bitcoin", "ethereum")
    - vs_currency: moeda de comparação (ex.: "usd", "brl")
    - days: quantos dias de histórico buscar (ex.: 30, 90, 365)

    Retorno:
    - Um dicionário (JSON) com listas como:
      "prices", "market_caps", "total_volumes"
    """

    # Endereço da API do CoinGecko para histórico de preços
    url = f"https://api.coingecko.com/api/v3/coins/{coin_id}/market_chart"

    # Parâmetros enviados para a API (moeda de comparação e período)
    params = {"vs_currency": vs_currency, "days": int(days)}

    # Faz a chamada na API com limite de tempo para não travar o programa
    try:
        with httpx.Client(timeout=timeout_s) as client:
            r = client.get(url, params=params)
            r.raise_for_status()  # se vier erro (404, 500 etc), levanta exceção
            return r.json()
    except httpx.TimeoutException as e:
        # Erro comum: internet lenta ou API demorou para responder
        raise RuntimeError("A API do CoinGecko demorou demais para responder (timeout).") from e
    except httpx.HTTPStatusError as e:
        # Erro: a API respondeu, mas com status de erro (ex.: moeda não existe)
        raise RuntimeError(
            f"Erro ao buscar dados no CoinGecko: status {e.response.status_code}."
        ) from e
    except httpx.RequestError as e:
        # Erro: falha de rede (sem internet, DNS, bloqueio, etc.)
        raise RuntimeError("Falha de rede ao acessar o CoinGecko. Verifique sua conexão.") from e


def extract_prices(payload: Dict[str, Any]) -> List[float]:
    """
    Extrai somente os preços do payload retornado pela API.

    Formato típico do CoinGecko:
    payload["prices"] = [[timestamp_ms, price], [timestamp_ms, price], ...]

    Saída:
    - Lista de preços: [price, price, ...]
    """

    raw = payload.get("prices", [])

    out: List[float] = []
    for item in raw:
        # Cada item deve ser uma lista com 2 valores: [timestamp, price]
        if not (isinstance(item, list) and len(item) >= 2):
            continue

        try:
            out.append(float(item[1]))
        except (TypeError, ValueError):
            # Se o preço vier quebrado/inesperado, ignora e segue
            continue

    return out


def extract_timestamps(payload: Dict[str, Any]) -> List[int]:
    """
    Extrai somente os timestamps (datas em milissegundos) do payload.

    Formato típico do CoinGecko:
    payload["prices"] = [[timestamp_ms, price], ...]

    Saída:
    - Lista de timestamps: [timestamp_ms, timestamp_ms, ...]
    """

    raw = payload.get("prices", [])

    out: List[int] = []
    for item in raw:
        # Cada item deve ser uma lista com 2 valores: [timestamp, price]
        if not (isinstance(item, list) and len(item) >= 2):
            continue

        try:
            out.append(int(item[0]))
        except (TypeError, ValueError):
            # Se o timestamp vier quebrado/inesperado, ignora e segue
            continue

    return out
