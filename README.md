### 🧠 Agente de Data Science com Google ADK

Este projeto demonstra a construção de um **Agente de Data Science orientado a ferramentas (*tool-first*)** utilizando o **Google ADK (Agent Development Kit)**.

O foco principal é mostrar como transformar um modelo de linguagem em um **agente analítico confiável**, com ênfase em:

- **dados reais** (sem simulações ou números inventados),
- **análises reproduzíveis** e determinísticas,
- **explicabilidade** dos resultados,
- **governança de execução** (controle, limites e auditabilidade).

📌 **Ideia central:**  
> não é um chatbot opinativo,  
> é um **agente de dados** que pensa, decide e responde **apoiado exclusivamente em ferramentas reais**.

---

### 0️⃣ Pré-requisitos

Antes de iniciar, garanta que o ambiente possui:

- **Windows** com **PowerShell**
- **Python 3.10 ou superior** (disponível no PATH)
- **Visual Studio Code**
- **Git**

> 💡 Dica rápida de verificação:
> ```powershell
> python --version
> git --version
> ```

---

### 1️⃣ Criar a pasta do projeto (raiz única)

Crie uma pasta dedicada para o projeto e abra-a no VS Code:

```powershell
mkdir agent-data-science-adk
cd agent-data-science-adk
code .
```

Por que uma raiz única?
* Evita conflitos de caminhos e dependências
* Centraliza código, ambiente virtual e configurações
* Facilita versionamento e reprodução do projeto

---

### 2️⃣ Criar e ativar a VENV (ambiente virtual)

No terminal integrado do VS Code
(View → Terminal), crie o ambiente virtual:
```powershell
py -m venv .venv
```

Ative o ambiente virtual:
```powershell
.\.venv\Scripts\Activate.ps1
```

---

### 3️⃣ Atualizar e instalar dependências (habilitando capacidades)

Com o ambiente virtual **ativo**, atualize o gerenciador de pacotes e instale as dependências do projeto:

```powershell
pip install -U pip
pip install google-adk httpx pandas numpy matplotlib
```

#### 📦 3.1 Por que atualizar o pip primeiro?
**pip install -U pip**
- Atualiza o gerenciador de pacotes
- Corrige problemas conhecidos de:
* SSL
* build de dependências
* resolução de versões
- Evita falhas silenciosas durante a instalação das bibliotecas
- 👉 Sem esse passo, o setup pode quebrar logo no início.


#### 🧠 3.2 Dependências do projeto (papel de cada uma)
**google-adk — o cérebro do agente**
Framework oficial do Google Agent Development Kit.
Responsável por:
* criação de agentes de IA
* registro e execução de tools
* gerenciamento de fluxo de decisão
* controle de execução e memória
- Sem o ADK, você teria apenas scripts Python isolados — não um agente.


**httpx — canal de comunicação com o mundo externo**
Cliente HTTP moderno (sync + async), usado para:
* chamadas de APIs externas
* busca de dados reais
* integração com serviços externos
* Mais robusto que requests.
- Sem isso, o agente fica cego ao mundo externo.


**pandas — camada de negócio dos dados**
Biblioteca central para manipulação de dados tabulares.
Usada para:
* leitura de CSV / JSON
* limpeza de dados
* agregações
* análises exploratórias
- Sem pandas, você ficaria preso (a) a listas e dicionários (ineficiente e pouco escalável).


**numpy — motor matemático**
Base de computação numérica do projeto.
Responsável por:
* operações vetoriais rápidas
* cálculos estatísticos
* suporte interno ao pandas
- Sem numpy, a performance cai ou o código simplesmente quebra.


**matplotlib — visualização e explicabilidade**
Biblioteca de visualização gráfica.
Usada para:
* geração de gráficos
* validação visual de hipóteses
* explicabilidade dos resultados
* storytelling de dados
- Sem visualização, análise vira número sem contexto.

✅ Após este passo, o projeto deixa de ser apenas setup e passa a ser um sistema ativo com capacidades reais.

---

### 4️⃣ Criar a estrutura do projeto

Crie as pastas e arquivos base do projeto:

