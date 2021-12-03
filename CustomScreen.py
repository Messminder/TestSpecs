from rich.panel import Panel
from rich.align import Align
from rich.text import Text
from rich.traceback import install
from rich.style import Style
from textual.app import App
from textual.events import Click
from textual.reactive import Reactive
from textual.widget import Widget
from textual.widgets import Placeholder
install()
import os
import psutil
import time
import platform
import distro
import GPUtil
import cpuinfo
from datetime import datetime

#OS Screen contains software centric system information and returns it wrapped in a panel.
class OSScreen(Widget):
    def render(self):
        osname = platform.uname()
        OStitleText = "[bold cyan]OPERATING SYSTEM[/bold cyan]"
        osinfo = f"""[bold green]KERNEL:[/bold green][green] {platform.system()} release {platform.release()} [/green]
[bold green]DISTRIBUTION:[/bold green][green] {distro.name() + " " + "GNU/" + platform.system()}[/green]

                 """

        return Panel(osinfo, title=OStitleText, title_align="left", border_style="blue")

class HWScreen(Widget):
    def on_mount(self):
        self.set_interval(7, self.refresh)


    def render(self):
        HWtitleText = "[bold cyan]HARDWARE INFORMATION[/bold cyan]"
        hwinfo = f"""[bold green]CPU:[/bold green][green] {cpuinfo.get_cpu_info()["brand_raw"]} [/green]
   [bold green]ARCHITECTURE:[/bold green][green] {cpuinfo.get_cpu_info()["arch_string_raw"] + " " + "(" +  str(cpuinfo.get_cpu_info()["bits"]) + "-bits" + ")"} [/green]
   [bold green]VENDOR:[/bold green][green] {cpuinfo.get_cpu_info()["vendor_id_raw"]} [/green]
   [bold green]FREQUENCY:[/bold green] [green]{cpuinfo.get_cpu_info()["hz_actual_friendly"]}[/green]
            [bold green]ADVERTISED:[/bold green][green] {cpuinfo.get_cpu_info()["hz_advertised_friendly"]} [/green]
            [bold green]ACTUAL:[/bold green][green] {str(cpuinfo.get_cpu_info()["hz_actual"]) + " GHz"} [/green]

                  """

        return Panel(hwinfo, title=HWtitleText, title_align="left", border_style="blue")

class Clock(Widget):
    def on_mount(self):
        self.set_interval(1, self.refresh)

    def render(self):
        currentTime = Panel(Text(datetime.now().strftime("%c")))
        return (Align.center(currentTime, vertical="top"))

class Test(App):
    async def on_mount(app) -> None:
        await app.view.dock(OSScreen(), HWScreen(),  z=-1, edge="left", size=int((os.get_terminal_size().columns - 28) /2))
        await app.view.dock(Clock(), edge="right", z=0, size=28)


if __name__ == '__main__':
    Test.run()
