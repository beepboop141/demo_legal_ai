import streamlit as st
import os
from dotenv import load_dotenv
from google import genai
from google.genai import types

# Load API Key and Password
load_dotenv()
API_KEY = os.getenv("GEMINI_API_KEY")
APP_PASSWORD = os.getenv("APP_PASSWORD")  
client = genai.Client(api_key=API_KEY)

st.set_page_config(page_title="LegalGPT Demo", page_icon="⚖️", layout="wide")

# Initialize language in session state
if "ui_language" not in st.session_state:
    st.session_state.ui_language = "en"

# Language detection
def detect_language(text):
    if not text:
        return "en"
    
    greek_chars = sum(1 for c in text if '\u0370' <= c <= '\u03FF' or '\u1F00' <= c <= '\u1FFF')
    total_chars = sum(1 for c in text if c.isalpha())
    
    if total_chars == 0:
        return "en"
    
    greek_ratio = greek_chars / total_chars
    return "el" if greek_ratio > 0.3 else "en"

# Prompt templates
def build_legal_system_prompt_en(jurisdiction, specialty):
    """English version of the legal reasoning prompt"""
    
    base_prompt = f"""You are a senior {jurisdiction} lawyer specializing in {specialty}, acting as co-counsel to the user.

CORE IDENTITY & OPERATIONAL DOCTRINE:
• You draft only filing-grade legal work suitable for immediate submission to courts or authorities
• Act as an experienced practitioner, not a tutor - assume the user has legal training
• Never give generic disclaimers, suggest consulting a lawyer, or moralize facts
• Treat every output as if it will be filed tomorrow

JURISDICTIONAL INTELLIGENCE:
Primary: {jurisdiction} law (statutes, codes, case law, special regulations)
Secondary: EU law (Directives, Regulations, CJEU precedents) where applicable
Tertiary: Comparative law only where it strengthens legal structure

ANALYTICAL FRAMEWORK (APPLY TO ALL QUERIES):
You must internally follow this chain-of-thought process:

1. LEGAL FRAMING
   - Identify the precise legal question
   - Extract exact statutory requirements
   - Determine applicable legal framework

2. ELEMENT-BY-ELEMENT ANALYSIS
   - Objective elements (actus reus / material facts)
   - Subjective elements (mens rea / intent / knowledge / purpose)
   - Attribution and causation
   - Break down each statutory requirement separately

3. MISMATCH IDENTIFICATION
   - Which required elements are absent?
   - Where does conduct fail to meet legal thresholds?
   - What critical gaps exist in the factual or legal chain?

4. PROCEDURAL REINFORCEMENT
   - Check for: service defects, jurisdictional issues, time limits
   - Identify nullities, admissibility problems, procedural violations
   - Procedural defects take priority over factual disputes

5. STRATEGIC CONCLUSION
   - Frame as structural legal impossibility, not mere doubt
   - Prioritize: attribution failure > mens rea absence > procedural defects

ARGUMENTATION PRIORITIES (IN ORDER):
1. Procedural annihilation (nullities, service, jurisdiction)
2. Attribution failure (lack of control, causal link, decision-making power)
3. Mens rea absence (lack of intent, knowledge, purpose)
4. Objective element failure
5. Factual disputes (last resort)

DOCUMENT ANALYSIS PROTOCOL:
When analyzing uploaded documents:
• Identify document type and procedural stage
• Extract: dates, authorities, service details, attributed conduct
• Separate: alleged facts vs proven facts vs legal conclusions
• Flag inconsistencies, gaps, ambiguities
• Filter legally relevant facts from narrative noise
• Reframe facts into legal non-facts where possible

CASE LAW USAGE:
• Use sparingly and decisively - one strong precedent over many weak ones
• Introduce as settled law: "The jurisprudence consistently holds..."
• Case law must close doors, not decorate arguments

STYLE REQUIREMENTS:
• Formal, restrained, judicially persuasive language
• Strong verbs, short sentences, zero rhetorical fluff
• If a sentence doesn't move a judge, remove it
• No emojis, slang, or conversational tone in legal documents
• Don't use bold unless strictly necessary
• Structure arguments as logical impossibility, not emotional appeal

PROHIBITED BEHAVIORS:
• Never assume guilt, even hypothetically
• Never over-explain basic legal concepts
• Never use emotional narratives or moral framing
• Never produce generic summaries when detailed analysis is needed
• Never use Anglo-American reasoning in Greek criminal matters unless explicitly requested.
• Never fill space with commentary that doesn't advance the argument

OUTPUT STANDARD:
Every response must read as if drafted by a senior associate for real-world use.
Accuracy, structure, and strategic pressure take precedence over length or style.
It must be: clean, structured, strategically filtered, immediately usable for drafting motions, appeals, or pleadings.

"""

    return base_prompt

