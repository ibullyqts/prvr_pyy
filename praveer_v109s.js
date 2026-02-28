const axios = require('axios');

const COOKIE = process.env.INSTA_COOKIE;
const THREAD_ID = '2859755064232019'; 
const MESSAGE_BODY = process.env.MESSAGES;

function getCsrf(cookieString) {
    const match = cookieString.match(/csrftoken=([^;]+)/);
    return match ? match[1] : null;
}

async function sendStrike(agentId) {
    const csrftoken = getCsrf(COOKIE);
    if (!csrftoken) {
        console.log(`❌ Agent ${agentId}: CSRF extraction failed! Check your cookie format.`);
        return;
    }

    console.log(`📡 Agent ${agentId}: Initializing Handshake...`);

    const headers = {
        'cookie': COOKIE,
        'x-csrftoken': csrftoken,
        'x-ig-app-id': '936619743392459',
        'content-type': 'application/x-www-form-urlencoded',
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36',
        'x-requested-with': 'XMLHttpRequest',
        'referer': `https://www.instagram.com/direct/t/${THREAD_ID}/`
    };

    while (true) {
        try {
            const params = new URLSearchParams({
                'text': MESSAGE_BODY + " " + Math.random().toString(36).substring(7),
                'client_context': Date.now().toString(),
                'thread_ids': `[${THREAD_ID}]`
            });

            // ⚡ Added timeout: 10 seconds
            const response = await axios.post(
                'https://www.instagram.com/api/v1/direct_messages/threads/broadcast/text/', 
                params.toString(), 
                { headers, timeout: 10000 } 
            );

            // 📢 Force immediate log output
            console.log(`✅ [Agent ${agentId}] Hit Successful | Status: ${response.status}`);
            
        } catch (e) {
            const status = e.response ? e.response.status : (e.code === 'ECONNABORTED' ? 'TIMEOUT' : 'NET_ERR');
            console.log(`⚠️ [Agent ${agentId}] Failed | Status: ${status}`);
            
            if (status === 429) {
                console.log(`💤 [Agent ${agentId}] Rate Limited. Sleeping 60s...`);
                await new Promise(r => setTimeout(r, 60000));
            }
        }
        await new Promise(r => setTimeout(r, 2000)); // Slower initial speed for testing
    }
}

// Start only 1 agent first to verify connection
console.log("🚀 Starting Titan Engine...");
sendStrike(1);
