// background.js
console.log("=== BG boot ===", Date.now());

const sentCache = new Map(); // videoId -> lastSentTs

chrome.runtime.onMessage.addListener((msg, sender, sendResponse) => {
  if (msg.type === 'PING') {
    sendResponse({ ok: true });
    return;
  }

  if (msg.type === 'YOUTUBE_VIDEO') {
    const info = msg.data || {};
    const { videoId } = info;

    if (!videoId) {
      console.warn('[BG] Missing videoId in payload', info);
      sendResponse({ ok: false, error: 'missing videoId' });
      return;
    }

    const prevTs = sentCache.get(videoId);
    if (prevTs && Date.now() - prevTs < 15_000) {
      // Ignore duplicates within 15s window (tune as desired)
      console.log('[BG] Skipping duplicate video send', videoId);
      sendResponse({ ok: true, skipped: true });
      return;
    }

    sentCache.set(videoId, Date.now());
    enqueueSend(info);
    sendResponse({ ok: true, queued: true });
  }
  // No async response afterwards.
});

// --- Simple send queue (robust vs service worker idle) ---
const queue = [];
let sending = false;

function enqueueSend(payload) {
  queue.push({ payload, attempts: 0 });
  processQueue();
}

async function processQueue() {
  if (sending) return;
  sending = true;

  while (queue.length) {
    const item = queue[0];
    try {
      await sendPayload(item.payload);
      queue.shift();
    } catch (e) {
      item.attempts += 1;
      console.warn('[BG] send failed attempt', item.attempts, e.message);
      if (item.attempts >= 5) {
        console.error('[BG] Dropping payload after 5 attempts', item.payload);
        queue.shift();
      } else {
        // exponential-ish backoff
        const delay = Math.min(30000, 1000 * 2 ** item.attempts);
        await sleep(delay);
      }
    }
  }

  sending = false;
}

function sleep(ms) {
  return new Promise(r => setTimeout(r, ms));
}

async function sendPayload(data) {
  const res = await fetch('http://127.0.0.1:5001/log', {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify(data),
    // Keepalive not needed for service worker, but if you later send during unload:
    // keepalive: true
  });
  if (!res.ok) {
    throw new Error('HTTP ' + res.status);
  }
  console.log('[BG] Sent video', data.videoId);
}
