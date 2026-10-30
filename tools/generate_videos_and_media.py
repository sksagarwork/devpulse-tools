import os, subprocess, shutil

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
MEDIA_DIR = os.path.join(BASE_DIR, "media")
VIDEO_DIR = os.path.join(MEDIA_DIR, "videos")
FRAMES_DIR = os.path.join(MEDIA_DIR, "frames")

os.makedirs(VIDEO_DIR, exist_ok=True)
os.makedirs(FRAMES_DIR, exist_ok=True)

def render_svg_to_png(svg_str, png_path):
    svg_path = png_path.replace(".png", ".svg")
    with open(svg_path, "w", encoding="utf-8") as f:
        f.write(svg_str)
    subprocess.run(["convert", svg_path, png_path], check=True)
    os.remove(svg_path)

# ==============================================================================
# 1. GENERATE HIGH-RES OG SOCIAL PREVIEW (1200x630)
# ==============================================================================
print("Generating og-image.png...")
og_svg = """<svg xmlns="http://www.w3.org/2000/svg" width="1200" height="630" viewBox="0 0 1200 630">
  <defs>
    <linearGradient id="bg" x1="0%" y1="0%" x2="100%" y2="100%">
      <stop offset="0%" stop-color="#0b0f19"/>
      <stop offset="100%" stop-color="#0f172a"/>
    </linearGradient>
    <linearGradient id="cardGrad" x1="0%" y1="0%" x2="100%" y2="100%">
      <stop offset="0%" stop-color="#1e293b"/>
      <stop offset="100%" stop-color="#111827"/>
    </linearGradient>
    <linearGradient id="accentGrad" x1="0%" y1="0%" x2="100%" y2="0%">
      <stop offset="0%" stop-color="#3b82f6"/>
      <stop offset="50%" stop-color="#8b5cf6"/>
      <stop offset="100%" stop-color="#10b981"/>
    </linearGradient>
  </defs>
  <rect width="1200" height="630" fill="url(#bg)"/>
  <rect x="40" y="40" width="1120" height="550" rx="24" fill="url(#cardGrad)" stroke="#334155" stroke-width="2"/>
  
  <!-- Header -->
  <text x="80" y="110" fill="#3b82f6" font-family="DejaVu Sans, sans-serif" font-weight="bold" font-size="28">⚡ CRYPTOCALC PRO</text>
  <text x="80" y="180" fill="#ffffff" font-family="DejaVu Sans, sans-serif" font-weight="bold" font-size="52">High-Precision Web3 Financial Suite</text>
  <text x="80" y="235" fill="#94a3b8" font-family="DejaVu Sans, sans-serif" font-size="24">Zero KYC • 100% Client-Side Math • Free Open-Source DeFi Calculators</text>

  <!-- 3 Feature Pillars -->
  <rect x="80" y="275" width="320" height="230" rx="16" fill="#0f172a" stroke="#334155" stroke-width="2"/>
  <text x="110" y="340" fill="#3b82f6" font-family="DejaVu Sans, sans-serif" font-size="40">⛽</text>
  <text x="110" y="390" fill="#ffffff" font-family="DejaVu Sans, sans-serif" font-weight="bold" font-size="22">ETH Gas &amp; L2</text>
  <text x="110" y="430" fill="#94a3b8" font-family="DejaVu Sans, sans-serif" font-size="16">Live Gwei to USD Converter</text>
  <text x="110" y="460" fill="#94a3b8" font-family="DejaVu Sans, sans-serif" font-size="16">Uniswap V3 &amp; NFT gas</text>
  <text x="110" y="490" fill="#10b981" font-family="DejaVu Sans, sans-serif" font-weight="bold" font-size="16">99.7% L2 Savings Model</text>

  <rect x="440" y="275" width="320" height="230" rx="16" fill="#0f172a" stroke="#334155" stroke-width="2"/>
  <text x="470" y="340" fill="#10b981" font-family="DejaVu Sans, sans-serif" font-size="40">📈</text>
  <text x="470" y="390" fill="#ffffff" font-family="DejaVu Sans, sans-serif" font-weight="bold" font-size="22">Crypto SIP &amp; DCA</text>
  <text x="470" y="430" fill="#94a3b8" font-family="DejaVu Sans, sans-serif" font-size="16">Monthly Bitcoin accumulation</text>
  <text x="470" y="460" fill="#94a3b8" font-family="DejaVu Sans, sans-serif" font-size="16">Compounding CAGR models</text>
  <text x="470" y="490" fill="#3b82f6" font-family="DejaVu Sans, sans-serif" font-weight="bold" font-size="16">Halving cycle simulator</text>

  <rect x="800" y="275" width="320" height="230" rx="16" fill="#0f172a" stroke="#334155" stroke-width="2"/>
  <text x="830" y="340" fill="#8b5cf6" font-family="DejaVu Sans, sans-serif" font-size="40">⚖️</text>
  <text x="830" y="390" fill="#ffffff" font-family="DejaVu Sans, sans-serif" font-weight="bold" font-size="22">Impermanent Loss</text>
  <text x="830" y="430" fill="#94a3b8" font-family="DejaVu Sans, sans-serif" font-size="16">AMM constant product math</text>
  <text x="830" y="460" fill="#94a3b8" font-family="DejaVu Sans, sans-serif" font-size="16">LP swap fees vs HODL</text>
  <text x="830" y="490" fill="#f59e0b" font-family="DejaVu Sans, sans-serif" font-weight="bold" font-size="16">Uniswap V2 &amp; V3 Pools</text>

  <!-- URL footer -->
  <text x="80" y="555" fill="#38bdf8" font-family="DejaVu Sans, sans-serif" font-weight="bold" font-size="22">👉 sksagarwork.github.io/devpulse-tools/</text>
</svg>
"""
og_png = os.path.join(BASE_DIR, "og-image.png")
render_svg_to_png(og_svg, og_png)

