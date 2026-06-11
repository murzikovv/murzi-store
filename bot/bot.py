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
ADMIN = cfg.get("admin_id")  # Telegram chat id that receives activity notifications

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
    "saffron":   {"title": "Saffron · restaurant",            "price": 690, "file": "saffron.zip",
                  "blurb": "A warm-dark restaurant site with full-bleed photography, a short menu, a gallery and reservations."},
    "lumen":     {"title": "Lumen · eCommerce product",       "price": 690, "file": "lumen.zip",
                  "blurb": "A quiet-luxury single-product brand page: photo hero, ingredient grid, the ritual and reviews."},
    "marin":     {"title": "The Marin · real estate",         "price": 690, "file": "marin.zip",
                  "blurb": "An architectural property listing with a full-bleed home tour, a facts row, a gallery and a viewing CTA."},
    "resume-modern":  {"title": "Resume — Modern · CV template",  "price": 390, "file": "resume-modern.zip",
                       "blurb": "A two-column modern resume: sidebar with skill bars and a clean timeline. Print-ready A4."},
    "resume-classic": {"title": "Resume — Classic · FREE",        "price": 0,   "file": "resume-classic.zip",
                       "blurb": "A clean, single-column, ATS-friendly resume. Our free gift, no payment needed."},
    "resume-bold":    {"title": "Resume — Bold · CV template",    "price": 390, "file": "resume-bold.zip",
                       "blurb": "A confident resume with a colour banner and two-column body. Stands out, reads clean. A4."},
    "resume-twotone": {"title": "Resume — Two-Tone · CV template","price": 390, "file": "resume-twotone.zip",
                       "blurb": "A full-colour sidebar resume with skill bars. Memorable and still professional. A4."},
    "resume-executive":{"title": "Resume — Executive · CV",       "price": 390, "file": "resume-executive.zip",
                       "blurb": "An understated, editorial resume for senior roles. Serif, calm, confident. A4."},
    "cover-letter":   {"title": "Cover Letter · template",        "price": 290, "file": "cover-letter.zip",
                       "blurb": "A matching cover letter: same typography and accent as the resume set. A4."},
    "fitness":   {"title": "Apex · fitness / gym studio site",          "price": 690, "file": "fitness.zip",
                  "blurb": "A high-energy website for a gym or strength studio. Cinematic hero, programs grid, a real weekly class schedule, coaches, three membership tiers and a free-trial CTA. One HTML file."},
    "clinic":    {"title": "Aurelia · clinic (surgery / dental) site",  "price": 790, "file": "clinic.zip",
                  "blurb": "A couture website for an aesthetic, plastic surgery or dental clinic. Treatments grid, surgeon profiles, accreditations, process, FAQ and a private booking form. One HTML file, no build step."},
    "home-services": {"title": "Brightwork · home services site",      "price": 690, "file": "home-services.zip",
                  "blurb": "A trust-first website for plumbers, electricians, handymen and remodelers. Services grid, four-step process, reviews, FAQ and a quote form. One HTML file, no build step."},
    "pitch-deck": {"title": "Northstar · investor pitch deck (.pptx)", "price": 590, "file": "pitch-deck.zip",
                   "blurb": "A 12-slide seed pitch deck in editable PowerPoint. Problem, market, traction chart, ask — every slide ready to fill in. Built-in fonts, opens anywhere."},
    "tracker":   {"title": "Ledger · budget & cashflow tracker (.xlsx)", "price": 490, "file": "tracker.zip",
                  "blurb": "A small-business budget tracker in Excel. Type your income and expenses; the dashboard, monthly net and charts update themselves. Plain SUM formulas, no macros."},
    "bundle":    {"title": "All sixteen website templates · bundle", "price": 2990, "file": "murzi-templates-bundle.zip",
                  "blurb": "Every website template in the store, together, with every future one added free."},
}

logging.basicConfig(level=logging.INFO, format="%(asctime)s %(levelname)s %(message)s")
log = logging.getLogger("murzi-store")

dp = Dispatcher()


def who(u) -> str:
    un = f"@{u.username}" if u.username else "no username"
    return f"{u.full_name} ({un}, id <code>{u.id}</code>)"


async def notify_admin(bot, text: str) -> None:
    """Send an activity notification to the admin chat, if configured."""
    if not ADMIN:
        return
    try:
        await bot.send_message(ADMIN, text)
    except Exception as e:  # never let admin notify break the user flow
        log.warning("admin notify failed: %s", e)


def catalog_keyboard() -> InlineKeyboardBuilder:
    kb = InlineKeyboardBuilder()
    for key, p in CATALOG.items():
        price = "FREE 🎁" if p["price"] == 0 else f"★ {p['price']}"
        kb.row(InlineKeyboardButton(
            text=f"{p['title'].split('—')[0].split('·')[0].strip()} · {price}",
            callback_data=f"buy:{key}",
        ))
    if STORE_URL:
        kb.row(InlineKeyboardButton(text="See live previews", url=STORE_URL))
    return kb


async def deliver(message: Message, key: str, free: bool = False) -> None:
    """Send the product zip to the chat."""
    p = CATALOG[key]
    path = DIST / p["file"]
    if not path.exists():
        await message.answer("The file is being prepared, "
                             f"contact {SUPPORT} if it doesn't arrive shortly.")
        log.error("MISSING FILE %s", path)
        return
    head = f"Here's <b>{p['title']}</b>, free. Enjoy! 🎁" if free else f"Thanks for buying <b>{p['title']}</b>. ❤️"
    await message.answer_document(
        FSInputFile(path),
        caption=(
            f"{head}\n\n"
            "Inside: the template, a README and the license.\n"
            "Open index.html in any browser, edit the text, print to PDF or ship it.\n\n"
            f"More templates: {STORE_URL}"
        ),
    )


async def send_invoice(message: Message, key: str) -> None:
    p = CATALOG.get(key)
    if not p:
        await message.answer("That item isn't in the store. Send /start to see what's available.")
        return
    if p["price"] == 0:
        await deliver(message, key, free=True)
        await notify_admin(message.bot, f"🎁 Free download: <b>{p['title']}</b>\nchat id <code>{message.chat.id}</code>")
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
    await notify_admin(message.bot, f"👀 Opened the store\n{who(message.from_user)}")


@dp.callback_query(F.data.startswith("buy:"))
async def on_buy(call: CallbackQuery) -> None:
    await call.answer()
    key = call.data.split(":", 1)[1]
    await send_invoice(call.message, key)
    p = CATALOG.get(key, {})
    await notify_admin(call.bot, f"🛒 Tapped buy: <b>{p.get('title', key)}</b> (★{p.get('price','?')})\n{who(call.from_user)}")


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
    await notify_admin(
        message.bot,
        f"💰 <b>SALE</b> ★{(p or {}).get('price','?')} — {(p or {}).get('title', key)}\n"
        f"by {who(message.from_user)}\ncharge <code>{sp.telegram_payment_charge_id}</code>"
    )
    if not p:
        await message.answer("Payment received, but I couldn't match the item. "
                             f"Contact {SUPPORT} and we'll sort it out.")
        return
    await deliver(message, key)


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
