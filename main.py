import tkinter as tk
import customtkinter as ctk
import time
import math

# Set light appearance mode for normal reading view
ctk.set_appearance_mode("Light")
ctk.set_default_color_theme("blue")

# --- Scandinavian / Warm Paper Neutral Palette ---
BG_COLOR = "#f6f5f1"          # Soft warm linen / paper tone
CARD_BG = "#ffffff"           # Pure crisp white card surface
CARD_SURFACE = "#eeece6"      # Subtle elevated surface (stat boxes, numpad keys)
CARD_HOVER = "#e5e2da"        # Gentle hover for touch buttons
BORDER_COLOR = "#e2ded6"      # Soft border outline
ACCENT_BRASS = "#b3823c"      # Brushed brass / warm golden tone
ACCENT_DARK = "#292524"       # Deep warm charcoal for buttons and high contrast
ACCENT_DARK_HOVER = "#1c1917"
TEXT_PRIMARY = "#1c1917"      # Deep charcoal text
TEXT_SECONDARY = "#57534e"    # Warm slate gray
TEXT_MUTED = "#8f8a81"        # Muted caption gray
STREAK_BG = "#f8f3e8"         # Warm subtle amber tint
STREAK_BORDER = "#e8dbbe"
STREAK_TEXT = "#8a5814"       # Warm golden brown for streak text

# Standby Mode Colors
STANDBY_BG = "#000000"        # Pure black for screen standby
STANDBY_TRACK = "#1e1e1e"     # Dark progress bar background
STANDBY_BAR = "#c28535"       # Warm glowing amber/brass bar in the dark
STANDBY_TEXT_PAGES = "#e5e5e5"# Crisp stats text in the dark

IDLE_TIMEOUT_SECONDS = 15     # 15s inactivity triggers black standby screen


