
import json
import os
import re
import asyncio
from datetime import datetime
from telethon import TelegramClient, events, Button
from telethon.tl.types import ChannelParticipantsAdmins
from welcome_goodbye import register as register_welcome
from topic_system import register_topic_system
from gpt_check import register as gpt_register
from filter_system import register as register_filter
from all import register as all_register
from quick import register as quick_register
from mute import register as mute_register
from tiktok_system import register_tiktok_system
from dm_system import register_dm_system
from file_system import register_file_system
from groupadm_system import register_groupadm_system
from sms_system import register_sms_system
from admin_system import register_admin_system
from group_only_commands import register_group_only_commands
from spam import register_spam
from shop import register_shop
from reply_system import register_reply_system
from translation import register_translation_system
from city_weather_full_system import register_all_system
from link import register_link_system
from clear import register_clear_system

# ================= CONFIG =================
api_id = 38180913
api_hash = "192dcce296fc8607d9828d83bc7b8bb5"
bot_token = "8593935916:AAE-5LFj-0X1SBKZ76TIEj1jsZADZ6KkIns"
OWNER_IDS = [-1003795852457,-1003721025417,7260737562,8597326828]

REPLY_FILE = "replies.json"
COUNTER_FILE = "counter.json"
GROUP_FILE = "groups.json"
AUTO_FILE = "auto_sticker.json"
REACT_FILE = "auto_react.json"
# ================= JSON =================
def load_json(file, default):
    if os.path.exists(file):
        with open(file, "r", encoding="utf-8") as f:
            return json.load(f)
    return default

def save_json(file, data):
    with open(file, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=4, ensure_ascii=False)

replies = load_json(REPLY_FILE, {})
counter = load_json(COUNTER_FILE, {})
groups = load_json(GROUP_FILE, [])

def save_group(chat_id):
    if chat_id not in groups:
        groups.append(chat_id)
        save_json(GROUP_FILE, groups)

# ================= CLIENT =================
client = TelegramClient("bot_session", api_id, api_hash).start(bot_token=bot_token)

# ================= /id COMMAND =================

@client.on(events.NewMessage(pattern=r'^/id$'))
async def id_handler(event):

    if event.is_reply:
        user = (await event.get_reply_message()).sender
    elif len(event.text.split()) == 2:
        user = await event.client.get_entity(event.text.split()[1])
    else:
        user = await event.get_sender()

    await event.reply(
        f"""
<blockquote expandable>
╭────────────────────────────╮
│ Target Name = {user.first_name}
│ Target ID   =      {user.id}
╰────────────────────────────╯
</blockquote>
""",
        parse_mode="html"
    )
PENDING_FILE = "pending.json"

def load_pending():
    return load_json(PENDING_FILE, [])

def save_pending(pending):
    save_json(PENDING_FILE, pending)



import asyncio
from datetime import datetime
from telethon import events, Button

running_tasks = {}
pause_state = {}  # ✅ store pause per user


@client.on(events.NewMessage(pattern=r'^/time$'))
async def time_now(event):

    user_id = event.sender_id

    if user_id in running_tasks:
        running_tasks[user_id].cancel()

    pause_state[user_id] = False

    msg = await event.reply(
        "⏳ Starting live clock...",
        buttons=[
            [Button.inline("⏸ Pause", b"pause"),
             Button.inline("⏹ Stop", b"stop")]
        ]
    )

    start_date = datetime(2025, 5, 19)

    async def updater():
        while True:
            try:
                if pause_state.get(user_id):
                    await asyncio.sleep(1)
                    continue

                now = datetime.now()

                delta = now - start_date
                total_days = delta.days
                total_months = (now.year - start_date.year) * 12 + (now.month - start_date.month)

                date = now.strftime("%d.%m.%Y")
                day = now.strftime("%A")

                hour = now.strftime("%I")
                minute = now.strftime("%M")
                second = now.strftime("%S")
                ampm = now.strftime("%p")

                # ✅ text must be inside try + inside loop
                text = f"""
<blockquote>
╭──────────────────────────────────╮
│        A Day Full Of Site Ko Lovers SaNoe
╰──────────────────────────────────╯

╭──────────────────────────────────╮
│ VALENTINE`S DAY   - 19.5.2025
│ MONTHS            - {total_months} Months
│ NUMBER OF DAYS    - {total_days} Days
╰──────────────────────────────────╯

╭──────────────────────────────────╮
│ DATE              = {date}
│ DAY               = {day}
│ TIME              = {hour}:{minute}:{second} {ampm}
╰──────────────────────────────────╯
</blockquote>
"""

                await msg.edit(
                    text,
                    parse_mode="html",
                    buttons=[
                        [Button.inline("⏸ Pause", b"pause"),
                         Button.inline("⏹ Stop", b"stop")]
                    ]
                )

                await asyncio.sleep(2)

            except asyncio.CancelledError:
                break
            except Exception as e:
                print("ERROR:", e)
                break

    task = asyncio.create_task(updater())
    running_tasks[user_id] = task

