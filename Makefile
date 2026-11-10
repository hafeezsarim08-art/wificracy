# ============================================================================
#               WIFICRACY: MASTER AUTOMATION SYSTEM SHORTCUTS
# ============================================================================
# Simplifies interaction down to single-word execution rules.
# ============================================================================

.PHONY: install run scan crack clean help

# 1. Register the launcher globally so you can type 'wificracy' from anywhere
install:
	@echo "[*] Registering wificracy command system-wide..."
	@if [ "$$(id -u)" -ne 0 ]; then echo "[-] Error: Run with sudo."; exit 1; fi
	cp wificracy.py /usr/local/bin/wificracy
	chmod +x /usr/local/bin/wificracy
	@echo "[+] Success! You can now launch the tool from anywhere using: sudo wificracy <interface>"

# 2. Short-word shortcut rule to boot the live AP engine instantly
run:
	@if [ -z "$(IFACE)" ]; then echo "[-] Usage: make run IFACE=wlan0"; exit 1; fi
	sudo python3 wificracy.py $(IFACE)

# 3. Short-word shortcut rule to boot the Nmap network scanner
scan:
	sudo python3 wificracy.py -s

# 4. Short-word shortcut rule to boot the cryptographic crackers
crack:
	@if [ -z "$(FILE)" ]; then echo "[-] Usage: make crack FILE=capture.pcap"; exit 1; fi
	sudo python3 wificracy.py -f $(FILE)

# 5. Reset local environment logs and temporary staging profiles
clean:
	@echo "[*] Purging volatile workspace cache profiles..."
	-rm -f /tmp/wificracy_auto_deploy.p3
	-sudo pkill -f bettercap
	-sudo pkill -f wifipumpkin3
	@echo "[+] Workspace clean."

help:
	@echo "Wificracy Command Matrix Shortcuts:"
	@echo "  make install         - Install wificracy as a global system command"
	@echo "  make run IFACE=wlan0 - Boot the live AP interface pipeline"
	@echo "  make scan            - Launch the integrated Nmap network scanner"
	@echo "  make crack FILE=x.pc - Launch the aircrack/hashcat parser loop"
	@echo "  make clean           - Flush active processes and cached profiles"
