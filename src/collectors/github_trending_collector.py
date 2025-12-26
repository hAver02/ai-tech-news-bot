"""
GitHub Trending Collector - Repos trending del día

Recopila repos que están trending en GitHub:
- Por lenguaje
- Por período (daily, weekly, monthly)
- 100% GRATIS
- Fuente: https://gh-trending-api.gainor.xyz (API pública estable)

Nota: GitHub no tiene API oficial de trending, usamos proxies públicos
"""

import requests
from typing import List, Dict
from datetime import datetime


class GitHubTrendingCollector:
    """
    Recopilador de repositorios trending de GitHub.
    
    Características:
    - Repos trending del día
    - Por lenguaje
    - 100% gratuito
    """
    
    def __init__(self):
        """Inicializa el collector de GitHub Trending."""
        self.base_url = "https://gh-trending-api.gainor.xyz/repositories"
    
    def collect(
        self,
        language: str = "",
        since: str = "daily",
        max_results: int = 10
    ) -> List[Dict]:
        """
        Recopila repos trending.
        
        Args:
            language: Lenguaje (vacío = todos, o "python", "typescript", etc.)
            since: Período ("daily", "weekly", "monthly")
            max_results: Máximo repos
            
        Returns:
            Lista de repos como noticias
        """
        print(f"\n⭐ GitHub Trending: {language or 'all languages'}")
        print(f"   Período: {since} | Max: {max_results}")
        
        params = {'since': since}
        if language:
            params['language'] = language
        
        try:
            response = requests.get(
                self.base_url,
                params=params,
                timeout=30
            )
            response.raise_for_status()
            repos = response.json()
            
            # Limitar resultados
            repos = repos[:max_results]
            print(f"   ✅ {len(repos)} repos")
            
            news_list = []
            for repo in repos:
                # Construir título descriptivo
                title = f"⭐ {repo.get('author', '')}/{repo.get('name', '')}"
                
                # Stars ganadas hoy
                stars_today = repo.get('starsSince', 0)
                
                news_list.append({
                    'title': title,
                    'link': repo.get('url', ''),
                    'summary': f"{repo.get('description', '')} | +{stars_today} stars hoy | {repo.get('stars', 0)} total",
                    'full_content': repo.get('description', ''),
                    'published': datetime.now().isoformat(),
                    'source': 'GitHub Trending',
                    'score': stars_today,
                    'language': repo.get('language', ''),
                    'total_stars': repo.get('stars', 0),
                    'forks': repo.get('forks', 0)
                })
            
            return news_list
            
        except requests.exceptions.RequestException as e:
            print(f"   ❌ Error en GitHub Trending: {str(e)}")
            return []
    
    def collect_multiple_languages(
        self,
        languages: List[str],
        max_results_per_language: int = 5
    ) -> List[Dict]:
        """
        Recopila trending para múltiples lenguajes.
        
        Args:
            languages: Lista de lenguajes
            max_results_per_language: Resultados por lenguaje
            
        Returns:
            Lista combinada
        """
        all_repos = []
        
        for lang in languages:
            repos = self.collect(
                language=lang,
                since='daily',
                max_results=max_results_per_language
            )
            all_repos.extend(repos)
        
        return all_repos


# Ejemplo de uso
if __name__ == "__main__":
    collector = GitHubTrendingCollector()
    
    # Trending de múltiples lenguajes
    repos = collector.collect_multiple_languages(
        languages=['python', 'typescript', 'rust', 'go'],
        max_results_per_language=3
    )
    
    print(f"\n📰 Total: {len(repos)} repos")
    for r in repos:
        print(f"   - [{r['language']}] {r['title']}")