# ================= CALLBACK =================

@client.on(events.CallbackQuery)
async def callback_handler(event):

    user_id = event.sender_id
    data = event.data.decode()

    if user_id not in running_tasks:
        return await event.answer("No active timer")

    # ⏸ PAUSE
    if data == "pause":
        pause_state[user_id] = True
        await event.answer("Paused ⏸")
        await event.edit(buttons=[
            [Button.inline("▶ Resume", b"resume"),
             Button.inline("⏹ Stop", b"stop")]
        ])

    # ▶ RESUME
    elif data == "resume":
        pause_state[user_id] = False
        await event.answer("Resumed ▶")
        await event.edit(buttons=[
            [Button.inline("⏸ Pause", b"pause"),
             Button.inline("⏹ Stop", b"stop")]
        ])

    # ⏹ STOP
    elif data == "stop":
        task = running_tasks.get(user_id)
        if task:
            task.cancel()
            del running_tasks[user_id]

        pause_state.pop(user_id, None)

        await event.edit(
    "<blockquote>⛔ Stopped Clock</blockquote>",
    buttons=None,
    parse_mode="html"
)

from telethon import events, Button

# ================= MENU TEXT =================
MENU_TEXT = """<blockquote expandable>
Reply Bot Command List ကို ကြည့်ရန် Buttons Open ကိုနှိပ်ပါ။
</blockquote>"""
GROUP_CMDS = """<blockquote expandable>
╔═══════ Group Only Command List  ════════╗

🔇 /mute              → reply + time mute
🔊 /unmute          → mute ရပ်
⛔ /ban                 → user ban
📢 /report             → report user
⚠️ /warn               → warn user
👢 /kip                  → kick user
📌 /pin                  → message pin
📍 /unpin              → unpin message
🛠 /admin             → reply + title admin မြှင့်
📋 /adminlist        → Group Admin List
❌ /rmadmin         → admin ဖြုတ်
⚙️ /groupadm      → group admin tools
🔎 /filter                 → word filter + reply
📑 /filterlist            → filter list
🗑 /rmfilter            → filter ဖျက်
🚫 /quick                → ban text set
📃 /quicklist           → ban list
🧹 /rmquick            → ban ဖျက်
👥 /all                       → mention all
🛑 /stop                   → mention ရပ်
💬 /sms                   → sms spam
🌐 /translation        → translate reply
⏰ /time                   → အချိန်ကြည့်
🌆 /city                    → မြို့ကြည့်
🏠 /mycity               → အိမ်နီးချင်းကြည့်
🤖 /gpt                    → reply AI စာစစ်
🧵 /topic                 → topic set
🎵 /tiktok                 → TikTok Logo Video
📂 /file                      → Group broadcast (1 day limit)
📊 /fileinfo               → file remaining time
╚═════════════════════════════════╝
Channel : @DanGerOus_SKO
Owner   : @DanGerOusSiteKo
</blockquote>"""
# ================= /help =================
@client.on(events.NewMessage(pattern="/help"))
async def show_menu(event):
    await event.reply(
        MENU_TEXT,
        parse_mode="html",
        buttons=[
            [Button.inline("Open", data="group_cmds")],
            [Button.url("Channel", "https://t.me/DanGerOus_SKO")]
        ]
    )

# ================= EXPAND =================
@client.on(events.CallbackQuery(data=b"group_cmds"))
async def group_cmds(event):
    await event.edit(
        GROUP_CMDS,
        parse_mode="html",
        buttons=[
            [Button.inline("🔙 Back", data="back_menu")]
        ]
    )

# ================= BACK =================
@client.on(events.CallbackQuery(data=b"back_menu"))
async def back_menu(event):
    await event.edit(
        MENU_TEXT,
        parse_mode="html",
        buttons=[
            [Button.inline("Open", data="group_cmds")],
            [Button.url("Channel", "https://t.me/DanGerOus_SKO")]
        ]
    )

# ================= GROUP AUTO SAVE =================
@client.on(events.NewMessage)
async def main_handler(event):
    if event.is_group:
        save_group(event.chat_id)
from telethon import events, Button
from telethon.tl.functions.messages import SendReactionRequest
from telethon.tl.types import ReactionEmoji
import asyncio
import io

