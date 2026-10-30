#!/usr/bin/env python3
"""
Social Media & Community Launch Generator for CryptoCalc Pro.
Generates tailored, high-engagement posts for Reddit, Twitter/X, and Telegram.
Usage: python3 tools/generate_social_promo.py
"""

POSTS = {
    "reddit_r_defi": """
[Title] I built a free, zero-bloat DeFi suite (Impermanent Loss + L1 vs L2 Gas Fee + Staking APY)

Hey r/defi!

I got tired of bloated calculator sites loaded with popups and KYC trackers, so I built an open-source, client-side financial toolkit specifically for liquidity providers and active on-chain users:

👉 **Live Site:** https://sksagarwork.github.io/devpulse-tools/

### What's included:
1. **Uniswap V2/V3 Impermanent Loss Calculator**: Compare LP swap fee APY against simple HODLing with exact divergence math.
2. **Ethereum Gas Fee & L2 Savings Estimator**: Live Gwei to USD calculator for transfers, ERC20 swaps, and contract deployments (with real comparison to Arbitrum/Base/Optimism).
3. **Compound Staking Yield Calculator**: Daily, weekly, and monthly auto-compounding models for ETH, SOL, and liquid staking.
4. **Futures Liquidation Price**: Exact formulas for long & short positions across Binance and Bybit.
5. **Crypto SIP & DCA Backtester**: Model monthly accumulation over 1-10 years.

Everything runs 100% in your browser. Zero backend logging, zero tracking cookies. 

Would love any feedback or feature requests!
""",

    "twitter_thread": """
🧵 1/7 Most crypto traders lose money because of hidden costs: Impermanent Loss, exchange fees, and miscalculated liquidation levels.

I built a free 100% client-side Web3 calculator suite to fix this:
https://sksagarwork.github.io/devpulse-tools/

Here is what it does 👇

2/7 ⛽ Ethereum Gas & L2 Calculator:
Ever wondered how much a Uniswap V3 swap actually costs right now in USD?
Punch in the Gwei & ETH price to see costs for Transfers, Swaps, LP adds, and compare exact savings on Arbitrum & Base.

3/7 📉 Impermanent Loss vs HODL:
Model your Uniswap/PancakeSwap liquidity pools before depositing. See exact dollar divergence vs fee yields so you never get surprised.

4/7 📊 Crypto SIP & Compounding:
Historical 4-year halving cycle simulation. Compare your monthly Bitcoin accumulation against the S&P 500.

5/7 ⚡ Futures Liquidation Price:
Calculate your exact liquidation price at 5x to 100x leverage on Long and Short positions before opening futures trades.

6/7 🔒 100% Private & Open Source:
- Zero data leaves your browser
- Embeddable on any site or documentation
- No annoying paywalls

7/7 Bookmark the suite: https://sksagarwork.github.io/devpulse-tools/
Retweet if you found this useful! 🔄
"""
}

def main():
    print("=" * 60)
    print("CRYPTO COMMUNITY PROMOTION TEMPLATES")
    print("=" * 60)
    for platform, content in POSTS.items():
        print(f"\n--- {platform.upper()} ---")
        print(content.strip())
        print("-" * 60)

if __name__ == "__main__":
    main()
