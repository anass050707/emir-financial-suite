import streamlit as st
import pandas as pd
import time

# --- IMPORTATION DES MODULES ---
from modules.data_loader import load_data, generer_donnees_demo
from modules.detective import detect_anomalies
from modules.oracle import predict_future, calculer_score_sante
from modules.narrator import generer_rapport
from modules.expoter import create_pdf
from modules.assistant import ask_financial_brain

# --- CONFIGURATION DE LA PAGE ---
st.set_page_config(
    page_title="EMIR Financial Suite", 
    page_icon="🦅", 
    layout="wide",
    initial_sidebar_state="expanded"
)

# --- STYLE CSS "LINUX LUXE" ---
# C'est ici qu'on change le look pour faire "Hacker Chic / Banque Privée"
st.markdown("""
    <style>
    /* Import d'une police style "Code/Terminal" moderne */
    @import url('https://fonts.googleapis.com/css2?family=JetBrains+Mono:wght@400;700&display=swap');

    /* Application de la police partout */
    html, body, [class*="css"] {
        font-family: 'JetBrains Mono', monospace;
    }

    /* Titres en Or */
    h1, h2, h3 {
        color: #D4AF37 !important;
        font-weight: 700;
        letter-spacing: -1px;
    }

    /* Champs de saisie style "Terminal" */
    .stTextInput input {
        background-color: #0E1117 !important;
        color: #00FF00 !important; /* Texte vert matrix pour la saisie */
        border: 1px solid #333 !important;
        border-radius: 5px;
    }
    .stTextInput input:focus {
        border-color: #D4AF37 !important; /* Bordure Or quand on clique */
        box-shadow: 0 0 10px #D4AF3750;
    }

    /* Boutons personnalisés */
    .stButton button {
        background-color: #1E1E1E !important;
        color: #D4AF37 !important;
        border: 1px solid #D4AF37 !important;
        border-radius: 5px;
        transition: all 0.3s ease;
    }
    .stButton button:hover {
        background-color: #D4AF37 !important;
        color: #000 !important;
        box-shadow: 0 0 15px #D4AF37;
    }

    /* Alertes et Messages plus discrets/pros */
    .stAlert {
        background-color: #1E1E1E;
        border-left: 5px solid #D4AF37;
        color: #EEE;
    }
    </style>
""", unsafe_allow_html=True)
# ... (tes imports) ...

