from aiogram.fsm.state import State, StatesGroup


class MainMenuState(StatesGroup):
    main_menu = State()


class ProfileState(StatesGroup):
    profile = State()
