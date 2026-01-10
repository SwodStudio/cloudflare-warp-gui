import customtkinter as ctk
import subprocess
import threading
import time
from utils import get_size, get_public_ip
from widgets import ToggleSwitch
from monitor import TrafficMonitor


class WarpAnimatedToggleGUI(ctk.CTk):
    def __init__(self):
        super().__init__()
        self.title("WARP GUI")
        self.geometry("300x400")
        self.configure(fg_color="white")
        self.resizable(False, False)

        self.warp_connected = False
        self.traffic_monitor = TrafficMonitor(self)

        self.logo = ctk.CTkLabel(
            self,
            text="WARP",
            text_color="#FF5B2E",
            font=ctk.CTkFont(size=36, weight="bold"),
        )
        self.logo.pack(pady=(30, 10))

        self.toggle = ToggleSwitch(self, command=self.on_toggle)
        self.toggle.pack(pady=(10, 20))

        self.status_label = ctk.CTkLabel(
            self, text="Checking...", text_color="black", font=ctk.CTkFont(size=20)
        )
        self.status_label.pack()

        self.privacy_label = ctk.CTkLabel(
            self, text="Checking...", text_color="black", font=ctk.CTkFont(size=14)
        )
        self.privacy_label.pack(pady=(5, 20))

        self.traffic_download_label = ctk.CTkLabel(
            self, text="Download: 0 B", text_color="black", font=ctk.CTkFont(size=12)
        )
        self.traffic_download_label.pack()

        self.traffic_upload_label = ctk.CTkLabel(
            self, text="Upload: 0 B", text_color="black", font=ctk.CTkFont(size=12)
        )
        self.traffic_upload_label.pack()

        # bottom bar
        self.bottom = ctk.CTkFrame(self, fg_color="#f2f2f2", corner_radius=0)
        self.bottom.pack(side="bottom", fill="x")
        self.bottom.grid_columnconfigure((0, 2), weight=1)

        self.warp_label = ctk.CTkLabel(
            self.bottom,
            text="WARP\nby Cloudflare",
            font=ctk.CTkFont(size=10),
            text_color="black",
        ).grid(row=0, column=0, padx=10, pady=10, sticky="w")
        self.warp_setting_label = ctk.CTkLabel( # it's a label, cuz there is nothing here, I just want to make it look like windows cloudflare warp application
            self.bottom, text="⚙", font=ctk.CTkFont(size=16)
        ).grid(row=0, column=2, padx=10, pady=10, sticky="e")  # fmt:skip

        self.ip_address_label = ctk.CTkLabel(
            self.bottom,
            text="IP: N/A",
            font=ctk.CTkFont(size=10),
            text_color="black",
        )
        self.ip_address_label.grid(row=1, column=0, padx=10, pady=5, sticky="w")

        self.show_ip_button = ctk.CTkButton(
            self.bottom,
            text="Show IP Address",
            command=self._show_ip_address_action,
            font=ctk.CTkFont(size=10),
            fg_color="#FF5B2E",
            hover_color="#E04F22",
            text_color="white",
            height=20,
        )
        self.show_ip_button.grid(row=1, column=2, padx=10, pady=5, sticky="e")

        self.protocol("WM_DELETE_WINDOW", self.on_closing)
        self.after(300, self.get_status)
        self.after(
            10000, self.get_status
        )  # check after 10sec, for who startup both warp and this program (warp connecting tooooo slow and idk how to sync the status, i don't want keep check)

    def _show_ip_address_action(self):
            current_btn_text = self.show_ip_button.cget("text")
    
            if current_btn_text == "Hide IP Address":
                self.ip_address_label.configure(text="IP: N/A")
                self.show_ip_button.configure(text="Show IP Address")
                return
    
            def task():
                self.after(0, lambda: self.ip_address_label.configure(text="IP: Fetching..."))
                
                try:
                    ip_address = get_public_ip()
                except Exception:
                    ip_address = "Error"
    
                def update_ui():
                    self.ip_address_label.configure(text=f"IP: {ip_address}")
                    self.show_ip_button.configure(text="Hide IP Address")
                
                self.after(0, update_ui)
    
            threading.Thread(target=task, daemon=True).start()

    def on_closing(self):
        if self.traffic_monitor:
            self.traffic_monitor.stop()
        self.destroy()

    def run_command(self, args):
        try:
            return subprocess.run(
                ["warp-cli"] + args, capture_output=True, text=True, timeout=5
            ).stdout
        except:
            return ""

    def get_status(self):
        def task():
            output = self.run_command(["status"])
            if "Connected" in output:
                self.warp_connected = True
            elif "Disconnected" in output:
                self.warp_connected = False
            self.after(0, self.update_ui)

        threading.Thread(target=task, daemon=True).start()

    def update_ui(self):
        self.status_label.configure(
            text="Connected" if self.warp_connected else "Disconnected"
        )
        self.privacy_label.configure(
            text="Your Internet is private."
            if self.warp_connected
            else "Your Internet is not private.",
            text_color="#FF5B2E" if self.warp_connected else "gray",
        )
        if self.toggle.on != self.warp_connected:
            self.toggle.on = self.warp_connected
            self.toggle.animate_toggle(self.warp_connected)

        if self.warp_connected:
            if not self.traffic_monitor._running:
                self.traffic_monitor.start()
        else:
            if self.traffic_monitor._running:
                self.traffic_monitor.stop()

    def update_traffic_labels(self):
        self.traffic_download_label.configure(
            text=f"Download: {get_size(self.traffic_monitor.download_traffic)}"
        )
        self.traffic_upload_label.configure(
            text=f"Upload: {get_size(self.traffic_monitor.upload_traffic)}"
        )

    def on_toggle(self, state):
        def task():
            if state:
                self.status_label.configure(text="Connecting...")
                self.run_command(["connect"])
                self.check_until("Connected")
            else:
                self.status_label.configure(text="Disconnecting...")
                self.run_command(["disconnect"])
                self.check_until("Disconnected")

        threading.Thread(target=task, daemon=True).start()

    def check_until(self, target, max_try=20):
        def task():
            for _ in range(max_try):
                out = self.run_command(["status"])
                if target in out:
                    break
                time.sleep(0.5)
            self.get_status()

        threading.Thread(target=task, daemon=True).start()
