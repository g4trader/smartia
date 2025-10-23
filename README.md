# SmartIA - Clínica Inteligente

Sistema completo de automação para clínicas com IA integrada ao WhatsApp, agendamento automático, CRM e lembretes.

## 🚀 Funcionalidades

### ✅ Landing Page Refinada
- **Componentes reutilizáveis**: Hero, ComoFunciona, Beneficios, Planos, FAQ
- **Meta tags Open Graph**: Otimizada para redes sociais
- **Seção Smart IA Sprint**: Integração rápida em 30 dias
- **FAQ completo**: 6 perguntas frequentes sobre integrações, prazos, suporte
- **Design responsivo**: Layout adaptável para todos os dispositivos

### ✅ Fluxo de Webhook Completo
- **Parser Meta Cloud API**: Processamento de mensagens, botões e status
- **FlowOrchestrator**: Estados NEW_INTENT → ASK_DATE → ASK_TIME → CONFIRM → DONE
- **Detecção de intenções**: agendar, remarcar, cancelar, dúvidas
- **Persistência SQLite**: Conversas e estados salvos automaticamente
- **Envio de mensagens**: Integração com WhatsApp via Meta API

### ✅ Integração com Google Calendar
- **CalendarService plugável**: Interface clara para trocar provedores
- **Métodos CRUD**: list_slots, book_slot, cancel_event, get_event
- **OAuth2**: Autenticação segura com Google
- **Timezone configurável**: Suporte a diferentes fusos horários
- **Conflitos automáticos**: Verificação de disponibilidade

### ✅ CRM Mínimo Viável
- **Modelos completos**: Patient, Interaction, Appointment
- **Endpoints REST**: GET /patients, GET /appointments, GET /metrics
- **Métricas avançadas**: Taxa de confirmação, lead→consulta, faltas
- **Histórico completo**: Todas as interações salvas
- **Serialização**: Pronto para dashboard frontend

### ✅ Provedores Alternativos
- **Estratégia plugável**: Meta, Twilio, Zenvia
- **Injeção por ENV**: Configuração via variáveis de ambiente
- **Endpoints genéricos**: /webhook/{provider}
- **Factory pattern**: Criação dinâmica de provedores
- **Backward compatibility**: Endpoints legados mantidos

### ✅ Sistema de Lembretes e No-Shows
- **Jobs automatizados**: Lembretes 24h e 2h antes
- **No-show handler**: Marcação automática de faltas
- **Reengajamento**: Mensagens para pacientes que faltaram
- **Métricas detalhadas**: Taxa de faltas, conclusão, lembretes
- **Execução flexível**: Script, cron, Cloud Scheduler, Cloud Run Jobs

## 🏗️ Arquitetura

```
smartia/
├── apps/
│   ├── web/                 # Next.js Frontend
│   │   ├── components/      # Componentes reutilizáveis
│   │   ├── pages/          # Páginas da aplicação
│   │   └── package.json    # Dependências frontend
│   └── api/                # FastAPI Backend
│       ├── models/         # Modelos SQLAlchemy
│       ├── parsers/        # Parsers de webhook
│       ├── orchestrator/   # Fluxo de conversação
│       ├── services/       # Serviços (Calendar, etc)
│       ├── providers/      # Provedores WhatsApp
│       ├── jobs/           # Jobs de automação
│       └── tests/          # Testes unitários
├── packages/
│   └── shared/             # Código compartilhado
└── README.md
```

## 🛠️ Tecnologias

### Frontend
- **Next.js 14**: Framework React com pages router
- **TypeScript**: Tipagem estática
- **CSS Inline**: Estilos simples e responsivos

### Backend
- **FastAPI**: API moderna e rápida
- **SQLAlchemy**: ORM para banco de dados
- **SQLite**: Banco de dados local (configurável)
- **Pydantic**: Validação de dados
- **Pytest**: Testes unitários

### Integrações
- **Meta WhatsApp Cloud API**: Mensagens WhatsApp
- **Google Calendar API**: Agendamento
- **Twilio/Zenvia**: Provedores alternativos

## 🚀 Instalação e Configuração

### 1. Clone o repositório
```bash
git clone https://github.com/seu-usuario/smartia.git
cd smartia
```

### 2. Instale dependências
```bash
# Frontend
cd apps/web
npm install

# Backend
cd ../api
pip install -r requirements.txt
```