```powershell
mkdir tools
mkdir agent

New-Item tools\__init__.py -ItemType File
New-Item tools\pipeline.py -ItemType File
New-Item tools\market_data.py -ItemType File
New-Item tools\analysis.py -ItemType File

New-Item agent\agent.py -ItemType File

New-Item test_tools.py -ItemType File
New-Item .env -ItemType File
New-Item .gitignore -ItemType File
```

#### 🧱 4.1 Estrutura e responsabilidades

📁 **tools/ — domínio de capacidades do agente**
Camada responsável por o que o agente sabe fazer.
Funções típicas:
* acesso a dados
* cálculos
* validações
* lógica de negócio
- Mental model: capabilities do agente


📁 **agent/ — domínio do agente**
Camada onde o agente é definido.
Responsabilidades:
* instanciar o agente ADK
* registrar tools
* definir comportamento e regras
* servir como ponto de entrada do sistema
- Mental model: control plane


📄 **tools/__init__.py**
Transforma a pasta tools em um módulo Python.
* Permite imports como: from tools.market_data import fetch_crypto_prices
Sem esse arquivo, o Python não reconhece tools como módulo.


📄 **tools/market_data.py**
Camada de aquisição de dados.
Responsabilidade única:
* buscar dados externos
* chamar APIs
* ler arquivos
* Dados entram aqui.
- Nenhuma regra de negócio vive nesta camada.


📄 **tools/analysis.py**
Camada de inteligência e análise.
Responsabilidade única:
* limpeza de dados
* cálculos
* regras estatísticas
* geração de insights
- Aqui os dados viram informação.


📄 **tools/pipeline.py**
Camada de orquestração determinística.
Responsabilidade:
* conectar ingestão + análise + visualização
* gerar um relatório completo e reproduzível
- É o “mini-sistema” que o agente é obrigado a usar.


📄 **agent/agent.py**
Entry point do agente.
Responsabilidades:
* criar o LLM Agent
* definir instruções e regras
* registrar tools permitidas
- Se você rodar algo, é daqui que tudo começa.


📄 **test_tools.py**
Camada de validação isolada.
Responsabilidades:
* testar ingestão e análise sem o agente
* validar dados e cálculos
* garantir confiança antes da integração
- Mental model: rede de segurança


📄 **.env**
Arquivo de configuração sensível.
Usado para:
* API keys
* tokens
* URLs
* segredos
🚫 Nunca versionar este arquivo.


📄 **.gitignore**
Governança do repositório.
Ignora:
* .venv
* .env
* arquivos temporários
* lixo de execução
Evita vazamento de segredos e poluição do Git.



#### 🧠 4.2 Visão sistêmica (por que este design funciona)
Este setup impõe separação clara de responsabilidades:
**tools** → o que o agente sabe fazer
**agent** → como o agente pensa e decide
**tests** → confiança e validação
**env** → segurança

Resultado:
* menos acoplamento
* mais previsibilidade
* agentes explicáveis
* código sustentável e extensível

---

### 5️⃣ Criar API Key do Google (Gemini)

O agente utiliza **modelos Gemini** via **Google ADK**, portanto é necessário criar e configurar uma **API Key** válida no Google Cloud.

---

#### 5.1 Criar um projeto no Google Cloud

Acesse o console do Google Cloud:

👉 https://console.cloud.google.com

Passos:
1. Clique em **Selecionar Projeto**
2. Selecione **Novo Projeto**
3. Defina o nome do projeto:
4. Clique em **Criar**

📌 Este projeto será o **container de governança** para uso da API Gemini.

---

#### 5.2 Criar a API Key no Google AI Studio

Acesse o Google AI Studio:

👉 https://aistudio.google.com/api-keys

Passos:
1. Clique em **Criar chave de API**
2. Selecione o projeto **data-science**
3. Gere a chave
4. **Copie a API Key** gerada

> ⚠️ Trate essa chave como um segredo.  
> Ela concede acesso direto aos modelos Gemini.

---

#### 5.3 Salvar a API Key no arquivo `.env`

Na raiz do projeto, edite o arquivo `.env` e adicione:

```env
GOOGLE_API_KEY=SUA_CHAVE_AQUI
```

#### 🔐 Boas práticas de segurança
- 🚫 Nunca versione o arquivo .env
- ✅ O .env deve estar listado no .gitignore
- 🔁 Em ambientes produtivos, prefira:

* variáveis de ambiente
* secret managers
* CI/CD secrets

---

