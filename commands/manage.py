from commands.baseapp import BaseApp

from commands.manage_command.elem_map import ManageMapXY
from commands.map.map import Map


class ManageUtility(BaseApp):
    def __init__(self):
        super().__init__()
        self._update_parser = None
        self._setup()

    def _setup(self):
        self._manage_parser = self._parser.add_subparsers(title="manage_map_commands",
                                                          description="tools for managing elements of map",
                                                          help="manage_command", dest="command")
        # rep command
        self._add_parser = self._manage_parser.add_parser("add", description="managing assemblies",
                                                          help="assembly help")
        self._add_parser.add_argument("--country", action="store_true", help="getting from remote repository")
        self._add_parser.add_argument("--dot", action="store_true", help="getting from local repository")
        self._add_parser.add_argument("--picture", action="store_true", help="upload only deb packages")

        self._dict_command["add"] = ManageMapXY(self._db_helper)

        # rep command
        self._get_parser = self._manage_parser.add_parser("map", description="managing projects",
                                                          help="project help")
        self._get_parser.add_argument("--country", type=str, action="store", default=None,
                                      help="path for getting from local repository")
        self._get_parser.add_argument("--zoom", type=int, action="store", default=None,
                                      help="path for getting from local repository")
        self._dict_command["map"] = Map(self._db_helper)

    def _execute(self):
        self._args = self._parser.parse_args()
        cmd = self._dict_command.get(self._args.command, None)
        if cmd:
            command = cmd
            try:
                command.run(self._args)
            except Exception as e:
                print(e)
        else:
            print("this command doesn't exist")


if __name__ == "__main__":
    upd = ManageUtility()
    upd.run()
