import requests
import streamlit as st
from typing import List, Dict
import json
from datetime import datetime, timedelta
import random
from functools import lru_cache
import time

class ArticleSearch:
    def __init__(self):
        self.api_key = st.secrets["SERPER_API_KEY"]
        self.base_url = "https://google.serper.dev/search"
        self.cache_timeout = 43200  # 12 heures en secondes
        
        # Plusieurs images par défaut pour chaque catégorie
        self.default_images = {
            'plantes': [
                'https://dolinasad.by/upload/medialibrary/823/8239d816da02039811c1adf511e29e9a.jpg',
                'https://kubantoday.ru/wp-content/uploads/2020/09/bdea610d6e38fbfb5b4c9c6b9b42b2a8.jpg',
                'https://s0.rbk.ru/v6_top_pics/media/img/0/45/347113711701450.webp',
                'https://pharmmedprom.ru/wp-content/uploads/2022/10/istock-1143843766.jpg',
                'https://moderator.az/file/articles/2023/01/25/1674622180_medicinal_herbs_071219.jpg'
            ],
            'nutrition': [
                'https://bopeepdaycare.com/wp-content/uploads/2021/12/Nutrition.jpg',
                'https://cen.acs.org/content/dam/cen/99/44/WEB/09944-feature1-nutrition.jpg',
                'https://www.hcbh.org/media/rdynpnx4/nutrition.png',
                'https://images.squarespace-cdn.com/content/v1/639f3fb4cb41156603ac38af/1673392963314-49PMDUT90PGQ2TB8A93T/96_1800x1800.jpg',
                'https://www.culture-nutrition.com/wp-content/uploads/2019/04/sante-publique-programme.jpg'
            ],
            'meditation': [
                'https://www.cancer.org/adobe/dynamicmedia/deliver/dm-aid--c705d936-4526-4d8f-a221-455a9c0a8ed5/man-meditating-outside-restricted.jpg',
                'https://ggia2.s3.us-west-2.amazonaws.com/assets/image/meditation_2023-2_-_abcdef_-_9c8d611802d588ff7312e25e69da318deffc042c.webp',
                'https://www.heart.org/-/media/AHA/H4GM/Article-Images/meditation.png',
                'https://cf.ltkcdn.net/garden/images/orig/331530-2121x1414-woman-meditating-in-garden.jpg',
                'https://www.arch2o.com/wp-content/uploads/2017/09/Arch2O-5-meditation-gardens-to-bring-out-your-inner-yogi-1.webp'
            ],
            'yoga': [
                'https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcSh0s6j_zhdmE5YT24cLaY1FQlhiXZB5Y4XEg&s',
                'https://centroclinicovidaesaude.com.br/wp-content/uploads/2024/12/libbsfarmaceutica_vidaplenalibbs_image_928-1.jpeg',
                'https://images.theconversation.com/files/602257/original/file-20240621-17-pa80sm.jpg'
            ],
            'medicine': [
                'https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcTvNTO8gh5k2ks_GqRGB3Skz5GNSc3XaJoX0A&s',
                'https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcTICSc6Kw518fhs_hjswAqYqRbpJHbP9ZGqRw&s',
                'https://images.contentstack.io/v3/assets/blt8a393bb3b76c0ede/blt0d055fcd73ce44b5/65a894507a1dd77bbbe13a44/Your_heart_medicines.jpg',
                'https://isbscience.org/wp-content/webp-express/webp-images/doc-root/wp-content/uploads/2024/10/PD5A3825-scaled.jpg.webp',
                'https://cdn.dal.ca/faculty/medicine/departments/core-units/undergraduate/program/med-4/_jcr_content/contentPar/staticimage.adaptive.full.high.jpg/1700096027077.jpg'
            ]
        }

    def _get_default_image(self, topic: str) -> str:
        """Renvoie une image par défaut appropriée en fonction du sujet de l'article"""
        if topic in self.default_images:
            return random.choice(self.default_images[topic])
        # Si le sujet n'est pas trouvé, renvoie une image aléatoire de n'importe quelle catégorie
        all_images = [img for images in self.default_images.values() for img in images]
        return random.choice(all_images)

    @lru_cache(maxsize=32)
    def _cached_search(self, query: str, language: str, timestamp: int) -> List[Dict]:
        """Recherche en cache d'articles avec filtrage des résultats"""
        payload = json.dumps({
            "q": query,
            "num": 30  # Demande plus de résultats pour un meilleur filtrage
        })
        
        headers = {
            'X-API-KEY': self.api_key,
            'Content-Type': 'application/json'
        }
        
        try:
            response = requests.post(
                self.base_url, 
                headers=headers, 
                data=payload,
                timeout=10
            )
            response.raise_for_status()
            results = response.json()
            
            # Filtre les résultats
            articles = []
            excluded_terms = ['amazon', 'boutique', 'shop', 'achat', 'prix', 'магазин', 'купить', 'аптека']
            
            for item in results.get('organic', []):
                title = item.get('title', '').lower()
                link = item.get('link', '').lower()
                
                # Ignore les résultats avec des termes commerciaux
                if any(term in title or term in link for term in excluded_terms):
                    continue
                    
                article = {
                    'title': item.get('title', ''),
                    'url': item.get('link', ''),
                    'snippet': item.get('snippet', '')
                }
                articles.append(article)
                
            return articles
            
        except Exception as e:
            print(f"Erreur de recherche: {str(e)}")
            return []

    def search_articles(self, query: str, language: str = 'fr') -> List[Dict]:
        """Recherche des articles avec la requête donnée"""
        excluded_terms = [
            'amazon', 'boutique', 'shop', 'achat', 'prix', 'магазин', 'купить', 'аптека',
            'buy', 'order', 'purchase', 'discount', 'deal', 'offer', 'promo', 'sale',
            'заказать', 'скидка', 'акция', 'распродажа', 'цена', 'стоимость'
        ]
        
        payload = json.dumps({
            "q": query,
            "num": 10,
            "tbm": "nws"  # Recherche uniquement les actualités
        })
        
        headers = {
            'X-API-KEY': self.api_key,
            'Content-Type': 'application/json'
        }
        
        try:
            response = requests.post(
                self.base_url, 
                headers=headers, 
                data=payload,
                timeout=10
            )
            response.raise_for_status()
            results = response.json()
            
            articles = []
            for item in results.get('organic', []):
                title = item.get('title', '').lower()
                link = item.get('link', '').lower()
                snippet = item.get('snippet', '').lower()
                
                # Ignore les résultats avec des termes commerciaux
                if any(term in title or term in link or term in snippet for term in excluded_terms):
                    continue
                    
                # Ignore les domaines commerciaux
                if any(domain in link for domain in ['amazon.', 'ebay.', 'pharmacy.', 'apteka.']):
                    continue
                    
                article = {
                    'title': item.get('title', ''),
                    'url': item.get('link', ''),
                    'snippet': item.get('snippet', '')
                }
                articles.append(article)
                
            return articles
            
        except Exception as e:
            print(f"Erreur de recherche: {str(e)}")
            return []

    def get_health_articles(self, language: str) -> List[Dict]:
        """Obtient des articles liés à la santé avec une distribution équilibrée des sujets"""
        timestamp = int(time.time()) // self.cache_timeout * self.cache_timeout
        
        queries = {
            'fr': [
                {
                    'topic': 'plantes',
                    'query': 'plantes médicinales bienfaits guide site:doctissimo.fr OR site:passeportsante.net -amazon -acheter -prix'
                },
                {
                    'topic': 'nutrition',
                    'query': 'nutrition conseils santé alimentation site:mangerbouger.fr OR site:santemagazine.fr -amazon -acheter'
                },
                {
                    'topic': 'meditation',
                    'query': 'méditation guide pratique bienfaits site:psychologies.com OR site:passeportsante.net -amazon'
                },
                {
                    'topic': 'yoga',
                    'query': 'yoga santé pratique débutant site:yogajournal.fr OR site:espritयoga.fr -amazon -boutique'
                },
                {
                    'topic': 'medicine',
                    'query': 'médecine naturelle conseils santé site:santemagazine.fr OR site:doctissimo.fr -amazon -pharmacie'
                }
            ],
            'en': [
                {
                    'topic': 'plantes',
                    'query': 'medicinal plants benefits guide site:healthline.com OR site:webmd.com -amazon -shop'
                },
                {
                    'topic': 'nutrition',
                    'query': 'nutrition health guide tips site:medicalnewstoday.com OR site:nutrition.org -amazon'
                },
                {
                    'topic': 'meditation',
                    'query': 'meditation wellness guide benefits site:mindful.org OR site:psychologytoday.com -amazon'
                },
                {
                    'topic': 'yoga',
                    'query': 'yoga health practice benefits site:yogajournal.com OR site:doyogawithme.com -amazon'
                },
                {
                    'topic': 'medicine',
                    'query': 'natural medicine health guide site:healthline.com OR site:webmd.com -amazon -shop'
                }
            ],
            'ru': [
                {
                    'topic': 'plantes',
                    'query': 'лечебные растения применение польза site:health-diet.ru OR site:medportal.ru -магазин -купить'
                },
                {
                    'topic': 'nutrition',
                    'query': 'здоровое питание советы гид site:health-diet.ru OR site:takzdorovo.ru -магазин'
                },
                {
                    'topic': 'meditation',
                    'query': 'медитация практика польза site:psychologies.ru OR site:yogajournal.ru -магазин'
                },
                {
                    'topic': 'yoga',
                    'query': 'йога здоровье практика site:yogajournal.ru OR site:ayoga.ru -магазин -купить'
                },
                {
                    'topic': 'medicine',
                    'query': 'натуральная медицина советы site:medportal.ru OR site:zdorovieinfo.ru -аптека -магазин'
                }
            ]
        }

        all_articles = []
        seen_urls = set()  # Pour suivre les URLs uniques
        articles_per_topic = {}  # Pour suivre le nombre d'articles par sujet

        # Premier passage - collecte des articles par sujet
        for topic_info in queries.get(language, queries['fr']):
            topic = topic_info['topic']
            query = topic_info['query']
            
            articles = self._cached_search(query, language, timestamp)
            articles_per_topic[topic] = []
            
            if articles:
                for article in articles:
                    url = article['url'].lower()
                    
                    # Vérifie l'URL par rapport aux domaines de confiance et à l'unicité
                    if url not in seen_urls and any(domain in url for domain in [
                        'doctissimo.fr', 'passeportsante.net', 'santemagazine.fr',
                        'psychologies.com', 'yogajournal.fr', 'healthline.com',
                        'webmd.com', 'medicalnewstoday.com', 'mindful.org',
                        'health-diet.ru', 'medportal.ru', 'takzdorovo.ru'
                    ]):
                        seen_urls.add(url)
                        article['photo'] = self._get_default_image(topic)
                        articles_per_topic[topic].append(article)

        # Deuxième passage - sélection d'un article par sujet
        final_articles = []
        topics = list(articles_per_topic.keys())
        
        # Continue jusqu'à avoir 5 articles ou jusqu'à épuisement des articles dans tous les sujets
        while len(final_articles) < 5 and any(articles_per_topic.values()):
            for topic in topics:
                if articles_per_topic[topic]:
                    article = articles_per_topic[topic].pop(0)  # Prend le premier article du sujet
                    final_articles.append(article)
                    if len(final_articles) >= 5:
                        break

        # Mélange les articles pour plus de variété
        random.shuffle(final_articles)
        return final_articles[:5]  # Renvoie au maximum 5 articles