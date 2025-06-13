# Importation des bibliothèques nécessaires
import nltk  # NLTK : Traitement du langage naturel
import os
import streamlit as st  # Streamlit : Interface web
import string  # Pour gérer la ponctuation


from nltk.tokenize import word_tokenize, sent_tokenize  # Tokenisation en mots et phrases
from nltk.corpus import stopwords  # Stopwords = mots fréquents inutiles pour l'analyse
from nltk.stem import WordNetLemmatizer  # Pour réduire les mots à leur forme de base (lemmatisation)

# Définir le chemin du dossier nltk_data local
nltk_data_dir = os.path.join(os.getcwd(), 'nltk_data')
nltk.data.path.append(nltk_data_dir)

# Télécharger les ressources dans ce dossier
nltk.download('punkt', download_dir=nltk_data_dir)
nltk.download('punkt_tab', download_dir=nltk_data_dir)
nltk.download('averaged_perceptron_tagger', download_dir=nltk_data_dir)
nltk.download('stopwords', download_dir=nltk_data_dir)
nltk.download('wordnet', download_dir=nltk_data_dir)
nltk.download('omw-1.4', download_dir=nltk_data_dir)


# Chargement du texte de l'entreprise
with open('pub_entreprise.txt', 'r', encoding='utf-8') as f:
    data = f.read().replace('\n', ' ')

# Découpe du texte en phrases
sentences = sent_tokenize(data)


# Fonction de nettoyage et préparation du texte
def preprocess(sentence):
    words = word_tokenize(sentence, language='french')  # Découpe en mots
    stop_words = stopwords.words('french')  # Liste des mots inutiles à ignorer

    # Minuscule, suppression stopwords et ponctuation
    words = [word.lower() for word in words if word.lower() not in stop_words and word not in string.punctuation]

    lemmatizer = WordNetLemmatizer()
    words = [lemmatizer.lemmatize(word) for word in words]  # Lemmatisation
    return words


# Prétraitement de tout le corpus
corpus = [preprocess(sentence) for sentence in sentences]


# Fonction de recherche de la phrase la plus pertinente
def get_most_relevant_sentence(query):
    query = preprocess(query)
    max_similarity = 0
    most_relevant_sentence = ""

    for i, sentence in enumerate(corpus):
        similarity = len(set(query).intersection(sentence)) / float(len(set(query).union(sentence)))

        if similarity > max_similarity:
            max_similarity = similarity
            most_relevant_sentence = sentences[i]  # Phrase d'origine non prétraitée
    return most_relevant_sentence


# Interface utilisateur Streamlit
st.title(" Chatbot de Jub Jubal Junbati")

st.subheader("Posez une question sur notre entreprise ")
question = st.text_input("Votre question ici :")

if question:
    response = get_most_relevant_sentence(question)

    if response:
        st.success(" Réponse : " + response)
    else:
        st.warning("Désolé, je n'ai pas compris votre question. Pouvez-vous reformuler ?")

