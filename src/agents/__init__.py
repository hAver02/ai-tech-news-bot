"""
Agents Package - Agentes inteligentes para el sistema

Este paquete contiene agentes especializados:
- NewsValidatorAgent: Valida relevancia y frescura con LLM
- ContinuousCollectorAgent: Recopila noticias continuamente
"""

from .news_validator_agent import NewsValidatorAgent
from .continuous_collector_agent import ContinuousCollectorAgent

__all__ = ['NewsValidatorAgent', 'ContinuousCollectorAgent']
