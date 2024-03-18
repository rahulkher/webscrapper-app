from langdetect import detect, LangDetectException

def detect_language(text):
    # Trim the text to remove leading/trailing whitespace
    text = text.strip()
    
    # Check if the text is empty or too short
    if not text or len(text) < 10:  # Adjust length as needed
        return {"status":"NotEnoughText"}
    
    try:
        # Attempt to detect the language
        return detect(text)
    except LangDetectException as e:
        # Handle the exception (e.g., log it, return a default language, etc.)
        return {"status":e}