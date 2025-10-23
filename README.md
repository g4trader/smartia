# Smart IA Platform – WhatsApp + Landing (Vercel + Cloud Run)

Monorepo inicial para **landing page de vendas** e **plataforma web** integrada ao WhatsApp (Meta Cloud API/Twilio/Zenvia).

- Frontend: Next.js (Vercel).
- Backend: FastAPI (Google Cloud Run).
- Repositório preparado para desenvolvimento no Cursor (Claude).

## Estrutura
```
smartia-whatsapp-platform/
├─ apps/
│  ├─ web/        # Next.js (landing + app)
│  └─ api/        # FastAPI (webhooks WhatsApp + orquestração)
├─ packages/
│  └─ shared/     # Tipos/utilidades compartilhadas (opcional)
├─ .github/
│  └─ workflows/
│     ├─ web-vercel-preview.yml   # preview de PRs no Vercel (opcional)
│     └─ api-cloud-run-ci.yml     # build & deploy Cloud Run
├─ .env.example
└─ README.md
```

### Variáveis de ambiente (consolidado)
Veja `.env.example` para a lista completa.

### Deploy Rápido
1) **Frontend (Vercel)**
- Conecte o repo no Vercel e defina as envs do `apps/web`.
- Build Command: `pnpm build`  /  Output: `.next`

2) **Backend (Cloud Run)**
- `gcloud builds submit --tag gcr.io/$PROJECT_ID/smartia-api`
- `gcloud run deploy smartia-api --image gcr.io/$PROJECT_ID/smartia-api --platform managed --allow-unauthenticated --region $REGION`

### Desenvolvimento
- Requisitos: Node 20+, PNPM, Python 3.11+
- `pnpm i && pnpm -w dev` (inicia web e api em paralelo)
