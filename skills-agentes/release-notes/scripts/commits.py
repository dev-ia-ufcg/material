#!/usr/bin/env python3
"""Extrai os commits desde a última tag e grava em commits.txt.

Uso:
    python3 commits.py                       # última tag até HEAD
    python3 commits.py --desde 4.15.0 --ate 4.16.0
"""
import argparse
import subprocess
import sys


def git(*args):
    resultado = subprocess.run(
        ["git", *args], capture_output=True, text=True
    )
    if resultado.returncode != 0:
        sys.exit(f"git {' '.join(args)}: {resultado.stderr.strip()}")
    return resultado.stdout.strip()


def main():
    parser = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    parser.add_argument("--desde", help="tag ou commit inicial (padrão: última tag)")
    parser.add_argument("--ate", default="HEAD", help="tag ou commit final (padrão: HEAD)")
    parser.add_argument("--saida", default="commits.txt", help="arquivo de saída")
    args = parser.parse_args()

    inicio = args.desde or git("describe", "--tags", "--abbrev=0", args.ate)
    intervalo = f"{inicio}..{args.ate}"

    log = git("log", "--no-merges", "--pretty=format:%h\t%an\t%s", intervalo)
    linhas = [linha for linha in log.splitlines() if linha]

    with open(args.saida, "w", encoding="utf-8") as arquivo:
        arquivo.write(f"# {intervalo}\n# hash\tautor\tassunto\n")
        for linha in linhas:
            arquivo.write(linha + "\n")

    print(f"{len(linhas)} commits em {intervalo} gravados em {args.saida}")


if __name__ == "__main__":
    main()
