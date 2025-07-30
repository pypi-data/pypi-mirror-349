from typing import Optional, Union
from eiogram.types import Message, InlineKeyboardMarkup
from ._base import MethodBase


class SendMessage(MethodBase):
    async def execute(
        self,
        chat_id: Union[int, str],
        text: str,
        reply_markup: Optional[InlineKeyboardMarkup] = None,
        reply_to_message_id: Optional[int] = None,
    ) -> Message:
        data = {
            "chat_id": chat_id,
            "text": text,
            "parse_mode": "HTML",
        }

        if reply_markup:
            data["reply_markup"] = reply_markup.dict()

        if reply_to_message_id:
            data["reply_to_message_id"] = reply_to_message_id

        response = await self._make_request("POST", "sendMessage", data)
        message = Message.from_dict(response["result"])
        message.set_bot(self.bot)
        return message
