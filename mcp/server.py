from mcp.server.mcpserver import MCPServer
from mcp.server.mcpserver.exceptions import ToolError

# "Banco de dados" mockado, mesmo domínio do exemplo apply_discount da aula de anatomia
PEDIDOS = {
    "1001": {"status": "enviado", "item": "teclado mecânico", "valor": 349.90},
    "1002": {"status": "processando", "item": "monitor 27 polegadas", "valor": 1899.00},
}

# Tabela de descontos e cupons vigentes (documento read-only do resource)
CUPONS = {
    "FRETEGRATIS": {"tipo": "frete", "regra": "frete grátis em pedidos acima de R$ 100"},
    "10OFF": {"tipo": "percentual", "desconto": 0.10, "maximo": 100.00},
    "BEMVINDO": {"tipo": "fixo", "desconto": 20.00, "minimo": 50.00},
}

server = MCPServer(name="loja-demo", version="1.0.0")


@server.tool()
def aplicar_desconto(id_pedido: str, cupom: str) -> str:
    """Aplica um cupom de desconto a um pedido e devolve o novo valor a pagar."""
    pedido = PEDIDOS.get(id_pedido)
    if pedido is None:
        validos = ", ".join(PEDIDOS.keys())
        raise ToolError(f"Pedido {id_pedido} não encontrado. Pedidos válidos: {validos}.")

    regra = CUPONS.get(cupom)
    if regra is None:
        validos = ", ".join(CUPONS.keys())
        raise ToolError(f"Cupom {cupom} inválido. Cupons disponíveis: {validos}.")

    valor = pedido["valor"]
    if regra["tipo"] == "percentual":
        desconto = min(valor * regra["desconto"], regra["maximo"])
    elif regra["tipo"] == "fixo":
        desconto = regra["desconto"] if valor >= regra["minimo"] else 0.0
    else:
        desconto = 0.0

    novo_valor = valor - desconto
    return (
        f"Cupom {cupom} aplicado no pedido {id_pedido} ({pedido['item']}). "
        f"Valor original R$ {valor:.2f} -> novo valor R$ {novo_valor:.2f} "
        f"(desconto de R$ {desconto:.2f})."
    )


@server.resource(
    "loja://regras/cupons",
    title="Regras de descontos e cupons",
    description="Documento de somente leitura com a tabela de cupons e regras de desconto da loja.",
    mime_type="application/json",
)
def regras_cupons() -> str:
    import json

    return json.dumps(CUPONS, ensure_ascii=False, indent=2)


@server.prompt(
    title="Resumir pedido para o cliente",
    description="Gera um template de mensagem resumindo um pedido para o cliente.",
)
def resumir_pedido(id_pedido: str) -> str:
    return f"Resuma o pedido {id_pedido} de forma simpática para o cliente, em uma frase."


if __name__ == "__main__":
    server.run(transport="stdio")
