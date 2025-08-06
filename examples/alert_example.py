import gi
gi.require_version('Gtk', '4.0')
from gi.repository import Gtk, GLib
import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "src"))
from sugar.graphics.alert import Alert, ConfirmationAlert, ErrorAlert, TimeoutAlert, NotifyAlert

class AlertExample(Gtk.ApplicationWindow):
    def __init__(self, app):
        super().__init__(application=app, title="Alert Example")
        self.set_default_size(600, 400)
        
        vbox = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=10)
        vbox.set_margin_top(20)
        vbox.set_margin_bottom(20)
        vbox.set_margin_start(20)
        vbox.set_margin_end(20)
        self.set_child(vbox)
        
        self.alert_box = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=5)
        vbox.append(self.alert_box)
        
        btn_simple = Gtk.Button(label="Show Simple Alert")
        btn_simple.connect("clicked", self.on_simple_alert)
        vbox.append(btn_simple)
        
        btn_confirm = Gtk.Button(label="Show Confirmation Alert")
        btn_confirm.connect("clicked", self.on_confirmation_alert)
        vbox.append(btn_confirm)
        
        btn_timeout = Gtk.Button(label="Show Timeout Alert")
        btn_timeout.connect("clicked", self.on_timeout_alert)
        vbox.append(btn_timeout)

    def on_simple_alert(self, button):
        alert = Alert()
        alert.props.title = "Simple Alert"
        alert.props.msg = "This is a basic alert message."
        alert.add_button(1, "OK")
        alert.connect("response", self.on_alert_response)
        self.alert_box.append(alert)

    def on_confirmation_alert(self, button):
        alert = ConfirmationAlert()
        alert.props.title = "Confirm Action"
        alert.props.msg = "Are you sure you want to continue?"
        alert.connect("response", self.on_alert_response)
        self.alert_box.append(alert)

    def on_timeout_alert(self, button):
        alert = TimeoutAlert(timeout=5)
        alert.props.title = "Timeout Alert"
        alert.props.msg = "This alert will disappear in 5 seconds."
        alert.connect("response", self.on_alert_response)
        self.alert_box.append(alert)

    def on_alert_response(self, alert, response_id):
        print(f"Alert response: {response_id}")
        self.alert_box.remove(alert)

class AlertApp(Gtk.Application):
    def do_activate(self):
        window = AlertExample(self)
        window.present()

if __name__ == "__main__":
    app = AlertApp()
    app.run()