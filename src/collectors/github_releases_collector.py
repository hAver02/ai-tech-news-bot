"""
GitHub Releases Collector - Monitora releases de repos importantes

Este collector obtiene los últimos releases/tags de repositorios clave:
- Next.js, TypeScript, Rust, etc.
- Detecta breaking changes
- Incluye release notes completas

100% GRATIS (GitHub API pública)
"""

import requests
from typing import List, Dict
from datetime import datetime, timedelta
from dotenv import load_dotenv
import os

load_dotenv()


class GitHubReleasesCollector:
    """
    Recopilador de releases de GitHub.
    
    Características:
    - Últimos releases de repos importantes
    - Release notes completas
    - Detección de breaking changes
    - 100% gratuito
    """
    
    def __init__(self, github_token: str = None):
        """
        Inicializa el collector.
        
        Args:
            github_token: GitHub token (opcional, aumenta rate limit)
        """
        self.github_token = github_token or os.getenv("GITHUB_TOKEN")
        self.base_url = "https://api.github.com"
        
        # Repos importantes para monitorear
        self.important_repos = [
            "vercel/next.js",
            "microsoft/TypeScript",
            "supabase/supabase",
            "facebook/react",
            "rust-lang/rust",
            "nodejs/node",
            "prisma/prisma",
            "denoland/deno",
            "openai/openai-python",
            "anthropics/anthropic-sdk-python",
            "sveltejs/svelte",
            "vuejs/core",
            "astro-build/astro",
            "remix-run/remix",
            "tailwindlabs/tailwindcss"
        ]
    
    def get_headers(self) -> Dict:
        """Obtiene headers para API de GitHub."""
        headers = {
            "Accept": "application/vnd.github.v3+json"
        }
        if self.github_token:
            headers["Authorization"] = f"token {self.github_token}"
        return headers
    
    def collect_repo_releases(
        self,
        repo: str,
        max_releases: int = 3,
        max_age_days: int = 30
    ) -> List[Dict]:
        """
        Recopila releases recientes de un repo.
        
        Args:
            repo: Nombre del repo (ej: "vercel/next.js")
            max_releases: Máximo releases a obtener
            max_age_days: Antigüedad máxima en días
            
        Returns:
            Lista de releases
        """
        url = f"{self.base_url}/repos/{repo}/releases"
        
        try:
            response = requests.get(
                url,
                headers=self.get_headers(),
                params={"per_page": max_releases},
                timeout=30
            )
            response.raise_for_status()
            releases = response.json()
            
            cutoff_date = datetime.now() - timedelta(days=max_age_days)
            recent_releases = []
            
            for release in releases:
                published = datetime.strptime(
                    release['published_at'],
                    '%Y-%m-%dT%H:%M:%SZ'
                )
                
                if published < cutoff_date:
                    continue
                
                # Detectar breaking changes
                body = release.get('body', '').lower()
                has_breaking = any(
                    term in body
                    for term in ['breaking', 'breaking change', 'migration']
                )
                
                recent_releases.append({
                    'title': f"🚀 {repo.split('/')[1]} {release['tag_name']} Released",
                    'link': release['html_url'],
                    'summary': (release.get('body', '') or release['name'])[:500],
                    'full_content': release.get('body', '') or release['name'],
                    'published': release['published_at'],
                    'source': f"GitHub Releases ({repo.split('/')[0]})",
                    'repo': repo,
                    'tag': release['tag_name'],
                    'prerelease': release.get('prerelease', False),
                    'has_breaking_changes': has_breaking
                })
            
            return recent_releases
            
        except requests.exceptions.RequestException as e:
            print(f"   ❌ Error en GitHub {repo}: {str(e)}")
            return []
    
    def collect_all(
        self,
        repos: List[str] = None,
        max_releases_per_repo: int = 2,
        max_age_days: int = 30
    ) -> List[Dict]:
        """
        Recopila releases de múltiples repos.
        
        Args:
            repos: Lista de repos (None = usar lista default)
            max_releases_per_repo: Releases por repo
            max_age_days: Antigüedad máxima
            
        Returns:
            Lista combinada de releases
        """
        repos = repos or self.important_repos
        
        print(f"\n📦 GitHub Releases Collector")
        print(f"   Monitoreando {len(repos)} repos...")
        
        all_releases = []
        
        for repo in repos:
            print(f"\n   📦 {repo}...", end=" ")
            releases = self.collect_repo_releases(
                repo,
                max_releases=max_releases_per_repo,
                max_age_days=max_age_days
            )
            
            if releases:
                print(f"✅ {len(releases)} releases")
                all_releases.extend(releases)
            else:
                print("⚪ Sin releases recientes")
        
        print(f"\n   📊 Total: {len(all_releases)} releases")
        
        return all_releases


# Ejemplo de uso
if __name__ == "__main__":
    collector = GitHubReleasesCollector()
    
    # Recopilar releases de últimos 7 días
    releases = collector.collect_all(
        max_releases_per_repo=2,
        max_age_days=7
    )
    
    print(f"\n📰 {len(releases)} releases encontrados")
    
    # Mostrar los que tienen breaking changes
    breaking = [r for r in releases if r.get('has_breaking_changes')]
    if breaking:
        print(f"\n⚠️  {len(breaking)} releases con BREAKING CHANGES:")
        for r in breaking:
            print(f"   - {r['title']}")