# ==============================================================================
# Helper to assemble 1080x1920 video with chimes & SVG frames
# ==============================================================================
def compile_video_from_svgs(video_name, svg_slides, audio_freq=500):
    tmp_dir = os.path.join(FRAMES_DIR, video_name.replace(".mp4", ""))
    os.makedirs(tmp_dir, exist_ok=True)
    
    slide_files = []
    for i, (svg_content, dur) in enumerate(svg_slides):
        png_path = os.path.join(tmp_dir, f"frame_{i}.png")
        render_svg_to_png(svg_content, png_path)
        slide_files.append((png_path, dur))

    concat_txt = os.path.join(tmp_dir, "concat.txt")
    with open(concat_txt, "w") as f:
        for img, dur in slide_files:
            f.write(f"file '{img}'\n")
            f.write(f"duration {dur}\n")
        f.write(f"file '{slide_files[-1][0]}'\n")

    out_video = os.path.join(VIDEO_DIR, video_name)
    total_dur = sum(dur for _, dur in slide_files)

    cmd = [
        "ffmpeg", "-y", "-f", "concat", "-safe", "0", "-i", concat_txt,
        "-f", "lavfi", "-i", f"sine=frequency={audio_freq}:duration={total_dur}",
        "-vf", "scale=1080:1920,format=yuv420p",
        "-c:v", "libx264", "-preset", "fast", "-crf", "22",
        "-c:a", "aac", "-b:a", "128k", "-shortest",
        out_video
    ]
    subprocess.run(cmd, check=True)
    print(f"Rendered video: {out_video} ({total_dur}s)")
    shutil.rmtree(tmp_dir, ignore_errors=True)

