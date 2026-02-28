const axios = require('axios');

const COOKIE = process.env.INSTA_COOKIE;
const THREAD_ID = '2859755064232019'; // 🎯 Your verified 16-digit ID
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
        'x-ig-app-id': '936619743392459',
        'content-type': 'application/x-www-form-urlencoded',
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36',
        'x-requested-with': 'XMLHttpRequest',
        'referer': `https://www.instagram.com/direct/t/${THREAD_ID}/`
    };

    let errorCount = 0;

    while (true) {
        try {
            const now = Date.now();
            const params = new URLSearchParams({
                'text': MESSAGE_BODY + " " + (Math.random() * 1000).toFixed(0),
                'client_context': now.toString(),
                'thread_ids': `[${THREAD_ID}]`
            });

            await axios.post(
                'https://www.instagram.com/api/v1/direct_messages/threads/broadcast/text/',
                params.toString(),
                { headers }
            );

            process.stdout.write(`✅ [Agent ${agentId}] Strike Success\r`);
            errorCount = 0; // Reset errors on success
        } catch (e) {
            const status = e.response ? e.response.status : 'CONN_ERR';
            
            if (status === 429) {
                // 🛡️ 429 bypass: exponential wait
                const wait = Math.min(60000 * Math.pow(2, errorCount), 300000); 
                console.log(`\n⚠️ Agent ${agentId}: Rate Limited (429). Waiting ${wait/1000}s...`);
                await new Promise(r => setTimeout(r, wait));
                errorCount++;
            } else if (status === 400) {
                console.log(`\n❌ Agent ${agentId}: 400 Bad Request. The ID format [${THREAD_ID}] is being rejected.`);
                process.exit(1);
            } else {
                console.log(`\n⚠️ Agent ${agentId}: Error ${status}`);
                await new Promise(r => setTimeout(r, 10000));
            }
        }
        // Human-like speed
        await new Promise(r => setTimeout(r, 1000 + Math.random() * 500));
    }
}

for (let i = 1; i <= 8; i++) { sendStrike(i); }
