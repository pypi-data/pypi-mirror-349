import traceback
from typing import Optional

import wx
from duit.ui.wx.WxPropertyRegistry import init_wx_registry


class UIContext:
    def __init__(self):
        self.wx_app: Optional[wx.App] = None

    def __enter__(self):
        self.init()
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        if exc_val is not None:
            self._handle_exception(exc_type, exc_val, exc_tb)
            return True

        self.run()
        return False

    def init(self):
        init_wx_registry()
        self.wx_app = wx.App(False)

    def run(self):
        self.wx_app.MainLoop()

    @staticmethod
    def _handle_exception(exc_type, exc_value, exc_traceback):
        # Print the exception with a full stack trace
        traceback.print_exception(exc_type, exc_value, exc_traceback)

        # Terminate the application
        wx.GetApp().ExitMainLoop()