# ==============================================================================
# 2. VIDEO 1: ETH GAS FEE SHOCK (1080x1920)
# ==============================================================================
print("Rendering Video 1: eth_gas_fee_shock.mp4...")
svg_v1_s1 = """<svg xmlns="http://www.w3.org/2000/svg" width="1080" height="1920">
  <rect width="1080" height="1920" fill="#0b0f19"/>
  <rect x="60" y="80" width="960" height="1760" rx="36" fill="#1e293b" stroke="#334155" stroke-width="3"/>
  <text x="120" y="190" fill="#3b82f6" font-family="DejaVu Sans" font-weight="bold" font-size="38">⚡ CRYPTOCALC PRO</text>
  <rect x="120" y="230" width="380" height="50" rx="10" fill="#ef4444"/>
  <text x="140" y="265" fill="#ffffff" font-family="DejaVu Sans" font-weight="bold" font-size="26">🚨 GAS FEE SHOCK</text>
  
  <text x="120" y="370" fill="#ffffff" font-family="DejaVu Sans" font-weight="bold" font-size="64">How Much Does A</text>
  <text x="120" y="450" fill="#38bdf8" font-family="DejaVu Sans" font-weight="bold" font-size="64">Uniswap Swap Cost?</text>

  <!-- Big Card -->
  <rect x="120" y="520" width="840" height="960" rx="28" fill="#0f172a" stroke="#475569" stroke-width="2"/>
  
  <text x="170" y="620" fill="#ffffff" font-family="DejaVu Sans" font-weight="bold" font-size="44">Ethereum Mainnet (25 Gwei)</text>
  <text x="170" y="680" fill="#94a3b8" font-family="DejaVu Sans" font-size="32">ETH Price: $2,600 USD</text>

  <text x="170" y="800" fill="#f8fafc" font-family="DejaVu Sans" font-size="40">ETH Transfer (21k gas):</text>
  <text x="750" y="800" fill="#38bdf8" font-family="DejaVu Sans" font-weight="bold" font-size="40">$1.36</text>

  <text x="170" y="920" fill="#f8fafc" font-family="DejaVu Sans" font-size="40">ERC-20 Token (65k gas):</text>
  <text x="750" y="920" fill="#a78bfa" font-family="DejaVu Sans" font-weight="bold" font-size="40">$4.22</text>

  <rect x="150" y="990" width="780" height="120" rx="16" fill="#1e293b" stroke="#f59e0b" stroke-width="2"/>
  <text x="180" y="1065" fill="#f59e0b" font-family="DejaVu Sans" font-weight="bold" font-size="44">Uniswap Swap:</text>
  <text x="720" y="1065" fill="#f59e0b" font-family="DejaVu Sans" font-weight="bold" font-size="52">$9.75</text>

  <text x="170" y="1220" fill="#ef4444" font-family="DejaVu Sans" font-size="40">Contract Deploy (1.5M):</text>
  <text x="750" y="1220" fill="#ef4444" font-family="DejaVu Sans" font-weight="bold" font-size="40">$97.50</text>

  <text x="170" y="1380" fill="#f87171" font-family="DejaVu Sans" font-weight="bold" font-size="34">⚠️ Gas fees can kill your small trades!</text>

  <!-- Footer CTA -->
  <text x="120" y="1620" fill="#3b82f6" font-family="DejaVu Sans" font-weight="bold" font-size="36">🔗 sksagarwork.github.io/devpulse-tools/</text>
  <text x="120" y="1680" fill="#94a3b8" font-family="DejaVu Sans" font-size="28">100% Free • Client-Side • No Sign-Up</text>
</svg>"""

svg_v1_s2 = """<svg xmlns="http://www.w3.org/2000/svg" width="1080" height="1920">
  <rect width="1080" height="1920" fill="#0b0f19"/>
  <rect x="60" y="80" width="960" height="1760" rx="36" fill="#1e293b" stroke="#334155" stroke-width="3"/>
  <text x="120" y="190" fill="#3b82f6" font-family="DejaVu Sans" font-weight="bold" font-size="38">⚡ CRYPTOCALC PRO</text>
  <rect x="120" y="230" width="380" height="50" rx="10" fill="#10b981"/>
  <text x="140" y="265" fill="#ffffff" font-family="DejaVu Sans" font-weight="bold" font-size="26">💡 LAYER 2 SOLUTION</text>
  
  <text x="120" y="370" fill="#ffffff" font-family="DejaVu Sans" font-weight="bold" font-size="64">Layer 2 Rollups</text>
  <text x="120" y="450" fill="#10b981" font-family="DejaVu Sans" font-weight="bold" font-size="64">Save Over 99.7%!</text>

  <!-- Big Card -->
  <rect x="120" y="520" width="840" height="960" rx="28" fill="#0f172a" stroke="#10b981" stroke-width="3"/>
  
  <text x="170" y="620" fill="#ffffff" font-family="DejaVu Sans" font-weight="bold" font-size="44">Same Swap on Arbitrum &amp; Base:</text>
  <text x="170" y="740" fill="#10b981" font-family="DejaVu Sans" font-weight="bold" font-size="76">$0.02</text>
  <text x="170" y="820" fill="#94a3b8" font-family="DejaVu Sans" font-size="32">Powered by EIP-4844 Blobs</text>

  <rect x="150" y="890" width="780" height="280" rx="20" fill="#1e293b" stroke="#334155" stroke-width="2"/>
  <text x="190" y="970" fill="#38bdf8" font-family="DejaVu Sans" font-weight="bold" font-size="44">YOUR TOTAL SAVINGS:</text>
  <text x="190" y="1060" fill="#10b981" font-family="DejaVu Sans" font-weight="bold" font-size="62">$9.73 / swap</text>
  <text x="190" y="1125" fill="#f8fafc" font-family="DejaVu Sans" font-size="30">Save hundreds of dollars every month!</text>

  <text x="170" y="1320" fill="#ffffff" font-family="DejaVu Sans" font-size="34">Compare live L1 vs L2 fees in 1-click:</text>
  <text x="170" y="1390" fill="#38bdf8" font-family="DejaVu Sans" font-weight="bold" font-size="36">Ethereum Gas Fee Calculator</text>

  <!-- Footer CTA -->
  <text x="120" y="1620" fill="#3b82f6" font-family="DejaVu Sans" font-weight="bold" font-size="36">🔗 sksagarwork.github.io/devpulse-tools/</text>
  <text x="120" y="1680" fill="#94a3b8" font-family="DejaVu Sans" font-size="28">100% Free • Client-Side • No Sign-Up</text>
</svg>"""

