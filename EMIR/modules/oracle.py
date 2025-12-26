# Fichier: modules/oracle.py
import pandas as pd
import numpy as np
from sklearn.linear_model import LinearRegression

def predict_future(df, jours_futurs=30):
    # Préparation des données (comme avant)
    df = df.copy()
    df['Date'] = pd.to_datetime(df['Date'])
    df = df.sort_values('Date')
    df['Jour_Index'] = (df['Date'] - df['Date'].min()).dt.days
    
    X = df[['Jour_Index']]
    y = df['Cumul_Tresorerie'] = df['Montant'].cumsum()
    
    model = LinearRegression()
    model.fit(X, y)
    
    dernier_jour = df['Jour_Index'].max()
    jours_futurs_index = np.array([[dernier_jour + i] for i in range(1, jours_futurs + 1)])
    predictions = model.predict(jours_futurs_index)
    
    tendance_par_jour = model.coef_[0]
    
    dates_futures = [df['Date'].max() + pd.Timedelta(days=i) for i in range(1, jours_futurs + 1)]
    df_future = pd.DataFrame({'Date': dates_futures, 'Prevision_Tresorerie': predictions})
    
    return df_future, tendance_par_jour

def calculer_score_sante(df, tendance, nb_anomalies):
    """
    Calcule une note sur 100 pour dire si l'entreprise va gagner ou perdre.
    """
    score = 50 # On commence à la moyenne
    
    # 1. CRITÈRE CROISSANCE (Le plus important)
    if tendance > 0:
        score += 30 # Ça monte, c'est bon signe
    elif tendance < 0:
        score -= 30 # Ça descend, danger
        
    # 2. CRITÈRE RISQUE (Anomalies)
    # Moins il y a d'anomalies, mieux c'est
    if nb_anomalies == 0:
        score += 10
    elif nb_anomalies > 5:
        score -= 15
    elif nb_anomalies > 10:
        score -= 25
        
    # 3. CRITÈRE VOLATILITÉ (Stabilité)
    # On regarde si les montants varient trop violemment
    std_dev = df['Montant'].std()
    mean_val = df['Montant'].mean()
    
    # Si l'écart type est énorme par rapport à la moyenne, c'est instable
    if abs(mean_val) > 0 and (std_dev / abs(mean_val)) > 2:
        score -= 10 # Trop instable
    else:
        score += 10 # Gestion saine
        
    # On borne le score entre 0 et 100
    score = max(0, min(100, score))
    
    # LE VERDICT
    if score >= 75:
        verdict = "EXCELLENT (Entreprise Gagnante 🚀)"
        couleur = "green"
    elif score >= 50:
        verdict = "MOYEN (Attention Requise ⚠️)"
        couleur = "orange"
    else:
        verdict = "CRITIQUE (Risque de Faillite ☠️)"
        couleur = "red"
        
    return score, verdict, couleur