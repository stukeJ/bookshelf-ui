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


def get_plant_phase(streak):
    """Maps reading streak to plant growth phase (1 = wilted, 2..5 = growing to blooming)."""
    if streak > 10:
        return 5
    elif streak > 7:
        return 4
    elif streak > 4:
        return 3
    elif streak >= 1:
        return 2
    else:
        return 1


def draw_plant_on_canvas(canvas, phase=1, dark_mode=False, w=110, h=110):
    """
    Draws an aesthetic minimalist potted plant in 5 cohesive growth phases (1..5)
    directly onto a native tkinter.Canvas.
    Phase 1: Wilted (streak == 0)
    Phase 2: Sprouting (streak 1..4)
    Phase 3: Growing (streak 5..7)
    Phase 4: Thriving full foliage (streak 8..10)
    Phase 5: Full bloom with Scandinavian blossoms (streak > 10)
    Requires zero PIL / ImageTk dependencies and runs natively on Python 3.7.3.
    """
    canvas.delete("all")
    phase = max(1, min(5, int(phase)))

    s = min(w, h) / 130.0
    cx = w / 2.0
    ground_y = h * 0.88
    pot_top_y = h * 0.64
    pot_top_w = w * 0.40
    pot_bot_w = w * 0.28

    if not dark_mode:
        bg_col = CARD_SURFACE
        pot_color = "#d5cdc2"
        pot_outline = "#b5aa9b"
        soil_color = "#6e6255"
        sparkle_color = "#b3823c"
        petal_fill = "#fffaf0"
        petal_stroke = "#d4c3a3"
        bloom_center = "#c88a2e"
        if phase == 1:
            stem_color = "#7d7465"
            leaf_fill = "#9c9284"
            leaf_stroke = "#6b6355"
        elif phase == 2:
            stem_color = "#4a7c59"
            leaf_fill = "#74c69d"
            leaf_stroke = "#40916c"
        elif phase == 3:
            stem_color = "#3f734d"
            leaf_fill = "#60bf90"
            leaf_stroke = "#347a5b"
        else:  # Phase 4 & 5
            stem_color = "#386641"
            leaf_fill = "#52b788"
            leaf_stroke = "#2d6a4f"
    else:  # Standby / sleep mode
        bg_col = STANDBY_BG
        pot_color = "#24221f"
        pot_outline = "#423d37"
        soil_color = "#181614"
        sparkle_color = "#e0a96d"
        petal_fill = "#f5ebd6"
        petal_stroke = "#b8a686"
        bloom_center = "#e0a96d"
        if phase == 1:
            stem_color = "#5c564c"
            leaf_fill = "#736b5f"
            leaf_stroke = "#8c8273"
        elif phase == 2:
            stem_color = "#4d8b6b"
            leaf_fill = "#6bc49c"
            leaf_stroke = "#86d4b0"
        elif phase == 3:
            stem_color = "#468e6b"
            leaf_fill = "#5cbe91"
            leaf_stroke = "#7bcfab"
        else:  # Phase 4 & 5
            stem_color = "#40916c"
            leaf_fill = "#52b788"
            leaf_stroke = "#74c69d"

    canvas.configure(bg=bg_col)

    # 1. Ceramic Pot Body (Tapered — identical across all 5 phases)
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
    rim_pad = 4 * s
    rim_h = 8 * s
    rx0, ry0 = p_tl[0] - rim_pad, pot_top_y - rim_h / 2.0
    rx1, ry1 = p_tr[0] + rim_pad, pot_top_y + rim_h / 2.0
    canvas.create_rectangle(rx0, ry0, rx1, ry1, fill=pot_color, outline=pot_outline, width=2)

    # Soil line
    canvas.create_line(p_tl[0] + 3 * s, pot_top_y, p_tr[0] - 3 * s, pot_top_y, fill=soil_color, width=2)

    # Helper to draw the species' signature smooth teardrop leaf
    def draw_leaf(lx, ly, angle_deg, l_len, l_w, droop=False):
        rad = math.radians(angle_deg)
        if droop:
            tx = lx + math.cos(rad) * l_len
            ty = ly + math.sin(rad) * l_len
            px = -math.sin(rad) * l_w
            py = math.cos(rad) * l_w
        else:
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

    def draw_sparkle(sp_x, sp_y, r):
        canvas.create_line(sp_x - r, sp_y, sp_x + r, sp_y, fill=sparkle_color, width=2)
        canvas.create_line(sp_x, sp_y - r, sp_x, sp_y + r, fill=sparkle_color, width=2)

    def draw_blossom(bx, by, petal_r):
        dist = petal_r * 0.95
        for k in range(5):
            ang = math.radians(k * 72 - 90)
            px = bx + math.cos(ang) * dist
            py = by + math.sin(ang) * dist
            canvas.create_oval(
                px - petal_r, py - petal_r,
                px + petal_r, py + petal_r,
                fill=petal_fill,
                outline=petal_stroke,
                width=1
            )
        cr = petal_r * 0.72
        canvas.create_oval(
            bx - cr, by - cr,
            bx + cr, by + cr,
            fill=bloom_center,
            outline=""
        )

    # 2. Plant Stem, Leaves & Blooms by Growth Phase
    if phase == 1:
        # --- Phase 1: Wilted / Drooping Plant ---
        stem_pts = []
        for t in range(25):
            prog = t / 24.0
            sx = cx + prog * (28.0 * s)
            sy = pot_top_y - math.sin(prog * math.pi * 0.7) * (15.0 * s) + (prog ** 2) * (26.0 * s)
            stem_pts.extend([sx, sy])
        canvas.create_line(*stem_pts, fill=stem_color, width=3.5, capstyle="round", smooth=True)

        draw_leaf(cx + 10 * s, pot_top_y - 6 * s, 75, 24 * s, 9 * s, droop=True)
        draw_leaf(cx + 20 * s, pot_top_y + 2 * s, 85, 26 * s, 10 * s, droop=True)
        tip_x, tip_y = stem_pts[-2], stem_pts[-1]
        draw_leaf(tip_x, tip_y, 80, 22 * s, 9 * s, droop=True)

        # Fallen dry leaf on the ground
        draw_leaf(cx - 26 * s, ground_y - 2 * s, 10, 18 * s, 6 * s, droop=True)
        return

    # Shared upright S-curve stem trajectory for Phases 2..5 (clearly the same plant growing taller)
    height_ratios = {2: 0.21, 3: 0.33, 4: 0.44, 5: 0.44}
    sway_mults = {2: 0.50, 3: 0.78, 4: 1.00, 5: 1.00}
    stem_widths = {2: 2.8, 3: 3.2, 4: 3.5, 5: 3.8}

    h_ratio = height_ratios[phase]
    sway = sway_mults[phase]

    def stem_xy(prog):
        sx = cx + math.sin(prog * math.pi) * (7.0 * s * sway)
        sy = pot_top_y - prog * (h * h_ratio)
        return sx, sy

    stem_pts = []
    for t in range(25):
        sx, sy = stem_xy(t / 24.0)
        stem_pts.extend([sx, sy])
    canvas.create_line(*stem_pts, fill=stem_color, width=stem_widths[phase], capstyle="round", smooth=True)

    tip_x, tip_y = stem_xy(1.0)

    if phase == 2:
        # --- Phase 2: Reviving Sprout (short upright stem + first 2 young leaves + bud) ---
        lx1, ly1 = stem_xy(0.45)
        lx2, ly2 = stem_xy(0.68)
        draw_leaf(lx1 - 1 * s, ly1, 145, 21 * s, 8.5 * s)
        draw_leaf(lx2 + 1 * s, ly2, 35, 22 * s, 9 * s)
        draw_leaf(tip_x, tip_y, 90, 12 * s, 5 * s)

    elif phase == 3:
        # --- Phase 3: Mid-Growth (taller stem + 4 leaves + unfurling crown bud) ---
        lx1, ly1 = stem_xy(0.35)
        lx2, ly2 = stem_xy(0.52)
        lx3, ly3 = stem_xy(0.75)
        lx4, ly4 = stem_xy(0.90)
        draw_leaf(lx1 - 2 * s, ly1, 145, 26 * s, 10.5 * s)
        draw_leaf(lx2 + 2 * s, ly2, 35, 28 * s, 11 * s)
        draw_leaf(lx3 - 2 * s, ly3, 150, 22 * s, 9 * s)
        draw_leaf(lx4 + 2 * s, ly4, 30, 23 * s, 9.5 * s)
        draw_leaf(tip_x, tip_y, 88, 15 * s, 6 * s)

    elif phase == 4:
        # --- Phase 4: Full-Grown Thriving Plant (full height + 6 lush leaves + sparkle) ---
        draw_leaf(cx - 3 * s, pot_top_y - 16 * s, 145, 30 * s, 12 * s)
        draw_leaf(cx + 7 * s, pot_top_y - 24 * s, 35, 32 * s, 13 * s)
        draw_leaf(cx - 2 * s, pot_top_y - 36 * s, 150, 26 * s, 11 * s)
        draw_leaf(cx + 6 * s, pot_top_y - 46 * s, 30, 28 * s, 11 * s)
        draw_leaf(cx + 2 * s, pot_top_y - 56 * s, 80, 22 * s, 9 * s)
        draw_leaf(cx - 2 * s, pot_top_y - 56 * s, 100, 22 * s, 9 * s)

        draw_sparkle(cx + 24 * s, pot_top_y - 54 * s, 4 * s)

    else:
        # --- Phase 5: Mature Blooming Plant (full 6 leaves + base shoots + 3 blossoms + sparkles) ---
        # Small lush base shoots
        draw_leaf(cx - 4 * s, pot_top_y - 6 * s, 155, 19 * s, 7.5 * s)
        draw_leaf(cx + 5 * s, pot_top_y - 8 * s, 25, 20 * s, 7.5 * s)

        # Same 6 signature leaves as Phase 4
        draw_leaf(cx - 3 * s, pot_top_y - 16 * s, 145, 31 * s, 12.5 * s)
        draw_leaf(cx + 7 * s, pot_top_y - 24 * s, 35, 33 * s, 13.5 * s)
        draw_leaf(cx - 2 * s, pot_top_y - 36 * s, 150, 27 * s, 11.5 * s)
        draw_leaf(cx + 6 * s, pot_top_y - 46 * s, 30, 29 * s, 11.5 * s)
        draw_leaf(cx + 2 * s, pot_top_y - 56 * s, 75, 22 * s, 9 * s)
        draw_leaf(cx - 2 * s, pot_top_y - 56 * s, 105, 22 * s, 9 * s)

        # Delicate Scandinavian blossoms crowning the same plant
        draw_blossom(cx, pot_top_y - 60 * s, 4.6 * s)
        draw_blossom(cx - 17 * s, pot_top_y - 46 * s, 3.6 * s)
        draw_blossom(cx + 20 * s, pot_top_y - 48 * s, 3.8 * s)

        # Twin golden sparkles
        draw_sparkle(cx + 27 * s, pot_top_y - 60 * s, 4.5 * s)
        draw_sparkle(cx - 25 * s, pot_top_y - 58 * s, 3.5 * s)


