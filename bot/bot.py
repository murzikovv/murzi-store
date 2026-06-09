"""
murzi/store — Telegram Stars checkout bot.

Sells the website templates for Telegram Stars (currency XTR) and delivers
the matching .zip the moment payment succeeds. No external payment provider
is required for Stars.

Run:  python bot.py   (after `pip install -r requirements.txt`)
Token + settings live in config.json (never commit it).
"""

import asyncio
import json
import logging
from pathlib import Path

from aiogram import Bot, Dispatcher, F
from aiogram.client.default import DefaultBotProperties
from aiogram.enums import ParseMode
from aiogram.filters import CommandStart, Command, CommandObject
from aiogram.types import (
    Message, CallbackQuery, PreCheckoutQuery,
    LabeledPrice, FSInputFile, InlineKeyboardButton,
)
from aiogram.utils.keyboard import InlineKeyboardBuilder

BASE = Path(__file__).resolve().parent
DIST = BASE.parent / "dist"

cfg = json.loads((BASE / "config.json").read_text(encoding="utf-8"))
TOKEN = cfg["bot_token"]
STORE_URL = cfg.get("store_url", "")
SUPPORT = cfg.get("support_contact", "")

# --- catalog -------------------------------------------------------------
# price is in Telegram Stars (whole units). file is relative to /dist.
CATALOG = {
    "beacon":    {"title": "Beacon · AI / SaaS landing",       "price": 690, "file": "beacon.zip",
                  "blurb": "A precision SaaS landing with a live signal dashboard, blueprint grid and a dark band."},
    "portfolio": {"title": "Mara Vance · portfolio",           "price": 690, "file": "mara-vance.zip",
                  "blurb": "A poster-grade portfolio: oversized type, a marquee and a hover work index."},
    "nova":      {"title": "NOVA · link in bio",               "price": 690, "file": "nova.zip",
                  "blurb": "A drenched creator card with an aurora background and tappable links. Mobile-first."},
    "tempo":     {"title": "Tempo · mobile app landing",       "price": 690, "file": "tempo.zip",
                  "blurb": "A focus-app landing with glassy phone mockups, a live session ring and feature cards."},
    "vellum":    {"title": "Vellum · creative agency",         "price": 690, "file": "vellum.zip",
                  "blurb": "A brutalist studio site: oversized type, a marquee and a monochrome work grid."},
    "quanta":    {"title": "Quanta · fintech / payments",      "price": 690, "file": "quanta.zip",
                  "blurb": "A payments landing with a multi-currency account card and an animated chart."},
    "pulse":     {"title": "Pulse · conference / event",       "price": 690, "file": "pulse.zip",
                  "blurb": "An event page with a speaker lineup, a day schedule and three ticket tiers."},
    "cohort":    {"title": "Cohort · online course",           "price": 690, "file": "cohort.zip",
                  "blurb": "A warm editorial course landing with a curriculum, instructor and enrollment plans."},
    "frequency": {"title": "Frequency · podcast",              "price": 690, "file": "frequency.zip",
                  "blurb": "A podcast site with a player-style hero, an episode list and animated waveforms."},
    "atlas":     {"title": "Atlas · analytics dashboard",      "price": 690, "file": "atlas.zip",
                  "blurb": "An analytics SaaS landing with a real app-shell product mockup, KPIs and pricing."},
    "bundle":    {"title": "All ten templates · bundle",       "price": 2490, "file": "murzi-templates-bundle.zip",
                  "blurb": "Every template in the store, together, with every future template added free."},
}

logging.basicConfig(level=logging.INFO, format="%(asctime)s %(levelname)s %(message)s")
log = logging.getLogger("murzi-store")

dp = Dispatcher()


def catalog_keyboard() -> InlineKeyboardBuilder:
    kb = InlineKeyboardBuilder()
    for key, p in CATALOG.items():
        kb.row(InlineKeyboardButton(
            text=f"{p['title'].split('—')[0].strip()} · ★ {p['price']}",
            callback_data=f"buy:{key}",
        ))
    if STORE_URL:
        kb.row(InlineKeyboardButton(text="See live previews", url=STORE_URL))
    return kb


async def send_invoice(message: Message, key: str) -> None:
    p = CATALOG.get(key)
    if not p:
        await message.answer("That item isn't in the store. Send /start to see what's available.")
        return
    await message.answer_invoice(
        title=p["title"],
        description=p["blurb"],
        payload=key,
        currency="XTR",
        prices=[LabeledPrice(label=p["title"], amount=p["price"])],
        provider_token="",          # empty for Telegram Stars
        start_parameter=f"buy_{key}",
    )


@dp.message(CommandStart(deep_link=True))
async def start_deep_link(message: Message, command: CommandObject) -> None:
    arg = (command.args or "").strip()
    if arg.startswith("buy_"):
        await send_invoice(message, arg[4:])
    else:
        await start_plain(message)


@dp.message(CommandStart())
async def start_plain(message: Message) -> None:
    name = message.from_user.first_name or "there"
    text = (
        f"Hi {name}. This is the <b>murzi/store</b> checkout.\n\n"
        "Premium one-file website templates. Each is a single HTML file: "
        "no build step, no framework, edit in minutes.\n\n"
        "Pick one below and pay with <b>Telegram Stars</b> ★. "
        "The file is delivered here instantly after payment."
    )
    await message.answer(text, reply_markup=catalog_keyboard().as_markup())


@dp.callback_query(F.data.startswith("buy:"))
async def on_buy(call: CallbackQuery) -> None:
    await call.answer()
    await send_invoice(call.message, call.data.split(":", 1)[1])


@dp.pre_checkout_query()
async def on_pre_checkout(pre: PreCheckoutQuery) -> None:
    # Confirm the item still exists before charging.
    ok = pre.invoice_payload in CATALOG
    await pre.answer(ok=ok, error_message=None if ok else "This item is no longer available.")


@dp.message(F.successful_payment)
async def on_paid(message: Message) -> None:
    sp = message.successful_payment
    key = sp.invoice_payload
    p = CATALOG.get(key)
    log.info("PAID %s by %s charge=%s", key, message.from_user.id, sp.telegram_payment_charge_id)
    if not p:
        await message.answer("Payment received, but I couldn't match the item. "
                             f"Contact {SUPPORT} and we'll sort it out.")
        return
    path = DIST / p["file"]
    if not path.exists():
        await message.answer("Payment received. Your file is being prepared, "
                             f"contact {SUPPORT} if it doesn't arrive shortly.")
        log.error("MISSING FILE %s", path)
        return
    await message.answer_document(
        FSInputFile(path),
        caption=(
            f"Thanks for buying <b>{p['title']}</b>. ❤️\n\n"
            "Inside: the template HTML, a README and the license.\n"
            "Open index.html in any browser, edit the text and colors, ship it.\n\n"
            f"Questions or need a tweak? {SUPPORT} · murzi.studio"
        ),
    )


@dp.message(Command("paysupport"))
async def paysupport(message: Message) -> None:
    await message.answer(
        "Need help with an order or a refund? "
        f"Message {SUPPORT} with your order time and the template name. "
        "Digital goods are delivered instantly; refunds are handled case by case."
    )


@dp.message(Command("help"))
async def help_cmd(message: Message) -> None:
    await start_plain(message)


async def main() -> None:
    bot = Bot(TOKEN, default=DefaultBotProperties(parse_mode=ParseMode.HTML))
    log.info("murzi/store bot starting…")
    await bot.delete_webhook(drop_pending_updates=True)
    await dp.start_polling(bot)


if __name__ == "__main__":
    asyncio.run(main())