# Initialisation de l'état de session
if 'logged_in' not in st.session_state:
    st.session_state['logged_in'] = False



    # --- LE CODE DE L'APPLICATION COMMENCE ICI ---
    # (J'ai repris ton code exact et je l'ai mis dans ce bloc "else")

    st.title("🦅 EMIR : Financial Intelligence Unit")

    # --- 1. BARRE LATÉRALE ---
    st.sidebar.header("📡 DATA FEED")
    option = st.sidebar.radio("Input Source :", ["Mode Démo (Simulation)", "Upload File"])

    df = None

    if option == "Mode Démo (Simulation)":
        df = generer_donnees_demo()
        st.sidebar.success("✅ Simulation Loaded")
    elif option == "Upload File":
        uploaded_file = st.sidebar.file_uploader("Select CSV/XLSX", type=['csv', 'xlsx'])
        if uploaded_file:
            df = load_data(uploaded_file)
            st.sidebar.success("✅ Data Stream Connected")

    # --- 2. DASHBOARD PRINCIPAL ---
    if df is not None:
        # A. GRAPHIQUE
        st.subheader("📈 Cash Flow Overview")
        st.line_chart(df.set_index('Date')['Montant'])
        
        st.divider()

        # B. LE DÉTECTIVE
        st.subheader("🕵️‍♂️ Risk Detection Protocol")
        
        if st.button("RUN ANOMALY SCAN"):
            with st.spinner("Scanning transactions..."):
                suspects = detect_anomalies(df)
                st.session_state['suspects'] = suspects
                st.session_state['ia_done'] = True

        if st.session_state.get('ia_done'):
            suspects = st.session_state['suspects']
            if not suspects.empty:
                st.error(f"⚠️ {len(suspects)} THREATS DETECTED")
                st.dataframe(suspects[['Date', 'Description', 'Montant', 'Categorie']])
            else:
                st.success("✅ SYSTEM SECURE. No anomalies.")

        st.divider()

        # C. L'ORACLE & SCORE
        st.subheader("🔮 Predictive Analytics & Verdict")
        
        if st.button("EXECUTE FULL AUDIT"):
            with st.spinner("Calculating Score..."):
                df_future, tendance = predict_future(df)
                if 'suspects' not in st.session_state:
                    suspects = detect_anomalies(df)
                else:
                    suspects = st.session_state['suspects']

                score, verdict, couleur = calculer_score_sante(df, tendance, len(suspects))
                
                st.session_state['tendance'] = tendance
                st.session_state['df_future'] = df_future
                st.session_state['score'] = score
                st.session_state['verdict'] = verdict
                st.session_state['couleur_score'] = couleur
                st.session_state['oracle_done'] = True

        if st.session_state.get('oracle_done'):
            score = st.session_state['score']
            verdict = st.session_state['verdict']
            couleur = st.session_state['couleur_score']
            
            # Affichage Score stylisé
            st.markdown(f"""
            <div style="padding: 20px; border-radius: 5px; border: 1px solid {couleur}; background-color: #0E1117; text-align: center; margin-bottom: 20px;">
                <h3 style="color: {couleur}; margin:0; font-family: 'JetBrains Mono';">{verdict}</h3>
                <h1 style="font-size: 60px; margin:0; font-family: 'JetBrains Mono'; color: #FFF;">{score}<span style="font-size:20px">/100</span></h1>
                <p style="color: #888;">FINANCIAL HEALTH SCORE</p>
            </div>
            """, unsafe_allow_html=True)

            st.line_chart(st.session_state['df_future'].set_index('Date')['Prevision_Tresorerie'])

        st.divider()

        # D. CHATBOT EMIR
        st.subheader("💬 EMIR Assistant Interface")
        
        col_chat1, col_chat2 = st.columns([3, 1])
        with col_chat1:
            question_user = st.text_input("Command Line Input (ex: 'Total Salaires')", key="chat_input", placeholder="Enter query...")
        with col_chat2:
            st.write("") 
            st.write("") 
            bouton_ask = st.button("SEND QUERY ↵")

        if bouton_ask and question_user:
            with st.spinner("Processing..."):
                try:
                    reponse_ia = ask_financial_brain(df, question_user)
                    st.info(f"> {reponse_ia}")
                except Exception as e:
                    st.error(f"Syntax Error: {e}")

        st.divider()

        # E. EXPORT
        st.header("📝 Official Reporting")
        st.info("ℹ️ Compile analysis into secure PDF format.")

        if "pdf_pret" not in st.session_state:
            st.session_state.pdf_pret = None

        col_gauche, col_centre, col_droite = st.columns([1, 2, 1])

        with col_centre:
            if st.button("🧠 GENERATE EMIR REPORT", use_container_width=True):
                with st.spinner("Compiling Report..."):
                    try:
                        if 'suspects' not in st.session_state: suspects = detect_anomalies(df)
                        else: suspects = st.session_state['suspects']
                        
                        if 'tendance' not in st.session_state: _, tendance = predict_future(df)
                        else: tendance = st.session_state['tendance']
                            
                        score, verdict, _ = calculer_score_sante(df, tendance, len(suspects))
                        texte_complet = generer_rapport(df, suspects, tendance, score, verdict)
                        pdf_data = create_pdf(suspects, tendance, texte_complet)
                        
                        st.session_state.pdf_pret = pdf_data
                        st.success("✅ Report Generated Successfully.")
                        
                    except Exception as e:
                        st.error(f"System Error: {e}")

            if st.session_state.pdf_pret is not None:
                st.write("")
                st.download_button(
                    label="⬇️ DOWNLOAD ENCRYPTED PDF",
                    data=st.session_state.pdf_pret,
                    file_name="EMIR_Confidential_Report.pdf",
                    mime="application/pdf",
                    use_container_width=True,
                    type="primary"
                )