# 🧸 Sticker file_id
STICKER_ID = "BAADBQADDBgAAmGO0VbASxrUpkVFRwI"

# ================= GROUP AUTO SAVE =================
@client.on(events.NewMessage)
async def main_handler(event):
    if event.is_group:
        save_group(event.chat_id)

# ================= START COMMAND =================
@client.on(events.NewMessage(pattern=r'^/start$'))
async def start_cmd(event):
    user = await event.get_sender()
    user_id = user.id
    chat_id = event.chat_id
    mention = f"<a href='tg://user?id={user_id}'>{user.first_name}</a>"

    # ================= Reaction ❤️ =================
    try:
        await client(SendReactionRequest(
            peer=chat_id,
            msg_id=event.id,
            reaction=[ReactionEmoji(emoticon="❤️‍🔥")]  # Premium emoji
        ))
    except:
        pass

    # ================= Typing animation =================
    async with client.action(chat_id, "typing"):
        animation = ["𝒲", "𝒲𝑒", "𝒲𝑒𝓁", "𝒲𝑒𝓁𝒸", "𝒲𝑒𝓁𝒸𝑜",
                     "𝒲𝑒𝓁𝒸𝑜𝓂", "𝒲𝑒𝓁𝒸𝑜𝓂𝑒", "𝒲𝑒𝓁𝒸𝑜𝓂𝑒.",
                     "𝒲𝑒𝓁𝒸𝑜𝓂𝑒..", "𝒲𝑒𝓁𝒸𝑜𝓂𝑒...", "𝒲𝑒𝓁𝒸𝑜𝓂𝑒...."]
        msg = await event.reply(animation[0])
        for frame in animation[1:]:
            await asyncio.sleep(0.5)
            await msg.edit(frame)
        await asyncio.sleep(0.5)
        try:
            await msg.delete()
        except:
            pass

    # ================= Sticker =================
    try:
        sticker_msg = await event.respond(file=STICKER_ID, reply_to=event.id)
        await asyncio.sleep(5)
        try:
            await sticker_msg.delete()
        except:
            pass
    except:
        pass

    # ================= Profile Photo =================
    photos = await client.get_profile_photos(user.id, limit=1)
    file = None
    if photos.total > 0:
        file = io.BytesIO()
        await client.download_media(photos[0], file)
        file.name = "profile.jpg"
        file.seek(0)

    # ================= Final Welcome Message =================
    text = (
        f"<blockquote expandable>💖 𝐇𝐞𝐥𝐥𝐨 {mention}!\n\n"
        "𝐈 𝐚𝐦 𝐍𝐠𝐚𝐬𝐚𝐫 က 𝐆𝐫𝐨𝐮𝐩 𝐎𝐧𝐥𝐲 မှာ 𝐎𝐧𝐥𝐢𝐧𝐞 𝐌𝐞𝐦𝐛𝐞𝐫 တွေနဲ့ အတူ "
        "𝐑𝐞𝐩𝐥𝐲 ပြန်ပြီး စကားပြောသော ချစက်ရုပ်‌လေးတစ်ကောင်ပါ။</blockquote>"
    )

    buttons = [
        [Button.url("ᴘᴏꜱᴛ ʟɪɴᴋ", "https://t.me/DangerousSk/242")],
        [Button.url("ɢʀᴏᴜᴘ ʟɪɴᴋ", "https://t.me/DangerousParty")],
        [
            Button.url("Support", "https://t.me/Creator_Sk2"),
            Button.url("Owner", "https://t.me/DangerousSiteKo")
        ],
        [Button.url("➕ Group ထဲထည့်ပါ", "https://t.me/DanGerOusNgaSar_Bot?startgroup=true")]
    ]

    if file:
        await client.send_file(
            chat_id,
            file,
            caption=text,
            buttons=buttons,
            parse_mode="html"
        )
    else:
        await event.respond(text, buttons=buttons, parse_mode="html")

    # ================= Pending List Update =================
    pending = load_pending()
    pending.append({
        "user_id": user_id,
        "chat_id": chat_id,
        "cmd": "start"
    })
    save_pending(pending)
from telethon import events
from telethon.tl.functions.messages import SendReactionRequest
from telethon.tl.types import ReactionEmoji
import random

REACTIONS = [
    "❤️","🔥","😍","😂","👍","😎","🥰","💯",
    "💙","💖","💝","💔","💢","💦","😡","😱",
    "🥺","🤍","🖤","💗","💓","💞","✨"
]

# chat-wise counter
COUNTER = {}
REACTION_THRESHOLD = 20  # 20 messages per reaction

