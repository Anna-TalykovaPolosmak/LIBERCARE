import streamlit as st
from chatbot import MedicalChatbot
from styles import load_css
from search_utils import ArticleSearch
from datetime import datetime, timedelta
import asyncio
from concurrent.futures import ThreadPoolExecutor

# Configuration de la page
st.set_page_config(
    page_title='LIBERCARE',
    page_icon='🧘‍♀️',
    layout='wide'
)

# Chargement des styles
st.markdown(f"<style>{load_css()}</style>", unsafe_allow_html=True)

# Initialisation de l'état
if 'language' not in st.session_state:
    st.session_state.language = 'fr'
if 'terms_accepted' not in st.session_state:
    st.session_state.terms_accepted = False
if 'last_articles_update' not in st.session_state:
    st.session_state.last_articles_update = None
if 'cached_articles' not in st.session_state:
    st.session_state.cached_articles = None
if 'is_loading_articles' not in st.session_state:
    st.session_state.is_loading_articles = False

# Chargement asynchrone des articles
async def load_articles_async(article_search, language):
    loop = asyncio.get_event_loop()
    with ThreadPoolExecutor() as executor:
        articles = await loop.run_in_executor(
            executor, 
            article_search.get_health_articles,
            language
        )
    return articles

# Fenêtre modale avec conditions
if not st.session_state.terms_accepted:
    # Suppression des marges supérieures superflues
    st.markdown("""
        <style>
        [data-testid="stVerticalBlock"] > div:first-child {
            padding-top: 0;
        }
        div.stButton > button:first-child {
            margin-top: 2rem;
        }
        </style>
    """, unsafe_allow_html=True)
    
    # Contenu pour différentes langues
    modal_content = {
        'fr': {
            'title': 'Informations importantes',
            'disclaimer': 'Avis de non-responsabilité',
            'disclaimer_text': 'Ce site fournit des informations générales à titre indicatif uniquement. Ces informations ne remplacent en aucun cas un avis médical professionnel.',
            'self_medication': "L'automédication peut être dangereuse",
            'self_medication_text': 'Respectez strictement les doses recommandées et ne prolongez pas le traitement sans avis médical.',
            'consult': 'Consultez un médecin',
            'consult_text': "Si les symptômes persistent plus de 3 jours ou s'aggravent.",
            'terms_checkbox': "J'accepte les termes et conditions d'utilisation",
            'age_checkbox': "Je confirme avoir 18 ans ou plus",
            'continue_button': 'Continuer',
            'alert': "Vous devez accepter les conditions et confirmer votre âge pour continuer."
        },
        'en': {
            'title': 'Important Information',
            'disclaimer': 'Disclaimer',
            'disclaimer_text': 'This site provides general information for guidance purposes only. This information does not replace professional medical advice.',
            'self_medication': 'Self-medication can be dangerous',
            'self_medication_text': 'Strictly follow recommended doses and do not extend treatment without medical advice.',
            'consult': 'Consult a doctor',
            'consult_text': 'If symptoms persist for more than 3 days or worsen.',
            'terms_checkbox': 'I accept the terms and conditions',
            'age_checkbox': 'I confirm that I am 18 years or older',
            'continue_button': 'Continue',
            'alert': 'You must accept the terms and confirm your age to continue.'
        },
        'ru': {
            'title': 'Важная информация',
            'disclaimer': 'Отказ от ответственности',
            'disclaimer_text': 'Этот сайт предоставляет общую информацию только для ознакомления. Эта информация не заменяет профессиональную медицинскую консультацию.',
            'self_medication': 'Самолечение может быть опасным',
            'self_medication_text': 'Строго соблюдайте рекомендованные дозы и не продлевайте лечение без медицинской консультации.',
            'consult': 'Проконсультируйтесь с врачом',
            'consult_text': 'Если симптомы сохраняются более 3 дней или ухудшаются.',
            'terms_checkbox': 'Я принимаю условия использования',
            'age_checkbox': 'Я подтверждаю, что мне 18 лет или больше',
            'continue_button': 'Продолжить',
            'alert': 'Вы должны принять условия и подтвердить свой возраст, чтобы продолжить.'
        }
    }

    lang = st.session_state.language
    
    # Utilisation d'une seule colonne pour un meilleur contrôle de la largeur
    col1, col2, col3 = st.columns([1, 3, 1])
    with col2:
        with st.container():
            st.markdown(f"""
                <div class="modal-container">
                    <div class="modal">
                        <h4>⚠️ {modal_content[lang]['title']}</h4>
                        <ul>
                            <li>
                                <strong>{modal_content[lang]['disclaimer']}</strong>
                                {modal_content[lang]['disclaimer_text']}
                            </li>
                            <li>
                                <strong>{modal_content[lang]['self_medication']}</strong>
                                {modal_content[lang]['self_medication_text']}
                            </li>
                            <li>
                                <strong>{modal_content[lang]['consult']}</strong>
                                {modal_content[lang]['consult_text']}
                            </li>
                        </ul>
                    </div>
                </div>
            """, unsafe_allow_html=True)
            
            # Ajout d'une marge avant les cases à cocher
            st.markdown("<div style='margin-top: 1rem;'></div>", unsafe_allow_html=True)
            
            terms = st.checkbox(modal_content[lang]['terms_checkbox'])
            age = st.checkbox(modal_content[lang]['age_checkbox'])
            
            if st.button(modal_content[lang]['continue_button'], disabled=not (terms and age)):
                st.session_state.terms_accepted = True
                st.rerun()
    
    st.stop()

