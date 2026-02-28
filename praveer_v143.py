# -*- coding: utf-8 -*-
# 🚀 PROJECT: PRAVEER.OWNS (V146 OVERDRIVE)
# 📅 STATUS: ZERO-SAFETY | MAX-SPEED | 15-LINE-BURST

import os, time, sys, base64, threading, random
from concurrent.futures import ThreadPoolExecutor
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager

# --- ⚡ OVERDRIVE CONFIG ---
THREADS_PER_MACHINE = 4            
STRIKE_DELAY_MS = 60               # 🔥 Pure Speed (50-80ms range)
PURGE_INTERVAL_SEC = 300           # Reset every 5 mins to prevent CPU throttle

def get_driver():
    chrome_options = Options()
    chrome_options.add_argument("--headless=new") 
    chrome_options.add_argument("--no-sandbox") 
    chrome_options.add_argument("--disable-dev-shm-usage")
    chrome_options.add_argument("--disable-gpu")
    chrome_options.add_argument("--blink-settings=imagesEnabled=false")
    chrome_options.add_argument("--disable-blink-features=AutomationControlled")
    
    ua = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36"
    chrome_options.add_argument(f"--user-agent={ua}")
    
    service = Service(ChromeDriverManager().install())
    return webdriver.Chrome(service=service, options=chrome_options)

def v146_dispatch(driver, b64_text, delay):
    driver.execute_script("""
        window.praveer_active = true;
        window.msg_count = 0;
        
        // Safety Decode
        const rawText = decodeURIComponent(escape(atob(arguments[0])));

        async function strike(msg, ms) {
            const getBox = () => document.querySelector('div[role="textbox"], textarea, [contenteditable="true"]');
            
            while(window.praveer_active) {
                const box = getBox();
                if (box) {
                    box.focus();
                    // Direct Command Injection for Speed
                    document.execCommand('insertText', false, msg);
                    box.dispatchEvent(new Event('input', { bubbles: true }));
                    
                    let btn = [...document.querySelectorAll('div[role="button"], button')].find(b => b.innerText === 'Send' || b.textContent === 'Send');
                    if (btn) {
                        btn.click();
                    } else {
                        box.dispatchEvent(new KeyboardEvent('keydown', {key: 'Enter', code: 'Enter', keyCode: 13, bubbles: true}));
                    }
                    window.msg_count++;
                }
                // 🔥 No Jitter, No Recovery, Just Speed
                await new Promise(r => setTimeout(r, ms));
            }
        }
        strike(rawText, arguments[1]);
    """, b64_text, delay)

def run_agent(agent_id, machine_id, cookie, target, b64_text):
    # Instant Entry (3s stagger only to prevent crash)
    time.sleep(agent_id * 3) 
    driver = None
    try:
        driver = get_driver()
        driver.get("https://www.instagram.com/")
        time.sleep(5)
        driver.add_cookie({'name': 'sessionid', 'value': cookie.strip(), 'path': '/', 'domain': '.instagram.com'})
        driver.get(f"https://www.instagram.com/direct/t/{target}/")
        time.sleep(8)
        
        if "login" in driver.current_url: return 

        v146_dispatch(driver, b64_text, STRIKE_DELAY_MS)
        time.sleep(PURGE_INTERVAL_SEC)
    except: pass
    finally:
        if driver: driver.quit()

def main():
    cookie = os.environ.get("INSTA_COOKIE", "").strip()
    target = os.environ.get("TARGET_THREAD_ID", "").strip()
    # Pulls exactly what you paste in secrets
    raw_msg = os.environ.get("MESSAGES", "").strip()
    b64_msg = base64.b64encode(raw_msg.encode('utf-8')).decode('utf-8')
    machine_id = os.environ.get("MACHINE_ID", "1")
    
    while True:
        with ThreadPoolExecutor(max_workers=THREADS_PER_MACHINE) as executor:
            for i in range(THREADS_PER_MACHINE):
                executor.submit(run_agent, i+1, machine_id, cookie, target, b64_msg)
            time.sleep(PURGE_INTERVAL_SEC + 10)

if __name__ == "__main__":
    main()
