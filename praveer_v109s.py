import os
import time
import random
from instagrapi import Client
from instagrapi.exceptions import ClientError

# --- CONFIG ---
SESSION_ID = os.environ.get('INSTA_SESSION_ID')
# Your verified 16-digit ID
THREAD_ID = "2859755064232019"
MESSAGE_TEXT = os.environ.get('MESSAGES', "Titan Engine Active")

def start_strike():
    cl = Client()
    
    # 🔑 LOGIN
    try:
        print("🔗 Connecting via Mobile Emulation...")
        cl.login_by_sessionid(SESSION_ID)
        # Force a 'v2' user agent to look like a modern iPhone
        cl.set_user_agent("Instagram 269.0.0.18.75 (iPhone15,3; iOS 17_0_1; en_US; en-US; scale=3.00; 1290x2796; 444155981)")
        print(f"✅ Logged in as: {cl.username}")
    except Exception as e:
        print(f"❌ Login Failed: {e}")
        return

    print(f"🔥 Targeting Thread: {THREAD_ID}")
    
    while True:
        try:
            # 🚀 FORCING THE MOBILE THREAD ENDPOINT
            # direct_answer bypasses the /broadcast/ path entirely
            cl.direct_answer(THREAD_ID, f"{MESSAGE_TEXT} {random.randint(1000, 9999)}")
            
            print(f"✅ [SUCCESS] Strike Delivered to {THREAD_ID}")
            time.sleep(random.uniform(4, 8)) 
            
        except Exception as e:
            error_msg = str(e)
            if "404" in error_msg:
                print("❌ 404: Instagram is rejecting the ID. Trying User-to-Thread conversion...")
                try:
                    # If it's a User ID, this creates the thread first
                    cl.direct_send(f"{MESSAGE_TEXT} {random.randint(100, 999)}", user_ids=[int(THREAD_ID)])
                    print("✅ [SUCCESS] Message delivered via User path.")
                except Exception as e2:
                    print(f"🛑 Critical: {e2}")
            elif "429" in error_msg:
                print("💤 Rate Limited. Cooling off for 2 minutes...")
                time.sleep(120)
            else:
                print(f"⚠️ Error: {error_msg}")
                time.sleep(10)

if __name__ == "__main__":
    start_strike()