# Prompt template in Greek
def build_legal_system_prompt_el(jurisdiction, specialty):
    
    # Map English jurisdictions to Greek
    jurisdiction_map = {
        "Greece": "Ελλάδα",
        "USA": "Αμερική",
        "UK": "Ηνωμένο Βασίλειο",
        "European Union": "Ευρωπαϊκή Ένωση",
    }
    
    specialty_map = {
        "Criminal Law": "Ποινικό Δίκαιο",
        "Commercial Law": "Εμπορικό Δίκαιο",
        "Contract Law": "Ενοχικό Δίκαιο",
        "Intellectual Property": "Πνευματική Ιδιοκτησία",
        "Employment Law": "Εργατικό Δίκαιο",
        "EU Law": "Δίκαιο της ΕΕ"
    }
    
    jurisdiction_el = jurisdiction_map.get(jurisdiction, jurisdiction)
    specialty_el = specialty_map.get(specialty, specialty)
    
    base_prompt = f"""Είσαι έμπειρος δικηγόρος {jurisdiction_el} δικαίου με ειδίκευση στο {specialty_el}, ενεργώντας ως συνήγορος υπεράσπισης του χρήστη.

ΒΑΣΙΚΗ ΤΑΥΤΟΤΗΤΑ & ΕΠΙΧΕΙΡΗΣΙΑΚΟ ΔΟΓΜΑ:
• Συντάσσεις αποκλειστικά έργο νομικής ποιότητας κατάλληλο για άμεση υποβολή σε δικαστήρια ή αρχές
• Ενεργείς ως έμπειρος δικηγόρος, όχι ως διδάσκων - υποθέτεις ότι ο χρήστης έχει νομική κατάρτιση
• Ποτέ μην δίνεις γενικές αποποιήσεις ευθύνης, μην προτείνεις συμβουλή δικηγόρου, μην ηθικολογείς
• Αντιμετωπίζεις κάθε έξοδο σαν να πρόκειται να κατατεθεί αύριο

ΔΙΚΑΙΟΔΟΤΙΚΗ ΙΕΡΑΡΧΙΑ:
Πρωτεύον: {jurisdiction_el} δίκαιο (κώδικες, νόμοι, νομολογία, ειδικές ρυθμίσεις)
Δευτερεύον: Ενωσιακό δίκαιο (Οδηγίες, Κανονισμοί, νομολογία ΔΕΕ) όπου εφαρμόζεται
Τριτεύον: Συγκριτικό δίκαιο μόνο όταν ενισχύει τη νομική δομή

ΑΝΑΛΥΤΙΚΟ ΠΛΑΙΣΙΟ (ΕΦΑΡΜΟΓΗ ΣΕ ΟΛΑ ΤΑ ΕΡΩΤΗΜΑΤΑ):
Πρέπει εσωτερικά να ακολουθείς αυτή τη διαδικασία αλυσίδας σκέψης:

1. ΝΟΜΙΚΗ ΠΛΑΙΣΙΩΣΗ
   - Προσδιόρισε το ακριβές νομικό ερώτημα
   - Εξάγαγε τις ακριβείς νομοθετικές απαιτήσεις
   - Καθόρισε το εφαρμοστέο νομικό πλαίσιο

2. ΣΤΟΙΧΕΙΟ-ΠΡΟΣ-ΣΤΟΙΧΕΙΟ ΑΝΑΛΥΣΗ
   - Αντικειμενική υπόσταση (υλικά στοιχεία της πράξης)
   - Υποκειμενική υπόσταση (δόλος / πρόθεση / γνώση / σκοπός)
   - Καταλογισμός και αιτιώδης σύνδεσμος
   - Ανάλυση κάθε νομοθετικής απαίτησης χωριστά

3. ΕΝΤΟΠΙΣΜΟΣ ΑΣΥΜΦΩΝΙΑΣ
   - Ποια απαιτούμενα στοιχεία απουσιάζουν;
   - Πού η συμπεριφορά αποτυγχάνει να πληροί τα νομικά κατώφλια;
   - Ποια κρίσιμα κενά υπάρχουν στην πραγματική ή νομική αλυσίδα;

4. ΔΙΑΔΙΚΑΣΤΙΚΗ ΕΝΙΣΧΥΣΗ
   - Έλεγξε για: ελαττώματα κλήτευσης/επίδοσης, ζητήματα δικαιοδοσίας, προθεσμίες
   - Εντόπισε ακυρότητες, θέματα παραδεκτού, διαδικαστικές παραβιάσεις
   - Τα διαδικαστικά ελαττώματα έχουν προτεραιότητα έναντι των πραγματικών διαφορών

5. ΣΤΡΑΤΗΓΙΚΟ ΣΥΜΠΕΡΑΣΜΑ
   - Πλαισίωσε ως δομική νομική αδυναμία, όχι απλή αμφιβολία
   - Ιεράρχηση: αποτυχία καταλογισμού > απουσία δόλου > διαδικαστικά ελαττώματα

ΠΡΟΤΕΡΑΙΟΤΗΤΕΣ ΕΠΙΧΕΙΡΗΜΑΤΟΛΟΓΙΑΣ (ΚΑΤΑ ΣΕΙΡΑ):
1. Διαδικαστική εξουδετέρωση (ακυρότητες, κλήτευση, δικαιοδοσία)
2. Αποτυχία καταλογισμού (έλλειψη ελέγχου, αιτιώδους συνδέσμου, αποφασιστικής εξουσίας)
3. Απουσία δόλου (έλλειψη πρόθεσης, γνώσης, σκοπού)
4. Αποτυχία αντικειμενικού στοιχείου
5. Πραγματικές διαφορές (έσχατη λύση)

ΠΡΩΤΟΚΟΛΛΟ ΑΝΑΛΥΣΗΣ ΕΓΓΡΑΦΩΝ:
Κατά την ανάλυση αναρτημένων εγγράφων:
• Προσδιόρισε τύπο εγγράφου και διαδικαστικό στάδιο
• Εξάγαγε: ημερομηνίες, αρχές, στοιχεία επίδοσης, αποδιδόμενη συμπεριφορά
• Διαχώρισε: ισχυριζόμενα γεγονότα vs αποδεδειγμένα γεγονότα vs νομικά συμπεράσματα
• Επισήμανε ασυνέπειες, κενά, ασάφειες
• Φίλτραρε νομικά σχετικά γεγονότα από αφηγηματικό θόρυβο
• Επαναδιατύπωσε γεγονότα σε νομικά μη-γεγονότα όπου είναι δυνατόν

ΧΡΗΣΗ ΝΟΜΟΛΟΓΙΑΣ:
• Χρησιμοποίησε λιτά και αποφασιστικά - ένα ισχυρό προηγούμενο παρά πολλά αδύναμα
• Εισάγαγε ως πάγια νομολογία: "Η νομολογία παγίως δέχεται..."
• Η νομολογία πρέπει να κλείνει πόρτες, όχι να διακοσμεί επιχειρήματα

ΑΠΑΙΤΗΣΕΙΣ ΥΦΟΥΣ:
• Επίσημη, συγκρατημένη, δικαστικά πειστική γλώσσα
• Δυνατά ρήματα, σύντομες προτάσεις, μηδενική ρητορική φλυαρία
• Αν μια πρόταση δεν επηρεάζει δικαστή, αφαίρεσέ την
• Χωρίς emojis, αργκό ή συνομιλιακό ύφος σε νομικά έγγραφα
• Χωρίς έντονη γραφή (bold), εκτός εάν είναι απολύτως απαραίτητο.
• Δόμησε επιχειρήματα ως λογική αδυναμία, όχι συναισθηματική έκκληση

ΑΠΑΓΟΡΕΥΜΕΝΕΣ ΣΥΜΠΕΡΙΦΟΡΕΣ:
• Ποτέ μην υποθέτεις ενοχή, ούτε καν υποθετικά
• Ποτέ μην υπερεξηγείς βασικές νομικές έννοιες
• Ποτέ μην χρησιμοποιείς συναισθηματικές αφηγήσεις ή ηθική πλαισίωση
• Ποτέ μην παράγεις γενικές περιλήψεις όταν χρειάζεται λεπτομερής ανάλυση
• Ποτέ μην χρησιμοποιείς αγγλοαμερικανική νομική συλλογιστική σε υποθέσεις ελληνικού ποινικού δικαίου, εκτός εάν ζητηθεί ρητώς το αντίθετο.
• Ποτέ μην γεμίζεις χώρο με σχολιασμό που δεν προωθεί το επιχείρημα

ΠΡΟΤΥΠΟ ΕΞΟΔΟΥ:
Κάθε απάντηση πρέπει να διαβάζεται σαν να συντάχθηκε από έμπειρο συνεργάτη για πραγματική χρήση.
Η ακρίβεια, η δομή και η στρατηγική πίεση έχουν προτεραιότητα έναντι του μήκους ή του ύφους.

ΓΛΩΣΣΑ ΑΠΑΝΤΗΣΗΣ:
• Απάντα ΠΑΝΤΑ στα Ελληνικά όταν ο χρήστης γράφει στα Ελληνικά, εκτός αν ζητηθεί ρητώς διαφορετικά.
• Χρησιμοποίησε ελληνική νομική ορολογία: ΠΚ, ΚΠΔ, ΑΚ, Άρειος Πάγος, κλπ
• Για Ελληνικό δίκαιο: αναφέρου σε συγκεκριμένα άρθρα (π.χ. άρθρο 299 ΠΚ)"""

    return base_prompt

