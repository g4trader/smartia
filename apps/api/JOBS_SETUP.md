# Jobs Setup - Lembretes e No-Shows

## Visão Geral

O sistema de jobs automatiza o envio de lembretes e o tratamento de faltas (no-shows) para consultas agendadas.

## Jobs Disponíveis

### 1. Lembretes 24h
- **Função**: Envia lembretes 24 horas antes das consultas
- **Execução**: Diária às 9h
- **Endpoint**: `POST /jobs/reminders/24h`

### 2. Lembretes 2h
- **Função**: Envia lembretes 2 horas antes das consultas
- **Execução**: A cada hora
- **Endpoint**: `POST /jobs/reminders/2h`

### 3. No-Show Handler
- **Função**: Marca consultas como faltas e envia mensagens de reengajamento
- **Execução**: A cada hora
- **Endpoint**: `POST /jobs/no-shows`

### 4. Métricas
- **Função**: Coleta métricas de lembretes e faltas
- **Execução**: Manual ou agendada
- **Endpoint**: `GET /jobs/metrics`

## Execução via Script

```bash
# Lembretes 24h
python run_reminders.py --job 24h

# Lembretes 2h
python run_reminders.py --job 2h

# No-shows
python run_reminders.py --job no-show

# Métricas
python run_reminders.py --job metrics
```

## Agendamento com Cron

```bash
# Adicionar ao crontab
# Lembretes 24h - diário às 9h
0 9 * * * cd /path/to/api && python run_reminders.py --job 24h

# Lembretes 2h - a cada hora
0 * * * * cd /path/to/api && python run_reminders.py --job 2h

# No-shows - a cada hora
0 * * * * cd /path/to/api && python run_reminders.py --job no-show
```

## Cloud Scheduler (Google Cloud)

```yaml
# 24h reminders
- name: "24h-reminders"
  schedule: "0 9 * * *"
  target:
    httpTarget:
      uri: "https://your-api.com/jobs/reminders/24h"
      httpMethod: POST

# 2h reminders
- name: "2h-reminders"
  schedule: "0 * * * *"
  target:
    httpTarget:
      uri: "https://your-api.com/jobs/reminders/2h"
      httpMethod: POST

# No-show handler
- name: "no-show-handler"
  schedule: "0 * * * *"
  target:
    httpTarget:
      uri: "https://your-api.com/jobs/no-shows"
      httpMethod: POST
```

## Cloud Run Jobs

```yaml
# Dockerfile para jobs
FROM python:3.9-slim
WORKDIR /app
COPY requirements.txt .
RUN pip install -r requirements.txt
COPY . .
CMD ["python", "run_reminders.py", "--job", "24h"]
```

## Monitoramento

### Métricas Disponíveis
- Total de consultas (últimos 30 dias)
- Taxa de faltas
- Taxa de conclusão
- Mensagens de lembrete enviadas

### Logs
- Todos os jobs registram logs detalhados
- Interações são salvas no banco de dados
- Métricas são coletadas automaticamente

## Configuração

### Variáveis de Ambiente
```bash
# WhatsApp (obrigatório)
META_ACCESS_TOKEN=your_token
META_PHONE_NUMBER_ID=your_phone_id

# Database
DATABASE_URL=sqlite:///./smartia.db

# Timezone
CLINIC_TIMEZONE=America/Sao_Paulo
```

## Personalização

### Mensagens de Lembrete
Edite as mensagens em `jobs/reminders.py`:
- `_send_reminder()` - Lembretes 24h e 2h
- `_send_reengagement_message()` - Reengajamento após falta

### Horários
Ajuste os horários de execução conforme necessário:
- Lembretes 24h: 24 horas antes
- Lembretes 2h: 2 horas antes
- No-shows: 1 hora após horário agendado

## Troubleshooting

### Jobs não executam
1. Verifique as variáveis de ambiente
2. Confirme conectividade com WhatsApp API
3. Verifique logs de erro

### Mensagens não enviadas
1. Verifique tokens do WhatsApp
2. Confirme números de telefone válidos
3. Verifique limites de rate da API

### Métricas incorretas
1. Verifique timezone da clínica
2. Confirme status das consultas
3. Verifique datas no banco de dados
