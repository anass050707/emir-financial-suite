# Fichier: modules/assistant.py
import pandas as pd

def ask_financial_brain(df, question):
    """
    Un mini-cerveau qui analyse ta question et interroge les données.
    """
    question = question.lower()
    reponse = "🤖 Je n'ai pas compris. Essaie : 'Total Salaires' ou 'Moyenne Services'."
    
    # 1. On nettoie les données pour éviter les bugs
    # On s'assure que les dates sont bien des dates
    if 'Date' in df.columns:
        df['Date'] = pd.to_datetime(df['Date'])
    
    # 2. On détecte les Mots-Clés (L'intention)
    mot_cles_total = ['total', 'somme', 'montant', 'combien', 'dépensé']
    mot_cles_moyenne = ['moyenne', 'moyen']
    mot_cles_max = ['max', 'maximum', 'plus gros', 'record']
    mot_cles_nombre = ['nombre', 'combien de', 'transactions', 'opérations']
    
    # 3. On détecte la CATÉGORIE concernée
    # On regarde toutes les catégories qui existent dans ton fichier
    categories_existantes = df['Categorie'].unique()
    categorie_trouvee = None
    
    for cat in categories_existantes:
        # Si le nom de la catégorie (ex: "Salaires") est dans la question
        if str(cat).lower() in question:
            categorie_trouvee = cat
            break
    
    # --- LOGIQUE DE RÉPONSE ---
    
    # Si on a trouvé une catégorie, on filtre d'abord
    df_filtered = df
    nom_filtre = "toutes les opérations"
    
    if categorie_trouvee:
        df_filtered = df[df['Categorie'] == categorie_trouvee]
        nom_filtre = f"la catégorie '{categorie_trouvee}'"

    # CAS A : On demande un TOTAL (Somme)
    if any(mot in question for mot in mot_cles_total):
        total = df_filtered['Montant'].sum()
        reponse = f"💰 Le montant total pour {nom_filtre} est de *{total:,.2f} €*."

    # CAS B : On demande une MOYENNE
    elif any(mot in question for mot in mot_cles_moyenne):
        moyenne = df_filtered['Montant'].mean()
        reponse = f"📊 La moyenne des dépenses pour {nom_filtre} est de *{moyenne:,.2f} €*."

    # CAS C : On demande le MAXIMUM
    elif any(mot in question for mot in mot_cles_max):
        max_val = df_filtered['Montant'].max()
        reponse = f"📈 Le record (maximum) pour {nom_filtre} est de *{max_val:,.2f} €*."
        
    # CAS D : On demande le NOMBRE d'opérations
    elif any(mot in question for mot in mot_cles_nombre):
        count = len(df_filtered)
        reponse = f"🔢 Il y a eu *{count} opérations* enregistrées pour {nom_filtre}."

    return reponse