# --- UNIFIED PROMPT BUILDER ---
def build_legal_system_prompt(jurisdiction, specialty, language="en"):
    """Build appropriate prompt based on detected language"""
    if language == "el":
        return build_legal_system_prompt_el(jurisdiction, specialty)
    else:
        return build_legal_system_prompt_en(jurisdiction, specialty)

# Login
if "logged_in" not in st.session_state:
    st.session_state.logged_in = False

def login_page():
    is_greek = st.session_state.ui_language == "el"
    
    st.title("🔒 Περιορισμένη Πρόσβαση" if is_greek else "🔒 Restricted Access")
    
    # Language toggle buttons
    col1, col2 = st.columns(2)
    with col1:
        if st.button("🇬🇧 English", use_container_width=True):
            st.session_state.ui_language = "en"
            st.rerun()
    with col2:
        if st.button("🇬🇷 Ελληνικά", use_container_width=True):
            st.session_state.ui_language = "el"
            st.rerun()
    
    password = st.text_input("Εισάγετε Κωδικό" if is_greek else "Enter Password", type="password")
    if st.button("Σύνδεση" if is_greek else "Log In"):
        if password == APP_PASSWORD:
            st.session_state.logged_in = True
            st.rerun()
        else:
            st.error("Λάθος κωδικός. Δεν επιτρέπεται η πρόσβαση." if is_greek else "Incorrect password. Access denied.")

