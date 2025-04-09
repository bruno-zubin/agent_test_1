import tkinter as tk
from tkinter import ttk
import threading
import time
from main import chat_with_llm

class RetroChatUI:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("Retro LLM Chat")
        self.root.geometry("800x600")
        
        # Configure theme
        self.root.configure(bg="#1E1E1E")
        
        # Main container
        self.main_frame = tk.Frame(self.root, bg="#1E1E1E")
        self.main_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        # Chat display
        self.chat_display = tk.Text(
            self.main_frame,
            wrap=tk.WORD,
            bg="#1E1E1E",
            font=("Consolas", 12),
            insertbackground="#CCCCCC"
        )
        self.chat_display.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)
        self.chat_display.config(state=tk.DISABLED)
        
        # Input frame
        self.input_frame = tk.Frame(self.main_frame, bg="#1E1E1E")
        self.input_frame.pack(fill=tk.X, padx=5, pady=5)
        
        # Message input
        self.message_input = tk.Entry(
            self.input_frame,
            font=("Consolas", 12),
            bg="#2D2D2D",
            fg="#CCCCCC",
            insertbackground="#CCCCCC"
        )
        self.message_input.pack(side=tk.LEFT, fill=tk.X, expand=True, padx=(0, 5))
        self.message_input.bind("<Return>", self.send_message)
        
        # Send button
        self.send_button = tk.Button(
            self.input_frame,
            text="Send",
            command=self.send_message,
            width=10,
            bg="#2D2D2D",
            fg="#CCCCCC",
            font=("Consolas", 12),
            relief=tk.FLAT,
            activebackground="#3D3D3D",
            activeforeground="#CCCCCC"
        )
        self.send_button.pack(side=tk.RIGHT)
        
        # Configure tags for different text colors
        self.chat_display.tag_configure("user", foreground="#AAAAAA")  # Light grey
        self.chat_display.tag_configure("assistant", foreground="#CCCCCC")  # Lighter grey
        self.chat_display.tag_configure("thinking", foreground="#888888")  # Medium grey
        
        # Thinking animation variables
        self.thinking = False
        self.thinking_dots = 0
        
    def add_message(self, message, is_user=True):
        self.chat_display.config(state=tk.NORMAL)
        tag = "user" if is_user else "assistant"
        self.chat_display.insert(tk.END, f"{'You' if is_user else 'Assistant'}: ", tag)
        self.chat_display.insert(tk.END, f"{message}\n\n", tag)
        self.chat_display.config(state=tk.DISABLED)
        self.chat_display.see(tk.END)
        
    def update_thinking_animation(self):
        if self.thinking:
            self.chat_display.config(state=tk.NORMAL)
            # Remove previous thinking message
            self.chat_display.delete("end-3c linestart", "end-1c lineend")
            # Add updated thinking message
            self.chat_display.insert(tk.END, f"Assistant: Thinking{'.' * self.thinking_dots}\n\n", "thinking")
            self.chat_display.config(state=tk.DISABLED)
            self.chat_display.see(tk.END)
            
            self.thinking_dots = (self.thinking_dots + 1) % 4
            self.root.after(500, self.update_thinking_animation)
        
    def get_llm_response(self, message):
        # Start thinking animation
        self.thinking = True
        self.thinking_dots = 0
        self.root.after(0, self.update_thinking_animation)
        
        # Get response from LLM
        response = chat_with_llm(message)
        
        # Stop thinking animation
        self.thinking = False
        
        # Add response
        if response:
            self.root.after(0, lambda: self.add_message(response, False))
        else:
            self.root.after(0, lambda: self.add_message("Sorry, I couldn't get a response.", False))
        
    def send_message(self, event=None):
        message = self.message_input.get().strip()
        if message:
            self.add_message(message, True)
            self.message_input.delete(0, tk.END)
            
            # Get response from LLM in a separate thread
            threading.Thread(target=self.get_llm_response, args=(message,), daemon=True).start()
    
    def run(self):
        self.root.mainloop()

if __name__ == "__main__":
    app = RetroChatUI()
    app.run()