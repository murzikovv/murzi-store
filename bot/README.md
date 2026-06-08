# murzi/store — checkout bot

Sells the templates for **Telegram Stars** and delivers the `.zip` instantly
after payment. No external payment provider needed.

## Run it

```bash
cd bot
python -m venv .venv
.venv\Scripts\activate        # Windows  (use: source .venv/bin/activate on macOS/Linux)
pip install -r requirements.txt
python bot.py
```

Leave it running. While `bot.py` runs, the bot is live; when you stop it, it stops selling.
For always-on, run it on a small VPS or any machine that stays on (later we can move it to a host + `systemd`/PM2).

## Configuration

`config.json` holds the secrets — **never share or commit it**:

```json
{
  "bot_token": "…from @BotFather…",
  "store_url": "https://murzi.studio",
  "support_contact": "@murzi"
}
```

- `store_url` — where the "See live previews" button points (set this to the hosted storefront once it's online).
- `support_contact` — shown to buyers for help/refunds.

If the token ever leaks, open @BotFather → `/revoke`, then paste the new token here.

## How a sale flows

1. Buyer clicks **Get ★** on the storefront → opens `t.me/murzistudio_bot?start=buy_<item>`.
2. Bot sends a Stars invoice for that template.
3. Buyer pays → Telegram confirms → bot sends the matching `.zip` from `../dist/`.

## Catalog

Edit the `CATALOG` dict in `bot.py` to change prices (in Stars), titles, or which
zip each item delivers. Prices today: each template ★690, the bundle ★1490.

## Payout

Stars accumulate on the bot's balance and are withdrawn to TON via Telegram's
Fragment, then converted as you like. There's a holding period (~21 days) before
the first withdrawal.

## Commands

- `/start` — show the catalog
- `/help` — same as start
- `/paysupport` — support & refund info for buyers
