"""Interface Streamlit — CourseGraph."""

from __future__ import annotations

import streamlit as st

# ---------------------------------------------------------------------------
# Configuration de la page
# ---------------------------------------------------------------------------
st.set_page_config(
    page_title="CourseGraph",
    page_icon="📚",
    layout="wide",
    initial_sidebar_state="expanded",
)

API_BASE = "http://localhost:8000"

# ---------------------------------------------------------------------------
# Sidebar — sélection du cours et upload
# ---------------------------------------------------------------------------
with st.sidebar:
    st.title("📚 CourseGraph")
    st.caption("Assistant de révision RAG")

    st.divider()

    # TODO: sélecteur de cours existants (GET /recurrence)
    course_name = st.text_input("Nom du cours", placeholder="ex: Algorithmes S3")

    st.subheader("Ajouter des documents")
    doc_type = st.selectbox("Type", ["cours", "annale", "correction"])
    uploaded_file = st.file_uploader("PDF", type=["pdf"])
    year = st.number_input("Année (annale)", min_value=2000, max_value=2030, value=2024, step=1)

    if st.button("📤 Ingérer", disabled=uploaded_file is None):
        # TODO: POST /ingest
        st.info("Ingestion en cours…")

# ---------------------------------------------------------------------------
# Navigation par onglets
# ---------------------------------------------------------------------------
tab_chat, tab_recurrence, tab_quiz, tab_gaps, tab_eval = st.tabs(
    ["💬 Chat", "📊 Récurrence", "🧪 Quiz", "🎯 Lacunes", "📈 Évaluation"]
)

# ---------------------------------------------------------------------------
# Onglet Chat
# ---------------------------------------------------------------------------
with tab_chat:
    st.header("Chat sourcé")

    if "messages" not in st.session_state:
        st.session_state.messages = []

    for msg in st.session_state.messages:
        with st.chat_message(msg["role"]):
            st.markdown(msg["content"])

    if question := st.chat_input("Pose ta question sur le cours…"):
        st.session_state.messages.append({"role": "user", "content": question})
        with st.chat_message("user"):
            st.markdown(question)

        with st.chat_message("assistant"):
            # TODO: POST /ask (streaming SSE)
            st.warning("API non connectée — implémentation à venir.")

# ---------------------------------------------------------------------------
# Onglet Récurrence
# ---------------------------------------------------------------------------
with tab_recurrence:
    st.header("Tableau de récurrence des notions")
    st.caption("Frequence d'apparition dans les annales * poids de recence")

    if st.button("🔄 Calculer", key="recurrence_btn"):
        # TODO: GET /recurrence/{course_name}
        st.info("Calcul en cours…")

    # TODO: afficher un DataFrame trié par recurrence_score

# ---------------------------------------------------------------------------
# Onglet Quiz
# ---------------------------------------------------------------------------
with tab_quiz:
    st.header("QCM auto-généré")

    col1, col2 = st.columns([3, 1])
    with col1:
        chapter = st.selectbox("Chapitre", ["Tous"], key="quiz_chapter")
    with col2:
        n_q = st.number_input("Nb questions", min_value=3, max_value=20, value=5)

    if st.button("🎲 Générer le quiz", key="gen_quiz"):
        # TODO: POST /quiz/generate
        st.info("Génération en cours…")

    # TODO: afficher les questions et collecter les réponses
    # TODO: POST /quiz/submit et afficher le score

# ---------------------------------------------------------------------------
# Onglet Lacunes
# ---------------------------------------------------------------------------
with tab_gaps:
    st.header("Radar de maîtrise & Plan de révision")

    if st.button("📊 Calculer mes lacunes", key="gaps_btn"):
        # TODO: GET /gaps/{course_name}
        st.info("Calcul en cours…")

    # TODO: radar chart (st.plotly_chart) par chapitre
    # TODO: tableau plan de révision priorisé

# ---------------------------------------------------------------------------
# Onglet Évaluation
# ---------------------------------------------------------------------------
with tab_eval:
    st.header("Métriques du système")
    st.caption("Résultats de la dernière évaluation RAGAS sur le goldset.")

    # TODO: lire eval/results/latest.json et afficher les métriques
    st.info("Lancez `make eval` pour générer les métriques.")
