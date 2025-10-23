# SmartIA WhatsApp Agents – Landing + Mock Platform

Monorepo com **Landing Page** (Next.js + Vercel) e **API Mock** (Flask + Cloud Run) para demonstrar agentes de IA no WhatsApp com **state machine** inteligente.

## 🤖 Agentes Disponíveis
- **Agent SDR** - Qualificação de leads e vendas
- **Agent E‑commerce** - FAQ, catálogo e checkout por link  
- **Agent Autoatendimento** - Agendamentos, CRM e pagamentos
- **Agent RFM** - Reativação por cluster de comportamento (Recency, Frequency, Monetary)

## 🏗️ Estrutura do Projeto
```
apps/web/              # Next.js (Landing + Demo chat interativo)
├── app/               # App Router (Next.js 14)
├── components/        # Componentes React
├── tests/            # Testes com Vitest
└── package.json      # Dependências e scripts

services/api/          # Flask API (State Machine + Webhooks)
├── app.py            # API principal com state machines
├── tests/            # Testes com pytest
├── requirements.txt  # Dependências Python
└── Dockerfile        # Container para Cloud Run

.github/workflows/     # CI/CD GitHub Actions
├── ci.yml            # Lint, test e build
├── deploy-api.yml    # Deploy para Cloud Run
└── deploy-web.yml    # Deploy para Vercel

infra/                 # Configurações de infraestrutura
├── cloudbuild.yaml   # Google Cloud Build
└── vercel.json       # Configuração Vercel
```

## 🚀 Deploy Automatizado

### Pré-requisitos
Configure os seguintes secrets no GitHub:
- `GITHUB_TOKEN` - Token com permissão de repo
- `VERCEL_TOKEN` - Token do Vercel CLI
- `VERCEL_ORG_ID` - ID da organização Vercel
- `VERCEL_PROJECT_ID` - ID do projeto Vercel
- `GOOGLE_APPLICATION_CREDENTIALS` - JSON das credenciais GCP
- `GCP_PROJECT_ID` - ID do projeto Google Cloud
- `GCP_REGION` - Região do Cloud Run (padrão: us-central1)
- `NEXT_PUBLIC_API_BASE` - URL da API no Cloud Run

### 1. Deploy da API (Cloud Run)
```bash
# O deploy é automático via GitHub Actions
# Push para main → Deploy automático
```

**Configuração manual (se necessário):**
```bash
# Build e push da imagem
docker build -t gcr.io/$PROJECT_ID/smartia-agents-api ./services/api
docker push gcr.io/$PROJECT_ID/smartia-agents-api

# Deploy para Cloud Run
gcloud run deploy smartia-agents-api \
  --image gcr.io/$PROJECT_ID/smartia-agents-api \
  --region us-central1 \
  --allow-unauthenticated \
  --port 8080 \
  --set-env-vars MOCK_MODE=true,ALLOW_ORIGINS=*
```

### 2. Deploy do Web App (Vercel)
```bash
# Deploy automático via GitHub Actions
# Push para main → Deploy automático
```

**Configuração manual (se necessário):**
```bash
cd apps/web
vercel --prod
```

## 🧪 Testes e Qualidade

### Executar Testes Localmente
```bash
# Web App
cd apps/web
npm test
npm run lint
npm run type-check

# API
cd services/api
pytest -v
ruff check .
black --check .
```

### CI/CD Pipeline
- **Lint**: ESLint + Prettier (web), Ruff + Black (API)
- **Testes**: Vitest (web), pytest (API)
- **Build**: Next.js build, Docker build
- **Deploy**: Vercel (web), Cloud Run (API)
- **Security**: Trivy vulnerability scan

## 🔧 Desenvolvimento Local

### Web App
```bash
cd apps/web
npm install
npm run dev
# Acesse http://localhost:3000
```

### API
```bash
cd services/api
python -m venv .venv
source .venv/bin/activate  # Linux/Mac
# .venv\Scripts\activate   # Windows
pip install -r requirements.txt
python app.py
# API disponível em http://localhost:8080
```

## 📡 Endpoints da API

### Simulação de Conversas
```bash
POST /simulate/{agent}
Content-Type: application/json

{
  "message": "oi",
  "phone": "11999999999"
}
```

**Agentes disponíveis:**
- `sdr` - Agent SDR
- `ecom` - Agent E-commerce  
- `auto` - Agent Autoatendimento
- `rfm` - Agent RFM

### Webhook WhatsApp
```bash
POST /webhook/whatsapp
Content-Type: application/json

{
  "message": "payload do WhatsApp"
}
```

### Health Check
```bash
GET /health
```

## 🎯 State Machine

Cada agente possui uma **state machine** que gerencia o fluxo da conversa:

- **INITIAL** → **QUALIFYING** → **PROPOSAL** → **CLOSING** → **COMPLETED**

As sessões são mantidas em memória com ID único baseado em `phone + agent`.

## 🌐 URLs de Produção

Após o deploy, as URLs serão:
- **Web App**: `https://smartia-web.vercel.app`
- **API**: `https://smartia-agents-api-xxx.run.app`

## 📊 Monitoramento

- **Vercel**: Dashboard de analytics e performance
- **Cloud Run**: Logs e métricas no Google Cloud Console
- **GitHub Actions**: Status dos workflows e deploys

## 🔒 Segurança

- Secrets gerenciados via GitHub Secrets
- CORS configurado para produção
- Health checks implementados
- Vulnerabilidades escaneadas via Trivy

## 📝 Licença
MIT
# Deploy test
