# Guia de Deploy - SmartIA

## 🚀 Deploy Automático

### Frontend (Vercel)
O frontend já está configurado para deploy automático no Vercel:
- ✅ Conectado ao repositório GitHub
- ✅ Deploy automático a cada push na branch `main`
- ✅ URL: `https://smartia.vercel.app` (ou similar)

### Backend (Google Cloud Run)

#### 1. Configuração Inicial
```bash
# Instalar Google Cloud SDK
# https://cloud.google.com/sdk/docs/install

# Autenticar
gcloud auth login

# Configurar projeto
gcloud config set project SEU_PROJECT_ID
```

#### 2. Deploy via Cloud Build (Recomendado)
```bash
# Fazer push do código
git push origin main

# Trigger do build
gcloud builds submit --config cloudbuild.yaml
```

#### 3. Deploy Manual
```bash
# Build da imagem
cd apps/api
docker build -t gcr.io/SEU_PROJECT_ID/smartia-api .

# Push para Container Registry
docker push gcr.io/SEU_PROJECT_ID/smartia-api

# Deploy no Cloud Run
gcloud run deploy smartia-api \
  --image gcr.io/SEU_PROJECT_ID/smartia-api \
  --region us-central1 \
  --platform managed \
  --allow-unauthenticated \
  --port 8000 \
  --memory 1Gi \
  --cpu 1 \
  --max-instances 10 \
  --set-env-vars "DATABASE_URL=sqlite:///./smartia.db,CLINIC_TIMEZONE=America/Sao_Paulo"
```

## 🔧 Variáveis de Ambiente

### Frontend (Vercel)
Configure no painel do Vercel:
```
NEXT_PUBLIC_WHATSAPP_NUMBER=5511999999999
NEXT_PUBLIC_API_URL=https://smartia-api-xxxxx-uc.a.run.app
```

### Backend (Cloud Run)
Configure via gcloud ou painel:
```bash
# WhatsApp
META_ACCESS_TOKEN=seu_token_meta
META_VERIFY_TOKEN=seu_verify_token
META_PHONE_NUMBER_ID=seu_phone_id

# Twilio (opcional)
TWILIO_ACCOUNT_SID=seu_sid
TWILIO_AUTH_TOKEN=seu_token
TWILIO_WHATSAPP_NUMBER=whatsapp:+14155238886

# Zenvia (opcional)
ZENVIA_API_TOKEN=seu_token
ZENVIA_WHATSAPP_NUMBER=5511999999999

# Google Calendar
GOOGLE_CALENDAR_CREDENTIALS_FILE=/app/credentials.json
GOOGLE_CALENDAR_ID=seu_calendar_id@gmail.com

# Database
DATABASE_URL=sqlite:///./smartia.db

# Timezone
CLINIC_TIMEZONE=America/Sao_Paulo
```

## 📋 Checklist de Deploy

### Frontend
- [ ] Código commitado e pushado
- [ ] Vercel conectado ao repositório
- [ ] Variáveis de ambiente configuradas
- [ ] Deploy automático funcionando

### Backend
- [ ] Google Cloud Project criado
- [ ] APIs habilitadas (Cloud Run, Container Registry, Cloud Build)
- [ ] Service Account configurado
- [ ] Variáveis de ambiente configuradas
- [ ] Deploy realizado com sucesso
- [ ] Health check funcionando: `GET /health`

## 🔍 Verificação Pós-Deploy

### Frontend
```bash
# Verificar se está online
curl https://smartia.vercel.app

# Verificar build
npm run build
```

### Backend
```bash
# Health check
curl https://smartia-api-xxxxx-uc.a.run.app/health

# Testar webhook
curl -X POST https://smartia-api-xxxxx-uc.a.run.app/webhook/meta \
  -H "Content-Type: application/json" \
  -d '{"test": "webhook"}'

# Verificar providers
curl https://smartia-api-xxxxx-uc.a.run.app/providers
```

## 🚨 Troubleshooting

### Erro de Build
```bash
# Verificar logs
gcloud builds log --stream

# Verificar Dockerfile
docker build -t test ./apps/api
```

### Erro de Deploy
```bash
# Verificar logs do Cloud Run
gcloud run services logs read smartia-api --region us-central1

# Verificar configuração
gcloud run services describe smartia-api --region us-central1
```

### Erro de Variáveis
```bash
# Listar variáveis
gcloud run services describe smartia-api --region us-central1 --format="value(spec.template.spec.template.spec.containers[0].env[].name,spec.template.spec.template.spec.containers[0].env[].value)"

# Atualizar variáveis
gcloud run services update smartia-api --region us-central1 --set-env-vars "NOVA_VAR=valor"
```

## 📊 Monitoramento

### Cloud Run Metrics
- CPU e Memory usage
- Request count e latency
- Error rate
- Cold starts

### Logs
```bash
# Logs em tempo real
gcloud run services logs tail smartia-api --region us-central1

# Logs específicos
gcloud run services logs read smartia-api --region us-central1 --filter="severity>=ERROR"
```

## 🔄 CI/CD Automático

Para automatizar completamente:

1. **GitHub Actions** (alternativa ao Cloud Build)
2. **Webhook do Vercel** para rebuilds
3. **Cloud Scheduler** para jobs de lembretes
4. **Monitoring** com Cloud Monitoring

## 📞 Suporte

- **Documentação**: Este repositório
- **Issues**: GitHub Issues
- **Logs**: Google Cloud Console
- **Métricas**: Cloud Run Dashboard
