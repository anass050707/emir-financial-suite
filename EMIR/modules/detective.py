# Fichier: modules/detective.py
import pandas as pd
from sklearn.ensemble import IsolationForest

def detect_anomalies(df):
    data_to_analyze = df[['Montant']].fillna(0)
    
    # --- CHANGEMENT ICI ---
    # Avant : contamination=0.05 (5% -> 500 alertes sur 10k)
    # Après : contamination=0.001 (0.1% -> 10 alertes sur 10k)
    # On ne veut que le "haut du panier" des problèmes.
    model = IsolationForest(contamination=0.001, random_state=42)
    # ----------------------
    
    df['anomaly_score'] = model.fit_predict(data_to_analyze)
    
    # On récupère les suspects
    suspects = df[df['anomaly_score'] == -1].copy()
    
    # TRI INTELLIGENT : On trie pour afficher les plus gros montants en premier
    # Comme ça, le virement aux Caïmans (15 000) sera tout en haut
    suspects = suspects.sort_values('Montant', ascending=False)
    
    suspects['Statut'] = '🚨 ANOMALIE DÉTECTÉE'
    
    return suspects