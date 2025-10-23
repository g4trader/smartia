import pytest
from app import app, AgentType, AgentState, get_or_create_session, sdr_state_machine

@pytest.fixture
def client():
    app.config['TESTING'] = True
    with app.test_client() as client:
        yield client

def test_health_endpoint(client):
    """Test health check endpoint"""
    response = client.get('/health')
    assert response.status_code == 200
    data = response.get_json()
    assert data['status'] == 'healthy'
    assert data['service'] == 'smartia-agents-api'

def test_root_endpoint(client):
    """Test root endpoint"""
    response = client.get('/')
    assert response.status_code == 200
    data = response.get_json()
    assert 'message' in data
    assert 'endpoints' in data

def test_webhook_endpoint(client):
    """Test webhook endpoint"""
    payload = {'test': 'data'}
    response = client.post('/webhook/whatsapp', json=payload)
    assert response.status_code == 200
    data = response.get_json()
    assert data['status'] == 'ok'
    assert data['echo'] == payload

def test_simulate_sdr_initial(client):
    """Test SDR agent initial state"""
    response = client.post('/simulate/sdr', json={'message': 'oi', 'phone': 'test_user'})
    assert response.status_code == 200
    data = response.get_json()
    assert 'reply' in data
    assert data['agent'] == 'sdr'
    assert data['state'] == 'qualifying'

def test_simulate_sdr_qualifying(client):
    """Test SDR agent qualifying state"""
    # First message to get to qualifying state
    client.post('/simulate/sdr', json={'message': 'oi', 'phone': 'test_user2'})
    
    # Second message about price
    response = client.post('/simulate/sdr', json={'message': 'qual o preço?', 'phone': 'test_user2'})
    assert response.status_code == 200
    data = response.get_json()
    assert data['state'] == 'proposal'

def test_simulate_ecom(client):
    """Test E-commerce agent"""
    response = client.post('/simulate/ecom', json={'message': 'frete grátis?', 'phone': 'test_user3'})
    assert response.status_code == 200
    data = response.get_json()
    assert data['agent'] == 'ecom'
    assert 'frete' in data['reply'].lower()

def test_simulate_auto(client):
    """Test Autoatendimento agent"""
    response = client.post('/simulate/auto', json={'message': 'quero agendar', 'phone': 'test_user4'})
    assert response.status_code == 200
    data = response.get_json()
    assert data['agent'] == 'auto'
    assert 'agenda' in data['reply'].lower()

def test_simulate_rfm(client):
    """Test RFM agent"""
    response = client.post('/simulate/rfm', json={'message': 'desconto', 'phone': 'test_user5'})
    assert response.status_code == 200
    data = response.get_json()
    assert data['agent'] == 'rfm'
    assert 'desconto' in data['reply'].lower()

def test_simulate_invalid_agent(client):
    """Test invalid agent"""
    response = client.post('/simulate/invalid', json={'message': 'test'})
    assert response.status_code == 200
    data = response.get_json()
    assert 'Agente desconhecido' in data['reply']

def test_simulate_empty_message(client):
    """Test empty message"""
    response = client.post('/simulate/sdr', json={'message': ''})
    assert response.status_code == 200
    data = response.get_json()
    assert 'Envie uma mensagem' in data['reply']

def test_sdr_state_machine():
    """Test SDR state machine directly"""
    session = {
        'state': AgentState.INITIAL,
        'context': {},
        'phone': 'test',
        'agent': 'sdr'
    }
    
    # Test initial greeting
    reply, state = sdr_state_machine(session, 'oi')
    assert state == AgentState.QUALIFYING
    assert 'Sou o Agent SDR' in reply
    
    # Test price inquiry
    reply, state = sdr_state_machine(session, 'qual o preço?')
    assert state == AgentState.PROPOSAL
    assert 'proposta' in reply.lower()

def test_session_management():
    """Test session management"""
    from app import get_or_create_session
    
    # Create new session
    session1 = get_or_create_session('123456789', 'sdr')
    assert session1['phone'] == '123456789'
    assert session1['agent'] == 'sdr'
    assert session1['state'] == AgentState.INITIAL
    
    # Get existing session
    session2 = get_or_create_session('123456789', 'sdr')
    assert session1 is session2  # Same object reference