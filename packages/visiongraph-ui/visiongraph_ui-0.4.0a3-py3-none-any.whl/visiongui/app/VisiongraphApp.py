from abc import ABC, abstractmethod
from argparse import Namespace
from pathlib import Path
from typing import TypeVar, Generic


from duit.arguments.Arguments import Arguments
from duit.settings.Settings import Settings
from visiongraph.VisionGraph import VisionGraph

TG = TypeVar("TG", bound=VisionGraph)
TC = TypeVar("TC")


class VisiongraphApp(ABC, Generic[TG, TC]):
    def __init__(self, config: TC):
        self.config = config
        self.graph = self.create_graph()

        self._settings_handler = Settings()
        self._arguments_handler = Arguments()

    @abstractmethod
    def create_graph(self) -> TG:
        pass

    def load_config(self, path: Path):
        self._settings_handler.load(str(path), self.config)

    def save_config(self, path: Path):
        self._settings_handler.save(str(path), self.config)

    def configure(self, args: Namespace):
        self._arguments_handler.configure(args, self.config)
