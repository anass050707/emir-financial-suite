# Fichier: modules/narrator.py

def generer_rapport(df, suspects, tendance, score=None, verdict=None):
    nb_ops = len(df)
    nb_suspects = len(suspects)
    montant_max_anomalie = suspects['Montant'].max() if not suspects.empty else 0
    date_critique = suspects.loc[suspects['Montant'].idxmax(), 'Date'] if not suspects.empty else "N/A"
    
    # Logique de texte dynamique
    phrase_tendance = ""
    if tendance > 0:
        phrase_tendance = f"Votre tresorerie est sur une dynamique positive (+{tendance:.2f} EUR/jour)."
        conseil = "C'est le moment ideal pour investir ou placer votre excedent."
    else:
        phrase_tendance = f"ATTENTION : Votre tresorerie baisse de {abs(tendance):.2f} EUR/jour."
        conseil = "Il faut reduire les depenses immediatement pour eviter le deficit."

    # Gestion du score (si fourni)
    bloc_verdict = ""
    if score is not None:
        bloc_verdict = f"""
## VERDICT FINAL : {verdict}
*Score de Sante Financiere : {score}/100*

D'apres l'analyse algorithmique, cette entreprise est consideree comme : *{verdict}*.
Ce score prend en compte la croissance de la tresorerie, la stabilite des depenses et le nombre d'anomalies detectees.
"""

    rapport = f"""
# RAPPORT D'AUDIT FINANCIER

## 1. Bilan de Sante
{bloc_verdict}

## 2. Analyse de la Tendance
{phrase_tendance}
> *Conseil IA :* {conseil}

## 3. Risques et Anomalies ({nb_suspects} alertes)
L'IA a identifie *{nb_suspects} transactions* qui ne correspondent pas a vos standards habituels.
L'anomalie la plus critique est une operation de *{montant_max_anomalie:.2f} EUR* datee du {str(date_critique)[:10]}.

*Action requise :* Verifiez les justificatifs de ces operations immediatement.
"""
    return rapport