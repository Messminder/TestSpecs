# TestSpecs
TestSpecs is a terminal system information and specification fetching program written in Python using textual and rich python modules. It is not something to be used seriously for practical usage (for now?). The primary purpose of TestSpecs is to practice programming. The reason why this repo is public is for portfolio reasons only.
Since TestSpecs is a simple program, who's functional purpose is to list out system specifications (Hardware and Software) the features may not differ much from screenfetch or Neofetch. Aside from the pretty ASCII art Distro logo.
After aquiering a Raspberry Pi 4, I found out that this software could be more useful than i could have innitially thought. As it helped me see if i setted up the OSes for the Pi in the way i want, such as with a DE or without DE, which processor i am running, if i indeed have 4GB of RAM, and even identify SoC Chip Number. So I suppose it can be good to spot potential fake raspberry pis.

As a result of this discovery, i will continue to develop TestSpecs further, in the hope that it will work on all computers on any linux distro (and potentially) MacOS.


As textual runs on Linux and MacOS only, so is TestSpecs.

Dependencies for now(Shell):
>wmctrl package

  -sudo apt install wmctrl (Debian/Ubuntu)

  -sudo pacman -S wmctrl (Arch and Arch-based)

  -sudo xbps-install wmctrl (Void Linux)
 
 Python dependencies (pip installs):
 >rich
 >textual
 >psutil
 >distro
 >py-cpuinfo

