"""Módulo de recolectores de noticias."""

from .rss_collector import RSSCollector
from .news_api_collector import NewsAPICollector

__all__ = ['RSSCollector', 'NewsAPICollector']

