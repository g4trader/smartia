# Cursor (Claude) – Prompt de Autonomia para Setup Completo

Você é o engenheiro responsável por:
1) Criar e configurar dois projetos: **apps/web (Next.js)** no Vercel e **services/api (Flask)** no Google Cloud Run.
2) Configurar CI/CD no GitHub (tests + build + lint).
3) Realizar commits/push no GitHub com mensagens claras e atômicas.
4) Executar testes localmente e no CI antes de abrir PRs.
5) Documentar tudo no README.

## Restrições e Convenções
- Linguagens: **TypeScript** (web) e **Python 3.11** (API).
- Node LTS. Usar **pnpm** quando disponível.
- Padrões: ESLint + Prettier, Ruff + Black.
- Testes mínimos: web (vitest) e api (pytest).
- Secrets via variáveis de ambiente. Nunca commitar tokens.

## Acessos Necessários (injetar via env/secret)
- `GITHUB_TOKEN` com permissão de repo (commit, PR).
- Vercel: `VERCEL_TOKEN`, `VERCEL_ORG_ID`, `VERCEL_PROJECT_ID` (apps/web).
- Google Cloud: `GOOGLE_APPLICATION_CREDENTIALS` (json), `GCP_PROJECT_ID`, `GCP_REGION` (services/api).

## Plano de Ação
1. **Verificar toolchain**: Node, pnpm, Python 3.11, gcloud, docker, vercel-cli.
2. **Instalar deps** e configurar lint/test em ambos.
3. **Criar projetos** no Vercel e Cloud Run (ou conectar a repositório já existente).
4. **CI GitHub**:
   - Workflow `ci.yml`: lint + test (web e api).
   - Workflow `deploy-api.yml`: build + push imagem via Cloud Build + deploy Cloud Run.
   - Workflow `deploy-web.yml`: trigger Vercel deploy.
5. **Variáveis de ambiente**:
   - Web: `NEXT_PUBLIC_API_BASE=https://<cloud-run-url>`
   - API: `MOCK_MODE=true`, `ALLOW_ORIGINS=*`
6. **Testes**: executar `pnpm test` e `pytest -q` local/CI.
7. **Entrega**: abrir PR com checklist, rodar pipelines, publicar URLs.

## Comandos Sugeridos
```bash
# Web
cd apps/web
pnpm i
pnpm lint && pnpm test && pnpm build

# API
cd services/api
python -m venv .venv && source .venv/bin/activate
pip install -r requirements.txt
pytest -q
```

## Critérios de Aceite
- Landing com seções: Hero, Provas, Produtos (SDR, E‑commerce, Autoatendimento, RFM), Demo interativa (chat simulado), Planos, FAQ, CTA.
- API simulando fluxos de conversa por tipo de agente com **state machine** simples e payload estilo WhatsApp.
- Deploys automatizados e documentação de variáveis de ambiente.
