#
# This file needs to be placed like ~/.local/share/gedit/plugins/example/__init__.py
# or renamed like ~/.local/share/gedit/plugins/example.py depending on .plugin file

from gi.repository import GObject, Gtk, Gedit, PeasGtk, Gio


# For our example application, this class is not exactly required.
# But we had to make it because we needed the app menu extension to show the menu.
class ToggleExampleAppActivatable(GObject.Object, Gedit.AppActivatable):
    app = GObject.property(type=Gedit.App)
    __gtype_name__ = "ToggleExampleAppActivatable"

    def __init__(self):
        GObject.Object.__init__(self)
        self.menu_ext = None
        self.menu_item = None

    def do_activate(self):
        self._build_menu()

    def _build_menu(self):
        # Get the extension from tools menu
        self.menu_ext = self.extend_menu("tools-section")
        # This is the submenu which is added to a menu item and then inserted in tools menu.
        sub_menu = Gio.Menu()
        sub_menu_item = Gio.MenuItem.new("show/hide Content", 'win.toggle_document')
        sub_menu.append_item(sub_menu_item)
        self.menu_item = Gio.MenuItem.new_submenu("Toggle Content", sub_menu)
        self.menu_ext.append_menu_item(self.menu_item)
        # Setting accelerators, now our action is called when Ctrl+Alt+h is pressed.
        self.app.set_accels_for_action("win.toggle_document", ("<Primary><Alt>2", None))

    def do_deactivate(self):
        self._remove_menu()

    def _remove_menu(self):
        # removing accelerator and destroying menu items
        self.app.set_accels_for_action("win.dictonator_start", ())
        self.menu_ext = None
        self.menu_item = None


class ToggleExampleWindowActivatable(GObject.Object, Gedit.WindowActivatable, PeasGtk.Configurable):
    window = GObject.property(type=Gedit.Window)
    __gtype_name__ = "ToggleExampleWindowActivatable"
    text = ""

    def __init__(self):
        GObject.Object.__init__(self)

    # this is called every time the gui is updated
    def do_update_state(self):
        # if there is no document in sight, we disable the action, so we don't get NoneException
        if self.window.get_active_view() is not None:
            self.window.lookup_action('toggle_document').set_enabled(True)


    def do_activate(self):
        # Defining the action which was set earlier in AppActivatable.
        self._connect_menu()

    def _connect_menu(self):
        action = Gio.SimpleAction(name='toggle_document')
        action.connect('activate', self.action_cb)
        self.window.add_action(action)

    def action_cb(self, action, data):
        # On action clear the document.
        view = self.window.get_active_view()
        doc = self.window.get_active_document()
        docLength = doc.get_char_count();
        if(docLength==0):
            doc.set_text(self.text);
            # self.text = ""
        else:
            self.text = doc.get_text(doc.get_start_iter(), doc.get_end_iter(), False)
            doc.set_text("");

    def do_deactivate(self):
        pass

