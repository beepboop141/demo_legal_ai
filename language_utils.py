"""
Language detection and translation utilities
"""
from config import GREEK_DETECTION_THRESHOLD

def detect_language(text):
    """
    Detect if text is primarily Greek or English
    
    Args:
        text (str): Input text to analyze
        
    Returns:
        str: 'el' for Greek, 'en' for English
    """
    if not text:
        return "en"
    
    greek_chars = sum(1 for c in text if '\u0370' <= c <= '\u03FF' or '\u1F00' <= c <= '\u1FFF')
    total_chars = sum(1 for c in text if c.isalpha())
    
    if total_chars == 0:
        return "en"
    
    greek_ratio = greek_chars / total_chars
    return "el" if greek_ratio > GREEK_DETECTION_THRESHOLD else "en"


# Translation Maps
JURISDICTION_MAP = {
    "Greek": "Ελληνικό",
    "USA (Federal)": "Αμερικανικό (Ομοσπονδιακό)",
    "UK": "Βρετανικό",
    "European Union": "Ευρωπαϊκής Ένωσης",
}

SPECIALTY_MAP = {
    "Criminal Law": "Ποινικό Δίκαιο",
    "Commercial Law": "Εμπορικό Δίκαιο",
    "Contract Law": "Ενοχικό Δίκαιο",
    "Intellectual Property": "Πνευματική Ιδιοκτησία",
    "Employment Law": "Εργατικό Δίκαιο",
    "EU Law": "Δίκαιο της ΕΕ"
}

# UI Text Translations
UI_TRANSLATIONS = {
    "jurisdiction": {"en": "Jurisdiction", "el": "Δικαιοδοσία"},
    "specialty": {"en": "Legal Specialty", "el": "Ειδίκευση"},
    "upload": {"en": "Upload Legal Documents (PDF)", "el": "Ανέβασμα Νομικών Εγγράφων (PDF)"},
    "advanced": {"en": "⚙️ Advanced Options", "el": "⚙️ Προχωρημένες Επιλογές"},
    "depth": {"en": "Analysis Depth", "el": "Βάθος Ανάλυσης"},
    "focus": {"en": "Focus Areas", "el": "Εστίαση"},
    "logout": {"en": "Log Out", "el": "Αποσύνδεση"},
    "analyzing": {"en": "Analyzing legal framework...", "el": "Αναλύω το νομικό πλαίσιο..."},
    "placeholder": {
        "en": "Describe your legal matter or ask a question...",
        "el": "Περιγράψτε το νομικό σας ζήτημα ή κάντε μια ερώτηση..."
    }
}

FOCUS_OPTIONS = {
    "en": ["Procedural Defects", "Attribution Issues", "Mens Rea", 
           "Element Analysis", "Case Law", "Comparative Law"],
    "el": ["Διαδικαστικά Ελαττώματα", "Ζητήματα Καταλογισμού", "Δόλος", 
           "Ανάλυση Στοιχείων", "Νομολογία", "Συγκριτικό Δίκαιο"]
}