### 6️⃣ Tools — Camada de Dados (`tools/market_data.py`)

Esta seção implementa a **camada de aquisição de dados** do agente.  
Aqui vivem exclusivamente funções responsáveis por **buscar dados reais do mundo externo** e organizá-los em estruturas simples e previsíveis para análise posterior.

📌 **Regra de arquitetura:**  
> Nenhuma regra de negócio, cálculo ou decisão vive aqui.  
> Esta camada apenas **coleta e estrutura dados**.

---

#### 📄 Arquivo: `tools/market_data.py`

```python
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
```

---

🧩 **6.1 O que o código faz em alto nível**

Este script implementa uma **pipeline mínima de dados de mercado cripto**, seguindo o fluxo clássico:

buscar → transformar → estruturar

Em termos práticos, ele:
- Consulta a **API pública do CoinGecko**
- Baixa **preços históricos** de uma criptomoeda (ex.: Bitcoin)
- Processa o JSON bruto retornado pela API
- Converte os dados em **estruturas simples e previsíveis**
- Entrega dados **prontos para análise estatística e visualização**

📌 Não há inferência, previsão ou decisão aqui.  
Nada mágico. É **ETL limpo, explícito e controlado**.

---

🧠 **6.2 Resumo mental (para fixar)**
- `fetch_crypto_prices` → extrai dados reais do mundo externo  
- `extract_prices` → transforma o payload bruto em série numérica  
- `extract_timestamps` → organiza o eixo temporal  
- `httpx` → camada de comunicação com APIs externas  
- Tipagem explícita → código previsível, sustentável e seguro  

📌 **Mental model correto desta camada:**  
> “Aqui os dados entram no sistema.”  

A responsabilidade de **analisar, interpretar ou decidir** pertence às próximas camadas (`analysis` e `pipeline`).

---

### 7️⃣ Tools — Análises + Forecast (`tools/analysis.py`)

Este arquivo contém a **camada de análise** do agente: funções pequenas, testáveis e explicáveis para sumarizar séries temporais financeiras, detectar outliers, gerar um baseline de forecast e produzir um gráfico PNG pronto para uso em relatórios.

> **Princípio arquitetural:** aqui só há lógica analítica e visualização — **nenhuma** chamada externa. Input: listas numéricas limpas; output: dicionários simples e artefatos (PNG).

---

#### 📄 Conteúdo resumido do arquivo

- `_to_float_array(values: List[float]) -> np.ndarray`  
  Converte lista em `np.ndarray` float e remove `NaN`/`inf`.

- `summarize_returns(prices: List[float]) -> Dict[str, Any]`  
  Calcula retornos simples entre preços consecutivos e devolve estatísticas: `n`, `mean_return`, `volatility`, `min_return`, `max_return`. Retorna mensagens claras quando não há dados suficientes.

- `detect_outliers_iqr(series: List[float]) -> Dict[str, Any]`  
  Detecta outliers usando IQR: retorna `q1`, `q3`, `iqr`, `lo`, `hi`, `outliers_idx`, `outliers_count`. Protege contra séries muito pequenas ou sem variação.

- `forecast_naive_last(series: List[float], horizon: int = 7) -> Dict[str, Any]`  
  Baseline que repete o último valor observado por `horizon` passos. Retorna `model`, `horizon`, `last_value`, `forecast`.

- `plot_prices_png(timestamps_ms: Optional[List[int]], prices: List[float], title: str = "Preço histórico", out_dir: str = "artifacts") -> Dict[str, Any]`  
  Gera e salva um PNG na pasta `artifacts/` (cria se necessário). Aceita timestamps em ms ou `None`. Retorna `{"filename", "path"}` ou um dicionário com `reason` em caso de erro.

---

#### 📄 Arquivo: `analysis.py`

```python
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
``` 

---

🧩 **6.2 O que o código faz em alto nível**

Este código implementa uma **camada de análise explicável** sobre séries temporais de preços.

Em termos práticos, ele:

- Calcula **retornos financeiros** a partir de uma sequência de preços, extraindo métricas-chave como:
  - média dos retornos
  - volatilidade
  - menor e maior retorno observado

- Identifica **outliers** em séries numéricas utilizando o método estatístico
  do **IQR (Intervalo Interquartil)**, de forma:
  - robusta
  - determinística
  - facilmente explicável

