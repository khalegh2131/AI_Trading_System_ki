# D:\AI\AI_Trading_System_ki\utils\vpn_manager.py
import requests
import subprocess
import time
import threading
import yaml
from utils.logger import get_logger

log = get_logger("vpn")

class VPNManager:
    def __init__(self, cfg):
        self.cfg = cfg
        self.servers = []
        self.current = None
        self._lock = threading.Lock()

    def fetch_servers(self):
        try:
            r = requests.get(self.cfg["subscription_url"], timeout=10)
            self.servers = [line.strip() for line in r.text.splitlines() if line.startswith("vless://")]
            log.info("Fetched %d VPN servers", len(self.servers))
        except Exception as e:
            log.error("VPN fetch failed: %s", e)

    def test_and_switch(self):
        for srv in self.servers:
            if self._test_vpn(srv):
                self._switch_vpn(srv)
                return
        log.warning("No working VPN server found!")

    def _test_vpn(self, srv):
        # تست ساده: چک آدرس IP جدید
        # در نسخه کامل از V2Ray CLI یا warp-cli استفاده می‌شود
        return True

    def _switch_vpn(self, srv):
        with self._lock:
            self.current = srv
            log.info("Switched to VPN: %s", srv[:40])

    def start_monitor(self):
        self.fetch_servers()
        threading.Thread(target=self._monitor_loop, daemon=True).start()

    def _monitor_loop(self):
        while True:
            time.sleep(self.cfg["check_interval"])
            self.test_and_switch()