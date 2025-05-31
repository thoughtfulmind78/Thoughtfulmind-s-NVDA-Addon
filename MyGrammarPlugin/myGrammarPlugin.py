# Add-on development first example

import globalPluginHandler
import speech
import api
import ui # For dialog boxes
import os # For file paths
from pathlib import Path # For cross-platform desktop path
import time # Import the time module for tracking key presses
import webbrowser # Import for opening web pages
import urllib.request # Import for checking internet connection
import urllib.error # Import for catching URL errors

class GlobalPlugin(globalPluginHandler.GlobalPlugin):

    # Dictionary to store noun meanings
    noun_meanings = {
        "dog": "A domesticated carnivorous mammal that typically has a long snout, an acute sense of smell, non-retractable claws, and a barking, howling, or whining voice.",
        "cat": "A small domesticated carnivorous mammal with soft fur, a short snout, and retractile claws. It is widely kept as a pet or for catching mice and other vermin.",
        "house": "A building for human habitation, especially one that is lived in by a family or small group of people.",
        "river": "A large natural stream of water flowing in a channel to the sea, a lake, or another river.",
        "computer": "An electronic device for storing and processing data, typically in binary form, according to instructions given to it in a variable program.",
        "teacher": "A person who teaches, especially in a school.",
        "book": "A written or printed work consisting of pages glued or sewn together along one side and bound in covers.",
        "city": "A large town.",
        "happiness": "The state of being happy.",
        "freedom": "The power or right to act, speak, or think as one wants without hindrance or restraint."
    }

    # Variable to store spoken grammar terms for logging
    _grammar_log = []
    # Variable to store the last spoken grammar term for copying
    _last_spoken_grammar_term = ""

    # Variables for double-press detection
    _last_nvda_control_8_press_time = 0
    _double_press_threshold = 0.5  # Time in seconds for rapid succession

    def _check_internet_connection(self):
        """
        Checks if an internet connection is available by attempting to open a well-known URL.
        Returns True if connected, False otherwise.
        """
        try:
            urllib.request.urlopen("http://www.google.com", timeout=1)
            return True
        except urllib.error.URLError as e:
            api.log.warning(f"Internet connection check failed: {e}")
            return False

    def script_openResourcesForTheBlind(self, gesture):
        """
        Opens the Resources for the Blind Inc. website if an internet connection is available.
        """
        website_url = "https://blind.org.ph/"
        if self._check_internet_connection():
            speech.speakMessage(f"Opening {website_url}")
            webbrowser.open(website_url)
        else:
            speech.speakMessage("No internet connection available. Cannot open website.")
            api.log.warning("Attempted to open blind.org.ph but no internet connection.")

    def script_sayEnglishGrammar(self, gesture):
        message = "Noun -- A noun is any name given to a person, place, idea, and event.\nExample: Cebu is a noun belongs to a proper noun."
        speech.speakMessage(message)
        api.copyToClip(message)
        self._grammar_log.append(message)
        self._last_spoken_grammar_term = message # Store the last spoken term

    def script_sayEnglish(self, gesture):
        message = "Verb -- A verb is any action word in the sentence.\nExample: My brother gives me a glass of milk. The verb is gives."
        speech.speakMessage(message)
        self._grammar_log.append(message)
        self._last_spoken_grammar_term = message # Store the last spoken term

    def script_sayAdj(self, gesture):
        message = "Adjective -- An adjective is any word that modifies or describes nouns or pronouns.\nExample: God is good.\nGood is adjective."
        speech.speakMessage(message)
        api.copyToClip(message)
        self._grammar_log.append(message)
        self._last_spoken_grammar_term = message # Store the last spoken term

    def script_sayPro(self, gesture):
        message = "Pronoun -- A pronoun is any word that replaces the noun in any given sentence.\nExample: Basellio is a helpful child.\nIt can be written as: He helps her mother in cooking meals.\nThe pronoun 'He' is a subjective case singular pronoun for a male person."
        speech.speakMessage(message)
        self._grammar_log.append(message)
        self._last_spoken_grammar_term = message # Store the last spoken term

    def script_sayAdv(self, gesture):
        message = "Adverb -- An adverb is a word that modifies or describes a verb, adjective, or another adverb.\nExample: The child happily plays the piano.\nThe adverb is happily."
        speech.speakMessage(message)
        self._grammar_log.append(message)
        self._last_spoken_grammar_term = message # Store the last spoken term

    def script_sayCon(self, gesture):
        message = "Conjunction -- A conjunction is a word that connects or links words, phrases, or clauses.\nExample: The child and his sister play the piano.\nThe conjunction is and."
        speech.speakMessage(message)
        self._grammar_log.append(message)
        self._last_spoken_grammar_term = message # Store the last spoken term

    def script_sayPrep(self, gesture):
        message = "Preposition -- A preposition pertains to location of a noun or nominal phrase.\nIn some contexts, a preposition is used to indicate the indirect object of the sentence. Hi user. This is Leonard"
        speech.speakMessage(message)
        self._grammar_log.append(message)
        self._last_spoken_grammar_term = message # Store the last spoken term

    def script_sayInter(self, gesture):
        message = "Interjection -- An interjection is a word that expresses an intensed feeling of a speaker.\nExample: Oh, the sun is very hot!\nThe interjection is oh."
        speech.speakMessage(message)
        self._grammar_log.append(message)
        self._last_spoken_grammar_term = message # Store the last spoken term

    def script_sayModifiers(self, gesture):
        message = "Modifiers are words that are placed before and after a head noun in a phrase. \nAll beautiful fish in the sea. modifiers are: \nall beautiful-- pre-modifiers \nin the sea -- post modifiers."
        speech.speakMessage(message)
        self._grammar_log.append(message)
        self._last_spoken_grammar_term = message # Store the last spoken term

    def script_sayTwopartsofasentence(self, gesture):
        message = "The two parts of a sentence are:\n1. Subject -- it is being talked about in any sentence.\nExample: My neighbor is kind.\nThe subject is neighbor.\n2. Predicate -- It talks about the subject of the given sentence.\nExample: My neighbor is kind.\nThe predicate is kind. It belongs to a predicate adjective."
        speech.speakMessage(message)
        self._grammar_log.append(message)
        self._last_spoken_grammar_term = message # Store the last spoken term

    def script_findNounMeaning(self, gesture):
        # Open a dialog box for the user to type a noun
        noun_input = ui.inputBox("English Grammar: Enter a noun to find its meaning:", "Enter Noun")
        
        if noun_input: # If the user didn't cancel the dialog
            noun_input_lower = noun_input.lower() # Convert to lowercase for case-insensitive lookup
            if noun_input_lower in self.noun_meanings:
                meaning = f"The meaning of '{noun_input}' is: {self.noun_meanings[noun_input_lower]}"
                speech.speakMessage(meaning)
                self._grammar_log.append(f"Noun lookup: {meaning}")
                self._last_spoken_grammar_term = meaning # Store the last spoken term
            else:
                speech.speakMessage(f"Sorry, I don't have a meaning for '{noun_input}' in my dictionary.")
                self._grammar_log.append(f"Noun lookup: No meaning found for '{noun_input}'")
                self._last_spoken_grammar_term = "" # Clear if no meaning found
        else:
            speech.speakMessage("Noun meaning search cancelled.")
            self._last_spoken_grammar_term = "" # Clear if cancelled

    def script_announceNounMeaning(self, gesture):
        """
        Announces the meaning of the word 'noun' as defined in the dictionary.
        This function uses a direct definition for grammar terms.
        """
        message = "A noun is any name given to a person, place, idea, and event. For example, 'Cebu' is a noun that belongs to a proper noun category."
        speech.speakMessage(message)
        self._grammar_log.append(f"Announced: {message}")
        self._last_spoken_grammar_term = message # Store the last spoken term

    def script_handleNvdaControl8(self, gesture):
        """
        Handles the NVDA+control+8 gesture, checking for rapid double press.
        On single press, it prompts to save a grammar term.
        On double press, it copies the last spoken grammar term to the clipboard.
        """
        current_time = time.time()
        if (current_time - self._last_nvda_control_8_press_time) < self._double_press_threshold:
            # This is a double press
            self._copyLastGrammarTermToClipboard()
            self._last_nvda_control_8_press_time = 0 # Reset to prevent triple-press issues
        else:
            # This is a single press, record time and proceed with existing functionality
            self._last_nvda_control_8_press_time = current_time
            self._saveCurrentGrammarTerm()

    def script_copyGrammarTerm(self, gesture):
        """
        Copies the content of _last_spoken_grammar_term to the clipboard when NVDA+control+6 is pressed.
        """
        self._copyLastGrammarTermToClipboard()

    def _saveCurrentGrammarTerm(self):
        """
        Saves the last spoken grammar term (or a prompt for a new one) to the log.
        This function will prompt the user to enter the grammar term and its meaning.
        """
        term_to_save = ui.inputBox(
            "Enter the grammar term you want to save (e.g., Noun) and its meaning (e.g., A noun is any name given to a person, place, idea, and event.):",
            "Save Grammar Term"
        )
        if term_to_save:
            self._grammar_log.append(f"Manual Entry - Grammar Term: {term_to_save}")
            speech.speakMessage(f"Grammar term '{term_to_save}' saved to log.")
            self._last_spoken_grammar_term = term_to_save # Also update last spoken term
        else:
            speech.speakMessage("Saving grammar term cancelled.")
            self._last_spoken_grammar_term = "" # Clear if cancelled

    def _copyLastGrammarTermToClipboard(self):
        """
        Copies the content of _last_spoken_grammar_term to the clipboard.
        """
        if self._last_spoken_grammar_term:
            api.copyToClip(self._last_spoken_grammar_term)
            speech.speakMessage("Last grammar term copied to clipboard. Please press NVDA+c to know the clipboard content.")
            self._grammar_log.append(f"Copied to clipboard: {self._last_spoken_grammar_term}")
        else:
            speech.speakMessage("No grammar term available to copy.")

    def script_saveLogToDesktop(self, gesture):
        try:
            # Get the user's desktop path
            desktop_path = str(Path.home() / "Desktop")
            log_file_path = os.path.join(desktop_path, "nvda_grammar_log.txt")

            with open(log_file_path, "w", encoding="utf-8") as f:
                if self._grammar_log:
                    f.write("\n".join(self._grammar_log))
                    speech.speakMessage(f"Grammar log saved to {log_file_path}, please go to your desktop now and look for nvda_grammar_log.txt.")
                else:
                    f.write("No grammar terms found during this session. Jesus Christ is Lord.")
                    speech.speakMessage("No grammar terms found during this session to save.")
            
            # Clear the log after saving
            self._grammar_log.clear()

        except Exception as e:
            speech.speakMessage(f"Error saving log file: {e}")
            api.log.error(f"Error saving NVDA grammar log: {e}")

    __gestures={
        "kb:NVDA+Alt+n": "sayEnglishGrammar",
        "kb:NVDA+Alt+v": "sayEnglish",
        "kb:NVDA+Alt+a": "sayAdj",
        "kb:NVDA+Alt+p": "sayPro",
        "kb:NVDA+Alt+i": "sayInter",
        "kb:NVDA+shift+control+d": "sayAdv",
        "kb:NVDA+Alt+c": "sayCon",
        "kb:NVDA+Alt+r": "sayPrep",
        "kb:NVDA+Alt+d": "sayModifiers",
        "kb:NVDA+shift+control+t": "sayTwopartsofasentence",
        "kb:control+NVDA+7": "openResourcesForTheBlind", # Changed to open website
        "kb:NVDA+control+n": "announceNounMeaning", # New gesture for announcing the meaning of "noun"
        "kb:control+NVDA+8": "handleNvdaControl8", # Modified to handle single and double presses
        "kb:control+NVDA+6": "copyGrammarTerm", # New gesture for copying the last grammar term
        "kb:control+NVDA+9": "saveLogToDesktop" # New gesture to explicitly save the entire log to desktop
    }