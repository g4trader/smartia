import os
from enum import Enum
from typing import Dict, Any, Optional
from flask import Flask, request, jsonify
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

# State machine para simular conversas
class AgentState(Enum):
    INITIAL = "initial"
    QUALIFYING = "qualifying"
    PROPOSAL = "proposal"
    CLOSING = "closing"
    COMPLETED = "completed"

class AgentType(Enum):
    SDR = "sdr"
    ECOM = "ecom"
    AUTO = "auto"
    RFM = "rfm"

# Simulação de sessões de conversa
conversation_sessions: Dict[str, Dict[str, Any]] = {}

def get_session_id(phone: str, agent: str) -> str:
    """Gera ID único para sessão de conversa"""
    return f"{phone}_{agent}"

def get_or_create_session(phone: str, agent: str) -> Dict[str, Any]:
    """Obtém ou cria nova sessão de conversa"""
    session_id = get_session_id(phone, agent)
    if session_id not in conversation_sessions:
        conversation_sessions[session_id] = {
            "state": AgentState.INITIAL,
            "context": {},
            "phone": phone,
            "agent": agent
        }
    return conversation_sessions[session_id]

def sdr_state_machine(session: Dict[str, Any], message: str) -> tuple[str, AgentState]:
    """State machine para Agent SDR"""
    msg = message.lower()
    current_state = session["state"]
    
    if current_state == AgentState.INITIAL:
        if any(word in msg for word in ["oi", "olá", "bom dia", "boa tarde"]):
            session["state"] = AgentState.QUALIFYING
            return "Sou o Agent SDR. Qual é o seu objetivo principal: leads qualificados, reduzir CPL ou acelerar follow-ups?", AgentState.QUALIFYING
    
    elif current_state == AgentState.QUALIFYING:
        if any(word in msg for word in ["preço", "valor", "custo", "investimento"]):
            session["state"] = AgentState.PROPOSAL
            return "Posso ajudar! Qual é o tamanho do seu time e meta mensal? Assim envio a proposta certa e agendo uma call.", AgentState.PROPOSAL
        else:
            return "Entendi! Vou qualificar alguns pontos: segmento, ticket médio e CRM atual. Pode me dizer?", AgentState.QUALIFYING
    
    elif current_state == AgentState.PROPOSAL:
        session["state"] = AgentState.CLOSING
        return "Perfeito! Vou preparar uma proposta personalizada. Qual o melhor horário para uma call de 15min esta semana?", AgentState.CLOSING
    
    elif current_state == AgentState.CLOSING:
        session["state"] = AgentState.COMPLETED
        return "Excelente! Agendamento confirmado. Você receberá o link da reunião e a proposta por email. Obrigado!", AgentState.COMPLETED
    
    return "Como posso ajudar você hoje?", current_state

def ecom_state_machine(session: Dict[str, Any], message: str) -> tuple[str, AgentState]:
    """State machine para Agent E-commerce"""
    msg = message.lower()
    
    if "frete" in msg:
        return "Frete grátis acima de R$199. Quer ver opções de entrega para seu CEP?", AgentState.QUALIFYING
    elif any(word in msg for word in ["pagar", "checkout", "comprar"]):
        return "Enviei um link de pagamento seguro. Precisa de nota e CPF na NF?", AgentState.CLOSING
    else:
        return "Tenho ofertas em destaque hoje. Prefere ver por categoria ou por preço?", AgentState.QUALIFYING

def auto_state_machine(session: Dict[str, Any], message: str) -> tuple[str, AgentState]:
    """State machine para Agent Autoatendimento"""
    msg = message.lower()
    
    if any(word in msg for word in ["agendar", "consulta", "marcar"]):
        return "Perfeito! Tenho 10:30 e 14:00 amanhã. Qual prefere?", AgentState.QUALIFYING
    elif "confirmar" in msg:
        return "Confirmação realizada. Você receberá lembrete automático 24h antes.", AgentState.COMPLETED
    elif "pagar" in msg:
        return "Segue link de pagamento. Assim que confirmado, a agenda é bloqueada para você.", AgentState.CLOSING
    else:
        return "Sou o agente de autoatendimento. Posso agendar, confirmar, remarcar e enviar pagamentos.", AgentState.INITIAL

def rfm_state_machine(session: Dict[str, Any], message: str) -> tuple[str, AgentState]:
    """State machine para Agent RFM"""
    msg = message.lower()
    
    if "desconto" in msg:
        return "Para clientes frequentes, tenho 10% OFF hoje. Quer aplicar no seu próximo pedido?", AgentState.CLOSING
    else:
        return "Notei que faz um tempo desde sua última compra. Posso sugerir itens com base no seu histórico?", AgentState.QUALIFYING

@app.route("/simulate/<agent>", methods=["POST"])
def simulate(agent: str):
    """Endpoint para simular conversas com state machine"""
    data = request.get_json(silent=True) or {}
    message = (data.get("message") or "").strip()
    phone = data.get("phone", "demo_user")
    
    if not message:
        return jsonify({"reply": "Envie uma mensagem para iniciar.", "agent": agent})
    
    try:
        agent_type = AgentType(agent.lower())
    except ValueError:
        return jsonify({"reply": "Agente desconhecido.", "agent": agent})
    
    # Obter sessão da conversa
    session = get_or_create_session(phone, agent)
    
    # Processar mensagem com state machine
    if agent_type == AgentType.SDR:
        reply, new_state = sdr_state_machine(session, message)
    elif agent_type == AgentType.ECOM:
        reply, new_state = ecom_state_machine(session, message)
    elif agent_type == AgentType.AUTO:
        reply, new_state = auto_state_machine(session, message)
    elif agent_type == AgentType.RFM:
        reply, new_state = rfm_state_machine(session, message)
    else:
        reply = "Agente não implementado."
        new_state = AgentState.INITIAL
    
    return jsonify({
        "reply": reply,
        "agent": agent,
        "state": new_state.value,
        "session_id": get_session_id(phone, agent)
    })

@app.route("/webhook/whatsapp", methods=["POST"])
def webhook():
    """Webhook para receber mensagens do WhatsApp"""
    payload = request.get_json(silent=True) or {}
    
    # Simulação de parsing do payload do WhatsApp
    # Em produção, aqui faria parsing do provider (Twilio/Meta/360dialog)
    
    return jsonify({
        "status": "ok",
        "message": "Webhook recebido com sucesso",
        "echo": payload
    })

@app.route("/health", methods=["GET"])
def health():
    """Health check endpoint"""
    return jsonify({
        "status": "healthy",
        "service": "smartia-agents-api",
        "version": "1.0.0"
    })

@app.route("/", methods=["GET"])
def root():
    """Root endpoint"""
    return jsonify({
        "message": "SmartIA WhatsApp Agents API",
        "version": "1.0.0",
        "endpoints": {
            "simulate": "/simulate/<agent>",
            "webhook": "/webhook/whatsapp",
            "health": "/health"
        }
    })

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 8080))
    app.run(host="0.0.0.0", port=port, debug=False)
