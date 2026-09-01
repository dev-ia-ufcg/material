import asyncio
import json
import sys

from mcp import ClientSession
from mcp.client.stdio import StdioServerParameters, stdio_client


def log(direcao, session_message):
    print(f"\n--- {direcao} ---")
    if isinstance(session_message, Exception):
        print(f"(exceção na leitura: {session_message})")
        return
    bruto = session_message.message.model_dump_json(by_alias=True, exclude_unset=True)
    print(json.dumps(json.loads(bruto), indent=2, ensure_ascii=False))


class LoggingReadStream:
    def __init__(self, inner):
        self._inner = inner

    async def receive(self):
        item = await self._inner.receive()
        log("SERVER -> CLIENT", item)
        return item

    async def aclose(self):
        await self._inner.aclose()

    def __aiter__(self):
        return self

    async def __anext__(self):
        return await self.receive()

    async def __aenter__(self):
        await self._inner.__aenter__()
        return self

    async def __aexit__(self, *args):
        return await self._inner.__aexit__(*args)


class LoggingWriteStream:
    def __init__(self, inner):
        self._inner = inner

    async def send(self, item):
        log("CLIENT -> SERVER", item)
        await self._inner.send(item)

    async def aclose(self):
        await self._inner.aclose()

    async def __aenter__(self):
        await self._inner.__aenter__()
        return self

    async def __aexit__(self, *args):
        return await self._inner.__aexit__(*args)


async def main():
    params = StdioServerParameters(command=sys.executable, args=["server.py"])

    async with stdio_client(params) as (read_stream, write_stream):
        read_log = LoggingReadStream(read_stream)
        write_log = LoggingWriteStream(write_stream)

        async with ClientSession(read_log, write_log) as session:
            print("\n========== HANDSHAKE (initialize) ==========")
            await session.initialize()

            print("\n========== TOOLS/LIST ==========")
            await session.list_tools()

            print("\n========== TOOLS/CALL (sucesso, cupom 10OFF) ==========")
            await session.call_tool("aplicar_desconto", {"id_pedido": "1001", "cupom": "10OFF"})

            print("\n========== TOOLS/CALL (erro, cupom inválido) ==========")
            await session.call_tool("aplicar_desconto", {"id_pedido": "1001", "cupom": "NAOEXISTE"})

            print("\n========== RESOURCES/LIST ==========")
            await session.list_resources()

            print("\n========== RESOURCES/READ (loja://regras/cupons) ==========")
            await session.read_resource("loja://regras/cupons")

            print("\n========== PROMPTS/LIST ==========")
            await session.list_prompts()

            print("\n========== PROMPTS/GET (resumir_pedido, id_pedido=1001) ==========")
            await session.get_prompt("resumir_pedido", {"id_pedido": "1001"})


if __name__ == "__main__":
    asyncio.run(main())
