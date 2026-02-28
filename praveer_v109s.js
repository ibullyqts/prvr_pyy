const axios = require('axios');

const COOKIE = process.env.INSTA_COOKIE;
const THREAD_ID = process.env.TARGET_THREAD_ID;
const MESSAGE_BODY = process.env.MESSAGES;

function getCsrf(cookieString) {
    const match = cookieString.match(/csrftoken=([^;]+)/);
    return match ? match[1] : null;
}

async function sendStrike(agentId) {
    const csrftoken = getCsrf(COOKIE);
    if (!csrftoken) return;

    const headers = {
        'cookie': COOKIE,
        'x-csrftoken': csrftoken,
        'x-ig-app-id': '936619743392459', // Standard Web App ID
        'content-type': 'application/x-www-form-urlencoded',
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36',
        'x-requested-with': 'XMLHttpRequest',
        'referer': 'https://www.instagram.com/direct/inbox/'
    };

    while (true) {
        try {
            const now = Date.now();
            // 🔥 The 'broadcast' format works for both DMs and Groups
            const data = new URLSearchParams({
                'text': MESSAGE_BODY + " " + (Math.random() * 1000).toFixed(0),
                'client_context': now.toString(),
                'thread_ids': `[${THREAD_ID}]` // The ID must be inside brackets
            });

            await axios.post(
                'https://www.instagram.com/api/v1/direct_messages/threads/broadcast/text/',
                data.toString(),
                { headers }
            );

            process.stdout.write(`✅ [Agent ${agentId}] Hit\r`);
        } catch (e) {
            const status = e.response ? e.response.status : 'ERR';
            console.log(`\n⚠️ Agent ${agentId} Error: ${status}`);
            
            // If you still get a 404, it means the THREAD_ID is definitely wrong
            if (status === 404) {
                console.log("❌ 404 Found: Your THREAD_ID secret is not recognized. Check the URL of your chat!");
                process.exit(1);
            }
            await new Promise(r => setTimeout(r, 5000));
        }
        await new Promise(r => setTimeout(r, 100));
    }
}

for (let i = 1; i <= 8; i++) { sendStrike(i); }
