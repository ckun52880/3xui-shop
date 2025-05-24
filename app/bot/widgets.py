from aiogram.types import Message
from aiogram_dialog import DialogManager, ShowMode
from aiogram_dialog.widgets.input import BaseInput, MessageInput


class IgnoreInput(BaseInput):
    async def process_message(
        self, message: Message, widget: MessageInput, dialog_manager: DialogManager
    ):
        dialog_manager.show_mode = ShowMode.EDIT
