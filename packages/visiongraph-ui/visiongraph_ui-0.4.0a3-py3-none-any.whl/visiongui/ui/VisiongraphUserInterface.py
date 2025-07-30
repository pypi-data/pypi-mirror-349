import logging
import traceback
from pathlib import Path
from typing import Generic, TypeVar

from visiongui.app.VisiongraphApp import VisiongraphApp
from visiongui.ui.BaseUserInterface import T
from visiongui.ui.ImageViewerInterface import ImageViewerInterface
from visiongui.widgets.menu.BaseApplicationMenuBar import Menu, ButtonMenuItem

TA = TypeVar("TA", bound=VisiongraphApp)


class VisiongraphUserInterface(Generic[TA, T], ImageViewerInterface[T]):
    def __init__(self, app: TA, width: int = 800, height: int = 600,
                 attach_interrupt_handler: bool = False,
                 settings_panel_width: int = 400,
                 handle_graph_state: bool = True):
        super().__init__(app.config, app.graph.name, width, height, attach_interrupt_handler, settings_panel_width)

        self.app = app
        self.graph = app.graph
        self.graph.on_exception = self._on_graph_exception

        self.handle_graph_state = handle_graph_state
        if self.handle_graph_state:
            self.graph.open()

        self.on_open_settings += self._on_open_settings
        self.on_save_settings += self._on_save_settings

        self.graph_menu = Menu("VisionGraph", items=[
            ButtonMenuItem("Restart", "Restart VisionGraph", on_action=self._on_restart)
        ])
        self.menu_bar.add_menu(self.graph_menu)

    def _on_graph_exception(self, pipeline, ex):
        # display error message in console
        logging.warning("".join(traceback.TracebackException.from_exception(ex).format()))

        # close application on graph exception
        self.invoke_on_gui(lambda: exit(1))

    def _on_close(self):
        if self.handle_graph_state:
            self.graph.close()
        super()._on_close()

    def _on_restart(self, *args):
        self.graph.close()
        self.graph.open()

    def _on_open_settings(self, path: Path):
        self.app.load_config(path)

    def _on_save_settings(self, path: Path):
        self.app.save_config(path)