svg_v1_s3 = """<svg xmlns="http://www.w3.org/2000/svg" width="1080" height="1920">
  <rect width="1080" height="1920" fill="#0b0f19"/>
  <rect x="60" y="80" width="960" height="1760" rx="36" fill="#1e293b" stroke="#334155" stroke-width="3"/>
  <text x="120" y="190" fill="#3b82f6" font-family="DejaVu Sans" font-weight="bold" font-size="38">⚡ CRYPTOCALC PRO</text>
  <rect x="120" y="230" width="380" height="50" rx="10" fill="#3b82f6"/>
  <text x="140" y="265" fill="#ffffff" font-family="DejaVu Sans" font-weight="bold" font-size="26">⚡ FREE WEB3 SUITE</text>
  
  <text x="120" y="370" fill="#ffffff" font-family="DejaVu Sans" font-weight="bold" font-size="64">Never Guess Gas</text>
  <text x="120" y="450" fill="#38bdf8" font-family="DejaVu Sans" font-weight="bold" font-size="64">Fees Ever Again</text>

  <!-- Big Card -->
  <rect x="120" y="520" width="840" height="960" rx="28" fill="#0f172a" stroke="#3b82f6" stroke-width="3"/>
  
  <text x="170" y="630" fill="#ffffff" font-family="DejaVu Sans" font-weight="bold" font-size="44">Free Calculator Features:</text>
  <text x="170" y="730" fill="#38bdf8" font-family="DejaVu Sans" font-size="36">✓ Real-time Gwei to USD conversion</text>
  <text x="170" y="820" fill="#38bdf8" font-family="DejaVu Sans" font-size="36">✓ Presets: Slow, Standard, Turbo</text>
  <text x="170" y="910" fill="#38bdf8" font-family="DejaVu Sans" font-size="36">✓ Swaps, Transfers &amp; NFT mints</text>
  <text x="170" y="1000" fill="#38bdf8" font-family="DejaVu Sans" font-size="36">✓ Instant Layer 2 comparison</text>
  <text x="170" y="1090" fill="#38bdf8" font-family="DejaVu Sans" font-size="36">✓ Shareable links &amp; embed widget</text>

  <rect x="150" y="1170" width="780" height="230" rx="20" fill="#1e293b" stroke="#10b981" stroke-width="2"/>
  <text x="190" y="1250" fill="#ffffff" font-family="DejaVu Sans" font-size="32">Try it live in your browser:</text>
  <text x="190" y="1320" fill="#10b981" font-family="DejaVu Sans" font-weight="bold" font-size="40">sksagarwork.github.io/devpulse-tools</text>
  <text x="190" y="1365" fill="#94a3b8" font-family="DejaVu Sans" font-size="24">Bookmark this before your next swap!</text>

  <!-- Footer CTA -->
  <text x="120" y="1620" fill="#3b82f6" font-family="DejaVu Sans" font-weight="bold" font-size="36">🔗 sksagarwork.github.io/devpulse-tools/</text>
  <text x="120" y="1680" fill="#94a3b8" font-family="DejaVu Sans" font-size="28">100% Free • Client-Side • No Sign-Up</text>
</svg>"""

compile_video_from_svgs("eth_gas_fee_shock.mp4", [(svg_v1_s1, 3.5), (svg_v1_s2, 4.0), (svg_v1_s3, 3.5)], audio_freq=523)

