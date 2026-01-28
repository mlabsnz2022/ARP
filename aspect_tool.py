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
        screen = Gdk.Screen.get_default()
        provider = Gtk.CssProvider()
        style = b"""
            /* Main Window: Deep Forest Gray-Green */
            window { 
                background-color: #1a2421; 
                color: #e0e0e0; 
            }
            
            /* Inputs: Slightly lighter muted forest green */
            entry { 
                background-color: #24302c; 
                color: white; 
                border: 1px solid #364540; 
                border-radius: 8px;
                font-size: 18px;
                padding: 12px;
                font-weight: 500;
            }
            
            /* Highlight border when typing */
            entry:focus { border-color: #4e9a06; }

            label { font-weight: bold; margin-bottom: 5px; color: #9aad9a; font-size: 14px; }
            
            /* Detected Ratio Box */
            .ratio-box { 
                background-color: #131a18; 
                padding: 15px; 
                border-radius: 8px; 
                font-size: 18px; 
                color: #729fcf; /* Muted blue looks great against green */
                font-weight: bold;
            }
            
        /* Dropdown and special entries */
            combobox, combobox text {
                background-color: #24302c;
                color: white;
                border: 1px solid #364540;
                border-radius: 8px;
                padding: 10px;
            }
            
            button {
                background-color: #2c3834;
                color: #e0e0e0;
                border: 1px solid #364540;
                border-radius: 8px;
                padding: 5px 10px;
                font-size: 18px;
            }
            
            button:hover {
                background-color: #364540;
            }
            
            separator { margin: 10px 0; background-color: #2c3834; }
        """
        provider.load_from_data(style)
        Gtk.StyleContext.add_provider_for_screen(screen, provider, Gtk.STYLE_PROVIDER_PRIORITY_APPLICATION)

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
        
        hbox_presets.pack_start(self.preset_combo, True, True, 0)
        hbox_presets.pack_start(self.dpi_entry, False, False, 0)
        hbox_presets.pack_start(self.swap_btn, False, False, 0)
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
