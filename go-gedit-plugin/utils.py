# util.py
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

MAX_ERR_MSG_LEN = 500

def get_iter_cursor(buffer):
    cursor_position = buffer.get_property('cursor-position')
    return buffer.get_iter_at_offset(cursor_position)

def scroll_to_insert(buffer, view):
    insert = buffer.get_insert()
    view.scroll_to_mark(insert, 0.0, True)
