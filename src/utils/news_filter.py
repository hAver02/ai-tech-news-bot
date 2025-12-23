"""
News Filter - Filtrado básico de noticias

Este módulo realiza filtros básicos como:
- Eliminar duplicados
- Filtrar por antigüedad
- Validar longitud de títulos
"""

from datetime import datetime, timedelta
from typing import List, Dict
import hashlib


class NewsFilter:
    """Filtros básicos para noticias."""
    
    @staticmethod
    def remove_duplicates(news_list: List[Dict]) -> List[Dict]:
        """
        Elimina noticias duplicadas basándose en el título.
        
        Args:
            news_list: Lista de noticias
            
        Returns:
            Lista sin duplicados
        """
        seen_titles = set()
        unique_news = []
        
        for news in news_list:
            # Crear hash del título normalizado
            title_hash = hashlib.md5(
                news['title'].lower().strip().encode()
            ).hexdigest()
            
            if title_hash not in seen_titles:
                seen_titles.add(title_hash)
                unique_news.append(news)
        
        removed = len(news_list) - len(unique_news)
        if removed > 0:
            print(f"   🗑️  Eliminados {removed} duplicados")
        
        return unique_news
    
    @staticmethod
    def filter_by_age(news_list: List[Dict], max_hours: int = 24) -> List[Dict]:
        """
        Filtra noticias por antigüedad.
        
        Args:
            news_list: Lista de noticias
            max_hours: Máxima antigüedad en horas
            
        Returns:
            Lista filtrada
        """
        from datetime import timezone
        
        cutoff = datetime.now(timezone.utc) - timedelta(hours=max_hours)
        filtered = []
        
        for news in news_list:
            published = news.get('published')
            if published:
                try:
                    pub_date = datetime.fromisoformat(published)
                    # Hacer ambos datetimes timezone-aware para compararlos
                    if pub_date.tzinfo is None:
                        pub_date = pub_date.replace(tzinfo=timezone.utc)
                    if pub_date >= cutoff:
                        filtered.append(news)
                except ValueError:
                    # Si no se puede parsear, incluir la noticia
                    filtered.append(news)
            else:
                # Si no tiene fecha, incluir la noticia
                filtered.append(news)
        
        removed = len(news_list) - len(filtered)
        if removed > 0:
            print(f"   ⏰ Eliminadas {removed} noticias antiguas (>{max_hours}h)")
        
        return filtered
    
    @staticmethod
    def filter_by_title_length(
        news_list: List[Dict],
        min_length: int = 20,
        max_length: int = 200
    ) -> List[Dict]:
        """
        Filtra noticias por longitud del título.
        
        Args:
            news_list: Lista de noticias
            min_length: Longitud mínima del título
            max_length: Longitud máxima del título
            
        Returns:
            Lista filtrada
        """
        filtered = []
        
        for news in news_list:
            title_len = len(news.get('title', ''))
            if min_length <= title_len <= max_length:
                filtered.append(news)
        
        removed = len(news_list) - len(filtered)
        if removed > 0:
            print(f"   ✂️  Eliminadas {removed} noticias con títulos muy cortos/largos")
        
        return filtered
    
    @staticmethod
    def apply_all_filters(
        news_list: List[Dict],
        max_age_hours: int = 24,
        min_title_length: int = 20,
        max_title_length: int = 200
    ) -> List[Dict]:
        """
        Aplica todos los filtros básicos.
        
        Args:
            news_list: Lista de noticias
            max_age_hours: Máxima antigüedad en horas
            min_title_length: Longitud mínima del título
            max_title_length: Longitud máxima del título
            
        Returns:
            Lista filtrada
        """
        print(f"🔍 Aplicando filtros a {len(news_list)} noticias...")
        
        # Aplicar filtros en secuencia
        filtered = NewsFilter.remove_duplicates(news_list)
        filtered = NewsFilter.filter_by_age(filtered, max_age_hours)
        filtered = NewsFilter.filter_by_title_length(
            filtered, min_title_length, max_title_length
        )
        
        print(f"✅ {len(filtered)} noticias pasaron los filtros básicos")
        
        return filtered

