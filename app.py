from flask import Flask, jsonify, render_template_string
import requests

app = Flask(__name__)

HTML = '''
<!DOCTYPE html>
<html>
<head>
    <meta charset="UTF-8">
    <title>Dashboard</title>
    <style>
        body { font-family: system-ui, sans-serif; background: #0f172a; color: #e2e8f0; margin: 0; padding: 2rem; }
        h1 { text-align: center; margin-bottom: 2rem; }
        .grid { display: grid; grid-template-columns: repeat(auto-fit, minmax(300px, 1fr)); gap: 1.5rem; max-width: 900px; margin: 0 auto; }
        .card { background: #1e293b; padding: 1.5rem; border-radius: 12px; }
        .card h2 { margin-top: 0; font-size: 1.1rem; color: #94a3b8; }
        .value { font-size: 2rem; font-weight: 700; margin: 0.5rem 0; }
        .sub { font-size: 0.9rem; color: #64748b; }
        .error { color: #f87171; }
        .loading { color: #64748b; }
    </style>
</head>
<body>
    <h1>Dashboard en Tiempo Real</h1>
    <div class="grid">
        <div class="card">
            <h2>Clima - Ciudad de México</h2>
            <div id="weather" class="loading">Cargando...</div>
        </div>
        <div class="card">
            <h2>Bitcoin (BTC)</h2>
            <div id="btc" class="loading">Cargando...</div>
        </div>
        <div class="card">
            <h2>Ethereum (ETH)</h2>
            <div id="eth" class="loading">Cargando...</div>
        </div>
        <div class="card">
            <h2>Solana (SOL)</h2>
            <div id="sol" class="loading">Cargando...</div>
        </div>
    </div>
    <script>
        async function load() {
            try {
                const w = await fetch("/api/weather").then(r => r.json());
                document.getElementById("weather").innerHTML =
                    `<div class="value">${w.temperature}°C</div>` +
                    `<div class="sub">Viento: ${w.wind} km/h</div>`;
            } catch(e) {
                document.getElementById("weather").innerHTML = `<div class="error">Error</div>`;
            }
            try {
                const c = await fetch("/api/crypto").then(r => r.json());
                ["btc","eth","sol"].forEach(id => {
                    const d = c[id];
                    document.getElementById(id).innerHTML =
                        `<div class="value">$${d.usd.toLocaleString()}</div>` +
                        `<div class="sub">24h: ${d.change >= 0 ? "+" : ""}${d.change.toFixed(2)}%</div>`;
                });
            } catch(e) {
                ["btc","eth","sol"].forEach(id => {
                    document.getElementById(id).innerHTML = `<div class="error">Error</div>`;
                });
            }
        }
        load();
        setInterval(load, 60000);
    </script>
</body>
</html>
'''

@app.route("/")
def index():
    return render_template_string(HTML)

@app.route("/api/weather")
def weather():
    # Open-Meteo: gratis, sin API key
    url = "https://api.open-meteo.com/v1/forecast?latitude=19.43&longitude=-99.13&current=temperature_2m,wind_speed_10m"
    r = requests.get(url, timeout=10)
    data = r.json()
    current = data.get("current", {})
    return jsonify({
        "temperature": current.get("temperature_2m", "N/A"),
        "wind": current.get("wind_speed_10m", "N/A")
    })

@app.route("/api/crypto")
def crypto():
    # CoinGecko: gratis sin API key para uso básico
    url = "https://api.coingecko.com/api/v3/simple/price?ids=bitcoin,ethereum,solana&vs_currencies=usd&include_24hr_change=true"
    r = requests.get(url, timeout=10)
    data = r.json()
    return jsonify({
        "btc": {"usd": data["bitcoin"]["usd"], "change": data["bitcoin"]["usd_24h_change"]},
        "eth": {"usd": data["ethereum"]["usd"], "change": data["ethereum"]["usd_24h_change"]},
        "sol": {"usd": data["solana"]["usd"], "change": data["solana"]["usd_24h_change"]}
    })

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
