import gi
gi.require_version('Gtk', '3.0')
from gi.repository import Gtk, Gdk

class AspectRatioApp(Gtk.Window):
    def __init__(self):
        super().__init__(title="Aspect Ratio Tool")
        self.set_role("aspect-ratio-tool")
        self.set_wmclass("aspect-ratio-tool", "aspect-ratio-tool")
        
        # Set the icon for taskbar/panel
        # Make sure this file exists!
        try:
            self.set_icon_from_file("/home/mlabs/Apps/my-apps/ar_calc/icon.png")
        except:
            pass
            
        self.set_border_width(20)
        self.set_default_size(380, 500)

        # Apply Enhanced Dark Mode CSS
        self.screen = Gdk.Screen.get_default()
        self.provider = Gtk.CssProvider()
        Gtk.StyleContext.add_provider_for_screen(self.screen, self.provider, Gtk.STYLE_PROVIDER_PRIORITY_APPLICATION)
        
        # Initial Color
        initial_color = Gdk.RGBA()
        initial_color.parse("#1a2421")
        self.update_theme(initial_color)

        # Aspect Ratio Data (inches or ratios)
        self.presets = {
            "Select a Preset...": None,
            "--- Print ---": "header",
            "A4 (8.27 x 11.69)": (8.27, 11.69),
            "A3 (11.69 x 16.54)": (11.69, 16.54),
            "Letter (8.5 x 11)": (8.5, 11),
            "Legal (8.5 x 14)": (8.5, 14),
            "--- Photo ---": "header",
            "4x6 Photo": (4, 6),
            "5x7 Photo": (5, 7),
            "8x10 Photo": (8, 10),
            "11x14 Photo": (11, 14),
            "--- Film / Digital ---": "header",
            "16:9 HD/4K": (16, 9),
            "4:3 Standard": (4, 3),
            "21:9 Ultrawide": (21, 9),
            "1.85:1 Cinema": (1.85, 1),
            "2.39:1 Anamorphic": (2.39, 1),
            "--- Social Media ---": "header",
            "Instagram Square (1:1)": (1, 1),
            "Instagram Portrait (4:5)": (4, 5),
            "TikTok / Reel (9:16)": (9, 16),
            "Social Banner (3:1)": (3, 1),
        }

        # Layout Container
        vbox = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=15)
        self.add(vbox)

        # Presets Row
        vbox.pack_start(Gtk.Label(label="Presets & DPI", xalign=0), False, False, 0)
        hbox_presets = Gtk.Box(spacing=10)
        
        self.preset_combo = Gtk.ComboBoxText()
        for name in self.presets.keys():
            self.preset_combo.append_text(name)
        self.preset_combo.set_active(0)
        
        self.dpi_entry = Gtk.Entry(text="300")
        self.dpi_entry.set_placeholder_text("DPI")
        self.dpi_entry.set_width_chars(5)
        
        self.swap_btn = Gtk.Button(label="⇄")
        self.swap_btn.set_tooltip_text("Swap Orientation")
        
        self.color_btn = Gtk.ColorButton()
        self.color_btn.set_rgba(initial_color)
        self.color_btn.set_tooltip_text("Pick Theme Color")
        
        hbox_presets.pack_start(self.preset_combo, True, True, 0)
        hbox_presets.pack_start(self.dpi_entry, False, False, 0)
        hbox_presets.pack_start(self.swap_btn, False, False, 0)
        hbox_presets.pack_start(self.color_btn, False, False, 0)
        vbox.pack_start(hbox_presets, False, False, 0)

        vbox.pack_start(Gtk.Separator(), False, False, 5)

        # Inputs for Original Res
        vbox.pack_start(Gtk.Label(label="Original Resolution (X x Y)", xalign=0), False, False, 0)
        hbox_orig = Gtk.Box(spacing=10)
        
        self.orig_x = Gtk.Entry(text="3440")
        self.orig_y = Gtk.Entry(text="1440")
        
        # Set height requests to ensure they look big vertically
        self.orig_x.set_size_request(-1, 50)
        self.orig_y.set_size_request(-1, 50)
        
        hbox_orig.pack_start(self.orig_x, True, True, 0)
        hbox_orig.pack_start(self.orig_y, True, True, 0)
        vbox.pack_start(hbox_orig, False, False, 0)

        # Ratio Display
        self.ratio_label = Gtk.Label(label="Detected Ratio: 21:9")
        self.ratio_label.get_style_context().add_class("ratio-box")
        vbox.pack_start(self.ratio_label, False, False, 10)

        # New Resolution Section
        vbox.pack_start(Gtk.Separator(), False, False, 10)
        
        vbox.pack_start(Gtk.Label(label="New Width (X)", xalign=0), False, False, 0)
        self.new_x = Gtk.Entry(placeholder_text="Enter width...")
        self.new_x.set_size_request(-1, 50)
        vbox.pack_start(self.new_x, False, False, 0)

        vbox.pack_start(Gtk.Label(label="New Height (Y)", xalign=0), False, False, 0)
        self.new_y = Gtk.Entry(placeholder_text="Enter height...")
        self.new_y.set_size_request(-1, 50)
        vbox.pack_start(self.new_y, False, False, 0)

        # Connect the Logic
        self.preset_combo.connect("changed", self.on_preset_changed)
        self.dpi_entry.connect("changed", self.on_preset_changed)
        self.swap_btn.connect("clicked", self.swap_orientation)
        self.color_btn.connect("color-set", self.on_color_set)
        self.orig_x.connect("changed", self.update_calculation)
        self.orig_y.connect("changed", self.update_calculation)
        self.new_x.connect("changed", self.calc_height)
        self.new_y.connect("changed", self.calc_width)

    # Logic functions
    def swap_orientation(self, widget):
        x_val = self.orig_x.get_text()
        y_val = self.orig_y.get_text()
        self.orig_x.set_text(y_val)
        self.orig_y.set_text(x_val)

    def on_color_set(self, widget):
        self.update_theme(widget.get_rgba())

    def update_theme(self, rgba):
        r, g, b = rgba.red, rgba.green, rgba.blue
        brightness = (r * 0.299 + g * 0.587 + b * 0.114)
        bg_hex = "#{:02x}{:02x}{:02x}".format(int(r*255), int(g*255), int(b*255))
        
        if brightness > 0.5:
            text_color = "#1a2421"
            secondary_text = "#4a5d58"
            input_bg = "rgba(0,0,0,0.05)"
            border_color = "rgba(0,0,0,0.2)"
            accent = "#2e3436"
        else:
            text_color = "#e0e0e0"
            secondary_text = "#9aad9a"
            input_bg = "rgba(255,255,255,0.1)"
            border_color = "rgba(255,255,255,0.2)"
            accent = "#729fcf"

        css = f"""
            window {{ background-color: {bg_hex}; color: {text_color}; }}
            entry {{ background-color: {input_bg}; color: {text_color}; border: 1px solid {border_color}; border-radius: 8px; font-size: 18px; padding: 12px; }}
            entry:focus {{ border-color: {accent}; }}
            label {{ font-weight: bold; margin-bottom: 5px; color: {secondary_text}; font-size: 14px; }}
            .ratio-box {{ background-color: rgba(0,0,0,0.2); padding: 15px; border-radius: 8px; font-size: 18px; color: {accent}; font-weight: bold; }}
            combobox, combobox text {{ background-color: {input_bg}; color: {text_color}; border: 1px solid {border_color}; border-radius: 8px; padding: 10px; }}
            button {{ background-color: {input_bg}; color: {text_color}; border: 1px solid {border_color}; border-radius: 8px; padding: 5px 10px; font-size: 18px; }}
            button:hover {{ background-color: rgba(255,255,255,0.1); }}
            separator {{ margin: 10px 0; background-color: {border_color}; }}
        """
        self.provider.load_from_data(css.encode())

    def on_preset_changed(self, widget):
        preset_name = self.preset_combo.get_active_text()
        if not preset_name or self.presets.get(preset_name) is None or self.presets.get(preset_name) == "header":
            return
        
        try:
            dpi = float(self.dpi_entry.get_text())
            w_inches, h_inches = self.presets[preset_name]
            
            # Update original resolution fields
            self.orig_x.set_text(str(round(w_inches * dpi)))
            self.orig_y.set_text(str(round(h_inches * dpi)))
        except ValueError:
            pass
    def get_gcd(self, a, b):
        while b:
            a, b = b, a % b
        return a

    def update_calculation(self, widget):
        try:
            x, y = int(self.orig_x.get_text()), int(self.orig_y.get_text())
            common = self.get_gcd(x, y)
            self.ratio_label.set_text(f"Detected Ratio: {int(x/common)}:{int(y/common)}")
        except: pass

    def calc_height(self, widget):
        if self.new_x.is_focus():
            try:
                ratio = int(self.orig_x.get_text()) / int(self.orig_y.get_text())
                val = int(self.new_x.get_text()) / ratio
                self.new_y.set_text(str(round(val)))
            except: self.new_y.set_text("")

    def calc_width(self, widget):
        if self.new_y.is_focus():
            try:
                ratio = int(self.orig_x.get_text()) / int(self.orig_y.get_text())
                val = int(self.new_y.get_text()) * ratio
                self.new_x.set_text(str(round(val)))
            except: self.new_x.set_text("")

if __name__ == "__main__":
    win = AspectRatioApp()
    win.connect("destroy", Gtk.main_quit)
    win.show_all()
    Gtk.main()
