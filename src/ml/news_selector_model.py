"""
News Selector Model - Modelo ML para seleccionar las mejores noticias

Entrena un modelo que aprende qué noticias son más relevantes
basándose en features del contenido y feedback histórico.
"""

import json
import pickle
from pathlib import Path
from typing import List, Dict, Tuple
from datetime import datetime
import numpy as np


class NewsSelectorModel:
    """Modelo ML para seleccionar noticias relevantes."""
    
    def __init__(self, model_path: str = "models/news_selector.pkl"):
        """
        Inicializa el modelo de selección.
        
        Args:
            model_path: Ruta donde guardar/cargar el modelo
        """
        self.model_path = Path(model_path)
        self.model = None
        self.feature_names = []
        self.is_trained = False
        
        # Cargar modelo si existe
        if self.model_path.exists():
            self.load_model()
    
    def extract_features(self, news_item: Dict) -> Dict[str, float]:
        """
        Extrae features de una noticia para el modelo.
        
        Args:
            news_item: Noticia a procesar
            
        Returns:
            Dict con features extraídos
        """
        features = {}
        
        # 1. Features de engagement
        features['score'] = float(news_item.get('score', 0))
        features['num_comments'] = float(news_item.get('num_comments', 0))
        features['reactions'] = float(news_item.get('reactions', 0))
        features['engagement_score'] = float(news_item.get('engagement_score', 0))
        
        # 2. Features de contenido
        title = news_item.get('title', '')
        features['title_length'] = float(len(title))
        features['title_word_count'] = float(len(title.split()))
        
        content = news_item.get('full_content', news_item.get('summary', ''))
        features['content_length'] = float(len(content))
        features['has_full_content'] = 1.0 if news_item.get('full_content') else 0.0
        
        # 3. Features de keywords
        keywords = news_item.get('extracted_keywords', [])
        features['num_keywords'] = float(len(keywords))
        
        # Keywords tech relevantes
        tech_keywords = ['ai', 'ml', 'python', 'javascript', 'api', 'data', 'cloud', 
                        'security', 'crypto', 'blockchain', 'startup', 'tech']
        features['tech_keyword_count'] = sum(
            1 for kw in keywords if any(tech in kw.lower() for tech in tech_keywords)
        )
        
        # 4. Features de fuente
        source = news_item.get('source', '').lower()
        features['is_hackernews'] = 1.0 if 'hacker' in source else 0.0
        features['is_reddit'] = 1.0 if 'reddit' in source else 0.0
        features['is_arstechnica'] = 1.0 if 'ars technica' in source else 0.0
        features['is_devto'] = 1.0 if 'dev.to' in source else 0.0
        
        # 5. Features de comentarios
        top_comments = news_item.get('top_comments', [])
        features['has_quality_comments'] = 1.0 if len(top_comments) > 0 else 0.0
        features['num_quality_comments'] = float(len(top_comments))
        
        if top_comments:
            avg_comment_score = np.mean([c.get('score', 0) for c in top_comments])
            features['avg_comment_score'] = float(avg_comment_score)
        else:
            features['avg_comment_score'] = 0.0
        
        # 6. Features de tiempo (si está disponible)
        # TODO: Agregar features temporales cuando tengamos historial
        
        return features
    
    def prepare_training_data(self, labeled_news: List[Dict]) -> Tuple[np.ndarray, np.ndarray]:
        """
        Prepara datos para entrenar el modelo.
        
        Args:
            labeled_news: Lista de noticias con labels (relevante: 1, no relevante: 0)
            
        Returns:
            Tuple (X, y) para entrenamiento
        """
        X = []
        y = []
        
        for item in labeled_news:
            features = self.extract_features(item)
            
            # Guardar nombres de features (primera vez)
            if not self.feature_names:
                self.feature_names = sorted(features.keys())
            
            # Crear vector de features en orden consistente
            feature_vector = [features[name] for name in self.feature_names]
            X.append(feature_vector)
            
            # Label (debe estar en el item)
            label = item.get('label', item.get('is_relevant', 0))
            y.append(float(label))
        
        return np.array(X), np.array(y)
    
    def train(self, labeled_news: List[Dict]):
        """
        Entrena el modelo con noticias etiquetadas.
        
        Args:
            labeled_news: Noticias con labels
        """
        print(f"🧠 Entrenando modelo con {len(labeled_news)} ejemplos...")
        
        # Preparar datos
        X, y = self.prepare_training_data(labeled_news)
        
        print(f"   Features: {len(self.feature_names)}")
        print(f"   Ejemplos positivos: {int(y.sum())}")
        print(f"   Ejemplos negativos: {len(y) - int(y.sum())}")
        
        # Por ahora: modelo simple basado en pesos
        # TODO: Usar sklearn cuando tengamos más datos
        # from sklearn.ensemble import RandomForestClassifier
        # self.model = RandomForestClassifier(n_estimators=100)
        # self.model.fit(X, y)
        
        # Modelo simple: promedio de features de ejemplos positivos
        positive_examples = X[y == 1]
        if len(positive_examples) > 0:
            self.model = {
                'type': 'weighted_average',
                'weights': positive_examples.mean(axis=0),
                'threshold': 0.5
            }
            self.is_trained = True
            print("   ✅ Modelo entrenado (weighted average)")
        else:
            print("   ⚠️  No hay ejemplos positivos, usando modelo por defecto")
            self.model = None
        
        # Guardar modelo
        self.save_model()
    
    def predict_score(self, news_item: Dict) -> float:
        """
        Predice el score de relevancia de una noticia.
        
        Args:
            news_item: Noticia a evaluar
            
        Returns:
            Score de relevancia (0-100)
        """
        if not self.is_trained or self.model is None:
            # Fallback: usar engagement score
            return news_item.get('engagement_score', 
                   news_item.get('score', 0) / 10)
        
        # Extraer features
        features = self.extract_features(news_item)
        feature_vector = np.array([features[name] for name in self.feature_names])
        
        # Calcular score con modelo simple
        if self.model['type'] == 'weighted_average':
            weights = self.model['weights']
            # Normalizar y calcular similitud
            score = np.dot(feature_vector, weights) / (np.linalg.norm(weights) + 1e-10)
            # Escalar a 0-100
            score = min(max(score, 0), 100)
        else:
            score = 0.0
        
        return float(score)
    
    def select_top_news(
        self,
        news_items: List[Dict],
        top_n: int = 5,
        min_score: float = 10.0
    ) -> List[Dict]:
        """
        Selecciona las mejores noticias usando el modelo.
        
        Args:
            news_items: Lista de noticias
            top_n: Número de noticias a seleccionar
            min_score: Score mínimo requerido
            
        Returns:
            Lista de mejores noticias con scores
        """
        print(f"\n🤖 Seleccionando mejores {top_n} noticias con ML...")
        
        # Calcular scores
        scored_news = []
        for item in news_items:
            score = self.predict_score(item)
            item_copy = item.copy()
            item_copy['ml_relevance_score'] = score
            scored_news.append(item_copy)
        
        # Filtrar por score mínimo
        filtered = [item for item in scored_news if item['ml_relevance_score'] >= min_score]
        
        # Ordenar por score
        sorted_news = sorted(filtered, key=lambda x: x['ml_relevance_score'], reverse=True)
        
        # Seleccionar top N
        selected = sorted_news[:top_n]
        
        print(f"   ✅ {len(selected)} noticias seleccionadas")
        if selected:
            print(f"   📊 Score range: {selected[-1]['ml_relevance_score']:.1f} - {selected[0]['ml_relevance_score']:.1f}")
        
        return selected
    
    def save_model(self):
        """Guarda el modelo en disco."""
        if self.model is None:
            return
        
        self.model_path.parent.mkdir(exist_ok=True)
        
        model_data = {
            'model': self.model,
            'feature_names': self.feature_names,
            'is_trained': self.is_trained,
            'trained_at': datetime.now().isoformat()
        }
        
        with open(self.model_path, 'wb') as f:
            pickle.dump(model_data, f)
        
        print(f"💾 Modelo guardado en: {self.model_path}")
    
    def load_model(self):
        """Carga el modelo desde disco."""
        if not self.model_path.exists():
            return
        
        try:
            with open(self.model_path, 'rb') as f:
                model_data = pickle.load(f)
            
            self.model = model_data['model']
            self.feature_names = model_data['feature_names']
            self.is_trained = model_data['is_trained']
            
            print(f"✅ Modelo cargado desde: {self.model_path}")
            print(f"   Entrenado en: {model_data.get('trained_at', 'unknown')}")
            
        except Exception as e:
            print(f"⚠️  Error cargando modelo: {e}")
            self.model = None
            self.is_trained = False
    
    def add_feedback(self, news_item: Dict, is_relevant: bool):
        """
        Agrega feedback sobre una noticia (para reentrenamiento).
        
        Args:
            news_item: Noticia
            is_relevant: Si fue relevante o no
        """
        feedback_file = Path("data/feedback.jsonl")
        feedback_file.parent.mkdir(exist_ok=True)
        
        feedback = {
            'news_id': news_item.get('link', ''),
            'title': news_item.get('title', ''),
            'is_relevant': int(is_relevant),
            'features': self.extract_features(news_item),
            'timestamp': datetime.now().isoformat()
        }
        
        # Append to feedback file
        with open(feedback_file, 'a', encoding='utf-8') as f:
            f.write(json.dumps(feedback, ensure_ascii=False) + '\n')
        
        print(f"✅ Feedback guardado")


# Ejemplo de uso
if __name__ == "__main__":
    # Ejemplo: entrenar con datos de ejemplo
    labeled_news = [
        {
            'title': 'OpenAI releases new model',
            'score': 500,
            'num_comments': 200,
            'source': 'Hacker News',
            'label': 1  # Relevante
        },
        {
            'title': 'Random blog post',
            'score': 5,
            'num_comments': 1,
            'source': 'Unknown',
            'label': 0  # No relevante
        }
    ]
    
    model = NewsSelectorModel()
    model.train(labeled_news)
    
    # Predecir
    test_news = {
        'title': 'New Python release',
        'score': 300,
        'num_comments': 150,
        'source': 'Hacker News'
    }
    
    score = model.predict_score(test_news)
    print(f"\nScore predicho: {score:.2f}")
