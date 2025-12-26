# Fichier: modules/expoter.py
from fpdf import FPDF

class EmirPDF(FPDF):
    def header(self):
        # --- BANDEAU SUPERIEUR (Bleu Nuit) ---
        self.set_fill_color(14, 17, 23)
        self.rect(0, 0, 210, 40, 'F')
        
        # --- LOGO & TITRE (Or Métallique) ---
        self.set_y(10)
        self.set_font('Arial', 'B', 24)
        self.set_text_color(212, 175, 55)
        self.cell(0, 10, 'EMIR', 0, 1, 'C')
        
        self.set_font('Arial', '', 10)
        self.set_text_color(255, 255, 255)
        self.cell(0, 5, 'ENTERPRISE MANAGEMENT & INTELLIGENCE RESOURCE', 0, 1, 'C')
        
        # --- SOUS-TITRE ---
        self.ln(5)
        self.set_font('Arial', 'I', 9)
        self.set_text_color(200, 200, 200)
        self.cell(0, 5, 'Rapport d\'Audit Genere par IA', 0, 1, 'C')
        
        self.ln(20) # Marge après le bandeau pour ne pas coller au texte

    def footer(self):
        self.set_y(-15)
        self.set_draw_color(212, 175, 55)
        self.line(10, 282, 200, 282)
        self.set_font('Arial', 'I', 8)
        self.set_text_color(128, 128, 128)
        self.cell(0, 10, f'EMIR Financial Suite - Confidential - Page {self.page_no()}', 0, 0, 'C')

    def clean_text(self, text):
        if not isinstance(text, str):
            text = str(text)
        text = text.replace('€', ' EUR').replace('’', "'").replace('…', '...')
        for char in ['*', '#', '_', '`']:
            text = text.replace(char, '')
        return text.encode('latin-1', 'ignore').decode('latin-1').strip()

    def titre_section(self, label):
        self.ln(5)
        self.set_font("Arial", 'B', 14)
        self.set_text_color(14, 17, 23)
        self.cell(0, 8, label, 0, 1, 'L')
        self.set_draw_color(212, 175, 55)
        self.set_line_width(0.5)
        self.line(self.get_x(), self.get_y(), self.get_x() + 190, self.get_y())
        self.ln(5)

    def write_ai_content(self, raw_text):
        lines = raw_text.split('\n')
        for line in lines:
            clean_line = self.clean_text(line)
            if not clean_line: continue

            if line.strip().startswith('#'):
                # Vérifier s'il reste de la place, sinon nouvelle page
                if self.get_y() > 250: self.add_page()
                self.titre_section(clean_line)
            
            elif line.strip().startswith('-'):
                self.set_font("Arial", '', 11)
                self.set_text_color(50, 50, 50)
                self.cell(5) 
                self.set_text_color(212, 175, 55)
                self.cell(5, 6, chr(149), 0, 0)
                self.set_text_color(50, 50, 50)
                self.multi_cell(0, 6, clean_line.replace('-', '').strip())
            
            else:
                self.set_font("Arial", '', 11)
                self.set_text_color(50, 50, 50)
                self.multi_cell(0, 6, clean_line)
            self.ln(1)

def create_pdf(df_anomalies, tendance, texte_ia):
    pdf = EmirPDF()
    pdf.add_page()
    pdf.set_auto_page_break(auto=False) # On gère nous-mêmes les sauts de page pour le tableau

    # 1. Le Contenu Textuel (IA)
    pdf.write_ai_content(texte_ia)
    pdf.ln(10)
    
    # 2. Le Tableau "Audit Style"
    
    # FONCTION INTERNE : DESSINER LES EN-TÊTES
    def draw_table_header():
        pdf.set_font("Arial", 'B', 10)
        pdf.set_fill_color(14, 17, 23) # Bleu Nuit
        pdf.set_text_color(212, 175, 55) # Or
        pdf.cell(30, 10, "Date", 1, 0, 'C', 1)
        pdf.cell(90, 10, "Description", 1, 0, 'C', 1)
        pdf.cell(30, 10, "Montant", 1, 0, 'C', 1)
        pdf.cell(40, 10, "Categorie", 1, 1, 'C', 1)
        # Réinitialisation pour les données
        pdf.set_font("Arial", '', 9)
        pdf.set_text_color(0, 0, 0)

    # Vérification : Reste-t-il assez de place pour commencer le tableau ?
    # Si on est trop bas (> 220mm), on passe direct à la page suivante
    if pdf.get_y() > 220:
        pdf.add_page()

    pdf.titre_section("Tableau des Anomalies Detectees")
    draw_table_header()
    
    # Données du tableau
    top_suspects = df_anomalies.head(20) # On peut en mettre un peu plus maintenant
    fill = False
    
    for _, row in top_suspects.iterrows():
        # GESTION INTELLIGENTE DU SAUT DE PAGE
        # Si on arrive en bas de page (270mm), on saute et on remet les titres
        if pdf.get_y() > 270:
            pdf.add_page()
            draw_table_header() # ON RÉPÈTE LES TITRES !
            
        try:
            if fill:
                pdf.set_fill_color(245, 245, 245)
            else:
                pdf.set_fill_color(255, 255, 255)
            
            date = str(row['Date'])[:10]
            desc = pdf.clean_text(str(row['Description'])[:45])
            montant = str(round(row['Montant'], 2))
            cat = pdf.clean_text(str(row['Categorie'])[:20])
            
            pdf.cell(30, 8, date, 'LR', 0, 'C', fill)
            pdf.cell(90, 8, desc, 'LR', 0, 'L', fill)
            pdf.cell(30, 8, montant, 'LR', 0, 'R', fill)
            pdf.cell(40, 8, cat, 'LR', 1, 'C', fill)
            
            fill = not fill
        except:
            continue
            
    pdf.cell(190, 0, '', 'T') # Ligne de fin

    return pdf.output(dest='S').encode('latin-1', 'ignore')