- Gera uma **previsão simples (baseline)**, assumindo que o último valor
  observado se repete no curto prazo, servindo como ponto de comparação
  para modelos mais sofisticados.

- **Visualiza o histórico de preços** por meio de gráficos em imagem (PNG),
  permitindo:
  - inspeção visual
  - validação de hipóteses
  - auditoria dos dados

Nada mágico.

É **análise exploratória + estatística básica + visualização**, pronta para:
- apoiar decisões baseadas em dados
- alimentar um agente inteligente orientado a ferramentas
- servir como baseline confiável para evoluções futuras

---

### 8️⃣ Tools — Orquestração do Pipeline (`tools/pipeline.py`)

Este arquivo implementa a **camada de orquestração** do projeto.  
Ele conecta **dados reais → análise → visualização** em um fluxo único, determinístico e reutilizável.

📌 **Princípio arquitetural:**  
> O pipeline **não decide** e **não inventa dados**.  
> Ele apenas coordena ferramentas especializadas e devolve um relatório estruturado.

---

#### 📌 Para que serve este código?

Este arquivo gera um **mini-relatório automático do Bitcoin**.

Em termos simples, ele:

- Busca preços reais do Bitcoin na internet (CoinGecko)
- Organiza os dados em listas simples (preço e data)
- Calcula estatísticas básicas (ganhos e perdas)
- Identifica valores fora do padrão (outliers)
- Faz uma previsão simples (baseline)
- Cria um gráfico em PNG para visualização

⚠️ **Importante:**
- **NÃO** é recomendação financeira
- A previsão é propositalmente simples e serve apenas como **baseline de comparação**

---

#### 📄 Arquivo: `pipeline.py`

```python
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
```
---


### 9️⃣ Teste isolado do pipeline (ANTES do ADK)

Este script executa um **teste isolado** do pipeline, sem ADK, validando:

- ingestão de dados (CoinGecko)
- transformação (listas de preços + timestamps)
- estatísticas de retorno
- detecção de outliers (IQR)
- forecast baseline (naive last)
- geração de gráfico em PNG (`artifacts/`)

> 📌 Este teste garante que as tools funcionam antes de conectar o agente (boa prática de governança).

#### 📄 Arquivo: `test_tool.py`

```python
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
```

---

▶️ **9.1 Executar o teste**

Na raiz do projeto, com a VENV ativa:

```powershell
python test_tools.py
```

✅ Se o gráfico abrir corretamente:Data Scientist (agent) mode: ON 🚀

---

### 🔟 Criar o Agente ADK (`agent/agent.py`)

Esta etapa cria o **agente de IA propriamente dito**, utilizando o **Google ADK (Agent Development Kit)**.  
Aqui, um modelo de linguagem deixa de ser apenas um chatbot e passa a operar como um **agente analítico orientado a ferramentas**.

📌 **Princípio central:**  
> O agente **não calcula**, **não inventa** e **não opina**.  
> Ele **orquestra ferramentas reais** e **explica os resultados**.

---

#### 📌 Para que serve este código?

Este arquivo cria um **“analista virtual”** que gera automaticamente um **relatório completo sobre o Bitcoin**.

Sempre que o agente é executado, ele:

- Busca **dados reais** do preço do Bitcoin
- Calcula estatísticas simples:
  - média
  - variação
  - menor e maior valor
- Identifica valores fora do padrão (outliers)
- Gera uma previsão básica de preço (baseline)
- Cria um gráfico em imagem (PNG)

⚠️ **Importante:**
- O resultado é **apenas informativo**
- **Não existe recomendação** de compra ou venda
- O agente é **obrigado** a usar dados reais via tools

---

#### 🧠 Objetivo arquitetural

Demonstrar o uso de **Inteligência Artificial de forma controlada, explicável e baseada em dados**, evitando:

- alucinação
- cálculos inventados
- respostas opinativas
- inferências sem base factual

---

#### 📄 Arquivo: `agent.py`

