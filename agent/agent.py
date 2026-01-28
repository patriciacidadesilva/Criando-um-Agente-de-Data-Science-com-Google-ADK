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
