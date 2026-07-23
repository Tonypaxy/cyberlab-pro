import tkinter as tk
from tkinter import ttk, messagebox
import subprocess, threading, os, shutil
from datetime import datetime
from gui.base_module import BaseModule

class WirelessToolkit(BaseModule):
    def __init__(self, parent, db, logger):
        super().__init__(parent)
        self.db = db; self.logger = logger

    def build_content(self):
        self.add_title("Wireless Toolkit", "WiFi, Bluetooth, RFID, NFC, SDR, Zigbee")
        
        tk.Label(self.inner, text="Interface/Target:", font=("Courier",10), fg="#fff", bg="#1a1a2e").pack(anchor="w", padx=10)
        self.target_entry = tk.Entry(self.inner, font=("Courier",10), bg="#0f3460", fg="#fff", relief="flat")
        self.target_entry.pack(fill="x", padx=10, pady=3)
        self.target_entry.insert(0, "wlan0")
        
        bf = tk.Frame(self.inner, bg="#1a1a2e"); bf.pack(fill="x", padx=10, pady=5)
        
        tools = self._detect_tools()
        for name, cmd, color in tools:
            tk.Button(bf, text=name, font=("Courier",8), fg="#000", bg=color, relief="flat", padx=6,
                    command=lambda c=cmd: self._run(c)).pack(side="left", padx=2)
        
        tk.Button(bf, text="STOP", font=("Courier",8,"bold"), fg="#fff", bg="#cc0000", relief="flat", padx=6,
                command=self._stop).pack(side="right", padx=2)
        
        self.output = tk.Text(self.inner, font=("Courier",9), bg="#0a0a0a", fg="#00ff88", relief="flat", height=15)
        self.output.pack(fill="both", expand=True, padx=10, pady=5)
        self.status = self.add_status(f"Ready - {len(tools)} wireless tools detected")

    def _detect_tools(self):
        tools = []
        
        # === WIFI ===
        if shutil.which("aircrack-ng"):
            tools.append(("Aircrack","aircrack-ng -w wordlist.txt capture.cap","#ff4444"))
        if shutil.which("airmon-ng"):
            tools.append(("Airmon Start","airmon-ng start IFACE","#ff4444"))
            tools.append(("Airmon Stop","airmon-ng stop IFACE","#ff4444"))
        if shutil.which("airodump-ng"):
            tools.append(("Airodump","airodump-ng IFACE","#ff4444"))
        if shutil.which("aireplay-ng"):
            tools.append(("Aireplay Deauth","aireplay-ng --deauth 10 -a BSSID IFACE","#ff4444"))
        if shutil.which("wifite"):
            tools.append(("Wifite","wifite -i IFACE","#00ff88"))
        if shutil.which("wifite2"):
            tools.append(("Wifite2","wifite2 -i IFACE","#00ff88"))
        if shutil.which("fluxion"):
            tools.append(("Fluxion","fluxion -i IFACE","#ffaa00"))
        if shutil.which("airgeddon"):
            tools.append(("Airgeddon","airgeddon","#ffaa00"))
        if shutil.which("wifiphisher"):
            tools.append(("Wifiphisher","wifiphisher -i IFACE","#ff4444"))
        if shutil.which("reaver"):
            tools.append(("Reaver WPS","reaver -i IFACE -b BSSID -vv","#ff00ff"))
        if shutil.which("pixiewps"):
            tools.append(("PixieWPS","pixiewps -e PKE -s EHASH1 -z EHASH2 -a AUTHKEY -n EHASH2","#ff00ff"))
        if shutil.which("bully"):
            tools.append(("Bully WPS","bully IFACE -b BSSID","#ff00ff"))
        if shutil.which("hcxdumptool"):
            tools.append(("HCXDump","hcxdumptool -i IFACE -o capture.pcapng","#00ccff"))
        if shutil.which("hcxpcapngtool"):
            tools.append(("HCXConvert","hcxpcapngtool -o hash.hc22000 capture.pcapng","#00ccff"))
        if shutil.which("hashcat"):
            tools.append(("Hashcat WPA","hashcat -m 22000 hash.hc22000 wordlist.txt","#ff0000"))
        if shutil.which("kismet"):
            tools.append(("Kismet","kismet -c IFACE","#58a6ff"))
        if shutil.which("horst"):
            tools.append(("Horst","horst -i IFACE","#58a6ff"))
        if shutil.which("wavemon"):
            tools.append(("Wavemon","wavemon -i IFACE","#58a6ff"))
        if shutil.which("linssid"):
            tools.append(("LinSSID","linssid","#58a6ff"))
        
        # === BLUETOOTH ===
        if shutil.which("bluetoothctl"):
            tools.append(("BT Scan","bluetoothctl scan on","#3fb950"))
            tools.append(("BT Devices","bluetoothctl devices","#3fb950"))
        if shutil.which("hcitool"):
            tools.append(("HCItool Scan","hcitool scan","#3fb950"))
            tools.append(("HCItool Info","hcitool info","#3fb950"))
        if shutil.which("l2ping"):
            tools.append(("L2Ping","l2ping -c 4 MAC","#3fb950"))
        if shutil.which("sdptool"):
            tools.append(("SDP Browse","sdptool browse MAC","#3fb950"))
        if shutil.which("btscanner"):
            tools.append(("BTScanner","btscanner","#3fb950"))
        if shutil.which("blueranger"):
            tools.append(("BlueRanger","blueranger -i hci0","#3fb950"))
        if shutil.which("bluesnarfer"):
            tools.append(("BlueSnarfer","bluesnarfer -b MAC","#3fb950"))
        if shutil.which("crackle"):
            tools.append(("Crackle","crackle -i capture.pcap","#ff4444"))
        if shutil.which("btlejack"):
            tools.append(("BTLEJack","btlejack -f 0x129f3244 -t 0","#ff4444"))
        if shutil.which("gattacker"):
            tools.append(("GATTacker","gattacker","#ff4444"))
        if shutil.which("bettercap"):
            tools.append(("Bettercap BT","bettercap -eval ble.recon on","#cc88ff"))
        
        # === RFID / NFC ===
        if shutil.which("mfoc"):
            tools.append(("Mifare Crack","mfoc -O key.dump","#ffaa00"))
        if shutil.which("mfcuk"):
            tools.append(("Mifare UK","mfcuk -C -R 0:A -s 250 -S 250","#ffaa00"))
        if shutil.which("nfc-list"):
            tools.append(("NFC List","nfc-list","#d2991d"))
        if shutil.which("nfc-mfclassic"):
            tools.append(("NFC Read","nfc-mfclassic r a dump.mfd","#d2991d"))
            tools.append(("NFC Write","nfc-mfclassic w a dump.mfd","#d2991d"))
        if shutil.which("nfc-emulate"):
            tools.append(("NFC Emulate","nfc-emulate-forum-tag4","#d2991d"))
        if shutil.which("pm3"):
            tools.append(("Proxmark3","pm3","#ff4444"))
        if shutil.which("chameleon"):
            tools.append(("Chameleon","chameleon","#ff4444"))
        
        # === SDR (Software Defined Radio) ===
        if shutil.which("rtl_sdr"):
            tools.append(("RTL-SDR","rtl_sdr -f 433M capture.bin","#bc8cff"))
        if shutil.which("rtl_fm"):
            tools.append(("RTL-FM","rtl_fm -f 100M -M wbfm -s 200k -r 48k | aplay","#bc8cff"))
        if shutil.which("rtl_433"):
            tools.append(("RTL-433","rtl_433 -f 433920000","#bc8cff"))
        if shutil.which("dump1090"):
            tools.append(("Dump1090","dump1090 --interactive","#bc8cff"))
        if shutil.which("gqrx"):
            tools.append(("GQRX","gqrx","#bc8cff"))
        if shutil.which("hackrf_transfer"):
            tools.append(("HackRF RX","hackrf_transfer -r capture.bin -f 433M","#ff00ff"))
            tools.append(("HackRF TX","hackrf_transfer -t replay.bin -f 433M","#ff00ff"))
        if shutil.which("hackrf_sweep"):
            tools.append(("HackRF Sweep","hackrf_sweep -f 1:6000 -w 100000","#ff00ff"))
        if shutil.which("gps-sdr-sim"):
            tools.append(("GPS Sim","gps-sdr-sim -e brdc3540.14n -l 40.0,-74.0,100","#bc8cff"))
        if shutil.which("acarsdec"):
            tools.append(("ACARS Decode","acarsdec -r 0 131.525","#bc8cff"))
        if shutil.which("multimon-ng"):
            tools.append(("Multimon","multimon-ng -t raw capture.bin","#bc8cff"))
        if shutil.which("inspectrum"):
            tools.append(("Inspectrum","inspectrum capture.bin","#bc8cff"))
        if shutil.which("universal-radio-hacker"):
            tools.append(("URH","universal-radio-hacker","#bc8cff"))
        
        # === ZIGBEE / Z-WAVE ===
        if shutil.which("zbstumbler"):
            tools.append(("ZBStumbler","zbstumbler","#39c5cf"))
        if shutil.which("zbdump"):
            tools.append(("ZBDump","zbdump -c 11","#39c5cf"))
        if shutil.which("zbconvert"):
            tools.append(("ZBConvert","zbconvert capture.pcap","#39c5cf"))
        if shutil.which("killerbee"):
            tools.append(("KillerBee","killerbee","#39c5cf"))
        if shutil.which("attify-zigbee"):
            tools.append(("Attify Zigbee","attify-zigbee","#39c5cf"))
        
        # === LoRa / LoRaWAN ===
        if shutil.which("lorawan-packet-capture"):
            tools.append(("LoRa Capture","lorawan-packet-capture","#d2991d"))
        if shutil.which("chirpstack"):
            tools.append(("ChirpStack","chirpstack","#d2991d"))
        
        return tools

    def _run(self, cmd):
        target = self.target_entry.get().strip()
        cmd = cmd.replace("IFACE", target)
        
        self.output.insert("end", f"\n{'='*60}\n$ {cmd[:80]}\n{'='*60}\n\n")
        self.output.see("end")
        self.status.config(text=f"Running: {cmd.split()[0]}...")
        
        def do():
            try:
                p = subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, text=True)
                for line in p.stdout:
                    self.output.insert("end", line); self.output.see("end")
                p.wait()
                self.status.config(text=f"Done - Exit: {p.returncode}")
            except Exception as e:
                self.output.insert("end", f"\n[X] {e}\n")
        threading.Thread(target=do, daemon=True).start()

    def _stop(self):
        self.output.insert("end", "\n[STOPPED]\n")
        self.status.config(text="Stopped")