def draw_plant_on_canvas(canvas, alive=True, dark_mode=False, w=130, h=130):
    """
    Draws an aesthetic minimalist potted plant directly onto a native tkinter.Canvas.
    Requires zero PIL / ImageTk dependencies and runs natively on Python 3.7.3.
    """
    canvas.delete("all")

    cx = w / 2.0
    ground_y = h * 0.88
    pot_top_y = h * 0.64
    pot_top_w = w * 0.40
    pot_bot_w = w * 0.28

    if not dark_mode:
        bg_col = CARD_BG
        pot_color = "#d5cdc2"
        pot_outline = "#b5aa9b"
        soil_color = "#6e6255"
        if alive:
            stem_color = "#386641"
            leaf_fill = "#52b788"
            leaf_stroke = "#2d6a4f"
            sparkle_color = "#b3823c"
        else:
            stem_color = "#7d7465"
            leaf_fill = "#9c9284"
            leaf_stroke = "#6b6355"
    else:  # Standby / sleep mode
        bg_col = STANDBY_BG
        pot_color = "#24221f"
        pot_outline = "#423d37"
        soil_color = "#181614"
        if alive:
            stem_color = "#40916c"
            leaf_fill = "#52b788"
            leaf_stroke = "#74c69d"
            sparkle_color = "#e0a96d"
        else:
            stem_color = "#5c564c"
            leaf_fill = "#736b5f"
            leaf_stroke = "#8c8273"

    canvas.configure(bg=bg_col)

    # 1. Ceramic Pot Body (Tapered)
    p_tl = (cx - pot_top_w / 2.0, pot_top_y)
    p_tr = (cx + pot_top_w / 2.0, pot_top_y)
    p_br = (cx + pot_bot_w / 2.0, ground_y)
    p_bl = (cx - pot_bot_w / 2.0, ground_y)
    canvas.create_polygon(
        p_tl[0], p_tl[1],
        p_tr[0], p_tr[1],
        p_br[0], p_br[1],
        p_bl[0], p_bl[1],
        fill=pot_color,
        outline=pot_outline,
        width=2
    )

    # Pot Rim
    rim_pad = 4
    rim_h = 8
    rx0, ry0 = p_tl[0] - rim_pad, pot_top_y - rim_h / 2.0
    rx1, ry1 = p_tr[0] + rim_pad, pot_top_y + rim_h / 2.0
    canvas.create_rectangle(rx0, ry0, rx1, ry1, fill=pot_color, outline=pot_outline, width=2)

    # Soil line
    canvas.create_line(p_tl[0] + 3, pot_top_y, p_tr[0] - 3, pot_top_y, fill=soil_color, width=2)

    # 2. Plant Stem and Leaves
    if alive:
        # --- Upright, Thriving Plant ---
        stem_pts = []
        for t in range(25):
            prog = t / 24.0
            sx = cx + math.sin(prog * math.pi) * 7.0
            sy = pot_top_y - prog * (h * 0.44)
            stem_pts.extend([sx, sy])
        canvas.create_line(*stem_pts, fill=stem_color, width=3.5, capstyle="round", smooth=True)

        def draw_alive_leaf(lx, ly, angle_deg, l_len, l_w):
            rad = math.radians(angle_deg)
            tx = lx + math.cos(rad) * l_len
            ty = ly - math.sin(rad) * l_len
            px = -math.sin(rad) * l_w
            py = -math.cos(rad) * l_w
            mid_x = (lx + tx) / 2.0
            mid_y = (ly + ty) / 2.0
            canvas.create_polygon(
                lx, ly,
                mid_x + px, mid_y + py,
                tx, ty,
                mid_x - px, mid_y - py,
                fill=leaf_fill,
                outline=leaf_stroke,
                width=1.5,
                smooth=True
            )

        draw_alive_leaf(cx - 3, pot_top_y - 16, 145, 30, 12)
        draw_alive_leaf(cx + 7, pot_top_y - 24, 35, 32, 13)
        draw_alive_leaf(cx - 2, pot_top_y - 36, 150, 26, 11)
        draw_alive_leaf(cx + 6, pot_top_y - 46, 30, 28, 11)
        draw_alive_leaf(cx + 2, pot_top_y - 56, 80, 22, 9)
        draw_alive_leaf(cx - 2, pot_top_y - 56, 100, 22, 9)

        # Subtle gold sparkle near top
        sp_x = cx + 24
        sp_y = pot_top_y - 54
        canvas.create_line(sp_x - 4, sp_y, sp_x + 4, sp_y, fill=sparkle_color, width=2)
        canvas.create_line(sp_x, sp_y - 4, sp_x, sp_y + 4, fill=sparkle_color, width=2)

    else:
        # --- Wilted / Drooping Plant ---
        stem_pts = []
        for t in range(25):
            prog = t / 24.0
            sx = cx + prog * 28.0
            sy = pot_top_y - math.sin(prog * math.pi * 0.7) * 15.0 + (prog ** 2) * 26.0
            stem_pts.extend([sx, sy])
        canvas.create_line(*stem_pts, fill=stem_color, width=3.5, capstyle="round", smooth=True)

        def draw_droop_leaf(lx, ly, angle_deg, l_len, l_w):
            rad = math.radians(angle_deg)
            tx = lx + math.cos(rad) * l_len
            ty = ly + math.sin(rad) * l_len
            px = -math.sin(rad) * l_w
            py = math.cos(rad) * l_w
            mid_x = (lx + tx) / 2.0
            mid_y = (ly + ty) / 2.0
            canvas.create_polygon(
                lx, ly,
                mid_x + px, mid_y + py,
                tx, ty,
                mid_x - px, mid_y - py,
                fill=leaf_fill,
                outline=leaf_stroke,
                width=1.5,
                smooth=True
            )

        draw_droop_leaf(cx + 10, pot_top_y - 6, 75, 24, 9)
        draw_droop_leaf(cx + 20, pot_top_y + 2, 85, 26, 10)
        tip_x, tip_y = stem_pts[-2], stem_pts[-1]
        draw_droop_leaf(tip_x, tip_y, 80, 22, 9)

        # Fallen dry leaf on the ground
        fallen_x = cx - 26
        fallen_y = ground_y - 2
        draw_droop_leaf(fallen_x, fallen_y, 10, 18, 6)


