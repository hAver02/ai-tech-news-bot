"""
Query Builder - Construye queries específicas desde config

Lee advanced_queries.yaml y construye búsquedas optimizadas
"""

import yaml
from pathlib import Path
from typing import List, Dict
import random


class QueryBuilder:
    """
    Constructor de queries avanzadas para búsquedas.
    
    Usa config/advanced_queries.yaml para generar búsquedas específicas
    """
    
    def __init__(self, config_path: str = "config/advanced_queries.yaml"):
        """
        Inicializa el builder.
        
        Args:
            config_path: Ruta al archivo de configuración
        """
        self.config_path = Path(config_path)
        self.config = self._load_config()
    
    def _load_config(self) -> Dict:
        """Carga configuración desde YAML."""
        if not self.config_path.exists():
            print(f"⚠️  Config no encontrado: {self.config_path}")
            return {"categories": {}}
        
        with open(self.config_path, 'r', encoding='utf-8') as f:
            return yaml.safe_load(f)
    
    def get_queries_by_category(
        self,
        category: str,
        max_queries: int = 5
    ) -> List[str]:
        """
        Obtiene queries de una categoría específica.
        
        Args:
            category: Nombre de la categoría
            max_queries: Máximo queries a retornar
            
        Returns:
            Lista de queries
        """
        categories = self.config.get('categories', {})
        queries = categories.get(category, [])
        
        # Shuffle para variedad
        shuffled = queries.copy()
        random.shuffle(shuffled)
        
        return shuffled[:max_queries]
    
    def get_all_queries(self, queries_per_category: int = 3) -> List[str]:
        """
        Obtiene queries de todas las categorías.
        
        Args:
            queries_per_category: Queries por categoría
            
        Returns:
            Lista combinada de queries
        """
        all_queries = []
        categories = self.config.get('categories', {})
        
        for category, queries in categories.items():
            # Tomar sample de cada categoría
            sample = random.sample(
                queries,
                min(queries_per_category, len(queries))
            )
            all_queries.extend(sample)
        
        return all_queries
    
    def get_high_priority_queries(self, count: int = 10) -> List[str]:
        """
        Obtiene queries de categorías de alta prioridad.
        
        Args:
            count: Total de queries a retornar
            
        Returns:
            Lista de queries prioritarias
        """
        categories = self.config.get('categories', {})
        
        # Priorizar ciertas categorías
        high_priority_categories = [
            'ai_coding',
            'hardware_ai',
            'frameworks',
            'databases'
        ]
        
        queries = []
        for category in high_priority_categories:
            if category in categories:
                queries.extend(categories[category])
        
        # Shuffle y limitar
        random.shuffle(queries)
        return queries[:count]
    
    def get_exclude_terms(self) -> List[str]:
        """Obtiene términos a excluir."""
        return self.config.get('exclude_terms', [])
    
    def get_high_priority_terms(self) -> List[str]:
        """Obtiene términos de alta prioridad."""
        return self.config.get('high_priority_terms', [])


# Ejemplo de uso
if __name__ == "__main__":
    builder = QueryBuilder()
    
    # Queries de AI coding
    ai_coding = builder.get_queries_by_category('ai_coding', max_queries=3)
    print("AI Coding queries:")
    for q in ai_coding:
        print(f"  - {q}")
    
    # Queries prioritarias
    print("\nHigh priority queries:")
    priority = builder.get_high_priority_queries(count=5)
    for q in priority:
        print(f"  - {q}")
    
    # Términos a excluir
    print("\nExclude terms:")
    exclude = builder.get_exclude_terms()
    print(f"  {', '.join(exclude[:5])}...")