@client.on(events.NewMessage)
async def auto_reaction(event):

    # ✅ group only
    if not event.is_group:
        return

    # ❌ bot itself
    me = await event.client.get_me()
    if event.sender_id == me.id:
        return

    # ❌ ignore service messages
    if not event.message or event.message.action:
        return

    # ================= sender safe =================
    sender = await event.get_sender()
    if sender is None:
        return

    chat_id = event.chat_id
    COUNTER.setdefault(chat_id, 0)
    COUNTER[chat_id] += 1

    # ✅ react only after threshold
    if COUNTER[chat_id] >= REACTION_THRESHOLD:
        try:
            emoji = random.choice(REACTIONS)
            await event.client(SendReactionRequest(
                peer=chat_id,
                msg_id=event.id,
                reaction=[ReactionEmoji(emoticon=emoji)]
            ))
        except Exception as e:
            print("Reaction error:", e)
        finally:
            COUNTER[chat_id] = 0  # reset counter

# ================= OWNER COMMANDS =================
@client.on(events.NewMessage(pattern="/groups"))
async def groups_list(event):
    if event.sender_id not in OWNER_IDS:
        return

    if not groups:
        await event.reply("No groups saved.")
        return

    text = "📋 Group List:\n"
    for gid in groups:
        try:
            chat = await client.get_entity(gid)
            text += f"- {chat.title} ({gid})\n"
        except:
            text += f"- Unknown ({gid})\n"

    await event.reply(text)

@client.on(events.NewMessage(pattern="/send"))
async def broadcast(event):
    if event.sender_id not in OWNER_IDS:
        return

    if not event.is_reply:
        await event.reply("Reply to message to broadcast.")
        return

    msg = await event.get_reply_message()
    sent = 0

    for gid in groups:
        try:
            await msg.forward_to(gid)
            sent += 1
            await asyncio.sleep(1)
        except:
            pass

    await event.reply(f"✅ Sent to {sent} groups")
from telethon import events, Button
from telethon.errors import UserAdminInvalidError
import re
import asyncio

# ===== CONFIG =====
MAX_WARN = 3
MUTE_TIME = 300   # 🔇 5 minutes
DELETE_TIME = 300 # 🧹 5 minutes auto delete

warn_db = {}

BTN = [[Button.url("⚠ Dangerous Bot Channel", "https://t.me/DangerousSk")]]
BIO_PATTERN = re.compile(
    r"""
    # ===== ENGLISH VARIATIONS =====
    b[\s\W_]*i[\s\W_]*o |
    b1o | bi0 | b!o |
    b[\s\W_]*i[\s\W_]*o |
    ʙ[\s\W_]*ɪ[\s\W_]*ᴏ |
    𝙗[\s\W_]*𝙞[\s\W_]*𝙤 |
    𝗯[\s\W_]*𝗶[\s\W_]*𝗼 |
    ｂ်််ီ[\s\W_]*ｉ[\s\W_]*ｏ |
    ဘ[ီ]?[\s]*အိုင်[\s]*အို |
    ဘိုင်[\s-]*အို |
    b[\s]*အိုင်[\s]*o

    # ===== FANCY / FONT =====
    ʙ[\s\W_]*ɪ[\s\W_]*ᴏ |
    𝙗[\s\W_]*𝙞[\s\W_]*𝙤 |
    𝗯[\s\W_]*𝗶[\s\W_]*𝗼 |
    𝕓[\s\W_]*𝕚[\s\W_]*𝕠 |
    𝓫[\s\W_]*𝓲[\s\W_]*𝓸 |
    𝒃[\s\W_]*𝒊[\s\W_]*𝒐 |
    𝐛[\s\W_]*𝐢[\s\W_]*𝐨 |

    # ===== FULLWIDTH / SYMBOL =====
    ｂ[\s\W_]*ｉ[\s\W_]*ｏ |
    🅱[\s\W_]*🅸[\s\W_]*🅾 |

    # ===== BURMESE VARIATIONS =====
    ဘိုင် |
    ဘိုင်[\s-]*အို |
    ဘ[ီ]?[\s]*အိုင်[\s]*အို |
    ဘီအိုင်အို |
    ဘိုင်အို |
    ဘိုင်အိုး |
    ဘိုင်လား |
    ဘိုင်လာ |
    ဘို |
    ဘိုင်ဘို |

    # ===== MIX LANG =====
    b[\s]*အိုင်[\s]*o |
    b[\s]*a[\s]*i[\s]*o |
    bio[\s]*link |
    bio[\s]*chat |
    bio[\s]*tg |
    bio[\s]*pm |

    # ===== TELEGRAM STYLE =====
    b[\s]*i[\s]*o[\s]*link |
    b[\s]*i[\s]*o[\s]*dm |
    b[\s]*i[\s]*o[\s]*message |

    # ===== SPACED / HIDDEN =====
    b[\s\.\/_-]*i[\s\.\/_-]*o |
    b[\s]*i[\s]*o |
    b[\.\-_\s]*i[\.\-_\s]*o
    """,
    re.IGNORECASE | re.VERBOSE
)