def format_duration(total_seconds):
    """Formats total seconds cleanly as H:MM:SS."""
    sec = max(0, int(total_seconds))
    h = sec // 3600
    m = (sec % 3600) // 60
    s = sec % 60
    return f"{h}:{m:02d}:{s:02d}"


def split_duration(total_seconds):
    """Splits total seconds into (hours, minutes, seconds)."""
    sec = max(0, int(total_seconds))
    return sec // 3600, (sec % 3600) // 60, sec % 60


class BookshelfApp(ctk.CTk):
    def __init__(self):
        super().__init__()

        self.title("Kirjateline • Lukuseuranta")
        self.geometry("680x480")
        self.minsize(460, 300)
        self.attributes("-fullscreen", True)
        self.configure(fg_color=BG_COLOR)

        # Multiple books supported simultaneously ("book" with pages or "ebook" with duration)
        self.books = [
            {"title": "Tuntematon sotilas", "author": "Väinö Linna", "type": "book", "current_page": 0, "total_pages": 350},
            {"title": "Sapiens", "author": "Yuval Noah Harari", "type": "book", "current_page": 142, "total_pages": 464},
            {"title": "Seitsemän veljestä", "author": "Aleksis Kivi", "type": "book", "current_page": 85, "total_pages": 320},
        ]
        self.active_book_index = 0

        # Lukuputki alkaa aina nollasta ilman kellointegraatiota
        self.streak_count = 12

        # Kasvin tila: alussa kuihtunut, muuttuu eläväksi kun sivumäärää/kestoa päivitetään
        self.is_plant_alive = False
        self.plant_w = 110
        self.plant_h = 110

        # UI State: "summary", "numpad", or "book_list"
        self.current_view_mode = "summary"
        self.numpad_mode = "current_page"  # "current_page" or "total_pages"
        self.creating_ebook = False
        self.numpad_input_str = ""
        self.numpad_fresh = False

        # On-screen QWERTY keyboard state for touchscreen text entry
        self.active_text_entry = None
        self.qwerty_visible = False
        self.kb_shift = True
        self.kb_mode = "alpha"

        # 3-field duration input state: [hours, minutes, seconds]
        self.duration_inputs = ["", "", ""]
        self.active_duration_field = 0
        self.duration_field_fresh = False

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

    @property
    def plant_phase(self):
        return get_plant_phase(self.streak_count)

    @property
    def active_book(self):
        if not self.books:
            return None
        if self.active_book_index >= len(self.books):
            self.active_book_index = len(self.books) - 1
        return self.books[self.active_book_index]

    @property
    def is_active_ebook(self):
        book = self.active_book
        return book is not None and book.get("type") == "ebook"

    @property
    def current_page(self):
        book = self.active_book
        return book.get("current_page", 0) if book is not None else 0

    @current_page.setter
    def current_page(self, value):
        if self.active_book is not None:
            self.active_book["current_page"] = value

    @property
    def total_pages(self):
        book = self.active_book
        return book.get("total_pages", 0) if book is not None else 0

    @total_pages.setter
    def total_pages(self, value):
        if self.active_book is not None:
            self.active_book["total_pages"] = value

    def _build_ui(self):
        # 1. TOP HEADER (Left: "Uusi kirja" & "Vaihda kirjaa", Right: Close & Streak badge)
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
            width=96,
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
        self.new_book_btn.pack(side="left", padx=(24, 0), pady=13)

        # --- "Vaihda kirjaa" BUTTON (NEXT TO "Uusi kirja") ---
        self.switch_book_btn = ctk.CTkButton(
            self.header_frame,
            text="Vaihda kirjaa",
            width=114,
            height=36,
            corner_radius=8,
            fg_color=CARD_SURFACE,
            hover_color=CARD_HOVER,
            text_color=TEXT_PRIMARY,
            border_width=1,
            border_color=BORDER_COLOR,
            font=ctk.CTkFont(size=12, weight="bold"),
            command=self._show_book_list_view
        )
        self.switch_book_btn.pack(side="left", padx=(8, 0), pady=13)

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
        self.body_container.pack(fill="both", expand=True, padx=24, pady=12)

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

        # --- VIEW 3: Simple Book Switcher Frame ---
        self.book_list_frame = ctk.CTkFrame(self.main_card, fg_color="transparent")
        self._build_book_list_view()

        # Start with summary view visible
        self.summary_frame.pack(fill="both", expand=True, padx=24, pady=16)

    def _build_summary_view(self):
        """Standard reading overview with book title at top-left and native Canvas plant inside the gray stat box."""
        summary_head = ctk.CTkFrame(self.summary_frame, fg_color="transparent")
        summary_head.pack(fill="x", pady=(0, 8))

        self.summary_tag_lbl = ctk.CTkLabel(
            summary_head,
            text="NYKYINEN KIRJA",
            font=ctk.CTkFont(size=11, weight="bold"),
            text_color=ACCENT_BRASS,
            anchor="w"
        )
        self.summary_tag_lbl.pack(side="left", anchor="w")

        # Stat Card (Clean neutral tone box containing book title, current page/duration, plant in middle, and %)
        self.stat_box = ctk.CTkFrame(
            self.summary_frame,
            fg_color=CARD_SURFACE,
            corner_radius=14,
            border_width=1,
            border_color=BORDER_COLOR
        )
        self.stat_box.pack(fill="both", expand=True, pady=(0, 12))

        # Active book title & optional author at the top-left of the gray stat box
        title_box = ctk.CTkFrame(self.stat_box, fg_color="transparent")
        title_box.pack(side="top", fill="x", padx=28, pady=(18, 4))

        self.hero_book_title = ctk.CTkLabel(
            title_box,
            text="",
            font=ctk.CTkFont(size=26, weight="bold"),
            text_color=TEXT_PRIMARY,
            anchor="w",
            padx=0
        )
        self.hero_book_title.pack(side="top", anchor="w")

        self.hero_book_author = ctk.CTkLabel(
            title_box,
            text="",
            font=ctk.CTkFont(size=15),
            text_color=TEXT_SECONDARY,
            anchor="w",
            padx=0
        )
        self.hero_book_author.pack(side="top", anchor="w", pady=(2, 0))

        stat_inner = ctk.CTkFrame(self.stat_box, fg_color="transparent")
        stat_inner.pack(fill="both", expand=True, padx=28, pady=(2, 10))

        left_stat = ctk.CTkFrame(stat_inner, fg_color="transparent")
        left_stat.pack(side="left")

        self.page_caption = ctk.CTkLabel(
            left_stat,
            text="Nykyinen sivu",
            font=ctk.CTkFont(size=12),
            text_color=TEXT_MUTED
        )
        self.page_caption.pack(anchor="w")

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

        # --- CENTER PLANT INSIDE THE SAME GRAY BOX (Native tk.Canvas) ---
        self.plant_canvas = tk.Canvas(
            stat_inner,
            width=self.plant_w,
            height=self.plant_h,
            bg=CARD_SURFACE,
            highlightthickness=0,
            bd=0
        )
        self.plant_canvas.pack(side="left", expand=True)

        # "Päivitä sivu, jolla olet" Button
        self.add_pages_btn = ctk.CTkButton(
            self.summary_frame,
            text="Päivitä sivu, jolla olet",
            height=48,
            corner_radius=12,
            fg_color=ACCENT_DARK,
            hover_color=ACCENT_DARK_HOVER,
            text_color="#ffffff",
            font=ctk.CTkFont(size=15, weight="bold"),
            command=self._show_numpad_for_current_page
        )
        self.add_pages_btn.pack(fill="x", pady=(0, 2))

    def _build_numpad_view(self):
        """In-window form & compact touch numpad (no separate popup windows)."""
        numpad_head = ctk.CTkFrame(self.numpad_frame, fg_color="transparent")
        numpad_head.pack(fill="x", pady=(0, 8))

        self.numpad_tag_lbl = ctk.CTkLabel(
            numpad_head,
            text="MERKITSE SIVU",
            font=ctk.CTkFont(size=11, weight="bold"),
            text_color=ACCENT_BRASS,
            anchor="w"
        )
        self.numpad_tag_lbl.pack(side="left", anchor="w")

        # Toggle button shown in "Uusi kirja" view to switch to "Uusi e-kirja" (duration input)
        self.ebook_toggle_btn = ctk.CTkButton(
            numpad_head,
            text="Uusi e-kirja",
            width=116,
            height=30,
            corner_radius=8,
            fg_color=CARD_SURFACE,
            hover_color=CARD_HOVER,
            text_color=TEXT_PRIMARY,
            border_width=1,
            border_color=BORDER_COLOR,
            font=ctk.CTkFont(size=12, weight="bold"),
            command=self._toggle_new_book_type
        )

        # Prominent book title & optional author inputs (shown only when creating a new book)
        self.new_book_name_box = ctk.CTkFrame(self.numpad_frame, fg_color="transparent")
        self.new_book_name_box.grid_columnconfigure(0, weight=3)
        self.new_book_name_box.grid_columnconfigure(1, weight=2)

        name_caption = ctk.CTkLabel(
            self.new_book_name_box,
            text="Kirjan nimi",
            font=ctk.CTkFont(size=13, weight="bold"),
            text_color=TEXT_PRIMARY,
            anchor="w"
        )
        name_caption.grid(row=0, column=0, sticky="ew", padx=(0, 10), pady=(0, 4))

        author_caption = ctk.CTkLabel(
            self.new_book_name_box,
            text="Kirjailija (vapaaehtoinen)",
            font=ctk.CTkFont(size=13, weight="bold"),
            text_color=TEXT_SECONDARY,
            anchor="w"
        )
        author_caption.grid(row=0, column=1, sticky="ew", pady=(0, 4))

        self.new_book_name_entry = ctk.CTkEntry(
            self.new_book_name_box,
            height=42,
            corner_radius=10,
            fg_color=CARD_SURFACE,
            border_width=1,
            border_color=BORDER_COLOR,
            text_color=TEXT_PRIMARY,
            placeholder_text="Kirjoita kirjan nimi...",
            placeholder_text_color=TEXT_MUTED,
            font=ctk.CTkFont(size=15)
        )
        self.new_book_name_entry.grid(row=1, column=0, sticky="ew", padx=(0, 10))

        self.new_book_author_entry = ctk.CTkEntry(
            self.new_book_name_box,
            height=42,
            corner_radius=10,
            fg_color=CARD_SURFACE,
            border_width=1,
            border_color=BORDER_COLOR,
            text_color=TEXT_PRIMARY,
            placeholder_text="Kirjailijan nimi...",
            placeholder_text_color=TEXT_MUTED,
            font=ctk.CTkFont(size=14)
        )
        self.new_book_author_entry.grid(row=1, column=1, sticky="ew")

        # Dynamic focus border styling + touch on-screen QWERTY keyboard trigger
        for entry in (self.new_book_name_entry, self.new_book_author_entry):
            entry.bind("<Button-1>", lambda e, ent=entry: self._open_qwerty_for_entry(ent))
            entry.bind("<FocusIn>", lambda e, ent=entry: self._highlight_text_entry(ent))
            entry.bind("<FocusOut>", lambda e, ent=entry: self._unhighlight_text_entry(ent))

        self.key_container = ctk.CTkFrame(self.numpad_frame, fg_color="transparent")
        self.key_container.pack(fill="both", expand=True)

        self.key_container.grid_columnconfigure(0, weight=1)
        self.key_container.grid_columnconfigure(1, weight=0)
        self.key_container.grid_rowconfigure(0, weight=1)

        # --- LEFT COLUMN: Digital Page/Duration Display + Action Buttons ---
        left_col = ctk.CTkFrame(self.key_container, fg_color="transparent")
        left_col.grid(row=0, column=0, sticky="nsew", padx=(0, 16))

        # A) Single-value page display card (for regular books)
        self.disp_card = ctk.CTkFrame(
            left_col,
            fg_color=CARD_SURFACE,
            corner_radius=12,
            border_width=1,
            border_color=BORDER_COLOR
        )
        self.disp_card.pack(fill="x", pady=(0, 10))

        self.numpad_sub_lbl = ctk.CTkLabel(
            self.disp_card,
            text="Syötetty sivu",
            font=ctk.CTkFont(size=11),
            text_color=TEXT_MUTED
        )
        self.numpad_sub_lbl.pack(pady=(8, 0))

        self.numpad_display_num = ctk.CTkLabel(
            self.disp_card,
            text="0",
            font=ctk.CTkFont(size=32, weight="bold"),
            text_color=TEXT_PRIMARY
        )
        self.numpad_display_num.pack(pady=(0, 0))

        self.numpad_display_meta = ctk.CTkLabel(
            self.disp_card,
            text="/ 0 sivua (0%)",
            font=ctk.CTkFont(size=12, weight="bold"),
            text_color=ACCENT_BRASS
        )
        self.numpad_display_meta.pack(pady=(0, 8))

        # B) 3-field duration card (Tunnit / Minuutit / Sekunnit) for e-books / audiobooks
        self.duration_card = ctk.CTkFrame(
            left_col,
            fg_color=CARD_SURFACE,
            corner_radius=12,
            border_width=1,
            border_color=BORDER_COLOR
        )

        self.duration_sub_lbl = ctk.CTkLabel(
            self.duration_card,
            text="Äänikirjan kesto",
            font=ctk.CTkFont(size=11),
            text_color=TEXT_MUTED
        )
        self.duration_sub_lbl.pack(pady=(8, 4))

        fields_row = ctk.CTkFrame(self.duration_card, fg_color="transparent")
        fields_row.pack(fill="x", padx=12, pady=(0, 4))
        fields_row.grid_columnconfigure(0, weight=1)
        fields_row.grid_columnconfigure(1, weight=0)
        fields_row.grid_columnconfigure(2, weight=1)
        fields_row.grid_columnconfigure(3, weight=0)
        fields_row.grid_columnconfigure(4, weight=1)

        field_labels = ("Tunnit", "Minuutit", "Sekunnit")
        self.duration_field_btns = []
        for idx, caption in enumerate(field_labels):
            col = idx * 2
            lbl = ctk.CTkLabel(
                fields_row,
                text=caption,
                font=ctk.CTkFont(size=11),
                text_color=TEXT_SECONDARY
            )
            lbl.grid(row=0, column=col, pady=(0, 2))

            btn = ctk.CTkButton(
                fields_row,
                text="00",
                height=42,
                width=56,
                corner_radius=8,
                fg_color=CARD_BG,
                hover_color=CARD_HOVER,
                text_color=TEXT_PRIMARY,
                border_width=1,
                border_color=BORDER_COLOR,
                font=ctk.CTkFont(size=20, weight="bold"),
                command=lambda i=idx: self._select_duration_field(i)
            )
            btn.grid(row=1, column=col, sticky="ew", padx=2)
            self.duration_field_btns.append(btn)

            if idx < 2:
                colon = ctk.CTkLabel(
                    fields_row,
                    text=":",
                    font=ctk.CTkFont(size=20, weight="bold"),
                    text_color=TEXT_MUTED
                )
                colon.grid(row=1, column=col + 1, padx=2)

        self.duration_meta_lbl = ctk.CTkLabel(
            self.duration_card,
            text="tunnit : minuutit : sekunnit",
            font=ctk.CTkFont(size=12, weight="bold"),
            text_color=ACCENT_BRASS
        )
        self.duration_meta_lbl.pack(pady=(2, 8))

        self.action_row = ctk.CTkFrame(left_col, fg_color="transparent")
        self.action_row.pack(fill="x")
        self.action_row.grid_columnconfigure(0, weight=3)
        self.action_row.grid_columnconfigure(1, weight=2)

        self.numpad_save_btn = ctk.CTkButton(
            self.action_row,
            text="Tallenna sivu ✓",
            height=42,
            corner_radius=10,
            fg_color=ACCENT_DARK,
            hover_color=ACCENT_DARK_HOVER,
            text_color="#ffffff",
            font=ctk.CTkFont(size=13, weight="bold"),
            command=self._confirm_numpad
        )
        self.numpad_save_btn.grid(row=0, column=0, sticky="ew", padx=(0, 6))

        cancel_btn = ctk.CTkButton(
            self.action_row,
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
        cancel_btn.grid(row=0, column=1, sticky="ew")

        # Compact "Luettu loppuun" button (fills duration fields to 100% when updating e-book progress)
        self.mark_finished_btn = ctk.CTkButton(
            left_col,
            text="Luettu loppuun",
            width=126,
            height=30,
            corner_radius=8,
            fg_color="#ecfdf5",
            hover_color="#d1fae5",
            text_color="#15803d",
            border_width=1,
            border_color="#a7f3d0",
            font=ctk.CTkFont(size=11, weight="bold"),
            command=self._mark_ebook_finished
        )

        # --- RIGHT COLUMN: Compact Touch Keypad Grid ---
        keys_col = ctk.CTkFrame(self.key_container, fg_color="transparent")
        keys_col.grid(row=0, column=1, sticky="ne")

        keys = [
            ["1", "2", "3"],
            ["4", "5", "6"],
            ["7", "8", "9"],
            ["C", "0", "⌫"]
        ]

        for r, row in enumerate(keys):
            for c, key in enumerate(row):
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
                    width=68,
                    height=44,
                    corner_radius=9,
                    fg_color=fg,
                    hover_color=hover,
                    text_color=txt_col,
                    border_width=1,
                    border_color=BORDER_COLOR,
                    font=ctk.CTkFont(size=18, weight="bold"),
                    command=cmd
                )
                btn.grid(row=r, column=c, padx=3, pady=3)

        # --- ON-SCREEN TOUCH QWERTY KEYBOARD (shown when tapping title/author fields) ---
        self.qwerty_frame = ctk.CTkFrame(self.numpad_frame, fg_color="transparent")
        self._build_qwerty_keyboard()

    def _build_qwerty_keyboard(self):
        """Builds a compact Finnish/Nordic touchscreen QWERTY keyboard with 123 mode."""
        for r in range(4):
            self.qwerty_frame.grid_rowconfigure(r, weight=1, uniform="kb_row")
        for c in range(11):
            self.qwerty_frame.grid_columnconfigure(c, weight=1, uniform="kb_col")

        self.kb_alpha_rows = [
            ["q", "w", "e", "r", "t", "y", "u", "i", "o", "p", "å"],
            ["a", "s", "d", "f", "g", "h", "j", "k", "l", "ö", "ä"],
            ["z", "x", "c", "v", "b", "n", "m"],
        ]
        self.kb_num_rows = [
            ["1", "2", "3", "4", "5", "6", "7", "8", "9", "0", "-"],
            ["'", ":", ";", ",", ".", "!", "?", "(", ")", "/", "&"],
            ["+", "=", "*", "#", "%", "@", "\""],
        ]

        self.kb_char_btns = []

        # Row 0 & Row 1 (11 keys each)
        for r in (0, 1):
            row_btns = []
            for c in range(11):
                ch = self.kb_alpha_rows[r][c]
                btn = ctk.CTkButton(
                    self.qwerty_frame,
                    text=ch.upper(),
                    width=28,
                    height=34,
                    corner_radius=7,
                    fg_color=CARD_SURFACE,
                    hover_color=CARD_HOVER,
                    text_color=TEXT_PRIMARY,
                    border_width=1,
                    border_color=BORDER_COLOR,
                    font=ctk.CTkFont(size=14, weight="bold"),
                    command=lambda row_i=r, col_i=c: self._kb_press_grid_char(row_i, col_i)
                )
                btn.grid(row=r, column=c, padx=2, pady=2, sticky="nsew")
                row_btns.append(btn)
            self.kb_char_btns.append(row_btns)

        # Row 2: Shift (col 0), 7 letters (cols 1..7), apostrophe (col 8), Backspace (cols 9..10)
        self.kb_shift_btn = ctk.CTkButton(
            self.qwerty_frame,
            text="⇧",
            width=28,
            height=34,
            corner_radius=7,
            fg_color=STREAK_BG,
            hover_color=CARD_HOVER,
            text_color=STREAK_TEXT,
            border_width=1,
            border_color=ACCENT_BRASS,
            font=ctk.CTkFont(size=15, weight="bold"),
            command=self._kb_toggle_shift
        )
        self.kb_shift_btn.grid(row=2, column=0, padx=2, pady=2, sticky="nsew")

        row2_btns = []
        for idx in range(7):
            ch = self.kb_alpha_rows[2][idx]
            btn = ctk.CTkButton(
                self.qwerty_frame,
                text=ch.upper(),
                width=28,
                height=34,
                corner_radius=7,
                fg_color=CARD_SURFACE,
                hover_color=CARD_HOVER,
                text_color=TEXT_PRIMARY,
                border_width=1,
                border_color=BORDER_COLOR,
                font=ctk.CTkFont(size=14, weight="bold"),
                command=lambda col_i=idx: self._kb_press_grid_char(2, col_i)
            )
            btn.grid(row=2, column=idx + 1, padx=2, pady=2, sticky="nsew")
            row2_btns.append(btn)
        self.kb_char_btns.append(row2_btns)

        dash_btn = ctk.CTkButton(
            self.qwerty_frame,
            text="-",
            width=28,
            height=34,
            corner_radius=7,
            fg_color=CARD_SURFACE,
            hover_color=CARD_HOVER,
            text_color=TEXT_PRIMARY,
            border_width=1,
            border_color=BORDER_COLOR,
            font=ctk.CTkFont(size=14, weight="bold"),
            command=lambda: self._kb_insert_text("-")
        )
        dash_btn.grid(row=2, column=8, padx=2, pady=2, sticky="nsew")

        kb_bksp_btn = ctk.CTkButton(
            self.qwerty_frame,
            text="⌫",
            width=28,
            height=34,
            corner_radius=7,
            fg_color="#fdf2f2",
            hover_color="#fee2e2",
            text_color="#dc2626",
            border_width=1,
            border_color="#fecaca",
            font=ctk.CTkFont(size=15, weight="bold"),
            command=self._kb_backspace
        )
        kb_bksp_btn.grid(row=2, column=9, columnspan=2, padx=2, pady=2, sticky="nsew")

        # Row 3: 123/ABC toggle (cols 0..1), Space (cols 2..7), Period (col 8), Done (cols 9..10)
        self.kb_mode_btn = ctk.CTkButton(
            self.qwerty_frame,
            text="123",
            width=28,
            height=34,
            corner_radius=7,
            fg_color=CARD_SURFACE,
            hover_color=CARD_HOVER,
            text_color=TEXT_PRIMARY,
            border_width=1,
            border_color=BORDER_COLOR,
            font=ctk.CTkFont(size=13, weight="bold"),
            command=self._kb_toggle_mode
        )
        self.kb_mode_btn.grid(row=3, column=0, columnspan=2, padx=2, pady=2, sticky="nsew")

        space_btn = ctk.CTkButton(
            self.qwerty_frame,
            text="Välilyönti",
            width=28,
            height=34,
            corner_radius=7,
            fg_color=CARD_SURFACE,
            hover_color=CARD_HOVER,
            text_color=TEXT_SECONDARY,
            border_width=1,
            border_color=BORDER_COLOR,
            font=ctk.CTkFont(size=13, weight="bold"),
            command=lambda: self._kb_insert_text(" ")
        )
        space_btn.grid(row=3, column=2, columnspan=6, padx=2, pady=2, sticky="nsew")

        dot_btn = ctk.CTkButton(
            self.qwerty_frame,
            text=".",
            width=28,
            height=34,
            corner_radius=7,
            fg_color=CARD_SURFACE,
            hover_color=CARD_HOVER,
            text_color=TEXT_PRIMARY,
            border_width=1,
            border_color=BORDER_COLOR,
            font=ctk.CTkFont(size=14, weight="bold"),
            command=lambda: self._kb_insert_text(".")
        )
        dot_btn.grid(row=3, column=8, padx=2, pady=2, sticky="nsew")

        kb_done_btn = ctk.CTkButton(
            self.qwerty_frame,
            text="Valmis ✓",
            width=28,
            height=34,
            corner_radius=7,
            fg_color=ACCENT_DARK,
            hover_color=ACCENT_DARK_HOVER,
            text_color="#ffffff",
            font=ctk.CTkFont(size=13, weight="bold"),
            command=self._close_qwerty
        )
        kb_done_btn.grid(row=3, column=9, columnspan=2, padx=2, pady=2, sticky="nsew")

    def _build_book_list_view(self):
        """Simple in-window book switcher listing each book's name, progress, and 'Valitse kirja' button."""
        list_head = ctk.CTkFrame(self.book_list_frame, fg_color="transparent")
        list_head.pack(fill="x", pady=(0, 10))

        list_tag_lbl = ctk.CTkLabel(
            list_head,
            text="VAIHDA KIRJAA • KIRJASTO",
            font=ctk.CTkFont(size=11, weight="bold"),
            text_color=ACCENT_BRASS,
            anchor="w"
        )
        list_tag_lbl.pack(side="left")

        back_btn = ctk.CTkButton(
            list_head,
            text="Takaisin",
            width=84,
            height=30,
            corner_radius=8,
            fg_color=CARD_BG,
            hover_color=CARD_HOVER,
            text_color=TEXT_SECONDARY,
            border_width=1,
            border_color=BORDER_COLOR,
            font=ctk.CTkFont(size=12),
            command=self._show_summary_view
        )
        back_btn.pack(side="right")

        self.book_scroll_frame = ctk.CTkScrollableFrame(
            self.book_list_frame,
            fg_color="transparent",
            scrollbar_button_color=BORDER_COLOR,
            scrollbar_button_hover_color=TEXT_MUTED
        )
        self.book_scroll_frame.pack(fill="both", expand=True)

        # In-window delete confirmation overlay (stays inside fullscreen window)
        self.pending_delete_index = None
        self.confirm_delete_overlay = ctk.CTkFrame(
            self.book_list_frame,
            fg_color=CARD_BG,
            corner_radius=12
        )

        confirm_card = ctk.CTkFrame(
            self.confirm_delete_overlay,
            fg_color=CARD_SURFACE,
            corner_radius=14,
            border_width=1,
            border_color=BORDER_COLOR
        )
        confirm_card.place(relx=0.5, rely=0.5, anchor="center")

        confirm_inner = ctk.CTkFrame(confirm_card, fg_color="transparent")
        confirm_inner.pack(padx=28, pady=22)

        confirm_title = ctk.CTkLabel(
            confirm_inner,
            text="Poista kirja?",
            font=ctk.CTkFont(size=18, weight="bold"),
            text_color=TEXT_PRIMARY
        )
        confirm_title.pack(pady=(0, 6))

        self.confirm_delete_msg = ctk.CTkLabel(
            confirm_inner,
            text="",
            font=ctk.CTkFont(size=13),
            text_color=TEXT_SECONDARY,
            wraplength=340,
            justify="center"
        )
        self.confirm_delete_msg.pack(pady=(0, 18))

        confirm_btns = ctk.CTkFrame(confirm_inner, fg_color="transparent")
        confirm_btns.pack()

        confirm_yes_btn = ctk.CTkButton(
            confirm_btns,
            text="Poista",
            width=116,
            height=38,
            corner_radius=10,
            fg_color="#dc2626",
            hover_color="#b91c1c",
            text_color="#ffffff",
            font=ctk.CTkFont(size=13, weight="bold"),
            command=self._confirm_delete_book
        )
        confirm_yes_btn.pack(side="left", padx=(0, 10))

        confirm_no_btn = ctk.CTkButton(
            confirm_btns,
            text="Peruuta",
            width=116,
            height=38,
            corner_radius=10,
            fg_color=CARD_BG,
            hover_color=CARD_HOVER,
            text_color=TEXT_PRIMARY,
            border_width=1,
            border_color=BORDER_COLOR,
            font=ctk.CTkFont(size=13),
            command=self._cancel_delete_book
        )
        confirm_no_btn.pack(side="left")

    def _populate_book_list(self):
        """Rebuilds the rows of books with title, optional E-kirja badge, author, progress, 'Valitse kirja', and 'Poista'."""
        for child in self.book_scroll_frame.winfo_children():
            child.destroy()

        if not self.books:
            empty_lbl = ctk.CTkLabel(
                self.book_scroll_frame,
                text="Kirjasto on tyhjä. Lisää uusi kirja yläpalkista.",
                font=ctk.CTkFont(size=13),
                text_color=TEXT_MUTED
            )
            empty_lbl.pack(pady=24)
            return

        for idx, book in enumerate(self.books):
            is_active = (idx == self.active_book_index)
            is_ebook = (book.get("type") == "ebook")

            if is_ebook:
                cur_val = book.get("current_seconds", 0)
                total_val = book.get("total_seconds", 0)
                pct = (cur_val / total_val * 100) if total_val > 0 else 0
                progress_str = f"{format_duration(cur_val)} / {format_duration(total_val)} ({pct:.0f}%)"
            else:
                cur_val = book.get("current_page", 0)
                total_val = book.get("total_pages", 0)
                pct = (cur_val / total_val * 100) if total_val > 0 else 0
                progress_str = f"{cur_val} / {total_val} sivua ({pct:.0f}%)"

            row = ctk.CTkFrame(
                self.book_scroll_frame,
                fg_color=CARD_SURFACE,
                corner_radius=10,
                height=52,
                border_width=1,
                border_color=ACCENT_BRASS if is_active else BORDER_COLOR
            )
            row.pack(fill="x", pady=4)
            row.pack_propagate(False)

            row_inner = ctk.CTkFrame(row, fg_color="transparent")
            row_inner.pack(fill="both", expand=True, padx=14, pady=6)

            # Pack buttons on the right first so they always remain visible on small screens
            delete_btn = ctk.CTkButton(
                row_inner,
                text="Poista kirja",
                width=92,
                height=32,
                corner_radius=8,
                fg_color="#fdf2f2",
                hover_color="#fee2e2",
                text_color="#dc2626",
                border_width=1,
                border_color="#fecaca",
                font=ctk.CTkFont(size=12, weight="bold"),
                command=lambda i=idx: self._ask_delete_book(i)
            )
            delete_btn.pack(side="right", padx=(6, 0))

            select_btn = ctk.CTkButton(
                row_inner,
                text="Valitse kirja",
                width=104,
                height=32,
                corner_radius=8,
                fg_color=ACCENT_DARK,
                hover_color=ACCENT_DARK_HOVER,
                text_color="#ffffff",
                font=ctk.CTkFont(size=12, weight="bold"),
                command=lambda i=idx: self._select_book(i)
            )
            select_btn.pack(side="right", padx=(10, 0))

            title_lbl = ctk.CTkLabel(
                row_inner,
                text=book["title"],
                font=ctk.CTkFont(size=14, weight="bold"),
                text_color=TEXT_PRIMARY,
                anchor="w"
            )
            title_lbl.pack(side="left")

            if is_ebook:
                ebook_badge = ctk.CTkLabel(
                    row_inner,
                    text="E-kirja",
                    font=ctk.CTkFont(size=11, weight="bold"),
                    text_color=STREAK_TEXT,
                    fg_color=STREAK_BG,
                    corner_radius=6,
                    padx=7,
                    pady=2
                )
                ebook_badge.pack(side="left", padx=(8, 0))

            author = book.get("author", "").strip()
            if author:
                author_lbl = ctk.CTkLabel(
                    row_inner,
                    text=f"— {author}",
                    font=ctk.CTkFont(size=12),
                    text_color=TEXT_MUTED,
                    anchor="w"
                )
                author_lbl.pack(side="left", padx=(6, 0))

            progress_lbl = ctk.CTkLabel(
                row_inner,
                text=progress_str,
                font=ctk.CTkFont(size=12),
                text_color=TEXT_SECONDARY,
                anchor="w"
            )
            progress_lbl.pack(side="left", padx=(12, 0))

    def _hide_all_views(self):
        """Hides all main card sub-views before switching to another."""
        self._cancel_delete_book()
        self._close_qwerty()
        self.summary_frame.pack_forget()
        self.numpad_frame.pack_forget()
        self.book_list_frame.pack_forget()

    def _highlight_text_entry(self, entry):
        """Highlights the focused text entry."""
        for ent in (self.new_book_name_entry, self.new_book_author_entry):
            if ent == entry:
                ent.configure(border_width=2, border_color=ACCENT_BRASS)
            else:
                ent.configure(border_width=1, border_color=BORDER_COLOR)

    def _unhighlight_text_entry(self, entry):
        """Removes highlight when focus leaves an entry unless QWERTY is still targeting it."""
        if self.qwerty_visible and self.active_text_entry == entry:
            return
        entry.configure(border_width=1, border_color=BORDER_COLOR)

    def _open_qwerty_for_entry(self, entry):
        """Shows the in-window touch QWERTY keyboard for typing into the tapped entry."""
        if self.numpad_mode != "total_pages":
            return
        self.active_text_entry = entry
        self._highlight_text_entry(entry)
        self.kb_mode = "alpha"
        self.kb_shift = (len(entry.get()) == 0)
        self._refresh_qwerty_keys()
        if not self.qwerty_visible:
            self.key_container.pack_forget()
            self.qwerty_frame.pack(fill="both", expand=True)
            self.qwerty_visible = True

    def _close_qwerty(self):
        """Hides the touch QWERTY keyboard and restores the numpad/duration view."""
        if self.qwerty_visible:
            self.qwerty_frame.pack_forget()
            self.key_container.pack(fill="both", expand=True)
            self.qwerty_visible = False
        self.active_text_entry = None
        for ent in (self.new_book_name_entry, self.new_book_author_entry):
            ent.configure(border_width=1, border_color=BORDER_COLOR)
        if self.current_view_mode == "numpad":
            self.focus_set()

    def _refresh_qwerty_keys(self):
        """Updates QWERTY key labels for alpha/num and shift state."""
        if self.kb_mode == "alpha":
            rows = self.kb_alpha_rows
            self.kb_mode_btn.configure(text="123")
            self.kb_shift_btn.configure(
                text="⇧",
                state="normal",
                fg_color=STREAK_BG if self.kb_shift else CARD_SURFACE,
                border_color=ACCENT_BRASS if self.kb_shift else BORDER_COLOR,
                text_color=STREAK_TEXT if self.kb_shift else TEXT_PRIMARY
            )
            for r, row_btns in enumerate(self.kb_char_btns):
                for c, btn in enumerate(row_btns):
                    ch = rows[r][c]
                    btn.configure(text=ch.upper() if self.kb_shift else ch.lower())
        else:
            rows = self.kb_num_rows
            self.kb_mode_btn.configure(text="ABC")
            self.kb_shift_btn.configure(
                text="⇧",
                state="disabled",
                fg_color=CARD_SURFACE,
                border_color=BORDER_COLOR,
                text_color=TEXT_MUTED
            )
            for r, row_btns in enumerate(self.kb_char_btns):
                for c, btn in enumerate(row_btns):
                    btn.configure(text=rows[r][c])

    def _kb_toggle_shift(self):
        if self.kb_mode == "alpha":
            self.kb_shift = not self.kb_shift
            self._refresh_qwerty_keys()

    def _kb_toggle_mode(self):
        self.kb_mode = "num" if self.kb_mode == "alpha" else "alpha"
        self._refresh_qwerty_keys()

    def _kb_press_grid_char(self, row_i, col_i):
        if self.kb_mode == "alpha":
            ch = self.kb_alpha_rows[row_i][col_i]
            ch = ch.upper() if self.kb_shift else ch.lower()
            self._kb_insert_text(ch)
            if self.kb_shift:
                self.kb_shift = False
                self._refresh_qwerty_keys()
        else:
            ch = self.kb_num_rows[row_i][col_i]
            self._kb_insert_text(ch)

    def _kb_insert_text(self, text):
        entry = self.active_text_entry
        if entry is None:
            return
        entry.insert("insert", text)

    def _kb_backspace(self):
        entry = self.active_text_entry
        if entry is None:
            return
        pos = entry.index("insert")
        if pos > 0:
            entry.delete(pos - 1, pos)

    def _show_book_list_view(self):
        """Opens the simple book selection menu inside the same window."""
        self._cancel_delete_book()
        self._populate_book_list()
        self._hide_all_views()
        self.book_list_frame.pack(fill="both", expand=True, padx=24, pady=16)
        self.current_view_mode = "book_list"

    def _select_book(self, idx):
        """Selects a book from the list and returns to the active reading view."""
        if 0 <= idx < len(self.books):
            self.active_book_index = idx
        self._refresh_all_views()
        self._show_summary_view()

    def _ask_delete_book(self, idx):
        """Shows an in-window confirmation prompt before deleting a book."""
        if not (0 <= idx < len(self.books)):
            return
        self.pending_delete_index = idx
        title = self.books[idx]["title"]
        self.confirm_delete_msg.configure(
            text=f"Oletko varma, että haluat poistaa kirjan \"{title}\"?"
        )
        self.confirm_delete_overlay.place(relx=0, rely=0, relwidth=1, relheight=1)
        self.confirm_delete_overlay.lift()

    def _cancel_delete_book(self):
        """Closes the delete confirmation overlay without deleting."""
        self.pending_delete_index = None
        self.confirm_delete_overlay.place_forget()

    def _confirm_delete_book(self):
        """Confirms and deletes the pending book from the library."""
        idx = self.pending_delete_index
        self._cancel_delete_book()
        if idx is not None:
            self._delete_book(idx)

    def _delete_book(self, idx):
        """Removes a book from the library and refreshes both the list and active view."""
        if not (0 <= idx < len(self.books)):
            return
        self.books.pop(idx)
        if not self.books:
            self.active_book_index = 0
        elif idx < self.active_book_index:
            self.active_book_index -= 1
        elif self.active_book_index >= len(self.books):
            self.active_book_index = len(self.books) - 1
        self._refresh_all_views()
        self._populate_book_list()

    def _mark_ebook_finished(self):
        """Fills the 3 duration fields to the e-book's full duration so the user can choose to save."""
        if self.active_book is None or not self.is_active_ebook:
            return
        h, m, s = split_duration(self.active_book.get("total_seconds", 0))
        self.duration_inputs = [
            str(h) if h > 0 else "",
            str(m) if m > 0 else "",
            str(s) if s > 0 else "",
        ]
        self.duration_field_fresh = True
        self._update_numpad_display()

    def _is_duration_input_mode(self):
        """Returns True if the current numpad view edits H:M:S duration instead of page count."""
        if self.numpad_mode == "total_pages":
            return self.creating_ebook
        return self.is_active_ebook

    def _sync_input_cards(self):
        """Shows either the page display card or the 3-field duration card above action_row."""
        self.disp_card.pack_forget()
        self.duration_card.pack_forget()
        if self._is_duration_input_mode():
            self.duration_card.pack(fill="x", pady=(0, 10), before=self.action_row)
        else:
            self.disp_card.pack(fill="x", pady=(0, 10), before=self.action_row)

    def _select_duration_field(self, idx):
        """Selects Tunnit (0), Minuutit (1), or Sekunnit (2) as the active numpad target."""
        self.active_duration_field = idx
        self.duration_field_fresh = True
        self.focus_set()
        self._update_numpad_display()

    def _get_duration_seconds(self):
        """Converts the 3 duration input strings [h, m, s] to total seconds."""
        vals = []
        for s in self.duration_inputs:
            try:
                vals.append(int(s) if s else 0)
            except ValueError:
                vals.append(0)
        return vals[0] * 3600 + vals[1] * 60 + vals[2]

    def _toggle_new_book_type(self):
        """Toggles between creating a regular book (pages) and an e-book (H:M:S duration)."""
        self.creating_ebook = not self.creating_ebook
        if self.creating_ebook:
            self.numpad_tag_lbl.configure(text="UUSI E-KIRJA")
            self.ebook_toggle_btn.configure(
                text="Tavallinen kirja",
                fg_color=CARD_SURFACE,
                border_color=BORDER_COLOR,
                text_color=TEXT_PRIMARY
            )
            self.duration_sub_lbl.configure(text="Äänikirjan kesto")
            self.numpad_save_btn.configure(text="Aloita e-kirja ✓")
            self.duration_inputs = ["", "", ""]
            self.active_duration_field = 0
            self.duration_field_fresh = False
        else:
            self.numpad_tag_lbl.configure(text="UUSI KIRJA")
            self.ebook_toggle_btn.configure(
                text="Uusi e-kirja",
                fg_color=CARD_SURFACE,
                border_color=BORDER_COLOR,
                text_color=TEXT_PRIMARY
            )
            self.numpad_sub_lbl.configure(text="Kirjan sivumäärä yhteensä")
            self.numpad_save_btn.configure(text="Aloita kirja ✓")
            self.numpad_input_str = ""
            self.numpad_fresh = False

        self._sync_input_cards()
        self._update_numpad_display()

    def _show_numpad_for_current_page(self):
        """Switches in-place to numpad for updating current reading page or e-book duration."""
        if self.active_book is None:
            self._show_numpad_for_new_book()
            return
        self.numpad_mode = "current_page"
        self.ebook_toggle_btn.pack_forget()
        self.new_book_name_box.pack_forget()
        self.mark_finished_btn.pack_forget()

        if self.is_active_ebook:
            self.numpad_tag_lbl.configure(text="MERKITSE KESTO • KOSKETUSNÄPPÄIMISTÖ")
            self.duration_sub_lbl.configure(text="Nykyinen kohta")
            self.numpad_save_btn.configure(text="Tallenna kesto ✓")
            h, m, s = split_duration(self.active_book.get("current_seconds", 0))
            self.duration_inputs = [
                str(h) if h > 0 else "",
                str(m) if m > 0 else "",
                str(s) if s > 0 else "",
            ]
            self.active_duration_field = 0
            self.duration_field_fresh = True
            self.mark_finished_btn.pack(anchor="w", pady=(8, 0))
        else:
            self.numpad_tag_lbl.configure(text="MERKITSE SIVU • KOSKETUSNÄPPÄIMISTÖ")
            self.numpad_sub_lbl.configure(text="Nykyinen sivu")
            self.numpad_save_btn.configure(text="Tallenna sivu ✓")
            self.numpad_input_str = str(self.current_page) if self.current_page > 0 else ""
            self.numpad_fresh = True

        self._sync_input_cards()
        self._update_numpad_display()

        self._hide_all_views()
        self.numpad_frame.pack(fill="both", expand=True, padx=26, pady=16)
        self.current_view_mode = "numpad"

    def _show_numpad_for_new_book(self):
        """Switches in-place to new book form with prominent name field, e-book toggle, and compact numpad."""
        self.numpad_mode = "total_pages"
        self.creating_ebook = False
        self.mark_finished_btn.pack_forget()
        self.numpad_tag_lbl.configure(text="UUSI KIRJA")
        self.ebook_toggle_btn.configure(
            text="Uusi e-kirja",
            fg_color=CARD_SURFACE,
            border_color=BORDER_COLOR,
            text_color=TEXT_PRIMARY
        )
        self.ebook_toggle_btn.pack(side="right")

        self.new_book_name_entry.delete(0, "end")
        self.new_book_author_entry.delete(0, "end")
        self.new_book_name_box.pack(fill="x", pady=(0, 12), before=self.key_container)

        self.numpad_sub_lbl.configure(text="Kirjan sivumäärä yhteensä")
        self.numpad_save_btn.configure(text="Aloita kirja ✓")
        self.numpad_input_str = ""
        self.numpad_fresh = False
        self.duration_inputs = ["", "", ""]
        self.active_duration_field = 0
        self.duration_field_fresh = False

        self._sync_input_cards()
        self._update_numpad_display()

        self._hide_all_views()
        self.numpad_frame.pack(fill="both", expand=True, padx=26, pady=16)
        self.current_view_mode = "numpad"

    def _show_summary_view(self):
        """Transitions back to the reading summary card."""
        self._hide_all_views()
        self.summary_frame.pack(fill="both", expand=True, padx=24, pady=16)
        self.current_view_mode = "summary"

    def _update_numpad_display(self):
        if self._is_duration_input_mode():
            for idx, btn in enumerate(self.duration_field_btns):
                raw = self.duration_inputs[idx]
                if raw:
                    display_txt = raw.zfill(2) if idx > 0 else raw
                else:
                    display_txt = "00" if idx > 0 else "0"
                is_sel = (idx == self.active_duration_field)
                btn.configure(
                    text=display_txt,
                    border_width=2 if is_sel else 1,
                    border_color=ACCENT_BRASS if is_sel else BORDER_COLOR
                )

            cur_sec = self._get_duration_seconds()
            if self.numpad_mode == "current_page":
                total_sec = self.active_book.get("total_seconds", 0)
                pct = min(100.0, (cur_sec / total_sec) * 100) if total_sec > 0 else 0
                self.duration_meta_lbl.configure(text=f"/ {format_duration(total_sec)}  ({pct:.0f}%)")
            else:
                self.duration_meta_lbl.configure(text=f"Kesto: {format_duration(cur_sec)}")
            return

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
        if self._is_duration_input_mode():
            if self._is_name_entry_focused():
                self.focus_set()
            idx = self.active_duration_field
            if self.duration_field_fresh:
                self.duration_inputs[idx] = ""
                self.duration_field_fresh = False

            max_len = 3 if idx == 0 else 2
            cur_str = self.duration_inputs[idx]
            if len(cur_str) >= max_len:
                return
            if cur_str == "0":
                cur_str = digit
            else:
                cur_str += digit

            # Clamp minutes and seconds to 59
            if idx in (1, 2):
                try:
                    if int(cur_str) > 59:
                        cur_str = "59"
                except ValueError:
                    pass

            self.duration_inputs[idx] = cur_str
            self._update_numpad_display()
            return

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
        if self._is_duration_input_mode():
            self.duration_field_fresh = False
            idx = self.active_duration_field
            if self.duration_inputs[idx]:
                self.duration_inputs[idx] = self.duration_inputs[idx][:-1]
                self._update_numpad_display()
            return

        self.numpad_fresh = False
        if self.numpad_input_str:
            self.numpad_input_str = self.numpad_input_str[:-1]
            self._update_numpad_display()

    def _numpad_clear(self):
        if self._is_duration_input_mode():
            self.duration_field_fresh = False
            idx = self.active_duration_field
            if self.duration_inputs[idx]:
                self.duration_inputs[idx] = ""
            else:
                self.duration_inputs = ["", "", ""]
            self._update_numpad_display()
            return

        self.numpad_fresh = False
        self.numpad_input_str = ""
        self._update_numpad_display()

    def _confirm_numpad(self):
        if self._is_duration_input_mode():
            sec = self._get_duration_seconds()
            if self.numpad_mode == "current_page":
                total_sec = self.active_book.get("total_seconds", 0)
                if sec > total_sec:
                    sec = total_sec
                self.active_book["current_seconds"] = sec
                # Updating progress brings the plant to life and raises streak to at least 1
                self.is_plant_alive = True
                self.streak_count = max(1, self.streak_count)
            else:
                if sec <= 0:
                    return  # Must have positive duration
                entered_title = self.new_book_name_entry.get().strip()
                entered_author = self.new_book_author_entry.get().strip()
                book_title = entered_title if entered_title else f"E-kirja {len(self.books) + 1}"
                self.books.append({
                    "title": book_title,
                    "author": entered_author,
                    "type": "ebook",
                    "current_seconds": 0,
                    "total_seconds": sec,
                })
                self.active_book_index = len(self.books) - 1

            self._show_summary_view()
            self._refresh_all_views()
            return

        try:
            val = int(self.numpad_input_str) if self.numpad_input_str else 0
        except ValueError:
            val = 0

        if self.numpad_mode == "current_page":
            if val > self.total_pages:
                val = self.total_pages
            self.current_page = val
            # Updating page brings the plant to life and raises streak to at least 1
            self.is_plant_alive = True
            self.streak_count = max(1, self.streak_count)
        else:
            if val <= 0:
                return  # Must be positive page count
            entered_title = self.new_book_name_entry.get().strip()
            entered_author = self.new_book_author_entry.get().strip()
            book_title = entered_title if entered_title else f"Kirja {len(self.books) + 1}"
            self.books.append({
                "title": book_title,
                "author": entered_author,
                "type": "book",
                "current_page": 0,
                "total_pages": val,
            })
            self.active_book_index = len(self.books) - 1

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
            if self.active_book is None:
                self.standby_stats.configure(text="Ei valittua kirjaa")
                self.standby_progress.set(0)
            elif self.is_active_ebook:
                cur_sec = self.active_book.get("current_seconds", 0)
                total_sec = self.active_book.get("total_seconds", 0)
                pct = (cur_sec / total_sec * 100) if total_sec > 0 else 0
                self.standby_stats.configure(
                    text=f"{format_duration(cur_sec)} / {format_duration(total_sec)}  •  {pct:.0f}%"
                )
                self.standby_progress.set(min(1.0, cur_sec / max(1, total_sec)))
            else:
                pct = (self.current_page / self.total_pages * 100) if self.total_pages > 0 else 0
                self.standby_stats.configure(text=f"{self.current_page} / {self.total_pages} sivua  •  {pct:.0f}%")
                self.standby_progress.set(min(1.0, self.current_page / max(1, self.total_pages)))

            draw_plant_on_canvas(
                self.standby_plant_canvas,
                phase=self.plant_phase,
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

    def _is_name_entry_focused(self):
        focused = self.focus_get()
        if focused is None:
            return False
        for entry in (self.new_book_name_entry, self.new_book_author_entry):
            if focused == entry or str(focused).startswith(str(entry)):
                return True
        return False

    def _on_key_release(self, event=None):
        """Handles physical keyboard presses if used."""
        if self.is_standby:
            self._exit_standby()
            return
        self.last_interaction_time = time.time()
        self._schedule_idle_check()

        if event is None:
            return

        if self.current_view_mode == "book_list":
            if event.keysym == "Escape":
                if self.pending_delete_index is not None:
                    self._cancel_delete_book()
                else:
                    self._show_summary_view()
            return

        if self.current_view_mode == "numpad":
            if event.keysym == "Escape":
                if self.qwerty_visible:
                    self._close_qwerty()
                else:
                    self._show_summary_view()
                return
            if self.numpad_mode == "total_pages" and self._is_name_entry_focused():
                return
            if self._is_duration_input_mode():
                if event.keysym == "Left":
                    self._select_duration_field((self.active_duration_field - 1) % 3)
                    return
                elif event.keysym == "Right":
                    self._select_duration_field((self.active_duration_field + 1) % 3)
                    return
            if event.keysym in ("Return", "KP_Enter"):
                self._confirm_numpad()
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
        if self.active_book is None:
            self.summary_tag_lbl.configure(text="NYKYINEN KIRJA")
            self.hero_book_title.configure(text="Ei kirjoja kirjastossa")
            self.hero_book_author.configure(text="")
            self.page_caption.configure(text="Nykyinen sivu")
            self.hero_page_big.configure(text="0", font=ctk.CTkFont(size=38, weight="bold"))
            self.hero_total_lbl.configure(text="/ 0 sivua")
            self.hero_pct_big.configure(text="0%")
            self.hero_rem_lbl.configure(text="Lisää uusi kirja", text_color=TEXT_MUTED)
            self.add_pages_btn.configure(text="Lisää uusi kirja")
            self.footer_title_lbl.configure(text="Edistyminen: 0 / 0 sivua")
            self.footer_pct_lbl.configure(text="0.0%")
            self.progress_bar.set(0)
            self.footer_sub_lbl.configure(text="Ei aktiivista kirjaa.", text_color=TEXT_MUTED)
            draw_plant_on_canvas(self.plant_canvas, phase=self.plant_phase, dark_mode=False, w=self.plant_w, h=self.plant_h)
            draw_plant_on_canvas(self.standby_plant_canvas, phase=self.plant_phase, dark_mode=True, w=self.plant_w, h=self.plant_h)
            if self.streak_count == 1:
                self.streak_text.configure(text="Putki: 1 päivä")
            else:
                self.streak_text.configure(text=f"Putki: {self.streak_count} päivää")
            return

        # Update Reading Summary Card header & title
        self.hero_book_title.configure(text=self.active_book["title"])
        author = self.active_book.get("author", "").strip()
        self.hero_book_author.configure(text=author)

        if self.is_active_ebook:
            cur_sec = self.active_book.get("current_seconds", 0)
            total_sec = self.active_book.get("total_seconds", 0)
            pct = (cur_sec / total_sec * 100) if total_sec > 0 else 0
            left_sec = max(0, total_sec - cur_sec)

            self.summary_tag_lbl.configure(text="NYKYINEN E-KIRJA")
            self.page_caption.configure(text="Kuunneltu")
            self.hero_page_big.configure(
                text=format_duration(cur_sec),
                font=ctk.CTkFont(size=30, weight="bold")
            )
            self.hero_total_lbl.configure(text=f"/ {format_duration(total_sec)}")
            self.hero_pct_big.configure(text=f"{pct:.0f}%")
            self.add_pages_btn.configure(text="Päivitä kohta, jossa olet")

            if cur_sec >= total_sec and total_sec > 0:
                self.hero_rem_lbl.configure(text="Valmis! Kuunneltu loppuun", text_color="#15803d")
            else:
                self.hero_rem_lbl.configure(text=f"{format_duration(left_sec)} jäljellä", text_color=TEXT_MUTED)

            # Update Bottom Persistent Progress Bar
            self.footer_title_lbl.configure(
                text=f"Edistyminen: {format_duration(cur_sec)} / {format_duration(total_sec)}"
            )
            self.footer_pct_lbl.configure(text=f"{pct:.1f}%")
            self.progress_bar.set(min(1.0, cur_sec / max(1, total_sec)))

            if cur_sec >= total_sec and total_sec > 0:
                self.footer_sub_lbl.configure(text="E-kirja on kuunneltu loppuun!", text_color="#15803d")
            else:
                self.footer_sub_lbl.configure(
                    text=f"{format_duration(left_sec)} jäljellä maaliin.",
                    text_color=TEXT_MUTED
                )
        else:
            cur = self.current_page
            total = self.total_pages
            pct = (cur / total * 100) if total > 0 else 0
            left = max(0, total - cur)

            self.summary_tag_lbl.configure(text="NYKYINEN KIRJA")
            self.page_caption.configure(text="Nykyinen sivu")
            self.hero_page_big.configure(
                text=str(cur),
                font=ctk.CTkFont(size=38, weight="bold")
            )
            self.hero_total_lbl.configure(text=f"/ {total} sivua")
            self.hero_pct_big.configure(text=f"{pct:.0f}%")
            self.add_pages_btn.configure(text="Päivitä sivu, jolla olet")

            if cur >= total and total > 0:
                self.hero_rem_lbl.configure(text="Valmis! Luettu loppuun", text_color="#15803d")
            else:
                self.hero_rem_lbl.configure(text=f"{left} sivua jäljellä", text_color=TEXT_MUTED)

            # Update Bottom Persistent Progress Bar
            self.footer_title_lbl.configure(text=f"Edistyminen: {cur} / {total} sivua")
            self.footer_pct_lbl.configure(text=f"{pct:.1f}%")
            self.progress_bar.set(min(1.0, cur / max(1, total)))

            if cur >= total and total > 0:
                self.footer_sub_lbl.configure(text="Kirja on luettu loppuun!", text_color="#15803d")
            else:
                self.footer_sub_lbl.configure(text=f"{left} sivua jäljellä maaliin.", text_color=TEXT_MUTED)

        # Update Center Plant Canvas (5 growth phases driven by streak)
        draw_plant_on_canvas(
            self.plant_canvas,
            phase=self.plant_phase,
            dark_mode=False,
            w=self.plant_w,
            h=self.plant_h
        )
        draw_plant_on_canvas(
            self.standby_plant_canvas,
            phase=self.plant_phase,
            dark_mode=True,
            w=self.plant_w,
            h=self.plant_h
        )

        # Update Streak Badge (starts at 0, rises to 1 on update)
        if self.streak_count == 1:
            self.streak_text.configure(text="Putki: 1 päivä")
        else:
            self.streak_text.configure(text=f"Putki: {self.streak_count} päivää")


if __name__ == "__main__":
    app = BookshelfApp()
    app.mainloop()
