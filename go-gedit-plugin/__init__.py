# __init__.py
# Copyright (C) 2012 Juan Carlos Canaza Ayarachi <jccarlos.a@gmail.com>

# go-gedit3-plugin is free software: you can redistribute it and/or modify it
# under the terms of the GNU General Public License as published by the
# Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.

# go-gedit3-plugin is distributed in the hope that it will be useful, but
# WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.
# See the GNU General Public License for more details.

# You should have received a copy of the GNU General Public License along
# with this program.  If not, see <http://www.gnu.org/licenses/>.

from gi.repository import GObject, Gtk, GdkPixbuf, Gedit
from .completion import GoProvider
import sys
import os

class GoPlugin(GObject.Object, Gedit.WindowActivatable):
    __gtype_name__ = "GoPlugin"
    window = GObject.property(type=Gedit.Window)

    def __init__(self):
        GObject.Object.__init__(self)
        self._instances = {}
        self.views = {}
        self.icons = {}
        self.gobin_path = os.getenv("GOBIN", "")
        self._icons_path = os.path.dirname(__file__) + os.sep + "icons" + os.sep
        self._provider = GoProvider(self)
        # load completion icons
        self._load_completion_icons()

    def do_activate(self):
        self.do_update_state()

    def do_deactivate(self):
        print("")

    def do_update_state(self):
        self.update_ui()
    def update_ui(self):
        for view in self.window.get_views():
            completion = view.get_completion()
            completion.add_provider(self._provider)

    def _load_completion_icons(self):
        self.icons['var'] = GdkPixbuf.Pixbuf.new_from_file(self._icons_path + "var16.png")
        self.icons['const'] = GdkPixbuf.Pixbuf.new_from_file(self._icons_path + "const16.png")
        self.icons['func'] = GdkPixbuf.Pixbuf.new_from_file(self._icons_path + "func16.png")
        self.icons['interface'] = GdkPixbuf.Pixbuf.new_from_file(self._icons_path + "interface16.png")
        self.icons['package'] = GdkPixbuf.Pixbuf.new_from_file(self._icons_path + "package16.png")
        self.icons['struct'] = GdkPixbuf.Pixbuf.new_from_file(self._icons_path + "struct16.png")
        self.icons['gopher'] = GdkPixbuf.Pixbuf.new_from_file(self._icons_path + "gopher16.png")
