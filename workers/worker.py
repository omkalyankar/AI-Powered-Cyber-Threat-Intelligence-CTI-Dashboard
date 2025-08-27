import time
from feeds import abusech, otx

if __name__ == "__main__":
    while True:
        print("[*] Worker running feed collectors...")
        try:
            abusech.run()
            otx.run()
        except Exception as e:
            print("[!] Feed error:", e)
        time.sleep(1800)  # run every 30 minutes
