from abc import ABC, abstractmethod
from typing import List, Callable, Optional

from duit.event.Event import Event
from duit.model.DataField import DataField


class BaseMenuItem(ABC):
    pass


class SeparatorMenuItem(BaseMenuItem):
    pass


class TextMenuItem(BaseMenuItem):
    def __init__(self, text: str, help_text: str = ""):
        super().__init__()
        self.text = DataField(text)
        self.help_text = DataField(help_text)


class ButtonMenuItem(TextMenuItem):
    def __init__(self, text: str, help_text: str = "",
                 on_action: Optional[Callable[["ButtonMenuItem"], None]] = None):
        super().__init__(text, help_text)
        self.on_action: Event["ButtonMenuItem"] = Event()

        if on_action is not None:
            self.on_action += on_action


class CheckMenuItem(TextMenuItem):
    def __init__(self, text: str, help_text: str = "",
                 checked: bool = False,
                 on_action: Optional[Callable[[bool], None]] = None):
        super().__init__(text, help_text)
        self.checked: DataField[bool] = DataField(checked)

        if on_action is not None:
            self.checked.on_changed += on_action


class Menu:
    def __init__(self, title: str, items: Optional[List[BaseMenuItem]] = None, is_app_menu: bool = False):
        self.title = DataField(title)
        self.items = items if items is not None else []
        self.is_app_menu = is_app_menu


class BaseApplicationMenuBar(ABC):
    def __init__(self, title: str):
        self.title = title

        self.menus: List[Menu] = []

    def add_menu(self, menu: Menu):
        self.menus.append(menu)

    def attach(self):
        for menu in self.menus:
            self._attach_menu(menu)

            for item in menu.items:
                self._attach_menu_item(menu, item)

    @abstractmethod
    def _attach_menu(self, menu: Menu):
        pass

    @abstractmethod
    def _attach_menu_item(self, menu: Menu, item: BaseMenuItem):
        pass