### 3. Configure variáveis de ambiente
```bash
# apps/api/.env
META_VERIFY_TOKEN=your_meta_verify_token
META_ACCESS_TOKEN=your_meta_access_token
META_PHONE_NUMBER_ID=your_phone_number_id

DATABASE_URL=sqlite:///./smartia.db

# Google Calendar (opcional)
GOOGLE_CREDENTIALS_PATH=credentials.json
GOOGLE_TOKEN_PATH=token.json
GOOGLE_CALENDAR_ID=primary
CLINIC_TIMEZONE=America/Sao_Paulo

# Provedores alternativos (opcional)
TWILIO_ACCOUNT_SID=your_twilio_account_sid
TWILIO_AUTH_TOKEN=your_twilio_auth_token
TWILIO_WHATSAPP_NUMBER=your_twilio_whatsapp_number

ZENVIA_API_KEY=your_zenvia_api_key
ZENVIA_WHATSAPP_NUMBER=your_zenvia_whatsapp_number
```

### 4. Configure Google Calendar (opcional)
```bash
# Siga as instruções em apps/api/GOOGLE_CALENDAR_SETUP.md
```

### 5. Execute a aplicação
```bash
# Backend
cd apps/api
uvicorn main:app --reload

# Frontend
cd apps/web
npm run dev
```

## 📱 Uso

### 1. Landing Page
- Acesse `http://localhost:3000`
- Visualize componentes reutilizáveis
- Teste responsividade

### 2. Webhook WhatsApp
- Configure webhook: `https://sua-api.com/webhook/meta`
- Envie mensagens para testar fluxo
- Monitore conversas no banco de dados

### 3. Agendamento
- Paciente envia "quero agendar"
- Sistema pergunta data e horário
- Confirma e cria evento no Google Calendar
- Salva appointment no CRM

### 4. Lembretes
```bash
# Executar manualmente
python run_reminders.py --job 24h
python run_reminders.py --job 2h
python run_reminders.py --job no-show

# Via API
curl -X POST http://localhost:8000/jobs/reminders/24h
```

## 🧪 Testes

```bash
cd apps/api
python -m pytest tests/ -v
```

## 📊 Endpoints da API

### Webhooks
- `GET /webhook/{provider}` - Verificação de webhook
- `POST /webhook/{provider}` - Receber mensagens
- `GET /providers` - Listar provedores disponíveis

### Calendário
- `GET /calendar/slots` - Horários disponíveis
- `GET /calendar/events/{id}` - Detalhes do evento
- `DELETE /calendar/events/{id}` - Cancelar evento

### CRM
- `GET /patients` - Listar pacientes
- `GET /patients/{id}` - Detalhes do paciente
- `GET /appointments` - Listar consultas
- `GET /metrics` - Métricas da clínica

### Jobs
- `POST /jobs/reminders/24h` - Lembretes 24h
- `POST /jobs/reminders/2h` - Lembretes 2h
- `POST /jobs/no-shows` - Tratar faltas
- `GET /jobs/metrics` - Métricas de jobs

## 🔧 Configuração de Produção

### 1. Banco de Dados
```bash
# PostgreSQL
DATABASE_URL=postgresql://user:pass@localhost/smartia

# MySQL
DATABASE_URL=mysql://user:pass@localhost/smartia
```

### 2. Deploy
```bash
# Docker
docker build -t smartia-api apps/api/
docker run -p 8000:8000 smartia-api

# Cloud Run
gcloud run deploy smartia-api --source apps/api/
```

### 3. Jobs Agendados
```bash
# Cron
0 9 * * * cd /app && python run_reminders.py --job 24h
0 * * * * cd /app && python run_reminders.py --job 2h

# Cloud Scheduler
# Configure via Google Cloud Console
```

## 📈 Métricas Disponíveis

### CRM
- Total de pacientes
- Total de consultas
- Taxa de confirmação
- Taxa de conversão (lead → consulta)

### Jobs
- Lembretes enviados
- Taxa de faltas
- Taxa de conclusão
- Mensagens de reengajamento

## 🤝 Contribuição

1. Fork o projeto
2. Crie uma branch (`git checkout -b feature/nova-funcionalidade`)
3. Commit suas mudanças (`git commit -am 'Adiciona nova funcionalidade'`)
4. Push para a branch (`git push origin feature/nova-funcionalidade`)
5. Abra um Pull Request

## 📄 Licença

Este projeto está sob a licença MIT. Veja o arquivo [LICENSE](LICENSE) para detalhes.

## 🆘 Suporte

- **Documentação**: Consulte os arquivos `.md` em cada diretório
- **Issues**: Abra uma issue no GitHub
- **Email**: contato@smartia.com.br

## 🎯 Roadmap

- [ ] Dashboard web para métricas
- [ ] Integração com mais provedores
- [ ] IA para análise de sentimento
- [ ] Relatórios avançados
- [ ] API de terceiros
- [ ] Mobile app

---

**SmartIA** - Transformando clínicas com inteligência artificial 🤖🏥