class BookshelfApp(ctk.CTk):
    def __init__(self):
        super().__init__()

        self.title("Kirjateline • Lukuseuranta")
        self.geometry("680x560")
        self.minsize(560, 480)
        self.attributes("-fullscreen", True)
        self.configure(fg_color=BG_COLOR)

        # Single active book tracked directly
        self.current_page = 0
        self.total_pages = 350

        # Lukuputki alkaa aina nollasta ilman kellointegraatiota
        self.streak_count = 0

        # Kasvin tila: alussa kuihtunut, muuttuu eläväksi kun sivumäärää päivitetään
        self.is_plant_alive = False
        self.plant_w = 125
        self.plant_h = 125

        # UI State: "summary" or "numpad"
        self.current_view_mode = "summary"
        self.numpad_mode = "current_page"  # "current_page" or "total_pages"
        self.numpad_input_str = ""
        self.numpad_fresh = False

        # Idle / Standby Tracking
        self.is_standby = False
        self.idle_timer_id = None
        self.last_interaction_time = time.time()

        self._build_ui()
        self._build_standby_overlay()
        self._refresh_all_views()

        # Global event listeners for touchscreen taps, mouse clicks & movement
        self.bind_all("<ButtonPress>", self._on_user_activity)
        self.bind_all("<KeyRelease>", self._on_key_release)
        self.bind_all("<Motion>", self._on_user_motion)

        # Start 15s timer
        self._schedule_idle_check()

    def _build_ui(self):
        # 1. TOP HEADER (Left: "Uusi kirja", Right: Close & Streak badge)
        self.header_frame = ctk.CTkFrame(
            self,
            fg_color=CARD_BG,
            corner_radius=0,
            height=62,
            border_width=0
        )
        self.header_frame.pack(fill="x", side="top")
        self.header_frame.pack_propagate(False)

        hairline = ctk.CTkFrame(self, fg_color=BORDER_COLOR, height=1, corner_radius=0)
        hairline.pack(fill="x", side="top")

        # --- "Uusi kirja" BUTTON (TOP-LEFT) ---
        self.new_book_btn = ctk.CTkButton(
            self.header_frame,
            text="Uusi kirja",
            height=36,
            corner_radius=8,
            fg_color=CARD_SURFACE,
            hover_color=CARD_HOVER,
            text_color=TEXT_PRIMARY,
            border_width=1,
            border_color=BORDER_COLOR,
            font=ctk.CTkFont(size=12, weight="bold"),
            command=self._show_numpad_for_new_book
        )
        self.new_book_btn.pack(side="left", padx=(28, 0), pady=13)

        # --- CLOSE BUTTON (TOP-RIGHT) ---
        self.close_btn = ctk.CTkButton(
            self.header_frame,
            text="X",
            width=32,
            height=32,
            corner_radius=8,
            fg_color=CARD_SURFACE,
            hover_color=CARD_HOVER,
            text_color=TEXT_PRIMARY,
            border_width=1,
            border_color=BORDER_COLOR,
            font=ctk.CTkFont(size=14, weight="bold"),
            command=self.destroy
        )
        self.close_btn.pack(side="right", padx=(0, 12), pady=15)

        # --- STREAK BADGE (TOP-RIGHT, ONLY TEXT AND NUMBER, STARTS AT 0) ---
        self.streak_badge = ctk.CTkFrame(
            self.header_frame,
            fg_color=STREAK_BG,
            corner_radius=14,
            border_width=1,
            border_color=STREAK_BORDER
        )
        self.streak_badge.pack(side="right", padx=(0, 12), pady=13)

        self.streak_text = ctk.CTkLabel(
            self.streak_badge,
            text="Putki: 0 päivää",
            font=ctk.CTkFont(size=12, weight="bold"),
            text_color=STREAK_TEXT
        )
        self.streak_text.pack(padx=14, pady=5)

        # 2. BOTTOM PERSISTENT PROGRESS BAR
        self.footer_frame = ctk.CTkFrame(
            self,
            fg_color=CARD_BG,
            corner_radius=0,
            height=82,
            border_width=0
        )
        self.footer_frame.pack(fill="x", side="bottom")
        self.footer_frame.pack_propagate(False)

        footer_hairline = ctk.CTkFrame(self, fg_color=BORDER_COLOR, height=1, corner_radius=0)
        footer_hairline.pack(fill="x", side="bottom")

        footer_inner = ctk.CTkFrame(self.footer_frame, fg_color="transparent")
        footer_inner.pack(fill="both", expand=True, padx=28, pady=10)

        # Stats row
        meta_row = ctk.CTkFrame(footer_inner, fg_color="transparent")
        meta_row.pack(fill="x", pady=(0, 5))

        self.footer_title_lbl = ctk.CTkLabel(
            meta_row,
            text="Edistyminen",
            font=ctk.CTkFont(size=12, weight="bold"),
            text_color=TEXT_SECONDARY,
            anchor="w"
        )
        self.footer_title_lbl.pack(side="left")

        self.footer_pct_lbl = ctk.CTkLabel(
            meta_row,
            text="0%",
            font=ctk.CTkFont(size=13, weight="bold"),
            text_color=TEXT_PRIMARY,
            anchor="e"
        )
        self.footer_pct_lbl.pack(side="right")

        # Progress Bar
        self.progress_bar = ctk.CTkProgressBar(
            footer_inner,
            height=8,
            corner_radius=4,
            fg_color=CARD_SURFACE,
            progress_color=ACCENT_DARK
        )
        self.progress_bar.pack(fill="x")
        self.progress_bar.set(0)

        # Footer Subtext
        self.footer_sub_lbl = ctk.CTkLabel(
            footer_inner,
            text="",
            font=ctk.CTkFont(size=11),
            text_color=TEXT_MUTED
        )
        self.footer_sub_lbl.pack(anchor="w", pady=(3, 0))

        # 3. MAIN BODY CONTAINER
        self.body_container = ctk.CTkFrame(self, fg_color="transparent")
        self.body_container.pack(fill="both", expand=True, padx=28, pady=18)

        # Main Card
        self.main_card = ctk.CTkFrame(
            self.body_container,
            fg_color=CARD_BG,
            corner_radius=16,
            border_width=1,
            border_color=BORDER_COLOR
        )
        self.main_card.pack(fill="both", expand=True)

        # --- VIEW 1: Reading Summary Frame ---
        self.summary_frame = ctk.CTkFrame(self.main_card, fg_color="transparent")
        self._build_summary_view()

        # --- VIEW 2: Pure On-Screen Touch Numpad Frame ---
        self.numpad_frame = ctk.CTkFrame(self.main_card, fg_color="transparent")
        self._build_numpad_view()

        # Start with summary view visible
        self.summary_frame.pack(fill="both", expand=True, padx=30, pady=22)

    def _build_summary_view(self):
        """Standard reading overview with native Canvas plant illustration in the center."""
        # Stat Card (Clean neutral tone box)
        self.stat_box = ctk.CTkFrame(
            self.summary_frame,
            fg_color=CARD_SURFACE,
            corner_radius=14,
            border_width=1,
            border_color=BORDER_COLOR
        )
        self.stat_box.pack(fill="x", pady=(0, 10))

        stat_inner = ctk.CTkFrame(self.stat_box, fg_color="transparent")
        stat_inner.pack(fill="x", padx=26, pady=16)

        left_stat = ctk.CTkFrame(stat_inner, fg_color="transparent")
        left_stat.pack(side="left")

        page_caption = ctk.CTkLabel(
            left_stat,
            text="Nykyinen sivu",
            font=ctk.CTkFont(size=12),
            text_color=TEXT_MUTED
        )
        page_caption.pack(anchor="w")

        self.hero_page_big = ctk.CTkLabel(
            left_stat,
            text="0",
            font=ctk.CTkFont(size=38, weight="bold"),
            text_color=TEXT_PRIMARY
        )
        self.hero_page_big.pack(anchor="w")

        self.hero_total_lbl = ctk.CTkLabel(
            left_stat,
            text="/ 0 sivua",
            font=ctk.CTkFont(size=13),
            text_color=TEXT_SECONDARY
        )
        self.hero_total_lbl.pack(anchor="w")

        right_stat = ctk.CTkFrame(stat_inner, fg_color="transparent")
        right_stat.pack(side="right")

        self.hero_pct_big = ctk.CTkLabel(
            right_stat,
            text="0%",
            font=ctk.CTkFont(size=36, weight="bold"),
            text_color=ACCENT_DARK
        )
        self.hero_pct_big.pack(anchor="e")

        self.hero_rem_lbl = ctk.CTkLabel(
            right_stat,
            text="0 sivua jäljellä",
            font=ctk.CTkFont(size=13),
            text_color=TEXT_MUTED
        )
        self.hero_rem_lbl.pack(anchor="e")

        # --- CENTER PLANT DISPLAY (Native tk.Canvas - no PIL.ImageTk needed) ---
        self.plant_frame = ctk.CTkFrame(self.summary_frame, fg_color="transparent")
        self.plant_frame.pack(fill="both", expand=True, pady=(2, 8))

        self.plant_canvas = tk.Canvas(
            self.plant_frame,
            width=self.plant_w,
            height=self.plant_h,
            bg=CARD_BG,
            highlightthickness=0,
            bd=0
        )
        self.plant_canvas.pack(expand=True)

        # "Päivitä sivu, jolla olet" Button
        self.add_pages_btn = ctk.CTkButton(
            self.summary_frame,
            text="Päivitä sivu, jolla olet",
            height=50,
            corner_radius=12,
            fg_color=ACCENT_DARK,
            hover_color=ACCENT_DARK_HOVER,
            text_color="#ffffff",
            font=ctk.CTkFont(size=15, weight="bold"),
            command=self._show_numpad_for_current_page
        )
        self.add_pages_btn.pack(fill="x", pady=(0, 4))

    def _build_numpad_view(self):
        """Pure on-screen touch numpad directly in the same window (no separate popup windows)."""
        numpad_head = ctk.CTkFrame(self.numpad_frame, fg_color="transparent")
        numpad_head.pack(fill="x", pady=(0, 10))

        self.numpad_tag_lbl = ctk.CTkLabel(
            numpad_head,
            text="MERKITSE SIVU • KOSKETUSNÄPPÄIMISTÖ",
            font=ctk.CTkFont(size=11, weight="bold"),
            text_color=ACCENT_BRASS,
            anchor="w"
        )
        self.numpad_tag_lbl.pack(anchor="w")

        key_container = ctk.CTkFrame(self.numpad_frame, fg_color="transparent")
        key_container.pack(fill="both", expand=True)

        key_container.grid_columnconfigure(0, weight=4)
        key_container.grid_columnconfigure(1, weight=5)
        key_container.grid_rowconfigure(0, weight=1)

        # --- LEFT COLUMN: Digital Page Display + Action Buttons ---
        left_col = ctk.CTkFrame(key_container, fg_color="transparent")
        left_col.grid(row=0, column=0, sticky="nsew", padx=(0, 16))

        disp_card = ctk.CTkFrame(
            left_col,
            fg_color=CARD_SURFACE,
            corner_radius=12,
            border_width=1,
            border_color=BORDER_COLOR
        )
        disp_card.pack(fill="x", pady=(0, 14))

        self.numpad_sub_lbl = ctk.CTkLabel(
            disp_card,
            text="Syötetty sivu",
            font=ctk.CTkFont(size=11),
            text_color=TEXT_MUTED
        )
        self.numpad_sub_lbl.pack(pady=(12, 0))

        self.numpad_display_num = ctk.CTkLabel(
            disp_card,
            text="0",
            font=ctk.CTkFont(size=44, weight="bold"),
            text_color=TEXT_PRIMARY
        )
        self.numpad_display_num.pack(pady=(2, 0))

        self.numpad_display_meta = ctk.CTkLabel(
            disp_card,
            text="/ 0 sivua (0%)",
            font=ctk.CTkFont(size=12, weight="bold"),
            text_color=ACCENT_BRASS
        )
        self.numpad_display_meta.pack(pady=(2, 14))

        self.numpad_save_btn = ctk.CTkButton(
            left_col,
            text="Tallenna sivu ✓",
            height=46,
            corner_radius=10,
            fg_color=ACCENT_DARK,
            hover_color=ACCENT_DARK_HOVER,
            text_color="#ffffff",
            font=ctk.CTkFont(size=13, weight="bold"),
            command=self._confirm_numpad
        )
        self.numpad_save_btn.pack(fill="x", pady=(0, 8))

        cancel_btn = ctk.CTkButton(
            left_col,
            text="Peruuta",
            height=42,
            corner_radius=10,
            fg_color=CARD_BG,
            hover_color=CARD_HOVER,
            text_color=TEXT_SECONDARY,
            border_width=1,
            border_color=BORDER_COLOR,
            font=ctk.CTkFont(size=12),
            command=self._show_summary_view
        )
        cancel_btn.pack(fill="x")

        # --- RIGHT COLUMN: Pure Touch Keypad Grid ---
        keys_col = ctk.CTkFrame(key_container, fg_color="transparent")
        keys_col.grid(row=0, column=1, sticky="nsew")

        keys = [
            ["1", "2", "3"],
            ["4", "5", "6"],
            ["7", "8", "9"],
            ["C", "0", "⌫"]
        ]

        for r, row in enumerate(keys):
            keys_col.grid_rowconfigure(r, weight=1)
            for c, key in enumerate(row):
                keys_col.grid_columnconfigure(c, weight=1)
                if key == "C":
                    cmd = self._numpad_clear
                    fg = "#fdf2f2"
                    hover = "#fee2e2"
                    txt_col = "#dc2626"
                elif key == "⌫":
                    cmd = self._numpad_backspace
                    fg = CARD_SURFACE
                    hover = CARD_HOVER
                    txt_col = TEXT_PRIMARY
                else:
                    cmd = lambda num=key: self._numpad_append(num)
                    fg = CARD_SURFACE
                    hover = CARD_HOVER
                    txt_col = TEXT_PRIMARY

                btn = ctk.CTkButton(
                    keys_col,
                    text=key,
                    corner_radius=10,
                    fg_color=fg,
                    hover_color=hover,
                    text_color=txt_col,
                    border_width=1,
                    border_color=BORDER_COLOR,
                    font=ctk.CTkFont(size=20, weight="bold"),
                    command=cmd
                )
                btn.grid(row=r, column=c, padx=3, pady=3, sticky="nsew")

    def _show_numpad_for_current_page(self):
        """Switches in-place to numpad for updating current reading page."""
        self.numpad_mode = "current_page"
        self.numpad_tag_lbl.configure(text="MERKITSE SIVU • KOSKETUSNÄPPÄIMISTÖ")
        self.numpad_sub_lbl.configure(text="Nykyinen sivu")
        self.numpad_save_btn.configure(text="Tallenna sivu ✓")
        self.numpad_input_str = str(self.current_page) if self.current_page > 0 else ""
        self.numpad_fresh = True
        self._update_numpad_display()

        self.summary_frame.pack_forget()
        self.numpad_frame.pack(fill="both", expand=True, padx=26, pady=16)
        self.current_view_mode = "numpad"

    def _show_numpad_for_new_book(self):
        """Switches in-place to numpad for setting new book's total pages."""
        self.numpad_mode = "total_pages"
        self.numpad_tag_lbl.configure(text="UUSI KIRJA • KOKONAISSIVUMÄÄRÄ")
        self.numpad_sub_lbl.configure(text="Kirjan sivumäärä yhteensä")
        self.numpad_save_btn.configure(text="Aloita kirja ✓")
        self.numpad_input_str = ""
        self.numpad_fresh = False
        self._update_numpad_display()

        self.summary_frame.pack_forget()
        self.numpad_frame.pack(fill="both", expand=True, padx=26, pady=16)
        self.current_view_mode = "numpad"

    def _show_summary_view(self):
        """Transitions back to the reading summary card."""
        self.numpad_frame.pack_forget()
        self.summary_frame.pack(fill="both", expand=True, padx=30, pady=22)
        self.current_view_mode = "summary"

    def _update_numpad_display(self):
        val = self.numpad_input_str if self.numpad_input_str else "0"
        self.numpad_display_num.configure(text=val)

        if self.numpad_mode == "current_page":
            try:
                num = int(val)
                pct = min(100.0, (num / self.total_pages) * 100) if self.total_pages > 0 else 0
                self.numpad_display_meta.configure(text=f"/ {self.total_pages} sivua  ({pct:.0f}%)")
            except ValueError:
                self.numpad_display_meta.configure(text=f"/ {self.total_pages} sivua")
        else:
            self.numpad_display_meta.configure(text="sivua yhteensä")

    def _numpad_append(self, digit):
        if self.numpad_fresh:
            self.numpad_input_str = ""
            self.numpad_fresh = False

        if len(self.numpad_input_str) >= 5:
            return
        if self.numpad_input_str == "0":
            self.numpad_input_str = digit
        else:
            self.numpad_input_str += digit

        if self.numpad_mode == "current_page":
            try:
                if int(self.numpad_input_str) > self.total_pages:
                    self.numpad_input_str = str(self.total_pages)
            except ValueError:
                pass

        self._update_numpad_display()

    def _numpad_backspace(self):
        self.numpad_fresh = False
        if self.numpad_input_str:
            self.numpad_input_str = self.numpad_input_str[:-1]
            self._update_numpad_display()

    def _numpad_clear(self):
        self.numpad_fresh = False
        self.numpad_input_str = ""
        self._update_numpad_display()

    def _confirm_numpad(self):
        try:
            val = int(self.numpad_input_str) if self.numpad_input_str else 0
        except ValueError:
            val = 0

        if self.numpad_mode == "current_page":
            if val > self.total_pages:
                val = self.total_pages
            self.current_page = val
            # Updating page brings the plant to life and raises streak to 1!
            self.is_plant_alive = True
            self.streak_count = 1
        else:
            if val <= 0:
                return  # Must be positive page count
            self.total_pages = val
            self.current_page = 0
            # New book starts fresh with wilted plant & streak at 0
            self.is_plant_alive = False
            self.streak_count = 0

        self._show_summary_view()
        self._refresh_all_views()

    # --- 4. 15-SECOND BLACK STANDBY SCREEN SAVER ---
    def _build_standby_overlay(self):
        """Full-screen pitch black standby overlay with plant and large clean progress bar."""
        self.standby_frame = ctk.CTkFrame(
            self,
            fg_color=STANDBY_BG,
            corner_radius=0
        )

        center_box = ctk.CTkFrame(self.standby_frame, fg_color="transparent")
        center_box.place(relx=0.5, rely=0.5, anchor="center")

        # Plant also visible in sleep mode (native tk.Canvas)
        self.standby_plant_canvas = tk.Canvas(
            center_box,
            width=self.plant_w,
            height=self.plant_h,
            bg=STANDBY_BG,
            highlightthickness=0,
            bd=0
        )
        self.standby_plant_canvas.pack(pady=(0, 18))

        # Big, sleek progress bar in center
        self.standby_progress = ctk.CTkProgressBar(
            center_box,
            width=480,
            height=18,
            corner_radius=9,
            fg_color=STANDBY_TRACK,
            progress_color=STANDBY_BAR
        )
        self.standby_progress.pack(pady=(0, 16))

        # Page stats and percentage underneath
        self.standby_stats = ctk.CTkLabel(
            center_box,
            text="",
            font=ctk.CTkFont(size=18, weight="bold"),
            text_color=STANDBY_TEXT_PAGES
        )
        self.standby_stats.pack()

    def _enter_standby(self):
        """Activates pitch black standby screen with plant and large progress bar."""
        if not self.is_standby:
            self.is_standby = True
            pct = (self.current_page / self.total_pages * 100) if self.total_pages > 0 else 0
            self.standby_stats.configure(text=f"{self.current_page} / {self.total_pages} sivua  •  {pct:.0f}%")
            self.standby_progress.set(min(1.0, self.current_page / max(1, self.total_pages)))

            draw_plant_on_canvas(
                self.standby_plant_canvas,
                alive=self.is_plant_alive,
                dark_mode=True,
                w=self.plant_w,
                h=self.plant_h
            )

            self.standby_frame.place(relx=0, rely=0, relwidth=1, relheight=1)
            self.standby_frame.lift()

    def _exit_standby(self):
        """Wakes up from standby screen."""
        if self.is_standby:
            self.is_standby = False
            self.standby_frame.place_forget()
            self.last_interaction_time = time.time()
            self._schedule_idle_check()

    def _on_user_activity(self, event=None):
        """Fires on any touch tap or mouse click."""
        if self.is_standby:
            self._exit_standby()
            return
        self.last_interaction_time = time.time()
        self._schedule_idle_check()

    def _on_key_release(self, event=None):
        """Handles physical keyboard presses if used."""
        if self.is_standby:
            self._exit_standby()
            return
        self.last_interaction_time = time.time()
        self._schedule_idle_check()

        if self.current_view_mode == "numpad" and event is not None:
            if event.keysym in ("Return", "KP_Enter"):
                self._confirm_numpad()
            elif event.keysym == "Escape":
                self._show_summary_view()
            elif event.keysym == "BackSpace":
                self._numpad_backspace()
            elif event.char and event.char.isdigit():
                self._numpad_append(event.char)

    def _on_user_motion(self, event=None):
        """Throttled motion check."""
        if self.is_standby:
            self._exit_standby()
            return
        now = time.time()
        if now - self.last_interaction_time >= 1.0:
            self.last_interaction_time = now
            self._schedule_idle_check()

    def _schedule_idle_check(self):
        """Schedules standby transition after IDLE_TIMEOUT_SECONDS."""
        if self.idle_timer_id is not None:
            try:
                self.after_cancel(self.idle_timer_id)
            except Exception:
                pass
        self.idle_timer_id = self.after(IDLE_TIMEOUT_SECONDS * 1000, self._check_idle)

    def _check_idle(self):
        now = time.time()
        idle_elapsed = now - self.last_interaction_time
        if idle_elapsed >= IDLE_TIMEOUT_SECONDS:
            self._enter_standby()
        else:
            remaining_ms = int((IDLE_TIMEOUT_SECONDS - idle_elapsed) * 1000)
            self.idle_timer_id = self.after(max(100, remaining_ms), self._check_idle)

    def _refresh_all_views(self):
        cur = self.current_page
        total = self.total_pages
        pct = (cur / total * 100) if total > 0 else 0
        left = max(0, total - cur)

        # Update Reading Summary Card
        self.hero_page_big.configure(text=str(cur))
        self.hero_total_lbl.configure(text=f"/ {total} sivua")
        self.hero_pct_big.configure(text=f"{pct:.0f}%")

        if cur >= total and total > 0:
            self.hero_rem_lbl.configure(text="Valmis! Luettu loppuun", text_color="#15803d")
        else:
            self.hero_rem_lbl.configure(text=f"{left} sivua jäljellä", text_color=TEXT_MUTED)

        # Update Center Plant Canvas (wilted vs alive)
        draw_plant_on_canvas(
            self.plant_canvas,
            alive=self.is_plant_alive,
            dark_mode=False,
            w=self.plant_w,
            h=self.plant_h
        )
        draw_plant_on_canvas(
            self.standby_plant_canvas,
            alive=self.is_plant_alive,
            dark_mode=True,
            w=self.plant_w,
            h=self.plant_h
        )

        # Update Streak Badge (starts at 0, rises to 1 on update)
        if self.streak_count == 1:
            self.streak_text.configure(text="Putki: 1 päivä")
        else:
            self.streak_text.configure(text=f"Putki: {self.streak_count} päivää")

        # Update Bottom Persistent Progress Bar
        self.footer_title_lbl.configure(text=f"Edistyminen: {cur} / {total} sivua")
        self.footer_pct_lbl.configure(text=f"{pct:.1f}%")
        self.progress_bar.set(min(1.0, cur / max(1, total)))

        if cur >= total and total > 0:
            self.footer_sub_lbl.configure(text="Kirja on luettu loppuun!", text_color="#15803d")
        else:
            self.footer_sub_lbl.configure(text=f"{left} sivua jäljellä maaliin.", text_color=TEXT_MUTED)


if __name__ == "__main__":
    app = BookshelfApp()
    app.mainloop()
