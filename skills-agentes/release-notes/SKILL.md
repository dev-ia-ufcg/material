---
name: release-notes
description: Gera o rascunho das release notes da próxima versão a partir dos commits desde a última tag, no formato do projeto. Use quando o usuário pedir release notes, changelog ou notas da próxima versão.
---

# Release notes

Gere o rascunho em `RELEASE_NOTES_DRAFT.md`, na raiz do repositório.

1. Rode `python3 ${CLAUDE_SKILL_DIR}/scripts/commits.py`. O script grava `commits.txt` na raiz e imprime o intervalo e a contagem. Se o usuário indicar outro intervalo, passe `--desde` e `--ate`.
2. Leia `commits.txt`.
3. Leia [formato.md](formato.md) e aplique o formato, as categorias e as regras de exclusão.
4. Escreva as notas em `RELEASE_NOTES_DRAFT.md`.
5. Diga ao usuário o intervalo usado, quantos commits ficaram de fora e por quê.

Só o que está em `commits.txt` entra nas notas. Não publique, não crie tag e não altere outros arquivos.