```python
"""
📌 PARA QUE SERVE ESTE CÓDIGO?

Este arquivo cria um "analista virtual" que gera automaticamente
um relatório completo sobre o Bitcoin.

Sempre que o agente é executado, ele:
- Busca dados reais do preço do Bitcoin
- Calcula estatísticas simples (média, variação, menor e maior valor)
- Identifica valores fora do padrão
- Faz uma previsão básica de preço
- Gera um gráfico em imagem (PNG)

Importante:
- O resultado é apenas informativo
- Não existe recomendação de compra ou venda
- O agente é obrigado a usar dados reais para responder

Objetivo:
Demonstrar o uso de Inteligência Artificial de forma controlada,
explicável e baseada em dados.
"""

from __future__ import annotations
# Permite que o Python entenda melhor os tipos de dados,
# evitando erros em versões diferentes da linguagem.

from google.adk.agents import LlmAgent
# Importa a classe que cria um "agente de IA".
# Pense no agente como um funcionário virtual com uma função bem definida.

from tools.pipeline import bitcoin_report
# Importa a função que faz TODA a análise do Bitcoin:
# busca os dados, calcula números, gera previsões e cria o gráfico.

# Criação do agente principal do projeto
root_agent = LlmAgent(
    name="DataScientistAgent",
    # Nome do agente.
    # Serve apenas para identificação (logs, interface, organização).

    model="gemini-2.0-flash",
    # Modelo de inteligência artificial usado.
    # Ele é rápido e adequado para análises simples e objetivas.

    instruction=(
        "Você é um cientista de dados.\n"
        # Diz para a IA qual papel ela deve assumir.

        "Regra: SEMPRE use a ferramenta bitcoin_report para gerar o relatório completo.\n"
        # Regra importante: a IA NÃO pode responder sozinha.
        # Ela é obrigada a usar a função que faz a análise real dos dados.

        "Você deve entregar sempre:\n"
        "- estatísticas de retorno (média, variação, menor e maior valor)\n"
        "- identificação de valores fora do padrão\n"
        "- uma previsão simples baseada no último valor\n"
        "- um gráfico em imagem (PNG)\n"
        # Define exatamente o que deve aparecer no resultado final.

        "Sem recomendação de investimento."
        # Deixa claro que o resultado é apenas informativo,
        # não é uma sugestão para comprar ou vender.
    ),

    tools=[bitcoin_report],
    # Lista de ferramentas que o agente pode usar.
    # Aqui ele só pode usar uma, garantindo controle e previsibilidade.
)
```

---

🧩 **10.1 — O que esse código faz em alto nível**

Este arquivo (`agent/agent.py`) transforma um modelo de linguagem em um **agente analítico controlado**. Em alto nível ele:

- Cria um **agente de IA (LLM Agent)** usando o **Google ADK**.  
- Define o **papel** do agente: *cientista de dados* — comportamento e saída esperada ficam explícitos nas instruções.  
- Conecta o agente a **tools reais** (pipeline determinístico de ingestão + análise + visualização).  
- Permite que o modelo **execute tarefas concretas** por meio das ferramentas:
  - buscar dados de mercado (CoinGecko),
  - calcular retornos e risco,
  - detectar outliers,
  - gerar previsões simples (baseline),
  - criar gráficos PNG.
- Impõe boas práticas operacionais:
  - uso obrigatório de tools (tool-first),
  - explicitação de limitações (sem recomendação financeira),
  - saída verificável e auditável.

**Tradução executiva:** transforma um LLM em **agente analítico orientado a ferramentas**, não em um chatbot opinativo.

---

🧠 **10.2 — Leitura arquitetural (parte mais importante)**

**Princípio central:** o código do agente **não faz análise** — ele *orquestra*. As ferramentas fazem o trabalho real; o LLM só decide *quando* e *como* chamá-las e *explica* o resultado.

Componentes e responsabilidades:

- **Agent (LLM)**  
  - Responsabilidade: *decisão* (quando invocar qual tool; como estruturar a explicação).  
  - Não realiza cálculos críticos nem inventa números.  
  - Deve ser tratável como camada de controle (observável e testável).

- **Tools / Pipeline**  
  - Responsabilidade: *execução determinística* (ingestão, transformação, análise, visualização).  
  - Fornecem resultados factuais e artefatos (ex.: JSON, PNG).

- **Contrato entre camadas**  
  - Inputs e outputs claros (listas/JSON-friendly).  
  - Tools retornam estruturas previsíveis para evitar parsing frágil no LLM.  
  - Agente valida presença/qualidade dos dados antes de interpretar.

Benefícios deste design:

