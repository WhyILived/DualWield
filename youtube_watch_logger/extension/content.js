console.log('=== CONTENT SCRIPT BOOT ===', Date.now());
chrome.runtime.sendMessage({ type: 'PING' }, r => {
  console.log('[CS] PING ->', r, 'err:', chrome.runtime.lastError?.message);
});

let lastVideoId = null;
let lastSentHash = null;
let debounceTimer = null;

function hashPayload(p) {
  return JSON.stringify([p.videoId, p.title, p.channel]);
}

function collectVideoInfo() {
  if (!location.href.includes('/watch')) return null;

  const params = new URL(location.href).searchParams;
  const videoId = params.get('v');
  if (!videoId) return null;

  const title =
    document.querySelector('h1.title yt-formatted-string')?.textContent?.trim()
    || document.title.replace('- YouTube', '').trim();

  const channel =
    document.querySelector('#channel-name a')?.textContent?.trim()
    || document.querySelector('ytd-channel-name a')?.textContent?.trim()
    || '';

  return {
    ts: Date.now(),
    url: location.href,
    videoId,
    title,
    channel
  };
}

function maybeSend() {
  const info = collectVideoInfo();
  if (!info) return;

  // Only send if video actually changed OR metadata changed
  const h = hashPayload(info);
  if (info.videoId === lastVideoId && h === lastSentHash) {
    return;
  }

  lastVideoId = info.videoId;
  lastSentHash = h;

  console.log('[CS] Sending video info', info);
  chrome.runtime.sendMessage({ type: 'YOUTUBE_VIDEO', data: info }, resp => {
    if (chrome.runtime.lastError) {
      console.warn('[CS] sendMessage error:', chrome.runtime.lastError.message);
    } else {
      console.log('[CS] BG ack:', resp);
    }
  });
}

// Debounced runner e.g. after navigation or DOM mutations
function scheduleSend() {
  clearTimeout(debounceTimer);
  debounceTimer = setTimeout(maybeSend, 600); // allow DOM to settle
}

// 1. Listen to YouTube's internal navigation event.
window.addEventListener('yt-navigate-finish', () => {
  console.log('[CS] yt-navigate-finish');
  scheduleSend();
});

// 2. MutationObserver as backup (URL/title changes without event).
const observer = new MutationObserver((mutations) => {
  // Lightweight heuristic: if location.href changed or title node mutated
  scheduleSend();
});
observer.observe(document.documentElement, {
  subtree: true,
  childList: true,
  characterData: false
});

// 3. Periodic poll fallback (cheap).
setInterval(() => {
  // If youtube SPA changes URL w/out event/DOM we still catch
  maybeSend();
}, 5000);

// Initial attempt after load
scheduleSend();
