import streamlit as st
from openai import OpenAI
import pandas as pd
from langchain.vectorstores import Chroma
from langchain.embeddings import OpenAIEmbeddings
import os

# Fix for SQLite version issue
__import__('pysqlite3')
import sys
sys.modules['sqlite3'] = sys.modules.pop('pysqlite3')

class MedicalChatbot:
    def __init__(self, language='fr'):
        self.language = language
        MedicalChatbot.initialize_session_state()
        
        try:
            self.client = OpenAI(api_key=st.secrets["OpenAI_key"])
            self.embeddings = OpenAIEmbeddings(openai_api_key=st.secrets["OpenAI_key"])
            self.medications = pd.read_csv("medicaments_propre.csv")
            self.vectorstore = self._create_or_load_vectorstore()
        except Exception as e:
            st.error(f"Initialization error: {str(e)}")

    @staticmethod
    def initialize_session_state():
        if "messages" not in st.session_state:
            initial_messages = {
                'fr': "Bonjour! 👋 Je suis HealthBot. Comment puis-je vous aider?",
                'en': "Hello! 👋 I'm HealthBot. How can I help you?",
                'ru': "Здравствуйте! 👋 Я HealthBot. Как я могу вам помочь?"
            }
            st.session_state.messages = [
                {
                    "role": "system",
                    "content": "Tu es HealthBot, assistant médical professionnel 👨⚕️"
                },
                {
                    "role": "assistant",
                    "content": initial_messages['fr']
                }
            ]

    def _create_or_load_vectorstore(self):
        persist_directory = "./medical_db"
        if not os.path.exists(persist_directory):
            os.makedirs(persist_directory)
            
        try:
            vectorstore = Chroma(
                persist_directory=persist_directory,
                embedding_function=self.embeddings.embed_query
            )
            vectorstore.similarity_search("test", k=1)
            return vectorstore
        except Exception:
            documents = self._prepare_medical_documents()
            vectorstore = Chroma.from_texts(
                texts=[doc["content"] for doc in documents],
                metadatas=[doc["metadata"] for doc in documents],
                embedding=self.embeddings,
                persist_directory=persist_directory
            )
            vectorstore.persist()
            return vectorstore

    def _prepare_medical_documents(self):
        documents = []
        for _, med in self.medications.iterrows():
            try:
                content = f"Médicament: {med['titre']}\n"
                metadata = {
                    "name": med['titre'],
                    "category": med.get('categorie', ''),
                    "symptoms": med.get('symptomes', ''),
                    "posologie": med.get('posologie', ''),
                    "contre_indication": med.get('contre_indication', ''),
                    "grossesse_allaitement": med.get('grossesse_allaitement_fertilite', ''),
                    "effet_indesirable": med.get('effet_indesirable', '')
                }
                
                content += "\n".join([
                    f"Catégorie: {metadata['category']}",
                    f"Symptômes: {metadata['symptoms']}",
                    f"Posologie: {metadata['posologie']}",
                    f"Contre-indications: {metadata['contre_indication']}"
                ])
                
                documents.append({
                    "content": content,
                    "metadata": metadata
                })
            except Exception as e:
                st.warning(f"Erreur document: {med['titre']}: {str(e)}")
        return documents

    def get_response(self, user_input: str) -> str:
        try:
            embedding_response = self.embeddings.embed_query(user_input)
            
            similar_meds = self.vectorstore.similarity_search_by_vector(
                embedding_response,
                k=5
            )
            
            context = "Médicaments disponibles pour ces symptômes:\n"
            for med in similar_meds:
                context += f"\n---\n{med.page_content}\n"
            
            system_prompt = """Tu es HealthBot, un assistant médical professionnel 👨‍⚕️.
            
            Pour chaque demande, fournis:
            1. 💊 4-5 médicaments recommandés avec posologie, contre_indication, effet_indesirable. 
                IMPORTANT: Utilise EXACTEMENT les noms des médicaments (med['titre']) avec (substance_active), Posologie indiquée, Contre-indications importantes, Effets indésirables possibles de la base de données fournie dans le contexte. 
                NE PAS utiliser les noms génériques des substances actives.
                Pour chaque médicament, indique:
                - Le nom exact du médicament tel qu'il apparaît dans le contexte 
                - Posologie indiquée (de la base de données)
                - Contre-indications importantes
                - Effets indésirables possibles

             2. 🌿 4-5 remèdes naturels avec instructions
            
            Contexte des médicaments disponibles:
            {context}
            """
            
            messages = [
                {"role": "system", "content": system_prompt.format(context=context)},
                {"role": "user", "content": user_input}
            ]
            
            response = self.client.chat.completions.create(
                model="gpt-3.5-turbo",
                messages=messages,
                temperature=0.7,
                max_tokens=800
            )
            
            response_content = response.choices[0].message.content
            medications = []
            remedies = []
            precautions = []

            # Extraction des médicaments
            parts = response_content.split("💊")
            if len(parts) > 1:
                medications_part = parts[1].split("🌿")[0] if "🌿" in parts[1] else parts[1]
                medications = [med.strip() for med in medications_part.strip().split("\n") if med.strip()]
            
            # Extraction des remèdes naturels
            parts = response_content.split("🌿")
            if len(parts) > 1:
                remedies_part = parts[1].split("⚠️")[0] if "⚠️" in parts[1] else parts[1]
                remedies = [rem.strip() for rem in remedies_part.strip().split("\n") if rem.strip()]
            
            # Extraction des précautions
            parts = response_content.split("⚠️")
            if len(parts) > 1:
                precautions = [prec.strip() for prec in parts[1].strip().split("\n") if prec.strip()]

            # Construction de la réponse HTML
            html_response = """
            <div style="display: flex; flex-direction: column; gap: 20px;">
                <div style="display: flex; gap: 20px; flex-wrap: wrap;">
                    <div style="flex: 1; min-width: 300px; background-color: rgba(47, 53, 66, 0.8); padding: 15px; border-radius: 8px; color: white; margin-bottom: 10px;">
                        <h3 style="color: #2196f3;">💊 Médicaments recommandés</h3>
                        <ul style="list-style-type: none; padding-left: 0;">
            """
            
            for med in medications:
                if med.strip():
                    html_response += f'<li style="margin-bottom: 10px; padding-left: 20px; position: relative;">{med}</li>'
            
            html_response += """
                        </ul>
                    </div>
                    <div style="flex: 1; min-width: 300px; background-color: rgba(47, 53, 66, 0.8); padding: 15px; border-radius: 8px; color: white; margin-bottom: 10px;">
                        <h3 style="color: #4caf50;">🌿 Remèdes naturels</h3>
                        <ul style="list-style-type: none; padding-left: 0;">
            """
            
            for remedy in remedies:
                if remedy.strip():
                    html_response += f'<li style="margin-bottom: 10px; padding-left: 20px; position: relative;">{remedy}</li>'
            
            html_response += """
                        </ul>
                    </div>
                </div>
            """
            
            if precautions:
                html_response += """
                <div style="background-color: rgba(255, 152, 0, 0.2); padding: 15px; border-radius: 8px; color: white; margin-bottom: 10px;">
                    <h3 style="color: #ff9800;">⚠️ Précautions</h3>
                    <ul style="list-style-type: none; padding-left: 0;">
                """
                
                for precaution in precautions:
                    if precaution.strip():
                        html_response += f'<li style="margin-bottom: 10px; padding-left: 20px; position: relative;">{precaution}</li>'
                
                html_response += """
                    </ul>
                </div>
                """
            
            html_response += """
            </div>
            """
            
            return html_response

        except Exception as e:
            error_message = f"Désolé, une erreur s'est produite: {str(e)}"
            st.error(error_message)
            return "Je suis désolé, je ne peux pas répondre pour le moment. 😔"

    def display(self):
        try:
            with st.container():
                for message in st.session_state.messages:
                    if message["role"] != "system":
                        with st.chat_message(message["role"]):
                            st.markdown(message["content"], unsafe_allow_html=True)

                if prompt := st.chat_input("Décrivez vos symptômes..."):
                    st.session_state.messages.append({"role": "user", "content": prompt})
                    with st.chat_message("user"):
                        st.markdown(prompt)

                    with st.chat_message("assistant"):
                        with st.spinner("Analyse en cours..."):
                            response = self.get_response(prompt)
                            st.markdown(response, unsafe_allow_html=True)
                            st.session_state.messages.append({"role": "assistant", "content": response})
                        
        except Exception as e:
            st.error(f"Erreur d'affichage du chat: {str(e)}")

def main():
    st.set_page_config(
        page_title="Assistant Médical HealthBot",
        page_icon="👨‍⚕️",
        layout="wide"
    )
    
    st.title("Assistant Médical HealthBot 👨‍⚕️")
    
    chatbot = MedicalChatbot()
    chatbot.display()

if __name__ == "__main__":
    main()