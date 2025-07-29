
# Table of Contents

1.  [CO2 monitor](#org5277026)
    1.  [cli](#orgccda302)
    2.  [tray](#org6332d21)
    3.  [screen](#orgdf24a16)
2.  [Installation](#orged95805)
    1.  [Development](#org3e02004)
3.  [Pins](#org3b47f26)
    1.  [Screen](#org68d4c31)



<a id="org5277026"></a>

# CO2 monitor

This projects monitors the current CO₂ emissions per kWh of electricity being generated in the Netherlands. It obtains the data from [ned.nl](https://ned.nl), and gets updated every 15 minutes. It has three modes:

    $ co2monitor --help
    
    Usage: co2monitor [OPTIONS] COMMAND [ARGS]...
    
      Shows the current CO2 emissions per kWh of electricity in the Netherlands.
    
    Options:
      --debug / --no-debug
      --api-key TEXT        Override API_KEY environment variable.
      --api-url TEXT        [default: https://api.ned.nl/v1]
      --user-agent TEXT     Override USER_AGENT environment varaible.
      --polltime INTEGER    [default: 60]
      --version             Show the version and exit.
      -h, --help            Show this message and exit.
    
    Commands:
      cli     Print emissions to the commandline.
      screen  Show emissions on an EPD screen connected via GPIO.
      tray    Add a system tray icon with emissions.


<a id="orgccda302"></a>

## cli

This mode polls the API once per minute and outputs it in the current format:

    2024-11-29 19:30: 310.45g CO2/kWh


<a id="org6332d21"></a>

## tray

This creates a really ugly system tray icon showing the CO₂ emissions rounded to the nearest natural number, shown here below the tooltip:

![img](data/tray-screenshot.png)


<a id="orgdf24a16"></a>

## screen

This mode shows the current emisions a small EPD screen connected to some GPIO pins of the Raspberry Pi. It assumes that we are running on a Raspberry Pi, and fails otherwise.

See here a photo of how it looks on [my 2.9 inch screen](https://www.waveshare.com/product/displays/e-paper/2.9inch-e-paper-module-b.htm):

![img](data/screen-photo.jpg)

It uses the current locale (specifically, `LC_TIME`) to determine how the date looks. See [Pins](#org3b47f26) for an overview of what pins need to be connected to the screen.


<a id="orged95805"></a>

# Installation

I show `pip` commands here. However, `pip` isn&rsquo;t ideal for this: use `pipx` or, as I do, `uv` (`uv tool install co2monitor[tray]`, for example).

    $ pip install co2monitor

Is sufficient for the cli mode. The other modes require rather large libraries and are therefore excluded from the base package. Install the dependencies required for the `tray` mode (`Qt`, `pillow`) with

    $ pip install co2monitor[tray]

And, shockingly,

    $ pip install co2monitor[screen]

For the `screen` mode. This installs `pillow`, `RPi.GPIO` and `spidev`.


<a id="org3e02004"></a>

## Development

See the [Makefile](Makefile) for some handy dev commands. I use [uv](https://github.com/astral-sh/uv) to manage my dependencies, but it does not really matter all that much.

[pyproject.toml](pyproject.toml) has an [Entry Point](https://setuptools.pypa.io/en/latest/userguide/entry_point.html), which means that it installs a binary called `co2monitor` in the virtual environment. If you have the virtual environment activated, you can run `co2monitor`. For `uv`, you can execute `uv run co2monitor` to run the project.


<a id="org3b47f26"></a>

# Pins

<https://pinout.xyz/>


<a id="org68d4c31"></a>

## Screen

[Product](https://www.waveshare.com/product/displays/e-paper/2.9inch-e-paper-module-b.htm)

<table border="2" cellspacing="0" cellpadding="6" rules="groups" frame="hsides">


<colgroup>
<col  class="org-left" />

<col  class="org-left" />

<col  class="org-left" />

<col  class="org-right" />

<col  class="org-left" />
</colgroup>
<thead>
<tr>
<th scope="col" class="org-left">Name</th>
<th scope="col" class="org-left">Function</th>
<th scope="col" class="org-left">Color</th>
<th scope="col" class="org-right">Pin number</th>
<th scope="col" class="org-left">GPIO</th>
</tr>
</thead>
<tbody>
<tr>
<td class="org-left">VCC</td>
<td class="org-left">Power</td>
<td class="org-left">Grey</td>
<td class="org-right">1</td>
<td class="org-left">-</td>
</tr>

<tr>
<td class="org-left">GND</td>
<td class="org-left">Ground</td>
<td class="org-left">Brown</td>
<td class="org-right">6</td>
<td class="org-left">-</td>
</tr>

<tr>
<td class="org-left">DIN</td>
<td class="org-left">SPI MOSI</td>
<td class="org-left">Blue</td>
<td class="org-right">19</td>
<td class="org-left">10 (SPI0 MOSI)</td>
</tr>

<tr>
<td class="org-left">CLK</td>
<td class="org-left">SPI Clock</td>
<td class="org-left">Yellow</td>
<td class="org-right">23</td>
<td class="org-left">11 (SPI0 SCLK)</td>
</tr>

<tr>
<td class="org-left">CS</td>
<td class="org-left">SPI chip selection</td>
<td class="org-left">Orange</td>
<td class="org-right">24</td>
<td class="org-left">8  (SPI0 CE0)</td>
</tr>

<tr>
<td class="org-left">DC</td>
<td class="org-left">Data/Command selection</td>
<td class="org-left">Green</td>
<td class="org-right">22</td>
<td class="org-left">25</td>
</tr>

<tr>
<td class="org-left">RST</td>
<td class="org-left">Reset</td>
<td class="org-left">White</td>
<td class="org-right">11</td>
<td class="org-left">17</td>
</tr>

<tr>
<td class="org-left">BUSY</td>
<td class="org-left">Busy status output</td>
<td class="org-left">Purple</td>
<td class="org-right">18</td>
<td class="org-left">24</td>
</tr>
</tbody>
</table>

