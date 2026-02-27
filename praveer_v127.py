# -*- coding: utf-8 -*-
# 🚀 PROJECT: PRAVEER.OWNS (V130 ANTI-LOGOUT)
# 📅 STATUS: STAGGERED-START | STEALTH-UA | 16-AGENTS

import os, time, sys, base64, threading, random
from concurrent.futures import ThreadPoolExecutor
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager

# --- ⚡ STEALTH CONFIG ---
THREADS_PER_MACHINE = 4            
INTERNAL_DELAY_MS = 60             # Slightly increased to 60ms to avoid 'Burst' detection
PURGE_INTERVAL_SEC = 900          

def get_driver():
    chrome_options = Options()
    chrome_options.add_argument("--headless=new") 
    chrome_options.add_argument("--no-sandbox") 
    chrome_options.add_argument("--disable-dev-shm-usage")
    chrome_options.add_argument("--disable-gpu")
    
    # 🕵️ RANDOM FINGERPRINT: Prevents 'Same Device' Flagging
    ua_list = [
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/121.0.0.0 Safari/537.36",
        "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
        "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/121.0.0.0 Safari/537.36",
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36 Edg/122.0.0.0"
    ]
    chrome_options.add_argument(f"--user-agent={random.choice(ua_list)}")
    
    service = Service(ChromeDriverManager().install())
    return webdriver.Chrome(service=service, options=chrome_options)

def v130_stealth_dispatch(driver, b64_text, delay):
    driver.execute_script("""
        window.praveer_active = true;
        window.msg_count = 0;
        (async function fire(b64, ms) {
            const msg = atob(b64);
            const getBox = () => document.querySelector('div[role="textbox"], textarea, [contenteditable="true"]');
            
            while(window.praveer_active) {
                const box = getBox();
                if (box) {
                    box.focus();
                    const salt = Math.random().toString(36).substring(7);
                    document.execCommand('insertText', false, msg + "\\n" + salt);
                    box.dispatchEvent(new Event('input', { bubbles: true }));
                    
                    let btn = [...document.querySelectorAll('div[role="button"], button')].find(b => 
                        b.innerText === 'Send' || b.textContent === 'Send'
                    );

                    if (btn && !btn.disabled) {
                        btn.click();
                    } else {
                        box.dispatchEvent(new KeyboardEvent('keydown', {key: 'Enter', code: 'Enter', keyCode: 13, bubbles: true}));
                    }
                    window.msg_count++;
                }
                // 🎲 JITTER: Adds 0-10ms random delay to look human
                await new Promise(r => setTimeout(r, ms + Math.floor(Math.random() * 10)));
            }
        })(arguments[0], arguments[1]);
    """, b64_text, delay)

def run_agent(agent_id, machine_id, cookie, target, b64_text):
    # 🕒 STAGGERED START: Agents join 15-30 seconds apart
    time.sleep(agent_id * random.randint(15, 30))
    
    while True:
        driver = None
        try:
            driver = get_driver()
            driver.get("https://www.instagram.com/")
            time.sleep(random.randint(5, 8))
            driver.add_cookie({'name': 'sessionid', 'value': cookie.strip(), 'path': '/', 'domain': '.instagram.com'})
            driver.get(f"https://www.instagram.com/direct/t/{target}/")
            
            # Check if login survived
            time.sleep(10)
            if "login" in driver.current_url:
                print(f"❌ [M{machine_id}-A{agent_id}] Session Expired/Blocked.")
                return 

            v130_stealth_dispatch(driver, b64_text, INTERNAL_DELAY_MS)

            start = time.time()
            while (time.time() - start) < PURGE_INTERVAL_SEC:
                time.sleep(30)
                try:
                    c = driver.execute_script("return window.msg_count;")
                    print(f"💓 [M{machine_id}-A{agent_id}] Strike Active: {c}")
                    sys.stdout.flush()
                except: break
        except: pass
        finally:
            if driver: driver.quit()
            time.sleep(random.randint(10, 20))

def main():
    cookie = os.environ.get("INSTA_COOKIE", "").strip()
    target = os.environ.get("TARGET_THREAD_ID", "").strip()
    raw_text = os.environ.get("MESSAGES", "").strip()
    machine_id = os.environ.get("MACHINE_ID", "1")
    
    b64_text = base64.b64encode(raw_text.encode('utf-8')).decode('utf-8')
    
    with ThreadPoolExecutor(max_workers=THREADS_PER_MACHINE) as executor:
        for i in range(THREADS_PER_MACHINE):
            executor.submit(run_agent, i+1, machine_id, cookie, target, b64_text)
            time.sleep(15)

if __name__ == "__main__":
    main()
