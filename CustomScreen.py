from rich.panel import Panel
from rich.align import Align
from rich.text import Text
from rich.style import Style
from textual.app import App
from textual.events import Click
from textual.reactive import Reactive
from textual.widget import Widget
from textual.widgets import Placeholder
import os
import psutil
import time
import platform
import distro
import GPUtil
import cpuinfo
from datetime import datetime

# OS Screen contains software centric system information and returns it wrapped in a panel.
# TODO -Find a way to get window manager and/or Desktop environment name
# TODO -Get host name and uptime since boot in a politely readable manner
# TODO - Correctly identify if using Xorg or Wayland
class OSScreen(Widget):
    def render(self):
        OStitleText = "[bold cyan]OPERATING SYSTEM[/bold cyan]"
        osinfo = f"""[bold green]KERNEL:[/bold green][green] {platform.system()} release {platform.release()} [/green]
[bold green]DISTRIBUTION:[/bold green][green] {distro.name() + " " + "GNU/" + platform.system()}[/green]

                 """

        return Panel(osinfo, title=OStitleText, title_align="left", border_style="blue")


# HW Screen contains Hardware information and specifications.
# TODO -Hard drive info

class HWScreen(Widget):
   # cpuinfo is quite of a slow module. Perhaps it is the nature of interpreted languages, the fact that textual is a module in it's infancy, or (most likely) just me being terrible at programming.
   # What i do know is that the hypothesis of "Does textual play nice with two widgets (or more) that refreshes at the same time?" is "NO" and it was tested with a widget made with rich (Clock(Widget))
   # and a live CPU Frequency counter (HWScreen(Widget)) being this one. 
    def on_mount(self):
        self.set_interval(5, self.refresh)

   # render stuff like text here.
    def render(self):
        HWtitleText = "[bold cyan]HARDWARE INFORMATION[/bold cyan]"
        hwinfo = f"""[bold green]CPU:[/bold green][green] {cpuinfo.get_cpu_info()["brand_raw"]} [/green]
   [bold green]ARCHITECTURE:[/bold green][green] {cpuinfo.get_cpu_info()["arch_string_raw"] + " " + "(" +  str(cpuinfo.get_cpu_info()["bits"]) + "-bits" + ")"} [/green]
   [bold green]VENDOR:[/bold green][green] {cpuinfo.get_cpu_info()["vendor_id_raw"]} [/green]
   [bold green]FREQUENCY:[/bold green] [green]{cpuinfo.get_cpu_info()["hz_actual_friendly"]}[/green][bold green] (ACTUAL)[/bold green]

                  """
        # Return the results wrapped around a Panel, creating a beautiful window in your terminal.
        return Panel(hwinfo, title=HWtitleText, title_align="left", border_style="blue")

class Clock(Widget):
    #Rip in peace real-time clock
    #def on_mount(self):
    #    self.set_interval(1, self.refresh)

    def render(self):
        # Wrap the current time around a panel. string format time is the all-in-one because bleh.
        currentTime = Panel(Text(datetime.now().strftime("%c")), title="EXEC TIME")
        return (Align.center(currentTime, vertical="top"))

# App initializations
class Test(App):
    async def on_mount(app) -> None:
        # Dock both main screen widgets to the left at Z layer -1. Size is current terminal size minus clock widget size divided by 2.
        await app.view.dock(OSScreen(), HWScreen(),  z=-1, edge="left", size=int((os.get_terminal_size().columns - 28) /2))
        await app.view.dock(Clock(), edge="right", z=0, size=28)


if __name__ == '__main__':
    Test.run()
