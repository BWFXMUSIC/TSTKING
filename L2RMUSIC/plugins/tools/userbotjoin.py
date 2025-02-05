import asyncio
from pyrogram.enums import ChatMemberStatus
from pyrogram.errors import (
    ChatAdminRequired,
    InviteRequestSent,
    UserAlreadyParticipant,
    UserNotParticipant,
)
from pyrogram.types import InlineKeyboardButton, InlineKeyboardMarkup
from L2RMUSIC import app
from L2RMUSIC.misc import SUDOERS
from L2RMUSIC.utils.database import (
    get_assistant,
    get_lang,
    is_active_chat,
    is_maintenance,
)
from config import SUPPORT_CHAT
from strings import get_string

links = {}

def UserbotWrapper(command):
    async def wrapper(client, message):
        # Get user language settings
        language = await get_lang(message.chat.id)
        _ = get_string(language)

        # Maintenance check
        if await is_maintenance() is False:
            if message.from_user.id not in SUDOERS:
                return await message.reply_text(
                    text=f"{app.mention} is under maintenance, visit [support chat]({SUPPORT_CHAT}) for knowing the reason.",
                    disable_web_page_preview=True,
                )

        # Try to delete the message if possible
        try:
            await message.delete()
        except Exception as e:
            pass

        chat_id = message.chat.id

        # Check if the chat is active
        if not await is_active_chat(chat_id):
            userbot = await get_assistant(chat_id)
            try:
                # Try to get the assistant chat member
                try:
                    get = await app.get_chat_member(chat_id, userbot.id)
                except ChatAdminRequired:
                    return await message.reply_text(
                        "➥ Please make me an admin and give invite users power to invite my assistant in this chat."
                    )
                
                # Check if the assistant is banned or restricted
                if get.status == ChatMemberStatus.BANNED or get.status == ChatMemberStatus.RESTRICTED:
                    return await message.reply_text(
                        _["call_2"].format(
                            app.mention, userbot.id, userbot.name, userbot.username
                        ),
                        reply_markup=InlineKeyboardMarkup(
                            [
                                [
                                    InlineKeyboardButton(
                                        text="๏ Unban Assistant ๏",
                                        callback_data=f"unban_assistant",
                                    )
                                ]
                            ]
                        ),
                    )
            except UserNotParticipant:
                # Handle case where the userbot is not a participant
                if message.chat.username:
                    invitelink = message.chat.username
                    try:
                        await userbot.join_chat(invitelink)
                    except Exception as e:
                        pass
                else:
                    if chat_id in links:
                        invitelink = links[chat_id]
                        try:
                            await userbot.resolve_peer(invitelink)
                        except:
                            pass
                    else:
                        try:
                            invitelink = await app.export_chat_invite_link(chat_id)
                        except ChatAdminRequired:
                            return await message.reply_text(
                                "➥ Please make me an admin and give invite users power to invite my assistant in this chat."
                            )
                        except Exception as e:
                            return await message.reply_text(
                                f"Error while exporting invite link: {str(e)}"
                            )

                if invitelink.startswith("https://t.me/+"):
                    invitelink = invitelink.replace("https://t.me/+", "https://t.me/joinchat/")
                
                myu = await message.reply_text("Assistant is joining this chat...")
                try:
                    await asyncio.sleep(1)
                    await userbot.join_chat(invitelink)
                    await myu.delete()
                    await message.reply_text(
                        f"{app.mention} Assistant successfully joined this group✅\n\nId:- **@{userbot.username}**"
                    )
                except InviteRequestSent:
                    try:
                        await app.approve_chat_join_request(chat_id, userbot.id)
                    except Exception as e:
                        return await message.reply_text(
                            _["call_3"].format(app.mention, type(e).__name__)
                        )
                    await asyncio.sleep(3)
                    await myu.delete()
                    await message.reply_text(
                        f"{app.mention} Assistant successfully joined this group✅\n\nId:- **@{userbot.username}**"
                    )
                except UserAlreadyParticipant:
                    pass  # Assistant is already in the chat
                except Exception as e:
                    return await message.reply_text(
                        f"Error while assistant joining the chat: {str(e)}"
                    )

                # Save the invite link for future reference
                links[chat_id] = invitelink

                try:
                    await userbot.resolve_peer(chat_id)
                except Exception as e:
                    pass

        return await command(client, message, _, chat_id)

    return wrapper
