import customtkinter as ctk

# Appearance settings
ctk.set_appearance_mode("System")
ctk.set_default_color_theme("blue")


class SmallTestApp(ctk.CTk):
    def __init__(self):
        super().__init__()

        self.title("Pi Test")
        self.geometry("380x300")
        self.resizable(False, False)

        self.counter = 0

        # Title Label
        self.label = ctk.CTkLabel(
            self,
            text="Raspberry Pi Test",
            font=ctk.CTkFont(size=20, weight="bold"),
        )
        self.label.pack(pady=(20, 10))

        # Counter display & button
        self.counter_label = ctk.CTkLabel(
            self,
            text="Clicks: 0",
            font=ctk.CTkFont(size=16),
        )
        self.counter_label.pack(pady=5)

        self.click_btn = ctk.CTkButton(
            self,
            text="Click Me",
            command=self.on_click,
        )
        self.click_btn.pack(pady=10)

        # Text input & echo
        self.entry = ctk.CTkEntry(
            self,
            placeholder_text="Type something...",
            width=260,
        )
        self.entry.pack(pady=10)
        self.entry.bind("<KeyRelease>", self.on_text_change)

        self.echo_label = ctk.CTkLabel(
            self,
            text="",
            text_color="gray",
        )
        self.echo_label.pack(pady=5)

    def on_click(self):
        self.counter += 1
        self.counter_label.configure(text=f"Clicks: {self.counter}")

    def on_text_change(self, event=None):
        text = self.entry.get().strip()
        self.echo_label.configure(text=text if text else "")


if __name__ == "__main__":
    app = SmallTestApp()
    app.mainloop()
