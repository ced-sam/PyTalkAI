import customtkinter as ctk
import requests
import os
from datetime import datetime

# Charge les variables d'environnement
API_KEY = os.getenv("OPENAI_API_KEY")

# Historique des messages
message_history = []
current_history_index = -1
MAX_HISTORY = 100

def copy_text(event=None):
    try:
        selected_text = chat_box.selection_get()
        window.clipboard_clear()
        window.clipboard_append(selected_text)
    except:
        full_text = chat_box.get("1.0", "end-1c")
        window.clipboard_clear()
        window.clipboard_append(full_text)

def copy_all_text():
    full_text = chat_box.get("1.0", "end-1c")
    window.clipboard_clear()
    window.clipboard_append(full_text)

def send_message(event=None):
    global current_history_index, message_history
    message = entry_box.get("1.0", "end-1c").strip()
    if not message:
        return

    entry_box.configure(state="disabled")
    message = " ".join(message.split())

    now = datetime.now()
    timestamp = now.strftime("%m/%d/%Y, %H:%M:%S")
    chat_box.insert("end", f"\nVous ({timestamp}):\n{message}\n")

    message_history.append(message)
    if len(message_history) > MAX_HISTORY:
        message_history.pop(0)
    current_history_index = len(message_history)

    entry_box.delete("1.0", "end")

    if not API_KEY:
        chat_box.insert("end", f"\nErreur: Clé API non trouvée.\n")
        entry_box.configure(state="normal")
        return

    try:
        response = requests.post(
            "https://api.mistral.ai/v1/chat/completions",
            headers={"Authorization": f"Bearer {API_KEY}"},
            json={
                "model": "mistral-tiny",
                "messages": [{"role": "user", "content": message}]
            },
            timeout=10
        )
        response.raise_for_status()
        result = response.json()["choices"][0]["message"]["content"]
        chat_box.insert("end", f"\nBot ({timestamp}):\n{result}\n")
    except requests.exceptions.RequestException as e:
        chat_box.insert("end", f"\nErreur de requête ({timestamp}): {e}\n")
    except KeyError:
        chat_box.insert("end", f"\nErreur ({timestamp}): Réponse API invalide.\n")
    except Exception as e:
        chat_box.insert("end", f"\nErreur inattendue ({timestamp}): {e}\n")
    finally:
        entry_box.configure(state="normal")

def on_up_key(event):
    global current_history_index
    if message_history and current_history_index > 0:
        current_history_index -= 1
        entry_box.delete("1.0", "end")
        entry_box.insert("1.0", message_history[current_history_index])

def on_down_key(event):
    global current_history_index
    if message_history and current_history_index < len(message_history) - 1:
        current_history_index += 1
        entry_box.delete("1.0", "end")
        entry_box.insert("1.0", message_history[current_history_index])
    elif current_history_index == len(message_history) - 1:
        current_history_index += 1
        entry_box.delete("1.0", "end")

# Configuration de l'interface
ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("blue")

window = ctk.CTk()
window.title("Chat Mistral")
window.geometry("1200x800")

# Zone d'affichage des messages
chat_box = ctk.CTkTextbox(window, wrap="word", state="normal")
scrollbar = ctk.CTkScrollbar(window, command=chat_box.yview)
chat_box.configure(yscrollcommand=scrollbar.set)
chat_box.pack(fill="both", expand=True, padx=10, pady=10, side="left")
scrollbar.pack(side="right", fill="y")

# Zone de saisie
entry_box = ctk.CTkTextbox(window, height=150, wrap="word")
entry_box.pack(fill="x", padx=10, pady=5)
entry_box.bind("<Control-Return>", send_message)
entry_box.bind("<Up>", on_up_key)
entry_box.bind("<Down>", on_down_key)

# Boutons
send_button = ctk.CTkButton(window, text="Envoyer", command=send_message)
send_button.pack(pady=5)

copy_button = ctk.CTkButton(window, text="Copier tout", command=copy_all_text)
copy_button.pack(pady=5)

clear_button = ctk.CTkButton(window, text="Effacer", command=lambda: chat_box.delete("1.0", "end"))
clear_button.pack(pady=5)

# Menu contextuel pour copier
chat_box.bind("<Button-3>", lambda e: copy_text())
chat_box.bind("<Control-c>", lambda e: copy_text())

window.mainloop()
