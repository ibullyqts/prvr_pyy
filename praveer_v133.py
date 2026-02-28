import asyncio
import os
import json
from datetime import datetime
from playwright.async_api import async_playwright
from cfonts import render

# --- UI COLORS ---
CYAN, GREEN, RED, YELLOW, RESET = '\033[36m', '\033[1;32m', '\033[1;31m', '\033[1;33m', '\033[0m'
CONFIG_FILE = "config.json"

def banner():
    os.system("cls" if os.name == "nt" else "clear")
    print(render("• OVERLORD •", colors=["cyan", "white"]))
    print(f"{CYAN}Debug-Enabled Guard + Spammer | By Praveer{RESET}\n")

def get_settings():
    if os.path.exists(CONFIG_FILE):
        with open(CONFIG_FILE, "r") as f:
            saved = json.load(f)
        print(f"{GREEN}Saved settings found!{RESET}")
        print(f"Target Name: {saved['target_name']}")
        choice = input(f"\nUse previous settings? (y/n): ").strip().lower()
        if choice == 'y': return saved

    settings = {
        "session_id": input("Session ID: ").strip(),
        "dm_url": input("Group Chat URL: ").strip(),
        "target_name": input("Target Group Name: ").strip(),
        "spam_text": input("Text to Spam (1 min): ").strip()
    }
    with open(CONFIG_FILE, "w") as f:
        json.dump(settings, f, indent=4)
    return settings

banner()
cfg = get_settings()

async def spam_task(page):
    while True:
        try:
            msg_input = page.get_by_role("textbox", name="Message...")
            if await msg_input.is_visible():
                await msg_input.fill(cfg['spam_text'])
                await page.keyboard.press("Enter")
                print(f"{GREEN}[{datetime.now().strftime('%H:%M:%S')}] Spam Sent.{RESET}")
            await asyncio.sleep(60)
        except Exception:
            await asyncio.sleep(5)

async def guard_task(page):
    last_heartbeat = time.time()
    while True:
        try:
            # Broader selectors to find the title
            header_selectors = [
                "header span[role='link']", 
                "header div[role='button'] span",
                "h2", # Sometimes the title is an H2 in the info pane
                "div[role='main'] header span"
            ]
            
            current_name = None
            for selector in header_selectors:
                el = page.locator(selector).first
                if await el.is_visible():
                    current_name = await el.inner_text()
                    break

            if current_name:
                last_heartbeat = time.time() # Reset heartbeat if we see a name
                if current_name.strip() != cfg['target_name'].strip():
                    print(f"{RED}[!] CHANGE DETECTED: '{current_name}' -> '{cfg['target_name']}'{RESET}")
                    
                    # Open Info
                    await page.locator('svg[aria-label*="information"], svg[aria-label*="Details"]').first.click()
                    await asyncio.sleep(1.5)
                    
                    # Change Name
                    change_btn = page.get_by_text("Change name")
                    await change_btn.wait_for(state="visible", timeout=5000)
                    await change_btn.click()
                    
                    field = page.locator('input[name="groupChatName"]')
                    await field.fill("")
                    for char in cfg['target_name']:
                        await field.type(char, delay=350)
                    
                    await page.keyboard.press("Enter")
                    print(f"{GREEN}[+] Restored Successfully.{RESET}")
                    await page.get_by_label("Back").first.click()
            
            # Debug: Print what the bot currently sees every 10s
            if time.time() - last_heartbeat > 10:
                print(f"{YELLOW}[Heartbeat] Current visible name: '{current_name or 'NOT FOUND'}'{RESET}")
                last_heartbeat = time.time()

            # If not found for 30s, Force Refresh
            if not current_name and (time.time() - last_heartbeat > 30):
                print(f"{RED}[!] UI Stale. Force Refreshing...{RESET}")
                await page.reload()
                last_heartbeat = time.time()

            await asyncio.sleep(3)
        except Exception as e:
            await asyncio.sleep(3)

async def main():
    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=False)
        context = await browser.new_context(viewport={'width': 1280, 'height': 720})
        await context.add_cookies([{"name": "sessionid", "value": cfg['session_id'], "domain": ".instagram.com", "path": "/", "secure": True, "httpOnly": True}])
        page = await context.new_page()
        try:
            await page.goto(cfg['dm_url'], wait_until='networkidle')
            print(f"{CYAN}Guard Online...{RESET}")
            await asyncio.gather(guard_task(page), spam_task(page))
        finally:
            await browser.close()

if __name__ == "__main__":
    import time
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print(f"\n{RED}Stopped.{RESET}")
