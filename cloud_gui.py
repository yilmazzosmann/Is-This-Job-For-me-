import tkinter as tk
from tkinter import scrolledtext
from openai import OpenAI
import copy
import google.generativeai as genai
import os

genai.configure(api_key=os.environ["GEMINI_API_KEY"])


class GeminiChatApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Is This Job For Me?")

        # Make the window stay on top
        self.root.attributes("-topmost", True)

        # Set dark mode colors
        self.bg_color = "#2e2e2e"
        self.fg_color = "#ffffff"
        self.entry_bg_color = "#3e3e3e"
        self.entry_fg_color = "#ffffff"

        # Configure root window for dark mode
        self.root.configure(bg=self.bg_color)

        # Output text block
        tk.Label(root, text="Output", bg=self.bg_color, fg=self.fg_color).pack(padx=10, pady=5, fill=tk.BOTH, expand=True)
        self.output_text = scrolledtext.ScrolledText(root, wrap=tk.WORD, width=80, height=10, bg=self.entry_bg_color, fg=self.entry_fg_color, insertbackground=self.fg_color)
        self.output_text.pack(padx=10, pady=5, fill=tk.BOTH, expand=True)

        # Chat text block
        tk.Label(root, text="Chat", bg=self.bg_color, fg=self.fg_color).pack(padx=10, pady=5, fill=tk.BOTH, expand=True)
        self.chat_text = tk.Text(root, wrap=tk.WORD, width=80, height=3, bg=self.entry_bg_color, fg=self.entry_fg_color, insertbackground=self.fg_color)
        self.chat_text.pack(padx=10, pady=5, fill=tk.BOTH, expand=True)

        # Frame for buttons
        button_frame = tk.Frame(root, bg=self.bg_color)
        button_frame.pack(fill=tk.BOTH, expand=True)

        # Restart Chat button
        self.restart_button = tk.Button(button_frame, text="Restart Chat", command=self.restart_chat, bg=self.entry_bg_color, fg=self.fg_color)
        self.restart_button.pack(side=tk.LEFT, padx=10, pady=10)

        # Run Chat button
        self.run_button = tk.Button(button_frame, text="Send", command=self.run_gemini_chat, bg=self.entry_bg_color, fg=self.fg_color)
        self.run_button.pack(side=tk.RIGHT, padx=10, pady=10)

        # Bind Enter and Shift+Enter keys
        self.chat_text.bind("<Return>", self.on_enter_pressed)
        self.chat_text.bind("<Shift-Return>", self.on_shift_enter_pressed)

        self.chat_base = [
            {"role": "system", "content": """
            You are an AI assistant that checks if a job searcher's conditions align with a job description. 
            Focus only on given conditions and the job description. Do not check technical compatibility or 
            infer additional information. Analyze each provided condition against the job description. Provide a clear, concise 
            "Yes" or "No" response with a brief explanation. Do not offer additional advice or elaborations."""},

            {"role": "user", "content": """
            Conditions:
            - Please write here important conditions that you want to check against the job description.
            - It can be location, language, work permit, or any other condition.
            - It can be related to visa issues you can't comply.
            - It can be travel requirements you don't want.
            - It can be a specific skill you don't have that is mentioned a lot.

            Check these conditions against the following job description. Respond with "Yes" or "No" and a brief explanation in 1-2 sentences.
              If "No", cite the conflicting text from the job description.

            Job description:
            """}]
        
        # Initialize chat history
        self.chat_history = copy.deepcopy(self.chat_base)

        self.model = genai.GenerativeModel(
                "models/gemini-1.5-flash",
                system_instruction=self.chat_base[0]["content"],
            )
        
        self.chat = self.model.start_chat(history=[])
    
    def on_enter_pressed(self, event):
        self.run_gemini_chat()
        return "break"  # Prevent the default behavior of the Enter key
    
    def on_shift_enter_pressed(self, event):
        self.chat_text.insert(tk.INSERT, "\n")
        return "break"  # Prevent the default behavior of the Enter key   
     
    def display_chat_history(self):
        self.output_text.delete("1.0", tk.END)
        self.output_text.tag_configure("User", foreground="red")
        self.output_text.tag_configure("Assistant", foreground="red")

        for message in self.chat_history[1:]:
            role = message["role"].capitalize()
            content = message["content"]
            self.output_text.insert(tk.END, f"{role}: ", "User")
            self.output_text.insert(tk.END, f"{content}\n\n")
        self.output_text.see(tk.END)

    def run_gemini_chat(self):
        
        chat_input = self.chat_text.get("1.0", tk.END).strip()

        # Check if this is the first user input
        if len(self.chat_history) == 2:
            # Add the first user message as part of the preliminary chat history
            self.chat_history[1]["content"] += chat_input
        else:
            # Add subsequent user messages normally
            self.chat_history.append({"role": "user", "content": chat_input})

        # Send the user message to the Gemini model
        response = self.chat.send_message(self.chat_history[-1]["content"])

        # Process the response stream        
        self.output_text.insert(tk.END, response.text)
        self.output_text.see(tk.END)


        # Add assistant response to chat history
        self.chat_history.append({"role": "assistant", "content": response.text})

        # Display updated chat history
        self.display_chat_history()

        # Clear the chat input field
        self.chat_text.delete("1.0", tk.END)

    def restart_chat(self):
        self.chat_history = copy.deepcopy(self.chat_base)
        self.chat = self.model.start_chat(history=[])
        self.output_text.delete("1.0", tk.END)
        self.chat_text.delete("1.0", tk.END)

# Set up the main window
root = tk.Tk()
app = GeminiChatApp(root)
root.mainloop()