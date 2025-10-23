import os
from typing import Dict, Type
from .base import BaseProvider
from .meta import MetaProvider
from .twilio import TwilioProvider
from .zenvia import ZenviaProvider

class ProviderFactory:
    """Factory for creating WhatsApp providers"""
    
    _providers: Dict[str, Type[BaseProvider]] = {
        "meta": MetaProvider,
        "twilio": TwilioProvider,
        "zenvia": ZenviaProvider
    }
    
    @classmethod
    def create_provider(cls, provider_name: str) -> BaseProvider:
        """
        Create a provider instance
        
        Args:
            provider_name: Name of the provider (meta, twilio, zenvia)
            
        Returns:
            Provider instance
            
        Raises:
            ValueError: If provider is not supported
        """
        provider_name = provider_name.lower()
        
        if provider_name not in cls._providers:
            raise ValueError(f"Unsupported provider: {provider_name}")
        
        provider_class = cls._providers[provider_name]
        return provider_class()
    
    @classmethod
    def get_default_provider(cls) -> BaseProvider:
        """
        Get the default provider based on environment variables
        
        Returns:
            Default provider instance
        """
        # Check environment variables to determine default provider
        if os.getenv("META_ACCESS_TOKEN"):
            return cls.create_provider("meta")
        elif os.getenv("TWILIO_ACCOUNT_SID"):
            return cls.create_provider("twilio")
        elif os.getenv("ZENVIA_API_KEY"):
            return cls.create_provider("zenvia")
        else:
            # Default to Meta if no provider is configured
            return cls.create_provider("meta")
    
    @classmethod
    def get_available_providers(cls) -> list:
        """
        Get list of available providers based on environment variables
        
        Returns:
            List of available provider names
        """
        available = []
        
        if os.getenv("META_ACCESS_TOKEN"):
            available.append("meta")
        if os.getenv("TWILIO_ACCOUNT_SID"):
            available.append("twilio")
        if os.getenv("ZENVIA_API_KEY"):
            available.append("zenvia")
            
        return available