- **Redução de alucinações:** LLM só relata resultados de tools verificáveis.  
- **Evita cálculos inventados:** números vem da pipeline, não da geração de texto.  
- **Auditabilidade:** histórico de chamadas às tools e artefatos persistidos (PNG, JSON) permitem revisão.  
- **Governança e segurança:** instruções rígidas e lista restrita de tools controlam o comportamento do agente.

Regras práticas (exemplo de **guardrails** a manter no código/instrução):

- Obrigar uso de `bitcoin_report` para responder consultas sobre preços/estatísticas.  
- Retornar erro ou mensagem clara quando dados insuficientes forem detectados.  
- Proibir qualquer forma de recomendação financeira nas respostas.  
- Logar chamadas de tool e seus resultados para auditoria.

**Resumo final:** o agente é uma camada de orquestração e explicação. A ciência de dados acontece nas tools; o LLM é o orquestrador humano-legível — um tradutor entre execução determinística e resposta explicável.

---

## 1️⃣1️⃣ Subir um servidor local (para visualização dos artefatos) - Foto PNG do Gráfico

Algumas etapas do projeto geram **artefatos locais**, como gráficos em PNG.  
Para visualizá-los diretamente no navegador, é necessário subir um **servidor HTTP local** na raiz do projeto.

---

#### ▶️ 11.1 Como executar

No terminal, a partir da raiz do projeto `agent-data-science-adk`:

```powershell
cd "C:\Users\patricia\OneDrive\Area_de_Trabalho\Projetos\agent-data-science-adk"
python -m http.server 9000
```
**Observação aqui:** se você já estiver na pasta correta só precisa dar o comando
```powershell
python -m http.server 9000
```
---

#### 🌐 11.2 O que esse comando faz:
* Inicia um servidor HTTP simples usando o Python
* Expõe a pasta raiz do projeto via navegador
* Permite acessar arquivos estáticos (ex.: gráficos PNG)

Por padrão, o servidor ficará disponível em:
```ccp
http://127.0.0.1:9000
```

---

#### 🖼️ 11.3 Visualização dos gráficos

Os gráficos gerados pelo pipeline são salvos na pasta:
artifacts/

Com o servidor ativo, eles podem ser acessados em URLs como:
```arduino
http://127.0.0.1:9000/artifacts/price_chart_xxxxxxxx.png
```

---

#### 🧠 11.4 Por que isso é necessário?
* O agente gera arquivos locais, não imagens embutidas
* O servidor permite inspeção visual dos resultados
* Facilita debug, validação e demonstração do projeto
📌 Mental model correto:
Python gera o artefato → servidor expõe → navegador exibe

---

#### ⚠️ 11.5 Observações importantes
* O servidor é local (não exposto à internet)
* Ideal apenas para desenvolvimento e testes
Para produção, usar:
* storage dedicado (S3, GCS, etc.)
* APIs de entrega de arquivos
* dashboards ou frontends próprios

---

###  1️⃣2️⃣ Subir o ADK Web (Interface de Execução do Agente)

Nesta etapa, você inicia a **interface Web do Google ADK**, que permite **executar, testar, inspecionar e depurar agentes** diretamente pelo navegador.

Com isso, o projeto deixa de ser apenas código e passa a ser um **sistema interativo de agentes**.

---

#### ▶️ 12.1 Comando para subir o ADK Web

Com a **VENV ativa**, execute:

```powershell
.\.venv\Scripts\adk.exe web
```

---

#### 🧠 12.2 Tradução executiva
Este comando:
* inicia o servidor Web do Google ADK
* carrega os agentes definidos no projeto
* disponibiliza uma UI interativa para execução e observabilidade
👉 É o ambiente de playground profissional do ADK.

---

