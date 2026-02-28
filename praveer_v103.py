# -*- coding: utf-8 -*-
import os, time, random, threading, sys
from concurrent.futures import ThreadPoolExecutor
from selenium import webdriver
from selenium_stealth import stealth
from selenium.webdriver.chrome.options import Options

# --- ⚡ V103 JS-FORCE CONFIG ---
THREADS = 2 
BURST_SPEED = (1.2, 2.5)
TARGET_ID = os.environ.get("TARGET_THREAD_ID", "2859755064232019")

def get_driver(agent_id):
    options = Options()
    options.add_argument("--headless=new")
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")
    options.add_argument("--disable-gpu")
    options.add_argument(f"user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36")
    
    driver = webdriver.Chrome(options=options)
    stealth(driver, languages=["en-US"], vendor="Google Inc.", platform="Win32", fix_hairline=True)
    return driver

def js_force_send(driver, text):
    """Bypasses the React Virtual DOM to force a message delivery."""
    try:
        entropy = f"{random.randint(100,999)}"
        driver.execute_script("""
            const box = document.querySelector('div[role="textbox"], textarea');
            const msg = arguments[0] + " " + arguments[1];
            
            if (box) {
                box.focus();
                // 1. Inject via execCommand to trigger React's internal 'onChange'
                document.execCommand('insertText', false, msg);
                
                // 2. Find and force-click the Send button (bypasses Enter-key blocks)
                setTimeout(() => {
                    const btns = Array.from(document.querySelectorAll('div[role="button"], button'));
                    const sendBtn = btns.find(b => b.innerText === 'Send' || b.textContent === 'Send');
                    if (sendBtn) {
                        sendBtn.removeAttribute('disabled');
                        sendBtn.click();
                    } else {
                        // 3. Fallback: Synthetic Enter dispatch
                        box.dispatchEvent(new KeyboardEvent('keydown', {
                            key: 'Enter', code: 'Enter', keyCode: 13, which: 13, bubbles: true
                        }));
                    }
                }, 100);
            }
        """, text, entropy)
        return True
    except:
        return False

def run_life_cycle(agent_id, cookie, text):
    while True:
        driver = None
        try:
            driver = get_driver(agent_id)
            driver.get("https://www.instagram.com/")
            time.sleep(5)
            driver.add_cookie({'name': 'sessionid', 'value': cookie.strip(), 'domain': '.instagram.com'})
            
            driver.get(f"https://www.instagram.com/direct/t/{TARGET_ID}/")
            print(f"🚀 Agent {agent_id} Armed on {TARGET_ID}", flush=True)
            time.sleep(15) # UI Handshake

            while True:
                if js_force_send(driver, text):
                    sys.stdout.write("🔥")
                    sys.stdout.flush()
                time.sleep(random.uniform(*BURST_SPEED))
        except Exception as e:
            print(f"\n⚠️ Agent {agent_id} Restarting: {e}", flush=True)
        finally:
            if driver: driver.quit()
            time.sleep(10)

def main():
    cookie = os.environ.get("INSTA_COOKIE", "").strip()
    text = os.environ.get("MESSAGES", "V103_STRIKE").strip()
    
    with ThreadPoolExecutor(max_workers=THREADS) as executor:
        for i in range(THREADS):
            executor.submit(run_life_cycle, i+1, cookie, text)

if __name__ == "__main__":
    main()
