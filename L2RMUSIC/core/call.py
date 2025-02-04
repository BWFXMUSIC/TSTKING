import asyncio
import os
from datetime import datetime, timedelta
from typing import Union

from pyrogram import Client
from pyrogram.types import InlineKeyboardMarkup
from pytgcalls import PyTgCalls, StreamType
from pytgcalls.exceptions import (
    AlreadyJoinedError,
    NoActiveGroupCall,
    TelegramServerError,
)
from pytgcalls.types import Update
from pytgcalls.types.input_stream import AudioPiped, AudioVideoPiped
from pytgcalls.types.input_stream.quality import HighQualityAudio, MediumQualityVideo
from pytgcalls.types.stream import StreamAudioEnded

import config
from L2RMUSIC import LOGGER, YouTube, app
from L2RMUSIC.misc import db
from L2RMUSIC.utils.database import (
    add_active_chat,
    add_active_video_chat,
    get_lang,
    get_loop,
    group_assistant,
    is_autoend,
    music_on,
    remove_active_chat,
    remove_active_video_chat,
    set_loop,
)
from L2RMUSIC.utils.exceptions import AssistantErr
from L2RMUSIC.utils.formatters import check_duration, seconds_to_min, speed_converter
from L2RMUSIC.utils.inline.play import stream_markup
from L2RMUSIC.utils.stream.autoclear import auto_clean
from L2RMUSIC.utils.thumbnails import get_thumb
from strings import get_string

autoend = {}
counter = {}


async def _clear_(chat_id):
    db[chat_id] = []
    await remove_active_video_chat(chat_id)
    await remove_active_chat(chat_id)


class Call(PyTgCalls):
    def __init__(self):
        # Initialize Clients and PyTgCalls
        self.clients = [
            Client(name=f"L2RMUSICAss{i+1}", api_id=config.API_ID, api_hash=config.API_HASH, session_string=str(config[f"STRING{i+1}"]))
            for i in range(5)
        ]
        self.calls = [
            PyTgCalls(self.clients[i], cache_duration=100) for i in range(5)
        ]
    
    async def _get_assistant(self, chat_id: int):
        assistant = await group_assistant(self, chat_id)
        return assistant

    async def pause_stream(self, chat_id: int):
        assistant = await self._get_assistant(chat_id)
        await assistant.pause_stream(chat_id)

    async def resume_stream(self, chat_id: int):
        assistant = await self._get_assistant(chat_id)
        await assistant.resume_stream(chat_id)

    async def stop_stream(self, chat_id: int):
        assistant = await self._get_assistant(chat_id)
        try:
            await _clear_(chat_id)
            await assistant.leave_group_call(chat_id)
        except Exception as e:
            LOGGER(__name__).error(f"Error stopping stream: {e}")
    
    async def stop_stream_force(self, chat_id: int):
        for call in self.calls:
            try:
                await call.leave_group_call(chat_id)
            except Exception as e:
                LOGGER(__name__).error(f"Error forcing stop stream: {e}")
        await _clear_(chat_id)

    async def speedup_stream(self, chat_id: int, file_path, speed, playing):
        assistant = await self._get_assistant(chat_id)
        if str(speed) != "1.0":
            base = os.path.basename(file_path)
            chatdir = os.path.join(os.getcwd(), "playback", str(speed))
            os.makedirs(chatdir, exist_ok=True)
            out = os.path.join(chatdir, base)
            
            if not os.path.isfile(out):
                speed_factors = {"0.5": 2.0, "0.75": 1.35, "1.5": 0.68, "2.0": 0.5}
                vs = speed_factors.get(str(speed), 1)
                proc = await asyncio.create_subprocess_shell(
                    cmd=f"ffmpeg -i {file_path} -filter:v setpts={vs}*PTS -filter:a atempo={speed} {out}",
                    stdin=asyncio.subprocess.PIPE,
                    stderr=asyncio.subprocess.PIPE,
                )
                await proc.communicate()

            dur = await asyncio.get_event_loop().run_in_executor(None, check_duration, out)
            dur = int(dur)
            played, con_seconds = speed_converter(playing[0]["played"], speed)
            duration = seconds_to_min(dur)
            stream = (
                AudioVideoPiped(out, audio_parameters=HighQualityAudio(), video_parameters=MediumQualityVideo(), additional_ffmpeg_parameters=f"-ss {played} -to {duration}")
                if playing[0]["streamtype"] == "video"
                else AudioPiped(out, audio_parameters=HighQualityAudio(), additional_ffmpeg_parameters=f"-ss {played} -to {duration}")
            )
            if str(db[chat_id][0]["file"]) == str(file_path):
                await assistant.change_stream(chat_id, stream)
            else:
                raise AssistantErr("File mismatch")
            
            if str(db[chat_id][0]["file"]) == str(file_path):
                exis = (playing[0]).get("old_dur")
                if not exis:
                    db[chat_id][0]["old_dur"] = db[chat_id][0]["dur"]
                    db[chat_id][0]["old_second"] = db[chat_id][0]["seconds"]
                db[chat_id][0]["played"] = con_seconds
                db[chat_id][0]["dur"] = duration
                db[chat_id][0]["seconds"] = dur
                db[chat_id][0]["speed_path"] = out
                db[chat_id][0]["speed"] = speed

    async def force_stop_stream(self, chat_id: int):
        assistant = await self._get_assistant(chat_id)
        try:
            check = db.get(chat_id)
            check.pop(0)
        except Exception as e:
            LOGGER(__name__).error(f"Error during force stop stream: {e}")
        await remove_active_video_chat(chat_id)
        await remove_active_chat(chat_id)
        try:
            await assistant.leave_group_call(chat_id)
        except Exception as e:
            LOGGER(__name__).error(f"Error leaving group call: {e}")

    async def skip_stream(self, chat_id: int, link: str, video: Union[bool, str] = None, image: Union[bool, str] = None):
        assistant = await self._get_assistant(chat_id)
        stream = AudioVideoPiped(link, audio_parameters=HighQualityAudio(), video_parameters=MediumQualityVideo()) if video else AudioPiped(link, audio_parameters=HighQualityAudio())
        await assistant.change_stream(chat_id, stream)

    async def seek_stream(self, chat_id, file_path, to_seek, duration, mode):
        assistant = await self._get_assistant(chat_id)
        stream = (
            AudioVideoPiped(file_path, audio_parameters=HighQualityAudio(), video_parameters=MediumQualityVideo(), additional_ffmpeg_parameters=f"-ss {to_seek} -to {duration}")
            if mode == "video"
            else AudioPiped(file_path, audio_parameters=HighQualityAudio(), additional_ffmpeg_parameters=f"-ss {to_seek} -to {duration}")
        )
        await assistant.change_stream(chat_id, stream)

    async def join_call(self, chat_id: int, original_chat_id: int, link, video: Union[bool, str] = None, image: Union[bool, str] = None):
        assistant = await self._get_assistant(chat_id)
        language = await get_lang(chat_id)
        _ = get_string(language)

        stream = (
            AudioVideoPiped(link, audio_parameters=High
