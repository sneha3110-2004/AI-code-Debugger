class CodeDebuggerAI:
    def __init__(self):
        print("--- OFFLINE MODE: Using Mock AI (No Space Needed) ---")
        print("--- AI is Ready! ---")

    def analyze_code(self, code, language):
        # This acts as a placeholder so your app doesn't crash
        return (f"AI Analysis ({language}):\n"
                "I see your code! To fix this, ensure all brackets are closed "
                "and variables are defined before use. (Disk space low: Real AI disabled)")

debugger = CodeDebuggerAI()