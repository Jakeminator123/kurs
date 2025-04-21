# backend/session_utils.py

import json
from datetime import datetime

def save_progress(user_data, conversation_history):
    """
    Sparar användardata och konversationshistorik till en fil
    
    Args:
        user_data (dict): Användarens data och svar
        conversation_history (list): Historiken över konversationen
        
    Returns:
        str: Filnamnet som skapades
    """
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    filename = f"affarsplan_{timestamp}.json"
    
    data = {
        "user_data": user_data,
        "conversation_history": conversation_history,
        "timestamp": timestamp
    }
    
    with open(filename, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=4)
    
    return filename

def load_progress(filename):
    """
    Laddar användardata och konversationshistorik från en fil
    
    Args:
        filename (str): Sökvägen till filen som ska laddas
        
    Returns:
        tuple: (user_data, conversation_history)
    """
    try:
        with open(filename, "r", encoding="utf-8") as f:
            data = json.load(f)
        
        return data.get("user_data", {}), data.get("conversation_history", [])
    except Exception as e:
        return {}, [] 