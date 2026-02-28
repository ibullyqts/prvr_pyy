# -*- coding: utf-8 -*-
import os, time, random, threading, sys, tempfile
import undetected_chromedriver as uc
from selenium_stealth import stealth

# --- ⚡ SLIM-STEALTH CONFIG ---
THREADS = 2  # 🚀 REDUCED TO 2: This prevents GitHub from cancelling the run
STRIKE_DELAY = 0.5 
TARGET_ID = os.environ.get("TARGET_THREAD_ID", "2859755064232019")
MACHINE_ID = os.environ.get("MACHINE_ID", "1")

def get_driver(agent_id):
    options = uc.ChromeOptions()
    options.add_argument("--headless")
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")
    options.add_argument("--disable-gpu")
    # 📉 Low-Res mode saves massive amounts of RAM
    options.add_argument("--window-size=400,300") 
    
    temp_dir = os.path.join(tempfile.gettempdir(), f"pv_slim_m{MACHINE_ID}_a{agent_id}")
    
    # Force a specific version to avoid 'hanging' on download
    driver = uc.Chrome(options=options, user_data_dir=temp_dir, version_main=122)
    driver.set_page_load_timeout(20)
    
    stealth(driver, languages=["en-US"], vendor="Google Inc.", platform="Win32", fix_hairline=True)
    return driver

def v103_hyper_force(driver, text):
    try:
        entropy = f"{random.randint(100,999)}"
        driver.execute_script("""
            const box = document.querySelector('div[role="textbox"]');
            if (box) {
                const nativeSetter = Object.getOwnPropertyDescriptor(window.HTMLElement.prototype, 'innerText').set;
                nativeSetter.call(box, arguments[0] + " " + arguments[1]);
                box.dispatchEvent(new Event('input', { bubbles: true }));
                
                const sendBtn = Array.from(document.querySelectorAll('button')).find(b => b.innerText.includes('Send'));
                if (sendBtn) { sendBtn.click(); }
                else { box.dispatchEvent(new KeyboardEvent('keydown', {key: 'Enter', bubbles: true})); }
            }
        """, text, entropy)
        return True
    except: return False

def run_agent(agent_id, cookie, text):
    time.sleep(agent_id * 10) # ⏳ Longer stagger for stability
    while True:
        driver = None
        try:
            driver = get_driver(agent_id)
            driver.get("https://www.instagram.com/")
            time.sleep(5)
            driver.add_cookie({'name': 'sessionid', 'value': cookie.strip(), 'domain': '.instagram.com'})
            
            driver.get(f"https://www.instagram.com/direct/t/{TARGET_ID}/")
            print(f"✅ [M{MACHINE_ID}-A{agent_id}] ARMED", flush=True)
            time.sleep(15)

            while True:
                if "direct/t/" not in driver.current_url:
                    print(f"🛑 Detected. Sleeping...", flush=True)
                    time.sleep(60) 
                    break 

                if v103_hyper_force(driver, text):
                    sys.stdout.write(f"[{MACHINE_ID}-{agent_id}]")
                    sys.stdout.flush()
                
                time.sleep(STRIKE_DELAY + random.uniform(0.1, 0.3))
        except: pass
        finally:
            if driver: driver.quit()
            time.sleep(10)

def main():
    cookie = os.environ.get("INSTA_COOKIE", "").strip()
    text = os.environ.get("MESSAGES", "V103").strip()
    # Using simple threading to keep overhead low
    for i in range(THREADS):
        t = threading.Thread(target=run_agent, args=(i+1, cookie, text))
        t.start()

if __name__ == "__main__":
    main()
