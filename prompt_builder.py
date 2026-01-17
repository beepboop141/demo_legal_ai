"""
Build and enhance system prompts based on user settings
"""
from prompts import build_legal_system_prompt


def enhance_prompt_with_settings(base_prompt, settings, detected_lang):
    """
    Enhance the base system prompt with user settings
    
    Args:
        base_prompt (str): Base legal system prompt
        settings (dict): User settings from sidebar
        detected_lang (str): Detected language ('en' or 'el')
        
    Returns:
        str: Enhanced system prompt
    """
    enhanced_prompt = base_prompt
    
    # Add focus area instructions
    if settings.get("focus_area"):
        focus_text = ', '.join(settings["focus_area"])
        
        if detected_lang == "el":
            enhanced_prompt += f"\n\nΠΡΟΤΕΡΑΙΟΤΗΤΑ ΕΣΤΙΑΣΗΣ: Δώσε ιδιαίτερη προσοχή σε {focus_text}."
        else:
            enhanced_prompt += f"\n\nPRIORITY FOCUS: Pay special attention to {focus_text}."
    
    # Add analysis depth instructions
    analysis_depth = settings.get("analysis_depth", "Standard Analysis")
    
    if analysis_depth == "Deep Dive":
        depth_instruction = (
            "\n\nΟΔΗΓΙΑ ΒΑΘΟΥΣ: Παρέχεις ολοκληρωμένη ανάλυση στοιχείο-προς-στοιχείο με πλήρη διαδικαστική ανάλυση."
            if detected_lang == "el"
            else "\n\nDEPTH INSTRUCTION: Provide comprehensive element-by-element breakdown with full procedural analysis."
        )
        enhanced_prompt += depth_instruction
        
    elif analysis_depth == "Quick Review":
        depth_instruction = (
            "\n\nΟΔΗΓΙΑ ΒΑΘΟΥΣ: Παρέχεις συνοπτική στρατηγική αξιολόγηση εστιάζοντας μόνο σε κρίσιμα ζητήματα."
            if detected_lang == "el"
            else "\n\nDEPTH INSTRUCTION: Provide concise strategic assessment focusing on critical issues only."
        )
        enhanced_prompt += depth_instruction
    
    # Add document analysis instructions if files are uploaded
    uploaded_files = settings.get("uploaded_files")
    if uploaded_files:
        num_files = len(uploaded_files)
        
        doc_instruction = (
            f"\n\nΑΝΑΛΥΣΗ ΕΓΓΡΑΦΩΝ: Έχουν ανέβει {num_files} έγγραφα. Εφάρμοσε το Πρωτόκολλο Ανάλυσης Εγγράφων: "
            "εξάγαγε ημερομηνίες, προσδιόρισε διαδικαστικό στάδιο, επισήμανε ελαττώματα, διαχώρισε ισχυριζόμενα "
            "από αποδεδειγμένα γεγονότα, και φίλτραρε για νομική συνάφεια."
            if detected_lang == "el"
            else f"\n\nDOCUMENT ANALYSIS: {num_files} documents have been uploaded. Apply the Document Analysis Protocol: "
            "extract dates, identify procedural stage, flag defects, separate alleged from proven facts, and filter for legal relevance."
        )
        enhanced_prompt += doc_instruction
    
    return enhanced_prompt


def build_complete_system_prompt(jurisdiction, specialty, settings, detected_lang):
    """
    Build the complete system prompt with all enhancements
    
    Args:
        jurisdiction (str): Legal jurisdiction
        specialty (str): Legal specialty
        settings (dict): User settings from sidebar
        detected_lang (str): Detected language ('en' or 'el')
        
    Returns:
        str: Complete enhanced system prompt
    """
    base_prompt = build_legal_system_prompt(jurisdiction, specialty, detected_lang)
    return enhance_prompt_with_settings(base_prompt, settings, detected_lang)
