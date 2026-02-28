# -*- coding: utf-8 -*-
# 🚀 PROJECT: PRAVEER.OWNS (V103 CRON-MACHINE #77)
# 📅 STATUS: STABLE-STRIKE | 8-MACHINES | 16-AGENTS

import os, time, random, threading, sys, tempfile
import undetected_chromedriver as uc
from selenium_stealth import stealth

# --- ⚡ #77 CONFIG ---
THREADS = 2 # 2 Agents per Machine (Matrix x 8 = 16 Agents)
STRIKE_DELAY = 0.5 
TARGET_ID = os.environ.get("TARGET_THREAD_ID", "2859755064232019")
MACHINE_ID = os.environ.get("MACHINE_ID", "1")

def get_driver(agent_id):
    options = uc.ChromeOptions()
    options.add_argument("--headless")
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")
    options.add_argument("--window-size=500,400") 
    
    temp_dir = os.path.join(tempfile.gettempdir(), f"pv_v103_77_m{MACHINE_ID}_a{agent_id}")
    driver = uc.Chrome(options=options, user_data_dir=temp_dir, version_main=122)
    driver.set_page_load_timeout(25)
    
    stealth(driver, languages=["en-US"], vendor="Google Inc.", platform="Win32", fix_hairline=True)
    return driver

def force_lexical_strike(driver, text):
    """Bypasses React 18 DOM by injecting via the native browser setter."""
    try:
        entropy = f"{random.randint(100,999)}"
        driver.execute_script("""
            const box = document.querySelector('div[role="textbox"]');
            const msg = arguments[0] + " " + arguments[1];
            if (box) {
                box.focus();
                // 🛠️ The V103 #77 Special: Native Setter Bypass
                const nativeSetter = Object.getOwnPropertyDescriptor(window.HTMLElement.prototype, 'innerText').set;
                nativeSetter.call(box, msg);
                box.dispatchEvent(new Event('input', { bubbles: true }));

                setTimeout(() => {
                    const sendBtn = Array.from(document.querySelectorAll('button')).find(b => b.innerText.includes('Send'));
                    if (sendBtn) { sendBtn.click(); }
                    else { box.dispatchEvent(new KeyboardEvent('keydown', {key: 'Enter', bubbles: true})); }
                }, 100);
            }
        """, text, entropy)
        return True
    except: return False

def run_agent(agent_id, cookie, text):
    time.sleep(agent_id * 10) 
    while True:
        driver = None
        try:
            driver = get_driver(agent_id)
            driver.get("https://www.instagram.com/")
            time.sleep(5)
            driver.add_cookie({'name': 'sessionid', 'value': cookie.strip(), 'domain': '.instagram.com'})
            driver.get(f"https://www.instagram.com/direct/t/{TARGET_ID}/")
            
            # 🔒 Pin Navigation to prevent the 'Reload Loop'
            driver.execute_script("window.location.reload = function() { return false; };")
            print(f"✅ M{MACHINE_ID}-A{agent_id} ARMED", flush=True)
            time.sleep(15)

            while True:
                if "direct/t/" not in driver.current_url: break
                if force_lexical_strike(driver, text):
                    sys.stdout.write(f"[{MACHINE_ID}-{agent_id}]")
                    sys.stdout.flush()
                time.sleep(STRIKE_DELAY)
        except: pass
        finally:
            if driver: driver.quit()
            time.sleep(5)

def main():
    cookie = os.environ.get("INSTA_COOKIE", "").strip()
    text = os.environ.get("MESSAGES", "V103_77").strip()
    for i in range(THREADS):
        t = threading.Thread(target=run_agent, args=(i+1, cookie, text))
        t.daemon = True
        t.start()
    while True: time.sleep(10)

if __name__ == "__main__":
    main()