# ==============================================================================
# 3. VIDEO 2: CRYPTO SIP COMPOUNDING MATH (1080x1920)
# ==============================================================================
print("Rendering Video 2: crypto_sip_compounding.mp4...")
svg_v2_s1 = """<svg xmlns="http://www.w3.org/2000/svg" width="1080" height="1920">
  <rect width="1080" height="1920" fill="#0b0f19"/>
  <rect x="60" y="80" width="960" height="1760" rx="36" fill="#1e293b" stroke="#334155" stroke-width="3"/>
  <text x="120" y="190" fill="#3b82f6" font-family="DejaVu Sans" font-weight="bold" font-size="38">⚡ CRYPTOCALC PRO</text>
  <rect x="120" y="230" width="380" height="50" rx="10" fill="#10b981"/>
  <text x="140" y="265" fill="#ffffff" font-family="DejaVu Sans" font-weight="bold" font-size="26">📈 BITCOIN WEALTH</text>
  
  <text x="120" y="370" fill="#ffffff" font-family="DejaVu Sans" font-weight="bold" font-size="64">What If You Invested</text>
  <text x="120" y="450" fill="#10b981" font-family="DejaVu Sans" font-weight="bold" font-size="64">$250/Mo Into Bitcoin?</text>

  <!-- Big Card -->
  <rect x="120" y="520" width="840" height="960" rx="28" fill="#0f172a" stroke="#475569" stroke-width="2"/>
  
  <text x="170" y="620" fill="#ffffff" font-family="DejaVu Sans" font-weight="bold" font-size="44">The 5-Year Crypto SIP Model</text>
  <text x="170" y="680" fill="#94a3b8" font-family="DejaVu Sans" font-size="32">Disciplined monthly dollar-cost averaging</text>

  <text x="170" y="800" fill="#f8fafc" font-family="DejaVu Sans" font-size="40">• Monthly Buy: $250 / month</text>
  <text x="170" y="910" fill="#f8fafc" font-family="DejaVu Sans" font-size="40">• Time Horizon: 5 Years (60 mos)</text>
  <text x="170" y="1020" fill="#f8fafc" font-family="DejaVu Sans" font-size="40">• Total Invested: $15,000</text>
  <text x="170" y="1130" fill="#10b981" font-family="DejaVu Sans" font-weight="bold" font-size="40">• Historic CAGR: 35% (Conservative)</text>

  <rect x="150" y="1220" width="780" height="180" rx="16" fill="#1e293b" stroke="#3b82f6" stroke-width="2"/>
  <text x="190" y="1300" fill="#ffffff" font-family="DejaVu Sans" font-size="34">Let s look at the compound math...</text>
  <text x="190" y="1360" fill="#38bdf8" font-family="DejaVu Sans" font-weight="bold" font-size="38">You will be shocked by the result!</text>

  <!-- Footer CTA -->
  <text x="120" y="1620" fill="#3b82f6" font-family="DejaVu Sans" font-weight="bold" font-size="36">🔗 sksagarwork.github.io/devpulse-tools/</text>
  <text x="120" y="1680" fill="#94a3b8" font-family="DejaVu Sans" font-size="28">100% Free • Client-Side • No Sign-Up</text>
</svg>"""

svg_v2_s2 = """<svg xmlns="http://www.w3.org/2000/svg" width="1080" height="1920">
  <rect width="1080" height="1920" fill="#0b0f19"/>
  <rect x="60" y="80" width="960" height="1760" rx="36" fill="#1e293b" stroke="#334155" stroke-width="3"/>
  <text x="120" y="190" fill="#3b82f6" font-family="DejaVu Sans" font-weight="bold" font-size="38">⚡ CRYPTOCALC PRO</text>
  <rect x="120" y="230" width="380" height="50" rx="10" fill="#f59e0b"/>
  <text x="140" y="265" fill="#ffffff" font-family="DejaVu Sans" font-weight="bold" font-size="26">🚀 EXPONENTIAL GAIN</text>
  
  <text x="120" y="370" fill="#ffffff" font-family="DejaVu Sans" font-weight="bold" font-size="64">$15,000 Grows To</text>
  <text x="120" y="450" fill="#10b981" font-family="DejaVu Sans" font-weight="bold" font-size="64">$35,468 (+136%)</text>

  <!-- Big Card -->
  <rect x="120" y="520" width="840" height="960" rx="28" fill="#0f172a" stroke="#10b981" stroke-width="3"/>
  
  <text x="170" y="610" fill="#94a3b8" font-family="DejaVu Sans" font-size="30">PROJECTED PORTFOLIO VALUE</text>
  <text x="170" y="720" fill="#10b981" font-family="DejaVu Sans" font-weight="bold" font-size="80">$35,468.20</text>
  <text x="170" y="800" fill="#ffffff" font-family="DejaVu Sans" font-weight="bold" font-size="44">Net Profit: +$20,468.20</text>
  <text x="170" y="860" fill="#38bdf8" font-family="DejaVu Sans" font-size="32">2.36x Multiple on Invested Capital</text>

  <rect x="150" y="930" width="780" height="280" rx="20" fill="#1e293b" stroke="#334155" stroke-width="2"/>
  <text x="190" y="1000" fill="#f8fafc" font-family="DejaVu Sans" font-size="34">VS Traditional S&amp;P 500 (10% CAGR):</text>
  <text x="190" y="1060" fill="#94a3b8" font-family="DejaVu Sans" font-size="30">Stock Market yields: $19,360</text>
  <text x="190" y="1150" fill="#10b981" font-family="DejaVu Sans" font-weight="bold" font-size="48">+$16,108 EXTRA PROFIT IN CRYPTO!</text>

  <text x="170" y="1320" fill="#ffffff" font-family="DejaVu Sans" font-size="34">Model your personalized monthly plan:</text>
  <text x="170" y="1390" fill="#38bdf8" font-family="DejaVu Sans" font-weight="bold" font-size="36">Crypto SIP &amp; Compounding Calculator</text>

  <!-- Footer CTA -->
  <text x="120" y="1620" fill="#3b82f6" font-family="DejaVu Sans" font-weight="bold" font-size="36">🔗 sksagarwork.github.io/devpulse-tools/</text>
  <text x="120" y="1680" fill="#94a3b8" font-family="DejaVu Sans" font-size="28">100% Free • Client-Side • No Sign-Up</text>
</svg>"""

