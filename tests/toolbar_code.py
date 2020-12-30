# def init_toolbutton(self, stock, action_name, pos):
#     button = Gtk.ToolButton.new_from_stock(stock)
#     button.set_is_important(True)
#     button.set_action_name(action_name)
#     # insert the button at position in the toolbar
#     self.insert(button, pos)
#     button.show()

# def __init__(self):
#     # a toolbar
#     Gtk.Toolbar.__init__(self)

#     # which is the primary toolbar of the application
#     self.get_style_context().add_class(Gtk.STYLE_CLASS_PRIMARY_TOOLBAR)
#     self.set_hexpand(True)

#     self.init_toolbutton(Gtk.STOCK_ADD, "app.add", 0)
#     self.init_toolbutton(Gtk.STOCK_OPEN, "app.open", 1)
#     self.init_toolbutton(Gtk.STOCK_SAVE, "app.save_current", 2)
#     self.init_toolbutton(Gtk.STOCK_SAVE_AS, "app.save_dirty_as", 3)
