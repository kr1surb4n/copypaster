from gi.repository.GdkPixbuf import Pixbuf
from gi.repository import Gtk, GdkPixbuf
import gi
from os.path import basename, dirname, abspath, join as path_join
gi.require_version("Gtk", "3.0")

icons = ["edit-cut", "edit-paste", "edit-copy"]

THIS_FOLDER = dirname(abspath(__file__))


print(path_join(THIS_FOLDER, "icons/1.png"))

icons = ['address-book-new',
         'application-exit',
         'appointment-new',
         'call-start',
         'call-stop',
         'contact-new',
         'document-new',
         'document-open',
         'document-open-recent',
         'document-page-setup',
         'document-print',
         'document-print-preview',
         'document-properties',
         'document-revert',
         'document-save',
         'document-save-as',
         'document-send',
         'edit-clear',
         'edit-copy',
         'edit-cut',
         'edit-delete',
         'edit-find',
         'edit-find-replace',
         'edit-paste',
         'edit-redo',
         'edit-select-all',
         'edit-undo',
         'folder-new',
         'format-indent-less',
         'format-indent-more',
         'format-justify-center',
         'format-justify-fill',
         'format-justify-left',
         'format-justify-right',
         'format-text-direction-ltr',
         'format-text-direction-rtl',
         'format-text-bold',
         'format-text-italic',
         'format-text-underline',
         'format-text-strikethrough',
         'go-bottom',
         'go-down',
         'go-first',
         'go-home',
         'go-jump',
         'go-last',
         'go-next',
         'go-previous',
         'go-top',
         'go-up',
         'help-about',
         'help-contents',
         'help-faq',
         'insert-image',
         'insert-link',
         'insert-object',
         'insert-text',
         'list-add',
         'list-remove',
         'mail-forward',
         'mail-mark-important',
         'mail-mark-junk',
         'mail-mark-notjunk',
         'mail-mark-read',
         'mail-mark-unread',
         'mail-message-new',
         'mail-reply-all',
         'mail-reply-sender',
         'mail-send',
         'mail-send-receive',
         'media-eject',
         'media-playback-pause',
         'media-playback-start',
         'media-playback-stop',
         'media-record',
         'media-seek-backward',
         'media-seek-forward',
         'media-skip-backward',
         'media-skip-forward',
         'object-flip-horizontal',
         'object-flip-vertical',
         'object-rotate-left',
         'object-rotate-right',
         'process-stop',
         'system-lock-screen',
         'system-log-out',
         'system-run',
         'system-search',
         # 'system-reboot',
         'system-shutdown',
         'tools-check-spelling',
         'view-fullscreen',
         'view-refresh',
         'view-restore',
         'view-sort-ascending',
         'view-sort-descending',
         'window-close',
         'window-new',
         'zoom-fit-best',
         'zoom-in',
         'zoom-original',
         'zoom-out', ]


def icon_shooter():
    while True:
        for tooltip, icon in enumerate(icons):
            yield tooltip, icon


shooter = icon_shooter()


class IconViewWindow(Gtk.Window):
    def __init__(self):
        Gtk.Window.__init__(self)
        self.set_default_size(200, 200)

        liststore = Gtk.ListStore(Pixbuf, str, str)
        iconview = Gtk.IconView.new()
        iconview.set_model(liststore)
        iconview.set_item_width(10)
        iconview.set_pixbuf_column(0)
        iconview.set_text_column(1)
        iconview.set_tooltip_column(2)

        # for icon in icons:

        for _ in range(200):
            _, icon = next(shooter)
            pixbuf = Gtk.IconTheme.get_default().load_icon(icon, 16, 0)
            # pixbuf = GdkPixbuf.Pixbuf.new_from_file(
            #     "icons/{}.png".format(icon))
            liststore.append([pixbuf, icon, icon])

        self.add(iconview)


win = IconViewWindow()
win.connect("destroy", Gtk.main_quit)
win.show_all()
Gtk.main()