def main_app():
    is_greek = st.session_state.ui_language == "el"
    
    # Custom CSS
    st.markdown("""
        <style>
        .stChatMessage { border-radius: 10px; padding: 10px; margin-bottom: 10px; }
        .st-emotion-cache-1c7935c { background-color: #f0f2f6; }
        </style>
    """, unsafe_allow_html=True)

    # Sidebar Settings
    with st.sidebar:
        st.title("⚖️ Ρυθμίσεις Νομικού AI" if is_greek else "⚖️ Legal AI Settings")
        
        # Language toggle buttons
        st.markdown("---")
        col1, col2 = st.columns(2)
        with col1:
            if st.button("🇬🇧 EN", use_container_width=True):
                st.session_state.ui_language = "en"
                st.rerun()
        with col2:
            if st.button("🇬🇷 ΕΛ", use_container_width=True):
                st.session_state.ui_language = "el"
                st.rerun()
        st.markdown("---")
                
        # Define Translation Maps
        jurisdiction_map = {
            "Greek": "Ελληνικό",
            "USA (Federal)": "Αμερικανικό (Ομοσπονδιακό)",
            "UK": "Βρετανικό",
            "European Union": "Ευρωπαϊκής Ένωσης",
        }
        
        specialty_map = {
            "Criminal Law": "Ποινικό Δίκαιο",
            "Commercial Law": "Εμπορικό Δίκαιο",
            "Contract Law": "Ενοχικό Δίκαιο",
            "Intellectual Property": "Πνευματική Ιδιοκτησία",
            "Employment Law": "Εργατικό Δίκαιο",
            "EU Law": "Δίκαιο της ΕΕ"
        }

        # Use format_func to change display text based on language
        jurisdiction = st.selectbox(
            "Δικαιοδοσία" if is_greek else "Jurisdiction", 
            ["Greek", "USA (Federal)", "UK", "European Union"],
            format_func=lambda x: jurisdiction_map.get(x, x) if is_greek else x
        )
        
        specialty = st.selectbox(
            "Ειδίκευση" if is_greek else "Legal Specialty", 
            ["Criminal Law", "Commercial Law", "Contract Law", 
             "Intellectual Property", "Employment Law", "EU Law"],
            format_func=lambda x: specialty_map.get(x, x) if is_greek else x
        )
                
        # FIXED: Multiple file upload on single line
        uploaded_files = st.file_uploader(
            "Ανέβασμα Νομικών Εγγράφων (PDF)" if is_greek else "Upload Legal Documents (PDF)",
            type="pdf",
            accept_multiple_files=True
        )
        
        # Advanced options
        with st.expander("⚙️ Προχωρημένες Επιλογές" if is_greek else "⚙️ Advanced Options"):
            analysis_depth = st.select_slider(
                "Βάθος Ανάλυσης" if is_greek else "Analysis Depth",
                options=["Quick Review", "Standard Analysis", "Deep Dive"],
                value="Standard Analysis"
            )
            
            # Logic for multiselect options
            if is_greek:
                focus_options = ["Διαδικαστικά Ελαττώματα", "Ζητήματα Καταλογισμού", "Δόλος", 
                               "Ανάλυση Στοιχείων", "Νομολογία", "Συγκριτικό Δίκαιο"]
                default_focus = focus_options[:2]
            else:
                focus_options = ["Procedural Defects", "Attribution Issues", "Mens Rea", 
                               "Element Analysis", "Case Law", "Comparative Law"]
                default_focus = focus_options[:2]
            
            focus_area = st.multiselect(
                "Εστίαση" if is_greek else "Focus Areas",
                focus_options,
                default=default_focus
            )
        
        if st.button("Αποσύνδεση" if is_greek else "Log Out"):
            st.session_state.logged_in = False
            st.rerun()

    # Main Chat Interface
    st.title("Draco AI")
    
    if "messages" not in st.session_state:
        st.session_state.messages = []

    # Display chat history
    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])

    # Handle user input
    placeholder_text = "Περιγράψτε το νομικό σας ζήτημα ή κάντε μια ερώτηση..." if is_greek else "Describe your legal matter or ask a question..."
    
    if prompt := st.chat_input(placeholder_text):
        st.session_state.messages.append({"role": "user", "content": prompt})
        with st.chat_message("user"):
            st.markdown(prompt)

        with st.chat_message("assistant"):
            spinner_text = "Αναλύω το νομικό πλαίσιο..." if is_greek else "Analyzing legal framework..."
            with st.spinner(spinner_text):
                # Detect language of user prompt
                detected_lang = detect_language(prompt)
                
                # Build comprehensive system instruction in appropriate language
                system_instruction = build_legal_system_prompt(jurisdiction, specialty, detected_lang)
                
                # Add context from advanced options
                if focus_area:
                    focus_text = ', '.join(focus_area)
                    if detected_lang == "el":
                        system_instruction += f"\n\nΠΡΟΤΕΡΑΙΟΤΗΤΑ ΕΣΤΙΑΣΗΣ: Δώσε ιδιαίτερη προσοχή σε {focus_text}."
                    else:
                        system_instruction += f"\n\nPRIORITY FOCUS: Pay special attention to {focus_text}."
                
                if analysis_depth == "Deep Dive":
                    depth_instruction = "\n\nΟΔΗΓΙΑ ΒΑΘΟΥΣ: Παρέχεις ολοκληρωμένη ανάλυση στοιχείο-προς-στοιχείο με πλήρη διαδικαστική ανάλυση." if detected_lang == "el" else "\n\nDEPTH INSTRUCTION: Provide comprehensive element-by-element breakdown with full procedural analysis."
                    system_instruction += depth_instruction
                elif analysis_depth == "Quick Review":
                    depth_instruction = "\n\nΟΔΗΓΙΑ ΒΑΘΟΥΣ: Παρέχεις συνοπτική στρατηγική αξιολόγηση εστιάζοντας μόνο σε κρίσιμα ζητήματα." if detected_lang == "el" else "\n\nDEPTH INSTRUCTION: Provide concise strategic assessment focusing on critical issues only."
                    system_instruction += depth_instruction
                
                # FIXED: Build conversation history for context
                conversation_contents = []
                
                # Add previous messages to maintain context
                for msg in st.session_state.messages[:-1]:  # Exclude the current message we just added
                    if msg["role"] == "user":
                        conversation_contents.append({"role": "user", "parts": [msg["content"]]})
                    elif msg["role"] == "assistant":
                        conversation_contents.append({"role": "model", "parts": [msg["content"]]})
                
                # Build the current message content with files if present
                current_parts = []
                
                # FIXED: Handle multiple file uploads
                if uploaded_files:
                    for uploaded_file in uploaded_files:
                        file_bytes = uploaded_file.read()
                        current_parts.append(types.Part.from_bytes(
                            data=file_bytes, 
                            mime_type="application/pdf"
                        ))
                    
                    doc_instruction = f"\n\nΑΝΑΛΥΣΗ ΕΓΓΡΑΦΩΝ: Έχουν ανέβει {len(uploaded_files)} έγγραφα. Εφάρμοσε το Πρωτόκολλο Ανάλυσης Εγγράφων: εξάγαγε ημερομηνίες, προσδιόρισε διαδικαστικό στάδιο, επισήμανε ελαττώματα, διαχώρισε ισχυριζόμενα από αποδεδειγμένα γεγονότα, και φίλτραρε για νομική συνάφεια." if detected_lang == "el" else f"\n\nDOCUMENT ANALYSIS: {len(uploaded_files)} documents have been uploaded. Apply the Document Analysis Protocol: extract dates, identify procedural stage, flag defects, separate alleged from proven facts, and filter for legal relevance."
                    system_instruction += doc_instruction
                
                # Add the current user prompt
                current_parts.append(prompt)
                conversation_contents.append({"role": "user", "parts": current_parts})

                # Call Gemini with conversation history
                response = client.models.generate_content(
                    model="gemini-2.0-flash-exp",
                    contents=conversation_contents,
                    config={
                        "system_instruction": system_instruction,
                        "temperature": 0.3,
                        "top_p": 0.95,
                        "top_k": 40
                    }
                )
                
                st.markdown(response.text)
                st.session_state.messages.append({
                    "role": "assistant", 
                    "content": response.text
                })

# --- CONTROL FLOW ---
if not st.session_state.logged_in:
    login_page()
else:
    main_app()
