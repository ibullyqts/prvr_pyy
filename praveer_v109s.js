const axios = require('axios');

const COOKIE = process.env.INSTA_COOKIE;
const THREAD_ID = '2859755064232019'; // 🎯 Verified 16-digit ID
const MESSAGE_BODY = process.env.MESSAGES;

function getCsrf(cookieString) {
    const match = cookieString.match(/csrftoken=([^;]+)/);
    return match ? match[1] : null;
}

async function sendStrike(agentId) {
    const csrftoken = getCsrf(COOKIE);
    if (!csrftoken) return;

    // 🛡️ GRAPHQL-SPECIFIC HEADERS
    const headers = {
        'authority': 'www.instagram.com',
        'accept': '*/*',
        'content-type': 'application/json', // 👈 Crucial change
        'cookie': COOKIE,
        'origin': 'https://www.instagram.com',
        'referer': `https://www.instagram.com/direct/t/${THREAD_ID}/`,
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36',
        'x-csrftoken': csrftoken,
        'x-ig-app-id': '936619743392459',
        'x-requested-with': 'XMLHttpRequest'
    };

    console.log(`🚀 Agent ${agentId}: GraphQL Engine Armed.`);

    while (true) {
        try {
            const now = Date.now().toString();
            // 📦 JSON Payload (Bypasses 400 Bad Request issues)
            const payload = {
                "recipient_users": [], 
                "thread_id": THREAD_ID,
                "text": MESSAGE_BODY + " " + Math.random().toString(36).substring(7),
                "client_context": now,
                "offline_threading_id": now
            };

            await axios.post(
                'https://www.instagram.com/api/v1/direct_messages/threads/broadcast/text/', 
                payload, 
                { headers, timeout: 15000 }
            );

            process.stdout.write(`✅ [Agent ${agentId}] GraphQL Strike Success\r`);
            
        } catch (e) {
            const status = e.response ? e.response.status : 'ERR';
            console.log(`\n⚠️ [Agent ${agentId}] Status: ${status}`);

            if (status === 400) {
                console.log("📍 Data Mismatch: Re-formatting Payload...");
                // FALLBACK: Trying without brackets for 16-digit IDs
                try {
                    await axios.post(`https://www.instagram.com/api/v1/direct_messages/threads/${THREAD_ID}/send_item/`, `text=${MESSAGE_BODY}`, { headers });
                } catch(err) {}
            }
            await new Promise(r => setTimeout(r, 8000));
        }
        await new Promise(r => setTimeout(r, 1200));
    }
}

sendStrike(1);
