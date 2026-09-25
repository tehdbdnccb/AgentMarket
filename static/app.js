const $ = (id) => document.getElementById(id);

// Build API base URL - detect if on frontend domain and route to backend
const API_BASE = (() => {
  const hostname = window.location.hostname;
  // If on frontend domain, use the backend's public domain
  if (hostname.includes('frontend')) {
    return 'https://agentmarket-production-4e6f.up.railway.app';
  }
  // Otherwise use relative paths (for same-domain requests)
  return '';
})();

async function requestJSON(url, options = {}) {
  const fullUrl = API_BASE + url;
  console.log('Request:', fullUrl, options);
  const response = await fetch(fullUrl, options);
  const text = await response.text();
  let body = {};
  try { body = text ? JSON.parse(text) : {}; } catch { body = { raw: text }; }
  return { response, body };
}

function fmt(value, decimals = 2) {
  const n = Number(value);
  return Number.isFinite(n) ? n.toLocaleString(undefined, { minimumFractionDigits: decimals, maximumFractionDigits: decimals }) : "—";
}

function pct(value) {
  const n = Number(value) * 100;
  return Number.isFinite(n) ? `${n >= 0 ? "+" : ""}${n.toFixed(2)}%` : "—";
}

function time(ts) {
  if (!ts) return "timestamp unavailable";
  return new Date(Number(ts)).toLocaleTimeString([], {hour:"2-digit", minute:"2-digit", second:"2-digit"});
}

async function loadService() {
  try {
    const {response, body} = await requestJSON("/v1/services");
    if (!response.ok) throw new Error("service unavailable");
    const service = body.services[0];
    $("serviceStatus").textContent = service.active ? "service online" : "payment not configured";
    $("serviceStatusDot").classList.toggle("online", service.active);
    $("servicePrice").textContent = service.price;
    $("receiptPrice").textContent = service.price;
    $("networkLabel").textContent = service.network_label;
    $("receiptNetwork").textContent = service.network_label;
  } catch (e) {
    console.error('loadService error:', e);
    $("serviceStatus").textContent = "service unavailable";
  }
}

async function loadMarket() {
  try {
    const {response, body} = await requestJSON("/v1/market/xAAPL");
    if (!response.ok) throw new Error("market unavailable");
    $("livePrice").textContent = `$${fmt(body.price, 2)}`;
    $("liveBid").textContent = `$${fmt(body.bid, 2)}`;
    $("liveAsk").textContent = `$${fmt(body.ask, 2)}`;
    $("liveVolume").textContent = fmt(body.volume_24h, 0);
    $("liveReturn").textContent = pct(body.return_24h);
    $("liveTimestamp").textContent = `OKX · ${time(body.timestamp_ms)}`;
  } catch (e) {
    console.error('loadMarket error:', e);
    $("livePrice").textContent = "—";
    $("liveTimestamp").textContent = "live source unavailable";
  }
}

async function test402() {
  $("traceStatus").textContent = "REQUESTING";
  $("flowOutput").textContent = "> POST /v1/intelligence/financial-snapshot\n> xAAPL · 24h\n\nwaiting for x402 challenge…";
  try {
    const {response, body} = await requestJSON("/v1/intelligence/financial-snapshot", {
      method: "POST",
      headers: {"content-type":"application/json"},
      body: JSON.stringify({asset:"xAAPL", horizon:"24h", freshness_required_seconds:60})
    });
    const paymentRequired = response.headers.get("PAYMENT-REQUIRED");
    const requestId = response.headers.get("X-AgentMarket-Request-ID");
    if (requestId) $("receiptRequest").textContent = requestId;
    if (response.status === 402) {
      $("traceStatus").textContent = "402 READY";
      $("flowOutput").textContent = [
        "> POST /v1/intelligence/financial-snapshot",
        "",
        "← HTTP 402 Payment Required",
        `← PAYMENT-REQUIRED: ${paymentRequired ? "present" : "missing"}`,
        "",
        "Real unpaid request. The configured x402 middleware is asking for payment.",
        "Next: an agent signs the payment and replays the request."
      ].join("\n");
      return;
    }
    $("traceStatus").textContent = `HTTP ${response.status}`;
    $("flowOutput").textContent = JSON.stringify(body, null, 2);
  } catch (e) {
    console.error('test402 error:', e);
    $("traceStatus").textContent = "ERROR";
    $("flowOutput").textContent = "Endpoint unreachable. Configure the service and retry.";
  }
}

async function copyEndpoint() {
  await navigator.clipboard.writeText(`${API_BASE}/v1/intelligence/financial-snapshot`);
  $("copyEndpoint").textContent = "copied";
  setTimeout(() => $("copyEndpoint").textContent = "copy", 1400);
}

$("challengeButton").addEventListener("click", test402);
$("copyEndpoint").addEventListener("click", copyEndpoint);

Promise.all([loadService(), loadMarket()]);