# ===== AUTO DELETE =====
async def auto_delete(msg):
    await asyncio.sleep(DELETE_TIME)
    try:
        await msg.delete()
    except:
        pass


@client.on(events.NewMessage)
async def message_filter(event):
    if not event.is_group:
        return

    msg = event.message
    sender = await event.get_sender()
    sender_id = sender.id
    chat_id = event.chat_id
    mention_text = f"<a href='tg://user?id={sender_id}'>{sender.first_name}</a>"

    # ===== Admin Skip =====
    try:
        perms = await client.get_permissions(chat_id, sender_id)
        if perms.is_admin or perms.is_creator:
            return
    except:
        return

    text = msg.text or ""
    reason = None

    # ===== FILTER =====
    if re.search(r"@\w+", text):
        reason = "Member တွေကို Username Mention ခေါ်ခွင့်မပေးဘူး။"
    elif re.search(r"(https?://|t\.me/|telegram\.me/)", text):
        reason = "Group ထဲမှာ Link ပို့ခွင့်မပေးဘူး။"
    elif msg.forward and getattr(msg.forward, "from_id", None):
        if hasattr(msg.forward.from_id, "channel_id"):
            reason = "Channel Forward ပို့ခွင့်မပေးဘူး။"
    elif BIO_PATTERN.search(text):
        reason = "Bio မှာဘာပုတယ်ညာပုတယ်ဆိုဖျတ်တယ်။"

    if not reason:
        return

    # ===== DELETE USER MESSAGE =====
    try:
        await msg.delete()
    except:
        pass

    # ===== WARN SYSTEM =====
    warn_db.setdefault(chat_id, {})
    warn_db[chat_id].setdefault(sender_id, 0)

    warn_db[chat_id][sender_id] += 1
    warn_count = warn_db[chat_id][sender_id]

    # ===== MUTE =====
    if warn_count >= MAX_WARN:
        try:
            await client.edit_permissions(chat_id, sender_id, send_messages=False)

            m = await event.respond(
                f"<blockquote expandable>"
                f"🔇 {mention_text} {reason} {warn_count}/{MAX_WARN} Warn ပြည့်သွားလို့ 5 Minutes Mute လုပ်လိုက်တယ်။"
                f"</blockquote>",
                buttons=BTN,
                parse_mode="html"
            )
            asyncio.create_task(auto_delete(m))

            await asyncio.sleep(MUTE_TIME)

            await client.edit_permissions(chat_id, sender_id, send_messages=True)
            warn_db[chat_id][sender_id] = 0

            m2 = await event.respond(
                f"<blockquote expandable>🔓 {mention_text} - Muteဖြည်လိုက် ပြီးသွားပြီ။ နောက်ထပ် မလုပ်နဲ့။</blockquote>",
                buttons=BTN,
                parse_mode="html"
            )
            asyncio.create_task(auto_delete(m2))

        except UserAdminInvalidError:
            m = await event.respond(
                "<blockquote expandable>⚠ Bot ကို Admin ပေးထားဖို့လိုတယ်။</blockquote>",
                buttons=BTN,
                parse_mode="html"
            )
            asyncio.create_task(auto_delete(m))

    # ===== WARN =====
    else:
        m = await event.respond(
            f"<blockquote expandable>"
            f"❌ {mention_text} {reason} သတိ သုံးခါဆိုမြုမယ် {warn_count}/{MAX_WARN}"
            f"</blockquote>",
            buttons=BTN,
            parse_mode="html"
        )
        asyncio.create_task(auto_delete(m))

register_welcome(client)
register_topic_system(client)
gpt_register(client)
register_filter(client)
all_register(client)
quick_register(client)
mute_register(client)
register_tiktok_system(client)
register_dm_system(client)
register_file_system(client, OWNER_IDS)
register_groupadm_system(client)
register_sms_system(client)
register_admin_system(client)
register_group_only_commands(client)
register_spam(client)
register_shop(client)
register_reply_system(client)
register_translation_system(client)
register_all_system(client)
register_link_system(client, OWNER_IDS)
register_clear_system(client, OWNER_IDS)
# ================= RUN =================
print("✅ Telethon Bot Running...")
client.run_until_disconnected()


