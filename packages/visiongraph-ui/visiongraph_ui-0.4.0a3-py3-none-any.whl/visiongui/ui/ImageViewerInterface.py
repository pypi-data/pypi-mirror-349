from typing import Generic, Optional

import cv2
import numpy as np
import wx
from duit.ui.wx.WxPropertyPanel import WxPropertyPanel
from duit.ui.wx.widgets.WxGfxImageCanvas import WxGfxImageCanvas

from visiongui.ui.BaseUserInterface import BaseUserInterface, T


class ImageViewerInterface(Generic[T], BaseUserInterface[T]):

    def __init__(self, config: T, title: str,
                 width: int = 800, height: int = 600,
                 attach_interrupt_handler: bool = False,
                 settings_panel_width: int = 400):
        super().__init__(config, title, width, height, attach_interrupt_handler)

        self._settings_panel_width = settings_panel_width

        # setup base widgets
        self.image_view = WxGfxImageCanvas(self.panel, self.placeholder_image)

        self.settings_panel = WxPropertyPanel(self.panel)
        self.settings_panel.data_context = self.config

    def _create_ui_layout(self) -> wx.Sizer:
        # Create a sizer for layout management
        main_sizer = wx.BoxSizer(wx.HORIZONTAL)

        # Add image_view to the sizer with proportion=1 to allow it to scale
        main_sizer.Add(self.image_view, 1, wx.EXPAND | wx.ALL, 0)

        # Add settings_panel with a fixed size
        main_sizer.Add(self.settings_panel, 0, wx.EXPAND | wx.ALL, 0)
        self.settings_panel.SetMinSize((self._settings_panel_width, -1))

        return main_sizer

    def update_image_view(self, image: np.ndarray, image_widget: Optional[WxGfxImageCanvas] = None):
        view = image_widget if image_widget is not None else self.image_view
        image_rgb = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)

        def update():
            view.image = image_rgb

        self.invoke_on_gui(update)

    @property
    def placeholder_image(self) -> np.ndarray:
        return np.zeros(shape=(1, 1, 3), dtype="uint8")
