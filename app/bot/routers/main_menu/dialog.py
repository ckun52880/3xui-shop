from aiogram.fsm.state import State, StatesGroup
from aiogram.types import CallbackQuery, Message
from aiogram_dialog import Dialog, DialogManager, LaunchMode, ShowMode, Window
from aiogram_dialog.widgets.input import MessageInput
from aiogram_dialog.widgets.kbd import Button, Row, Start, SwitchTo, WebApp
from aiogram_dialog.widgets.text import Const, Format

from app.bot.states import MainMenuState, ProfileState
from app.bot.widgets import IgnoreInput

dialog = Dialog(
    Window(
        Const("Main Menu"),
        # Row(
        #     Start(
        #         text=Const("Profile"),
        #         id="profile",
        #         state=ProfileState.profile,
        #     ),
        # ),
        IgnoreInput(),
        state=MainMenuState.main_menu,
    ),
)