svg_v2_s3 = """<svg xmlns="http://www.w3.org/2000/svg" width="1080" height="1920">
  <rect width="1080" height="1920" fill="#0b0f19"/>
  <rect x="60" y="80" width="960" height="1760" rx="36" fill="#1e293b" stroke="#334155" stroke-width="3"/>
  <text x="120" y="190" fill="#3b82f6" font-family="DejaVu Sans" font-weight="bold" font-size="38">⚡ CRYPTOCALC PRO</text>
  <rect x="120" y="230" width="380" height="50" rx="10" fill="#3b82f6"/>
  <text x="140" y="265" fill="#ffffff" font-family="DejaVu Sans" font-weight="bold" font-size="26">⚡ FREE SIP TOOL</text>
  
  <text x="120" y="370" fill="#ffffff" font-family="DejaVu Sans" font-weight="bold" font-size="64">Plan Your Financial</text>
  <text x="120" y="450" fill="#10b981" font-family="DejaVu Sans" font-weight="bold" font-size="64">Freedom Today</text>

  <!-- Big Card -->
  <rect x="120" y="520" width="840" height="960" rx="28" fill="#0f172a" stroke="#3b82f6" stroke-width="3"/>
  
  <text x="170" y="630" fill="#ffffff" font-family="DejaVu Sans" font-weight="bold" font-size="44">Free Calculator Features:</text>
  <text x="170" y="730" fill="#38bdf8" font-family="DejaVu Sans" font-size="36">✓ Any monthly savings amount</text>
  <text x="170" y="820" fill="#38bdf8" font-family="DejaVu Sans" font-size="36">✓ Presets: Conservative vs Bull Run</text>
  <text x="170" y="910" fill="#38bdf8" font-family="DejaVu Sans" font-size="36">✓ 1 to 10 year investment horizons</text>
  <text x="170" y="1000" fill="#38bdf8" font-family="DejaVu Sans" font-size="36">✓ Full year-by-year schedule</text>
  <text x="170" y="1090" fill="#38bdf8" font-family="DejaVu Sans" font-size="36">✓ S&amp;P 500 comparison built-in</text>

  <rect x="150" y="1170" width="780" height="230" rx="20" fill="#1e293b" stroke="#10b981" stroke-width="2"/>
  <text x="190" y="1250" fill="#ffffff" font-family="DejaVu Sans" font-size="32">Test your numbers for free:</text>
  <text x="190" y="1320" fill="#10b981" font-family="DejaVu Sans" font-weight="bold" font-size="40">sksagarwork.github.io/devpulse-tools</text>
  <text x="190" y="1365" fill="#94a3b8" font-family="DejaVu Sans" font-size="24">Start your compounding journey!</text>

  <!-- Footer CTA -->
  <text x="120" y="1620" fill="#3b82f6" font-family="DejaVu Sans" font-weight="bold" font-size="36">🔗 sksagarwork.github.io/devpulse-tools/</text>
  <text x="120" y="1680" fill="#94a3b8" font-family="DejaVu Sans" font-size="28">100% Free • Client-Side • No Sign-Up</text>
</svg>"""

compile_video_from_svgs("crypto_sip_compounding.mp4", [(svg_v2_s1, 3.5), (svg_v2_s2, 4.0), (svg_v2_s3, 3.5)], audio_freq=587)

