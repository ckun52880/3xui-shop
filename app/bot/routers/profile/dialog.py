from aiogram.fsm.state import State, StatesGroup
from aiogram.types import CallbackQuery
from aiogram_dialog import Dialog, DialogManager, ShowMode, Window
from aiogram_dialog.widgets.kbd import Back, Button, Row, Start, SwitchTo
from aiogram_dialog.widgets.text import Const, Format

from app.bot.states import MainMenuState, ProfileState
from app.bot.widgets import IgnoreInput

dialog = Dialog(
    Window(
        Const("Profile"),
        Row(
            Start(
                text=Const("Back to Main Menu"),
                id="main_menu",
                state=MainMenuState.main_menu,
            ),
        ),
        IgnoreInput(),
        state=ProfileState.profile,
    )
)
