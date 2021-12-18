from rich.panel import Panel
from rich.align import Align
from rich.text import Text
from rich.style import Style
from textual.app import App
from textual.reactive import Reactive
from textual.widget import Widget
import os
import psutil
from psutil._common import bytes2human
import time
import platform
import distro
import subprocess
import cpuinfo
from datetime import datetime

class OSsoftware:
    
    def DetermineWM(self):
      # Execute shell command using package "wmctrl" to identify window manager and desktop environment. How this works is currently unknown.
      WMdata = subprocess.check_output("wmctrl -m", shell=True, text=True)
      WMname = ""
      
      if "Name: Mutter" in WMdata:
        WMname = "Mutter"
      if "Name : dwm" in WMdata:
        WMname = "DWM"
      
      elif "Name: N/A" in WMdata:
        WMname = "[red]Unable to determine WM[/red]"
      
      return WMname
      
    # Function that determines the Display Server. Either Xorg or Wayland.  
    def DetermineDS(self):
      DSdata = subprocess.check_output("loginctl show-session 1 -p Type",shell=True, text=True)
      DSname = ""
    
      if "Type=x11" in DSdata:
        DSname = "Xorg"
      if "Type=wayland" in DSdata:
        DSname = "Wayland" # I have no clue what wayland would return on loginctl so i'll just do it like this for now.
    
      elif "Type= " or " " in DSdata:
        DSName = "[red]No display server detected[/red]"
    
      return DSname
  

# OS Screen contains software centric system information and returns it wrapped in a panel.
class OSScreen(Widget):
    def render(self):
        # Received string from the function that gets the Window manager
        rwmstring =OSsoftware.DetermineWM(self)
        # Received string from the function that gets the Display server
        rdsstring = OSsoftware.DetermineDS(self)
        # Identify Desktop Environment
        desktopenvironmentinfo = subprocess.check_output("echo $XDG_CURRENT_DESKTOP", shell=True, text=True)
        # Window title
        OStitleText = "[bold cyan]OPERATING SYSTEM[/bold cyan]"
        # Computer uptime
        uptime = str(datetime.now() - datetime.fromtimestamp(psutil.boot_time()))
        # Computer uptime cutted string
        cutteduptime = (uptime[0:7])
        # The text inside
        osinfo = f"""[bold green]KERNEL:[/bold green][green] {platform.system()} release {platform.release()} [/green]
[bold green]DISTRIBUTION:[/bold green][green] {distro.name()}[/green]
[bold green]DISPLAY SERVER:[/bold green][green] {rdsstring} [/green]
[bold green]WINDOW MANAGER:[/bold green][green] {rwmstring} [/green]
[bold green]DESKTOP ENVIRONMENT:[/bold green][green] {desktopenvironmentinfo}[/green]
[bold green]USER LOGIN:[/bold green][green] {platform.node()}[/green]
[bold green]UPTIME:[/bold green][green] {cutteduptime}[/green]

                 """

        return Panel(osinfo, title=OStitleText, title_align="left", border_style="blue")


# HW Screen contains Hardware information and specifications.
class HWScreen(Widget):
   # cpuinfo is quite of a slow module. Perhaps it is the nature of interpreted languages, the fact that textual is a module in it's infancy, or (most likely) just me being terrible at programming. Or maybe because i'm coding on an old HP Compaq with a grand max of 2.50GHz processing which doesn't help python or whatsoever.
   # What i do know is that the hypothesis of "Does textual play nice with two widgets (or more) that refreshes at the same time?" is "NO" (or at least seems to be) and it was tested with a widget made with rich (Clock(Widget))
   # and a live CPU Frequency counter (HWScreen(Widget)) being this one. 

    # def on_mount(self):
      # The CPU counting refreshes every 10 seconds.
      #  self.set_interval(10, self.refresh)

   # render stuff like text here.
    def render(self):
        # Hardware screen title text
        HWtitleText = "[bold cyan]HARDWARE INFORMATION[/bold cyan]"
        # The text inside - disk_usage takes for argument a disk partition. In our case, Root. 
        hwinfo = f"""[bold green]CPU:[/bold green][green] {cpuinfo.get_cpu_info()["brand_raw"]} [/green]
   [bold green]ARCHITECTURE:[/bold green][green] {cpuinfo.get_cpu_info()["arch_string_raw"] + " " + "(" +  str(cpuinfo.get_cpu_info()["bits"]) + "-bits" + ")"} [/green]
   [bold green]VENDOR:[/bold green][green] {cpuinfo.get_cpu_info()["vendor_id_raw"]} [/green]
   [bold green]FREQUENCY:[/bold green] [green]{cpuinfo.get_cpu_info()["hz_actual_friendly"]}[/green][bold green] (ACTUAL)[/bold green]
   [bold green]CHIPSET:[/bold green] [green]{cpuinfo.get_cpu_info()["hardware_raw"]}
[bold green]MEMORY:[/bold green]
      [bold green]RAM:[/bold green]
          [green]TOTAL: {bytes2human(psutil.virtual_memory().total)}[/green]
          [green]USED: {bytes2human(psutil.virtual_memory().used) + " (" + str(psutil.virtual_memory().percent) + "%)"}[/green]
          [green]AVAIALBLE: {bytes2human(psutil.virtual_memory().available)}[/green]
      [bold green]HDD:[/bold green]
          [green]TOTAL: {bytes2human(psutil.disk_usage("/").total)}[/green]
          [green]USED: {bytes2human(psutil.disk_usage("/").used) + " (" + str(psutil.disk_usage("/").percent) + "%)"}[/green]
          [green]AVAILABLE: {bytes2human(psutil.disk_usage("/").free)}[/green]
     
                  """
        # Return the results wrapped around a Panel, creating a beautiful window in your terminal.
        return Panel(hwinfo, title=HWtitleText, title_align="left", border_style="blue")

class Clock(Widget):
  
    def on_mount(self):
        self.set_interval(1, self.refresh)

    def render(self):
        # Wrap the current time around a panel. string format time is the all-in-one because bleh.
        currentTime = Panel(Text(datetime.now().strftime("%c")), border_style="cyan")
        return (Align.center(currentTime, vertical="top"))

# App initialization
class TestSpecs(App):
    async def on_mount(app) -> None:
        clocksize = 28
        # Dock both main screen widgets to the left at Z layer -1. Size is current terminal size minus clock widget size divided by 2.
        await app.view.dock(OSScreen(), HWScreen(),  z=-1, edge="left", size=int((os.get_terminal_size().columns - clocksize) /2))
        await app.view.dock(Clock(), edge="right", z=0, size=clocksize)


if __name__ == '__main__':
    TestSpecs.run()