#### 🧠 12.3 Quebrando o comando em partes
```text
.\.venv\Scripts\```
Garante que você está usando o ADK instalado no ambiente virtual, mantendo:
* governança total
* isolamento de dependências
* nada instalado globalmente

```text
adk.exe
``` 
É o CLI do Google ADK (Agent Development Kit).
Instrui o ADK a: “Subir a interface Web e o runtime para execução e inspeção dos agentes.”

---

#### 🔎 12.4 O que acontece quando você executa
Ao rodar o comando:
* Um servidor local é iniciado
(geralmente em http://127.0.0.1:8000 ou similar)
* O ADK automaticamente:
- carrega agent.py
- registra todas as tools disponíveis
- valida a configuração do agente
- disponibiliza uma UI Web interativa

---

#### 🎮 12.5 O que você consegue fazer na interface Web
* Conversar com o agente
* Forçar chamadas de tools
* Ver quando e como as tools são executadas
* Inspecionar inputs e outputs
* Debugar comportamento do agente
* Validar instruções, regras e limites

📌 É um sandbox profissional, não um simples chat.

---

#### 🎯 12.6 Para que isso serve (na prática)
Este comando é usado para:
* Testar agentes sem escrever código adicional
* Validar se:
- o modelo está correto
- as tools estão registradas
- o agente chama funções reais
* Demonstrar o agente para outras pessoas
* Iterar rapidamente:
- prompts
- regras
- ferramentas
- arquitetura
Sem essa etapa, você teria apenas código estático.

---

#### 🧠 12.7 Mental model correto 
```text
agent.py      → definição do agente
adk.exe web   → runtime + interface
navegador     → observabilidade do agente
```
📌 Este comando é o que transforma: “código de agente” em sistema vivo, interativo e testável. A partir daqui, você não está mais configurando ambiente — você está operando um agente 🚀

---

### 1️⃣3️⃣ Abrir a UI Web do ADK

Após subir o ADK Web (`.\.venv\Scripts\adk.exe web`), abra no navegador o endereço exibido pelo CLI — normalmente:

http://127.0.0.1:8000

<img width="1917" height="1005" alt="image" src="https://github.com/user-attachments/assets/629e9b74-dbf6-41ae-89a7-71931408c67a" />

> Dica: clique no link exibido no terminal para **rodar/executar** 

**Observação:** Se você quiser **parar** o servidor ADK, volte ao terminal onde rodou o comando e pressione novamente `Ctrl+C`.

No painel da UI:

**1.** Clique em **agent**
<img width="1917" height="1032" alt="image" src="https://github.com/user-attachments/assets/ea40fecc-66bd-4e38-87cc-e007225a15e1" />

**2.** Selecione o DataScientistAgent - **agent**
<img width="1911" height="1026" alt="image" src="https://github.com/user-attachments/assets/421bcc49-767d-4ef1-8fff-e5a51a794ba8" />

---

#### 13.1 Prompt de teste (forçando as tools)

Use este prompt abaixo direto na interface do ADK (ou no campo de interação do agente) para forçar o uso da tool `bitcoin_report`:
* Busque 7 dias de Bitcoin, gere estatísticas de retorno, outliers IQR, previsão de 3 dias e mostre o gráfico.
* Com base nos últimos 7 dias, o Bitcoin mostrou mais estabilidade ou volatilidade?
* Explique o que significa não ter outliers detectados no período analisado.
* Gere o relatório do Bitcoin com 7 dias e depois com 3 dias e compare a volatilidade.


🤖🔍 **Busque 7 dias de Bitcoin, gere estatísticas de retorno, outliers IQR, previsão de 3 dias e mostre o gráfico.**
<img width="1600" height="900" alt="image" src="https://github.com/user-attachments/assets/43411cfc-d9ce-436b-ac99-ff5d6648a92e" />

<img width="2000" height="1073" alt="image" src="https://github.com/user-attachments/assets/3fd07bfb-a280-44f9-bca5-ab61a512b3b9" />

<img width="2000" height="1061" alt="image" src="https://github.com/user-attachments/assets/bc8a9e43-0000-47cc-aa08-a47d554c1f7b" />


🤖🔍**Com base nos últimos 7 dias, o Bitcoin mostrou mais estabilidade ou volatilidade?**
<img width="2000" height="1049" alt="image" src="https://github.com/user-attachments/assets/9da62d66-0631-4d5f-bf3b-a47f0b35f715" />


🤖🔍**Explique o que significa não ter outliers detectados no período analisado.**
<img width="2000" height="1057" alt="image" src="https://github.com/user-attachments/assets/440039c7-bf4c-439b-ade6-5016a289ba41" />

🤖🔍**Gere o relatório do Bitcoin com 7 dias e depois com 3 dias e compare a volatilidade.**
<img width="2000" height="1035" alt="image" src="https://github.com/user-attachments/assets/d0278cc2-c5bb-415e-ba80-9f9db7b7f904" />

🤖🔍**Explique como o retorno e a volatilidade foram calculados nesse relatório**
<img width="2000" height="1051" alt="image" src="https://github.com/user-attachments/assets/d7c5378e-61be-4975-9ba1-acb01fa10243" />

---

#### 13.2 O que esperar (resultado mínimo)
- Um relatório JSON-like contendo:
  - `coin: "bitcoin"`
  - `days: 15`
  - `n_prices` (quantidade de preços baixados)
  - `stats` (mean_return, volatility, min_return, max_return)
  - `outliers` (indices e contagem)
  - `forecast` (modelo `naive_last_value` com 7 valores)
  - `chart_filename` e `chart_path`
  - `chart_url` (se você tiver um servidor local `python -m http.server` rodando)
- Um arquivo PNG gerado em `artifacts/` (ex.: `artifacts/price_chart_xxxxxxxx.png`)
- Logs / timeline na UI do ADK mostrando a chamada à tool `bitcoin_report` e seus outputs

---

#### 13.3 Problemas comuns & soluções rápidas

- **Nada acontece / timeout**  
  - Verifique conexão de internet e disponibilidade da API do CoinGecko.  
  - Cheque o terminal do ADK para erros (stack trace).  

- **`n_prices` é muito pequeno (<3)**  
  - A API pode ter retornado poucos pontos para o `days` solicitado. Tente `days=30`.

- **PNG não aparece ao clicar no link (`chart_url`)**  
  - Rode um servidor local na raiz do projeto:
    ```powershell
    python -m http.server 9000
    ```
  - Abra `http://127.0.0.1:9000/artifacts/<chart_filename>`

