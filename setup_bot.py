from telethon import events, Button, errors
from iob_variables import iob
import re, random
from apscheduler.schedulers.asyncio import AsyncIOScheduler
from bot_utils import command
from urllib.parse import urlencode as uc

authorized_id = [241346256, 360110756, 471603924, 542401934]
order, order_text, order_type = None, None, None
msg_id_to_unpin = None
SQUAD_ID = -1001621995890

# Bot Testing Group
# SQUAD_ID = -1001460951730


async def unpin_order():
    global msg_id_to_unpin

    if msg_id_to_unpin is not None:
        try:
            await iob.unpin_message(entity=SQUAD_ID, message=msg_id_to_unpin)
        except Exception as e:
            print(f"Couldn't unpin: {e}")
        msg_id_to_unpin = None


def unpin_job():
    scheduler = AsyncIOScheduler()
    scheduler.configure(timezone="Asia/Kolkata")
    scheduler.start()
    scheduler.add_job(unpin_order, 'cron', hour='4', minute='30')
    scheduler.add_job(unpin_order, 'cron', hour='12', minute='30')
    scheduler.add_job(unpin_order, 'cron', hour='20', minute='30')
    print("Unpin jobs started.")


@iob.on(events.CallbackQuery())
async def set_order(event):
    global order, order_text, order_type, msg_id_to_unpin
    event_data = event.data.decode("utf-8")

    message = await event.get_message()

    if message.peer_id.user_id not in authorized_id:
        await event.answer("You're not authorised for this operation!")
        raise events.StopPropagation

    if event_data == "send_order":
        pinned = False

        if order_type == "attack":
            markup = iob.build_reply_markup(
                Button.url(f"⚔️{order}", url="http://t.me/share/url?" + uc({'url':order})))

            try:
                msg = await iob.send_message(SQUAD_ID, f"⚔️{order}{order_text}", buttons=markup)
                msg_id_to_unpin = msg.id
            except:
                await event.respond("Could not send. Is the bot added in that group?" + \
                                    " Also check that bot has the permission to send messages.")
                raise events.StopPropagation

            try:
                await iob.pin_message(entity=SQUAD_ID, message=msg.id)
                pinned = True
            except errors.rpcerrorlist.ChatAdminRequiredError:
                if random.random() > 0.5:
                    await iob.send_message(SQUAD_ID, "In order to pin, give pin permission to bot.")
            
            await event.respond("Order sent" + " and pinned." if pinned else " but could not pin.")
            raise events.StopPropagation

        else:
            markup = iob.build_reply_markup(
                Button.url(f"{order}", url="t.me/share/url?url=" + "🛡Defend"))

            msg = await iob.send_message(SQUAD_ID, f"{order}{order}{order_text}", buttons=markup)
            msg_id_to_unpin = msg.id

            try:
                await iob.pin_message(entity=SQUAD_ID, message=msg.id)
            except errors.rpcerrorlist.ChatAdminRequiredError:
                if random.random() > 0.5:
                    await iob.send_message(SQUAD_ID, "In order to pin, give pin perms to bot.")

    elif re.search(r"glacie|aqua|ventus|solo", event_data):
        order_text = "\n\nSpend gold, hide stocks!\nLet's go!"
        order_type = "attack"
        castles_list = {
            "glacie": "❄️",
            "aqua": "💧",
            "ventus": "🌩",
            "solo": "🪨"
        }
        
        buttons_layout = [Button.inline("Send the order to group", b"send_order")]
        order = castles_list[event_data]
        await event.edit(f"Alright, {order} selected!", buttons=buttons_layout)

    elif re.search(r"def", event_data):
        order_type = "def"
        order_text = "\n\nSpend gold, hide stocks!\nHold the wall tight comrades!"
        buttons_layout = [Button.inline("Send the order to group", b"send_order")]
        order = "🛡"
        await event.edit(f"Alright, {order} selected!", buttons=buttons_layout)
    
    await event.answer()


@events.register(events.NewMessage(pattern="", from_users=authorized_id))
async def test(event):

    if not event.is_private:
        raise events.StopPropagation

    if event.raw_text == "🎯Set Order":
        buttons_layout = [Button.inline("❄️", b"glacie"), Button.inline("💧", b"aqua"),
                          Button.inline("🌩", b"ventus"), Button.inline("🪨", b"solo"),
                          Button.inline("🛡", b"def")]
        await event.respond(f"Select the castle to ⚔️ attack or 🛡 defend Ignis.", buttons=buttons_layout)

    if command(event.raw_text, "start"):
        await iob.send_message(event.chat_id,
                               "Dunno, will put something later on here. Anyway, there's the button.",
                               buttons=[Button.text("🎯Set Order", resize=True, single_use=False)])
        raise events.StopPropagation
