import logging
from pathlib import Path

import configargparse
from duit.event.Event import Event
from visiongraph import VisionGraph
from visiongraph.util import LoggingUtils

from visiongui.ui.UIContext import UIContext
from visiongui.ui.VisiongraphUserInterface import VisiongraphUserInterface


class VisiongraphAppLauncher:
    def __init__(self, title: str, description: str,
                 graph_type: type[VisionGraph], app_type: type[VisiongraphUserInterface]):
        self.title = title
        self.description = description
        self.graph_type = graph_type
        self.app_type = app_type

        self.on_create_argument_parser: Event[configargparse.ArgumentParser] = Event()

    def launch(self):
        parser = self.create_argument_parser()
        args = parser.parse_args()

        LoggingUtils.setup_logging(args.loglevel)
        logging.info(f"Logging has ben set to {args.loglevel}")

        show_ui = not args.run_as_cli

        graph: VisionGraph = self.graph_type(multi_threaded=show_ui)
        graph.configure(args)

        if args.settings is not None:
            settings_path = Path(args.settings)
            if settings_path.exists():
                if hasattr(graph, "load_config"):
                    graph.load_config(settings_path)
        else:
            settings_path = None

        if show_ui:
            with UIContext():
                window = self.app_type(graph.config, graph)

                if settings_path is not None:
                    window.menu.settings_file = settings_path

                window.display()
        else:
            graph.open()

    def create_argument_parser(self) -> configargparse.ArgumentParser:
        parser = configargparse.ArgumentParser(prog=self.title, description=self.description)
        parser.add_argument("-c", "--config", required=False, is_config_file=True,
                            help="Configuration file path (ini).")
        parser.add_argument("-s", "--settings", type=str, required=False, help="Settings file path (json).")

        self.graph_type.add_params(parser)

        self.on_create_argument_parser(parser)
        return parser
