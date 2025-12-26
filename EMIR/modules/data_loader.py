# Fichier: modules/data_loader.py
import pandas as pd
import numpy as np

def load_data(uploaded_file):
    """
    Charge un fichier CSV ou Excel et nettoie les données de base.
    """
    if uploaded_file.name.endswith('.csv'):
        df = pd.read_csv(uploaded_file)
    else:
        df = pd.read_excel(uploaded_file)
    
    # On s'assure qu'il y a une date (convertir en datetime)
    # On suppose que la colonne s'appelle 'Date' ou 'Date_Operation'
    cols = df.columns.str.lower()
    if 'date' in cols:
        df['Date'] = pd.to_datetime(df['Date'])
    
    return df

def generer_donnees_demo():
    """
    Génère des fausses données comptables pour tester l'application.
    """
    # On crée 100 jours de transactions
    dates = pd.date_range(start="2024-01-01", periods=100)
    
    # Des montants normaux autour de 100€ + quelques aléas
    montants = np.random.normal(100, 20, 100)
    
    # On crée le DataFrame
    df = pd.DataFrame({
        'Date': dates,
        'Description': ['Achat Divers'] * 100,
        'Montant': montants,
        'Categorie': ['Opération Courante'] * 100
    })
    
    # On injecte artificiellement 3 Anomalies (Fraudes ?)
    anomalies = pd.DataFrame({
        'Date': [pd.Timestamp('2024-02-15'), pd.Timestamp('2024-03-10'), pd.Timestamp('2024-04-05')],
        'Description': ['VIRMENT SUSPECT', 'ERREUR SYSTEME', 'RETRAIT INCONNU'],
        'Montant': [5000.0, 12000.0, -500.0], # Des montants énormes ou bizarres
        'Categorie': ['ALERTE'] * 3
    })
    
    # On fusionne le tout
    df_final = pd.concat([df, anomalies], ignore_index=True)
    
    # On trie par date
    return df_final.sort_values('Date')