# Sélection de la langue dans la barre latérale
with st.sidebar:
    st.markdown("<h3>🌍 Langue / Language / Язык</h3>", unsafe_allow_html=True)
    language_options = {
        'Français': 'fr',
        'English': 'en',
        'Русский': 'ru'
    }
    selected_language = st.selectbox(
        "",
        options=list(language_options.keys()),
        index=list(language_options.values()).index(st.session_state.language)
    )
    st.session_state.language = language_options[selected_language]

# Titres selon la langue
titles = {
    'fr': 'COMMENT VOUS SENTEZ-VOUS AUJOURD\'HUI?',
    'en': 'HOW ARE YOU FEELING TODAY?',
    'ru': 'КАК ВЫ СЕБЯ ЧУВСТВУЕТЕ СЕГОДНЯ?'
}

st.markdown(
    f"<h1 class='title'>{titles[st.session_state.language]}</h1>",
    unsafe_allow_html=True
)

# Chatbot principal
with st.container():
    bot = MedicalChatbot(language=st.session_state.language)
    bot.display()

# Section des articles
article_titles = {
    'fr': 'Articles Recommandés',
    'en': 'Recommended Articles',
    'ru': 'Рекомендуемые статьи'
}

st.markdown(
    f"<h3 class='articles-title'>{article_titles[st.session_state.language]}</h3>",
    unsafe_allow_html=True
)

current_time = datetime.now()
should_update = (
    st.session_state.last_articles_update is None or
    current_time - st.session_state.last_articles_update > timedelta(hours=12)
)

if should_update and not st.session_state.is_loading_articles:
    st.session_state.is_loading_articles = True
    loading_messages = {
        'fr': "Chargement des articles...",
        'en': "Loading articles...",
        'ru': "Загрузка статей..."
    }
    with st.spinner(loading_messages[st.session_state.language]):
        article_search = ArticleSearch()
        try:
            articles = asyncio.run(load_articles_async(article_search, st.session_state.language))
            st.session_state.cached_articles = articles
            st.session_state.last_articles_update = current_time
        except Exception as e:
            st.error(f"Error loading articles: {str(e)}")
            articles = st.session_state.cached_articles or []
        finally:
            st.session_state.is_loading_articles = False
else:
    articles = st.session_state.cached_articles or []

if articles:
    st.markdown("<div class='article-container'>", unsafe_allow_html=True)
    cols = st.columns(min(len(articles), 5))
    for i, col in enumerate(cols):
        with col:
            article = articles[i]
            st.markdown(f"""
                <a href="{article['url']}" target="_blank" class="article-link">
                    <div class='article-card'>
                        <h4>{article['title'][:90] + '...' if len(article['title']) > 90 else article['title']}</h4>
                        <img loading="lazy" 
                             src="{article.get('photo', 'https://via.placeholder.com/400x300')}" 
                             alt="{article['title']}"
                             width="400" 
                             height="300">
                    </div>
                </a>
            """, unsafe_allow_html=True)
    st.markdown("</div>", unsafe_allow_html=True)
else:
    error_messages = {
        'fr': "Impossible de charger les articles. Veuillez réessayer plus tard.",
        'en': "Unable to load articles. Please try again later.",
        'ru': "Не удалось загрузить статьи. Пожалуйста, попробуйте позже."
    }
    st.warning(error_messages[st.session_state.language])

# Barre de recherche dans la barre latérale
with st.sidebar:
    search_placeholders = {
        'fr': "Rechercher des articles...",
        'en': "Search articles...",
        'ru': "Поиск статей..."
    }
    search_query = st.text_input(
        "",
        placeholder=search_placeholders[st.session_state.language]
    )
    
    if search_query:
        article_search = ArticleSearch()
        search_results = article_search.search_articles(
            search_query,
            st.session_state.language
        )
        
        if search_results:
            search_titles = {
                'fr': "Résultats de recherche",
                'en': "Search Results",
                'ru': "Результаты поиска"
            }
            st.markdown(f"### {search_titles[st.session_state.language]}")
            
            for result in search_results:
                st.markdown(f"""
                    <div class='search-result'>
                        <h4>
                            <a href="{result['url']}" target="_blank">
                                {result['title'][:90] + '...' if len(result['title']) > 90 else result['title']}
                            </a>
                        </h4>
                    </div>
                """, unsafe_allow_html=True)
        else:
            no_results_messages = {
                'fr': "Aucun résultat trouvé",
                'en': "No results found",
                'ru': "Результаты не найдены"
            }
            st.info(no_results_messages[st.session_state.language])


# Informations supplémentaires dans la barre latérale
with st.sidebar:
    st.markdown("---")
    st.markdown("### ℹ️ Information")
    
    info_text = {
        'fr': """
            **LIBERCARE** est un assistant médical virtuel qui vous aide à:
            - Trouver des médicaments appropriés
            - Découvrir des remèdes naturels
            - Obtenir des informations sur la santé
            
            ⚠️ *Consultez toujours un professionnel de santé pour un avis médical.*
        """,
        'en': """
            **LIBERCARE** is a virtual medical assistant that helps you:
            - Find appropriate medications
            - Discover natural remedies
            - Get health information
            
            ⚠️ *Always consult a healthcare professional for medical advice.*
        """,
        'ru': """
            **LIBERCARE** - это виртуальный медицинский ассистент, который поможет вам:
            - Найти подходящие лекарства
            - Узнать о природных средствах
            - Получить информацию о здоровье
            
            ⚠️ *Всегда консультируйтесь с врачом для получения медицинской консультации.*
        """
    }
    
    st.markdown(info_text[st.session_state.language])
    st.markdown("""<a href="https://www.doctolib.fr" target="_blank">👨‍⚕️ Prenez rendez-vous avec un professionnel de santé sur Doctolib.fr </a>""", unsafe_allow_html=True)