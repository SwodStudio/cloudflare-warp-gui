import psutil
import threading
import time


class TrafficMonitor:
    def __init__(self, parent_gui, interface="CloudflareWARP"):
        self.parent_gui = parent_gui
        self.interface = interface
        self._running = False
        self._thread = None
        self.download_traffic = 0
        self.upload_traffic = 0
        self.initial_rx_bytes = 0
        self.initial_tx_bytes = 0

    def start(self):
        if not self._running:
            self._running = True
            self.download_traffic = 0
            self.upload_traffic = 0
            # get initial stats for interface
            net_io = psutil.net_io_counters(pernic=True)
            if self.interface in net_io:
                self.initial_rx_bytes = net_io[self.interface].bytes_recv
                self.initial_tx_bytes = net_io[self.interface].bytes_sent
            else:
                print(
                    f"Warn! Interface {self.interface} not found, traffic monitoring is add all interfaces up to show something lol"
                )
                # fallback to add all interfaces up if cloudflare interface not found
                self.initial_rx_bytes = sum(
                    n.bytes_recv for n in psutil.net_io_counters(pernic=True).values()
                )
                self.initial_tx_bytes = sum(
                    n.bytes_sent for n in psutil.net_io_counters(pernic=True).values()
                )

            self._thread = threading.Thread(target=self._monitor_thread, daemon=True)
            self._thread.start()

    def stop(self):
        self._running = False
        if self._thread and self._thread.is_alive():
            self._thread.join(timeout=1)  # 1 sec
        self.download_traffic = 0
        self.upload_traffic = 0
        self.parent_gui.update_traffic_labels()  # update label

    def _monitor_thread(self):
        while self._running:
            net_io = psutil.net_io_counters(pernic=True)
            current_rx_bytes = 0
            current_tx_bytes = 0

            if self.interface in net_io:
                current_rx_bytes = net_io[self.interface].bytes_recv
                current_tx_bytes = net_io[self.interface].bytes_sent
            else:
                # if cloudfalre interface not found, it will add all interfaces up
                # if tun0 isn't correct
                # just for show something if yeah.. :3
                current_rx_bytes = sum(n.bytes_recv for n in net_io.values())
                current_tx_bytes = sum(n.bytes_sent for n in net_io.values())

            # make sure it have a starting point so the math actually works
            if self.initial_rx_bytes == 0 and self.initial_tx_bytes == 0:
                self.initial_rx_bytes = current_rx_bytes
                self.initial_tx_bytes = current_tx_bytes

            self.download_traffic = current_rx_bytes - self.initial_rx_bytes
            self.upload_traffic = current_tx_bytes - self.initial_tx_bytes

            self.parent_gui.after(1000, self.parent_gui.update_traffic_labels)
            time.sleep(1)
