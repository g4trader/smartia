import pytest
import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from parsers.meta_parser import MetaWebhookParser

class TestMetaWebhookParser:
    
    def test_parse_text_message(self):
        """Test parsing of text message from Meta webhook"""
        payload = {
            "object": "whatsapp_business_account",
            "entry": [{
                "id": "123456789",
                "changes": [{
                    "value": {
                        "messaging_product": "whatsapp",
                        "metadata": {
                            "display_phone_number": "15551234567",
                            "phone_number_id": "987654321"
                        },
                        "messages": [{
                            "id": "wamid.123456789",
                            "from": "5511999999999",
                            "timestamp": "1640995200",
                            "text": {
                                "body": "Olá, quero agendar uma consulta"
                            },
                            "type": "text"
                        }]
                    },
                    "field": "messages"
                }]
            }]
        }
        
        messages = MetaWebhookParser.parse_webhook(payload)
        
        assert len(messages) == 1
        assert messages[0].message_id == "wamid.123456789"
        assert messages[0].from_number == "5511999999999"
        assert messages[0].message_type == "text"
        assert messages[0].content == "Olá, quero agendar uma consulta"
    
    def test_parse_button_message(self):
        """Test parsing of button response from Meta webhook"""
        payload = {
            "object": "whatsapp_business_account",
            "entry": [{
                "id": "123456789",
                "changes": [{
                    "value": {
                        "messaging_product": "whatsapp",
                        "metadata": {
                            "display_phone_number": "15551234567",
                            "phone_number_id": "987654321"
                        },
                        "messages": [{
                            "id": "wamid.987654321",
                            "from": "5511999999999",
                            "timestamp": "1640995200",
                            "button": {
                                "text": "Sim",
                                "payload": "confirm_yes"
                            },
                            "type": "button"
                        }]
                    },
                    "field": "messages"
                }]
            }]
        }
        
        messages = MetaWebhookParser.parse_webhook(payload)
        
        assert len(messages) == 1
        assert messages[0].message_type == "button"
        assert messages[0].content == "Sim"
        assert messages[0].button_payload == "confirm_yes"
    
    def test_detect_intent_agendar(self):
        """Test intent detection for scheduling"""
        test_cases = [
            "Quero agendar uma consulta",
            "Gostaria de marcar um horário",
            "Preciso de uma consulta",
            "Tem horário disponível?"
        ]
        
        for text in test_cases:
            intent = MetaWebhookParser.detect_intent(text)
            assert intent == "agendar"
    
    def test_detect_intent_remarcar(self):
        """Test intent detection for rescheduling"""
        test_cases = [
            "Quero remarcar minha consulta",
            "Preciso reagendar",
            "Posso mudar o horário?",
            "Quero alterar a data"
        ]
        
        for text in test_cases:
            intent = MetaWebhookParser.detect_intent(text)
            assert intent == "remarcar"
    
    def test_detect_intent_cancelar(self):
        """Test intent detection for cancellation"""
        test_cases = [
            "Quero cancelar minha consulta",
            "Preciso desmarcar",
            "Não posso ir na consulta",
            "Vou cancelar o agendamento"
        ]
        
        for text in test_cases:
            intent = MetaWebhookParser.detect_intent(text)
            assert intent == "cancelar"
    
    def test_detect_intent_duvidas(self):
        """Test intent detection for questions"""
        test_cases = [
            "Tenho uma dúvida",
            "Qual o preço da consulta?",
            "Como funciona o atendimento?",
            "Onde fica a clínica?"
        ]
        
        for text in test_cases:
            intent = MetaWebhookParser.detect_intent(text)
            assert intent == "duvidas"