# ==============================================================================
# 4. VIDEO 3: IMPERMANENT LOSS TRAP & GOLDEN MATH (1080x1920)
# ==============================================================================
print("Rendering Video 3: impermanent_loss_trap.mp4...")
svg_v3_s1 = """<svg xmlns="http://www.w3.org/2000/svg" width="1080" height="1920">
  <rect width="1080" height="1920" fill="#0b0f19"/>
  <rect x="60" y="80" width="960" height="1760" rx="36" fill="#1e293b" stroke="#334155" stroke-width="3"/>
  <text x="120" y="190" fill="#3b82f6" font-family="DejaVu Sans" font-weight="bold" font-size="38">⚡ CRYPTOCALC PRO</text>
  <rect x="120" y="230" width="380" height="50" rx="10" fill="#ef4444"/>
  <text x="140" y="265" fill="#ffffff" font-family="DejaVu Sans" font-weight="bold" font-size="26">⚠️ DEFI DANGER</text>
  
  <text x="120" y="370" fill="#ffffff" font-family="DejaVu Sans" font-weight="bold" font-size="64">The Impermanent Loss</text>
  <text x="120" y="450" fill="#f59e0b" font-family="DejaVu Sans" font-weight="bold" font-size="64">Trap in Uniswap Pools</text>

  <!-- Big Card -->
  <rect x="120" y="520" width="840" height="960" rx="28" fill="#0f172a" stroke="#475569" stroke-width="2"/>
  
  <text x="170" y="620" fill="#ffffff" font-family="DejaVu Sans" font-weight="bold" font-size="44">Deposit $1,000 in ETH / USDC:</text>
  <text x="170" y="680" fill="#94a3b8" font-family="DejaVu Sans" font-size="32">Suppose ETH price goes up 2x (+100%)</text>

  <text x="170" y="800" fill="#f8fafc" font-family="DejaVu Sans" font-size="40">Value if you just HODL:</text>
  <text x="750" y="800" fill="#10b981" font-family="DejaVu Sans" font-weight="bold" font-size="40">$1,500.00</text>

  <text x="170" y="910" fill="#f8fafc" font-family="DejaVu Sans" font-size="40">Value in Liquidity Pool:</text>
  <text x="750" y="910" fill="#ef4444" font-family="DejaVu Sans" font-weight="bold" font-size="40">$1,414.21</text>

  <rect x="150" y="990" width="780" height="150" rx="16" fill="#1e293b" stroke="#ef4444" stroke-width="2"/>
  <text x="180" y="1060" fill="#ef4444" font-family="DejaVu Sans" font-weight="bold" font-size="42">IMPERMANENT LOSS:</text>
  <text x="180" y="1120" fill="#ef4444" font-family="DejaVu Sans" font-weight="bold" font-size="46">-$85.79 (-5.72%)</text>

  <text x="170" y="1250" fill="#94a3b8" font-family="DejaVu Sans" font-size="32">Arbitrage bots bought your cheap ETH!</text>
  <text x="170" y="1320" fill="#f59e0b" font-family="DejaVu Sans" font-weight="bold" font-size="36">So why does anyone provide LP?</text>

  <!-- Footer CTA -->
  <text x="120" y="1620" fill="#3b82f6" font-family="DejaVu Sans" font-weight="bold" font-size="36">🔗 sksagarwork.github.io/devpulse-tools/</text>
  <text x="120" y="1680" fill="#94a3b8" font-family="DejaVu Sans" font-size="28">100% Free • Client-Side • No Sign-Up</text>
</svg>"""

svg_v3_s2 = """<svg xmlns="http://www.w3.org/2000/svg" width="1080" height="1920">
  <rect width="1080" height="1920" fill="#0b0f19"/>
  <rect x="60" y="80" width="960" height="1760" rx="36" fill="#1e293b" stroke="#334155" stroke-width="3"/>
  <text x="120" y="190" fill="#3b82f6" font-family="DejaVu Sans" font-weight="bold" font-size="38">⚡ CRYPTOCALC PRO</text>
  <rect x="120" y="230" width="380" height="50" rx="10" fill="#10b981"/>
  <text x="140" y="265" fill="#ffffff" font-family="DejaVu Sans" font-weight="bold" font-size="26">🏆 THE GOLDEN MATH</text>
  
  <text x="120" y="370" fill="#ffffff" font-family="DejaVu Sans" font-weight="bold" font-size="64">When Trading Fees</text>
  <text x="120" y="450" fill="#10b981" font-family="DejaVu Sans" font-weight="bold" font-size="64">Beat Impermanent Loss</text>

  <!-- Big Card -->
  <rect x="120" y="520" width="840" height="960" rx="28" fill="#0f172a" stroke="#10b981" stroke-width="3"/>
  
  <text x="170" y="620" fill="#ffffff" font-family="DejaVu Sans" font-weight="bold" font-size="44">If Pool Swap Fee APR is 25%:</text>
  <text x="170" y="730" fill="#10b981" font-family="DejaVu Sans" font-weight="bold" font-size="64">1-Yr Fee Yield: +$353.55</text>
  
  <rect x="150" y="810" width="780" height="280" rx="20" fill="#1e293b" stroke="#10b981" stroke-width="2"/>
  <text x="190" y="890" fill="#94a3b8" font-family="DejaVu Sans" font-size="30">Pool Assets ($1,414) + Fees ($353):</text>
  <text x="190" y="990" fill="#10b981" font-family="DejaVu Sans" font-weight="bold" font-size="64">NET TOTAL: $1,767.76</text>
  <text x="190" y="1055" fill="#38bdf8" font-family="DejaVu Sans" font-weight="bold" font-size="34">Beats HODLing by +$267.76! 🏆</text>

  <text x="170" y="1220" fill="#f8fafc" font-family="DejaVu Sans" font-size="34">The Rule: If Fee APR &gt; IL %, YOU WIN.</text>
  <text x="170" y="1320" fill="#ffffff" font-family="DejaVu Sans" font-size="34">Test your pool before depositing:</text>
  <text x="170" y="1390" fill="#38bdf8" font-family="DejaVu Sans" font-weight="bold" font-size="36">Impermanent Loss Calculator</text>

  <!-- Footer CTA -->
  <text x="120" y="1620" fill="#3b82f6" font-family="DejaVu Sans" font-weight="bold" font-size="36">🔗 sksagarwork.github.io/devpulse-tools/</text>
  <text x="120" y="1680" fill="#94a3b8" font-family="DejaVu Sans" font-size="28">100% Free • Client-Side • No Sign-Up</text>
</svg>"""

