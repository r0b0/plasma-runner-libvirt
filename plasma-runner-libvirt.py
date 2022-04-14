from pydoc import doc

import dbus
import libvirt
import dbus.service
from dbus.mainloop.glib import DBusGMainLoop
from gi.repository import GLib

DBusGMainLoop(set_as_default=True)

OBJPATH = "/krunnerLibVirt"
IFACE = "org.kde.krunner1"
SERVICE = "cc.lamac.krunner-libvirt"
ICON_PATH = "virt-manager"
DOM_STATES = {
    libvirt.VIR_DOMAIN_RUNNING: "media-playback-start"
}


class Runner(dbus.service.Object):
    """Communicate with KRunner, deal with queries, provide and run actions."""

    def __init__(self) -> None:
        """Create dbus service, fetch firefox database and connect to klipper."""
        dbus.service.Object.__init__(
            self,
            dbus.service.BusName(SERVICE, dbus.SessionBus()),
            OBJPATH,
        )
        self.libvirt_conn = libvirt.open("qemu:///system")
        print(f"Connected to libvirt {self.libvirt_conn}")
        return None

    @dbus.service.method(IFACE, in_signature='s', out_signature='a(sssida{sv})')
    def Match(self, query: str):
        print(f"Received a Match {query}")
        """This method is used to get the matches and it returns a list of tupels"""
        matches = []
        for domain in self.libvirt_conn.listAllDomains():
            domain_name = domain.name()
            icon = DOM_STATES.get(domain.state()[0], "media-playback-stop")
            if query in domain_name:
                matches.append((
                    domain_name,
                    f"{domain_name} Libvirt VM",
                    icon,
                    100,
                    10.0,
                    {}
                ))
        return matches

    @dbus.service.method(IFACE, out_signature='a(sss)')
    def Actions(self):
        print("Received an Actions query")
        # id, text, icon
        return [
            ("start", "Start the VM", "media-playback-start"),
            ("stop", "Stop the VM", "media-playback-stop")
        ]

    @dbus.service.method(IFACE, in_signature='ss')
    def Run(self, data: str, action_id: str):
        print(f"Received a Run command {action_id} for {data}")
        for domain in self.libvirt_conn.listAllDomains():
            if domain.name() == data:
                if action_id == "start":
                    domain.create()
                    print(f"Started domain {domain.name()}")
                elif action_id == "stop":
                    domain.shutdown()
                    print(f"Stopped domain {domain.name()}")
                else:
                    if domain.state()[0] == libvirt.VIR_DOMAIN_RUNNING:
                        domain.shutdown()
                        print(f"Stopped domain {domain.name()}")
                    else:
                        domain.create()
                        print(f"Started domain {domain.name()}")

    @dbus.service.method(IFACE)
    def Teardown(self):
        self.libvirt_conn.close()


runner = Runner()
loop = GLib.MainLoop()
loop.run()