- **Erro ao iniciar `adk.exe web`**  
  - Confirme que o ADK foi instalado dentro do `.venv`.  
  - Verifique se a VENV está ativa e se `.\.venv\Scripts\adk.exe` existe.

---

#### 13.4 Boas práticas ao demonstrar

- Antes de compartilhar resultados, valide o conteúdo do PNG em `artifacts/`.  
- Capture a timeline das chamadas no ADK UI para auditability.  
- Se for apresentar para outras pessoas, prefira gerar o PNG e servir por `http.server` para links diretos nos slides/demonstração.

---

###🧾 1️⃣4️⃣  Seção final 

✅ **O que este projeto faz**
* Demonstra um agente de Data Science tool-first usando Google ADK
* Usa dados reais (CoinGecko) para análises reproduzíveis
* Implementa um pipeline modular:
- ingestão (market_data.py)
- análise/forecast/plot (analysis.py)
- orquestração (pipeline.py)
* Força boas práticas de governança:
- ferramentas determinísticas
- outputs auditáveis
- sem recomendações financeiras

---

### 🚫 1️⃣5️⃣   O que este projeto NÃO faz

* ❌ Não é um sistema de investimento/trading
* ❌ Não faz recomendação de compra/venda
* ❌ Não prevê o mercado de forma “inteligente” (forecast é baseline)
* ❌ Não substitui modelos quantitativos avançados
* ❌ Não é um produto pronto para produção (é um projeto de demonstração arquitetural)

---

### ⚠️ 1️⃣6️⃣  Limitações conhecidas
* A API pública do CoinGecko pode sofrer:
- instabilidade
- rate limit
- atrasos (timeout)
* O forecast é propositalmente simples (naive last value)
* Gráficos são salvos localmente e podem acumular arquivos em ./artifacts

---

### 🛣️ 1️⃣7️⃣   Próximos passos (ideias de evolução)

Se quiser evoluir este projeto, boas extensões são:
* Adicionar cache local (ex.: requests-cache / arquivo local) para reduzir chamadas na API
* Suportar múltiplas moedas (ex.: Ethereum, Solana) e múltiplas moedas de comparação (USD/BRL)
* Implementar novos baselines:
- média móvel
- suavização exponencial
* Adicionar logging estruturado e métricas (monitoramento)
* Exportar relatório para:
- JSON persistido
- Markdown
- PDF
* Integrar com armazenamento externo para artefatos (GCS/S3) em ambientes produtivos

---

### 📜 1️⃣8️⃣ Aviso legal

Este projeto tem finalidade educacional e demonstrativa.
* Não constitui recomendação de investimento
* Não oferece aconselhamento financeiro
