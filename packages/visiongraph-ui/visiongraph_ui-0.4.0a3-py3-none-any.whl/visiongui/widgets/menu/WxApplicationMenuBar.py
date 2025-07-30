from functools import partial
from typing import Dict, Optional

import wx
from duit.utils import os_utils

from visiongui.widgets.menu.BaseApplicationMenuBar import BaseApplicationMenuBar, Menu, BaseMenuItem, SeparatorMenuItem, \
    TextMenuItem, CheckMenuItem, ButtonMenuItem


class WxApplicationMenuBar(BaseApplicationMenuBar):
    def __init__(self, title: str, frame: wx.Frame):
        super().__init__(title)

        self.frame = frame
        self.menubar = wx.MenuBar()

        self.item_id_counter = 1 if os_utils.is_macos() else 0
        self.attached_menus: Dict[Menu, wx.Menu] = {}

    def _attach_menu(self, menu: Menu):
        if os_utils.is_macos() and menu.is_app_menu:
            wx_menu: wx.Menu = self.menubar.OSXGetAppleMenu()
            wx_menu.SetTitle(menu.title.value)
            wx_menu.AppendSeparator()
        else:
            wx_menu = wx.Menu()
            self.menubar.Append(wx_menu, menu.title.value)

        menu.title.on_changed += lambda v: wx_menu.SetTitle(v)
        self.attached_menus[menu] = wx_menu

    def _attach_menu_item(self, menu: Menu, item: BaseMenuItem):
        wx_menu = self.attached_menus.get(menu, None)
        assert wx_menu is not None, "WxMenu has not been registered yet."

        if isinstance(item, TextMenuItem):
            menu_item_id = self.item_id_counter

            wx_menu_item: Optional[wx.MenuItem] = None
            if isinstance(item, ButtonMenuItem):
                wx_menu_item = wx_menu.Append(menu_item_id, item.text.value, item.help_text.value)

                def handler(_: wx.CommandEvent, i: ButtonMenuItem):
                    i.on_action(i)

                self.frame.Bind(wx.EVT_MENU, partial(handler, i=item), id=menu_item_id)
            elif isinstance(item, CheckMenuItem):
                # todo: implement writing back the checked status
                wx_menu_item = wx_menu.AppendCheckItem(menu_item_id, item.text.value, item.help_text.value)

                def handler(_: wx.CommandEvent, i: CheckMenuItem, wmi: wx.MenuItem):
                    i.checked.value = wmi.IsChecked()

                self.frame.Bind(wx.EVT_MENU, partial(handler, i=item, wmi=wx_menu_item), id=menu_item_id)
            else:
                raise ValueError(f"TextMenuItem of type {type(item)} is not supported.")

            if wx_menu_item is not None:
                item.text.on_changed += lambda v: wx_menu_item.SetItemLabel(v)
                item.help_text.on_changed += lambda v: wx_menu_item.SetHelp(v)

            self.item_id_counter += 1
        elif isinstance(item, CheckMenuItem):
            pass
        elif isinstance(item, SeparatorMenuItem):
            wx_menu.AppendSeparator()
        else:
            raise ValueError(f"MenuItem of type {type(item)} is not supported.")

    def attach(self):
        self.frame.SetMenuBar(self.menubar)

        super().attach()

        if os_utils.is_macos():
            wx.MenuBar.MacSetCommonMenuBar(self.menubar)