svg_v3_s3 = """<svg xmlns="http://www.w3.org/2000/svg" width="1080" height="1920">
  <rect width="1080" height="1920" fill="#0b0f19"/>
  <rect x="60" y="80" width="960" height="1760" rx="36" fill="#1e293b" stroke="#334155" stroke-width="3"/>
  <text x="120" y="190" fill="#3b82f6" font-family="DejaVu Sans" font-weight="bold" font-size="38">⚡ CRYPTOCALC PRO</text>
  <rect x="120" y="230" width="380" height="50" rx="10" fill="#3b82f6"/>
  <text x="140" y="265" fill="#ffffff" font-family="DejaVu Sans" font-weight="bold" font-size="26">⚡ FREE DEFI TOOL</text>
  
  <text x="120" y="370" fill="#ffffff" font-family="DejaVu Sans" font-weight="bold" font-size="64">Model Any Pool</text>
  <text x="120" y="450" fill="#38bdf8" font-family="DejaVu Sans" font-weight="bold" font-size="64">Before You Deposit</text>

  <!-- Big Card -->
  <rect x="120" y="520" width="840" height="960" rx="28" fill="#0f172a" stroke="#3b82f6" stroke-width="3"/>
  
  <text x="170" y="630" fill="#ffffff" font-family="DejaVu Sans" font-weight="bold" font-size="44">Free Calculator Features:</text>
  <text x="170" y="730" fill="#38bdf8" font-family="DejaVu Sans" font-size="36">✓ Uniswap V2/V3, Pancake, Curve</text>
  <text x="170" y="820" fill="#38bdf8" font-family="DejaVu Sans" font-size="36">✓ Custom token price changes</text>
  <text x="170" y="910" fill="#38bdf8" font-family="DejaVu Sans" font-size="36">✓ Projected swap fee APR offset</text>
  <text x="170" y="1000" fill="#38bdf8" font-family="DejaVu Sans" font-size="36">✓ Clear verdict: Pool vs HODL</text>
  <text x="170" y="1090" fill="#38bdf8" font-family="DejaVu Sans" font-size="36">✓ Shareable links &amp; embed widget</text>

  <rect x="150" y="1170" width="780" height="230" rx="20" fill="#1e293b" stroke="#10b981" stroke-width="2"/>
  <text x="190" y="1250" fill="#ffffff" font-family="DejaVu Sans" font-size="32">Test your pools for free:</text>
  <text x="190" y="1320" fill="#10b981" font-family="DejaVu Sans" font-weight="bold" font-size="40">sksagarwork.github.io/devpulse-tools</text>
  <text x="190" y="1365" fill="#94a3b8" font-family="DejaVu Sans" font-size="24">Bookmark before your next LP deposit!</text>

  <!-- Footer CTA -->
  <text x="120" y="1620" fill="#3b82f6" font-family="DejaVu Sans" font-weight="bold" font-size="36">🔗 sksagarwork.github.io/devpulse-tools/</text>
  <text x="120" y="1680" fill="#94a3b8" font-family="DejaVu Sans" font-size="28">100% Free • Client-Side • No Sign-Up</text>
</svg>"""

compile_video_from_svgs("impermanent_loss_trap.mp4", [(svg_v3_s1, 3.5), (svg_v3_s2, 4.0), (svg_v3_s3, 3.5)], audio_freq=659)

print("\nALL MEDIA ASSETS & VIDEOS COMPILED SUCCESSFULLY!")
