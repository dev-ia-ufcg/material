# Formato das notas

O projeto publica as notas com o release-drafter, a partir das categorias abaixo. Escreva em inglês, como o restante do projeto.

## Estrutura

```markdown
## Unreleased

Suggested bump: minor

### Added
- Add Sinhala (si_LK) locale (#360)

### Fixed
- Fix `naturaldelta` truncating years instead of rounding (#295)
```

- Categorias, nesta ordem: Added, Changed, Deprecated, Removed, Fixed, Security.
- Omita a categoria que ficar vazia.
- Um item por linha, no imperativo, com o número do PR entre parênteses, como aparece no assunto do commit.
- Preserve o texto do assunto, só corrija a categoria e a pontuação se for preciso.

## Em que categoria cada commit entra

| Assunto do commit | Categoria |
|---|---|
| Add, Support | Added |
| Fix | Fixed |
| Drop support, ou remoção de funcionalidade pública | Removed |
| Remove que corrige um defeito, como tirar um resto indevido da saída | Fixed |
| Return, Use, Defer, Re-profile e outras mudanças de comportamento visíveis para quem usa a biblioteca | Changed |
| Correção de vulnerabilidade | Security |

## O que fica de fora

- Atualizações de dependência (assuntos "Update dependency ...", "Update github-actions", "Update docs/requirements.txt").
- Atualização automática do pre-commit.
- Ajustes de CI, de configuração de ferramentas e de matriz de testes.
- Mudanças que só afetam testes, doctests ou documentação interna.

Na dúvida entre incluir e omitir um commit, inclua e sinalize a dúvida na resposta ao usuário.

## Versão sugerida

Use a regra do release-drafter: Removed sugere major. Added, Changed, Deprecated e Security sugerem minor. Só Fixed sugere patch. Vale o maior incremento entre as categorias presentes.
