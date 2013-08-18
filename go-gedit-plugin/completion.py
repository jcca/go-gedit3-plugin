# completion.py
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

from gi.repository import Gio, GObject, Pango, Gtk, Gdk
from gi.repository import GtkSource as gsv
from . import utils
import subprocess
import json


class GoProvider(GObject.Object, gsv.CompletionProvider):
    __gtype_name__ = 'GoProvider'

    def __init__(self, plugin):
        GObject.Object.__init__(self)
        self._plugin = plugin

    def do_get_start_iter(self, context, proposal, iter):
        return False

    def do_get_name(self):
        return _("Go code completion")

    def do_get_icon(self):
        return self._plugin.icons['gopher']

    def do_match(self, context):
        lang = context.get_iter().get_buffer().get_language()

        if not lang:
            return False

        if lang.get_id() != 'go':
            return False

        return True

    def do_populate(self, context):
        it = context.get_iter()

        buffer = context.get_iter().get_buffer()
        odata = self._get_odata(buffer, utils.get_iter_cursor(buffer))

        if not odata:
            # no proposals
            return context.add_proposals(self, [], True)

        proposals = []
        for po in self._get_podata(odata):
                proposals.append(gsv.CompletionItem.new(po[0], po[1], po[2], po[3]))

        context.add_proposals(self, proposals, True)

    def do_get_activation(self):
        return gsv.CompletionActivation.USER_REQUESTED

    def _get_odata(self, buffer, cursor_iter):
        """
        Return gocode object data.
        """
        cursor_offset = cursor_iter.get_offset()
        text = buffer.get_text(buffer.get_start_iter(), buffer.get_end_iter(), False)
        byte_offset = len(buffer.get_text(buffer.get_start_iter(), buffer.get_iter_at_offset(cursor_offset), True))
        try:
            p = subprocess.Popen(['gocode',
                                '-f=json',
                                'autocomplete',
                                buffer.get_uri_for_display(),
                                str(byte_offset)],
                                stdin=subprocess.PIPE,
                                stdout=subprocess.PIPE,
                                stderr=subprocess.PIPE)
        except OSError as e:
            dialog = Gtk.MessageDialog(flags=Gtk.DialogFlags.MODAL,
                                        type=Gtk.MessageType.ERROR,
                                        buttons=Gtk.ButtonsType.OK,
                                        message_format='Error:')
            dialog.set_markup(_("An error occurred when <i>gocode</i> was attempted to run:"))
            dialog.format_secondary_markup('<span font_family="monospace">' +
                                           str(e) +
                                           '</span>')
            dialog.run()
            dialog.destroy()
            return []

        stdoutdata, stderrdata = p.communicate(str(text).encode())

        if len(stderrdata) != 0:
            dialog = Gtk.MessageDialog(flags=Gtk.DialogFlags.MODAL,
                                        type=Gtk.MessageType.ERROR,
                                        buttons=Gtk.ButtonsType.OK,
                                        message_format='Error:')
            dialog.set_markup(_("An error occurred while running <i>gocode</i>:"))
            if len(stderrdata) > utils.MAX_ERR_MSG_LEN: # cut down too long error messages
                stderrdata = stderrdata[:utils.MAX_ERR_MSG_LEN] + "..."
            dialog.format_secondary_markup('<span font_family="monospace">' +
                                           stderrdata +
                                           '</span>')
            dialog.run()
            dialog.destroy()
            return []

        try:
            return json.loads(stdoutdata.decode())
        except ValueError:
            print("ERROR: gocode input was invalid.")
            return []

    def _get_podata(self, odata):
        """
        Return parsed gocode's object data.
        """
        podata = []
        for candidate in odata[1]:
            if candidate['class'] == "func":
                info = candidate['class'] + " " + candidate['name'] + candidate['type'][len("func"):]
                icon = self._plugin.icons['func']
            else:
                info = candidate['class'] + " " + candidate['name'] + " " + candidate['type']

                icon = self._plugin.icons['var'] # default
                if candidate['class'] == "const":
                    icon = self._plugin.icons['const']
                elif candidate['class'] == "package":
                    icon = self._plugin.icons['package']
                elif candidate['class'] == "type":
                    if candidate['type'] == "interface":
                        icon = self._plugin.icons['interface']
                    elif candidate['type'] == "struct":
                        icon = self._plugin.icons['struct']

            podata.append((candidate['name'],
                           candidate['name'][odata[0]:],
                           icon,
                           info))
        return podata
GObject.type_register(GoProvider)
