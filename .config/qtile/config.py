
###########################
##       _   _ _         ##
##      | | (_) |        ##
##  __ _| |_ _| | ___    ##
## / _` | __| | |/ _ \   ##
## | (_| | |_| | |  __/   ##
## \__, |\__|_|_|\___|   ##
##    | |                ##
##    |_|                ##
###########################


## imports ##
import os
import psutil
import subprocess
from libqtile import bar, layout, widget, hook
from libqtile.config import Click, Drag, Group, Key, Match, Screen
from libqtile.lazy import lazy
from libqtile.utils import guess_terminal
from battery_widget import BatteryWidget
from libqtile.widget import CPUGraph , Volume , base , TextBox

mod = "mod4"
terminal = "xfce4-terminal"

# running dmenu
# def spawn_dmenu(cmd):
#       qtile.cmd_spawn("dmenu_run -p 'Run:' -nb '#1a1a1a' -nf '#dcdccc' -sb '#8f8f8f' -sf '#dcdccc' -fn 'Monospace-14'")  # Replace with your preferred dmenu command

# definiton of brigness control
@hook.subscribe.startup_once
def autostart():
    # ... (other autostart programs)

    # Set the initial brightness level
    brightnessctl_cmd = "brightnessctl s 50%"  # Adjust the value as needed
    subprocess.Popen(brightnessctl_cmd.split())

# wifi status function 
#if the wifi is connected we will get a wifi symbol 

def get_wifi_status():
    wifi_symbol = ""  # Use a Wi-Fi symbol of your choice
    interface = "wlan0"  # Replace with your Wi-Fi interface name

    # Check if the interface is connected to a network
    with open(f"/sys/class/net/{interface}/operstate", "r") as f:
        if f.read().strip() == "up":
            return wifi_symbol
        else:
            return ""

# battery status function 
#including the external battery script 
class ExternalScriptWidget(TextBox):
    def __init__(self, script_path, **config):
        super().__init__(**config)
        self.script_path = script_path

    def poll(self):
        return subprocess.check_output([self.script_path]).decode("utf-8").strip()


# picom setup
os.system("picom --config ~/.config/picom/picom.conf &")
#  volume controls 


keys = [
    # A list of available commands that can be bound to keys can be found
    # at https://docs.qtile.org/en/latest/manual/config/lazy.html
    # Switch between windows
    Key([mod], "h", lazy.layout.left(), desc="Move focus to left"),
    Key([mod], "l", lazy.layout.right(), desc="Move focus to right"),
    Key([mod], "j", lazy.layout.down(), desc="Move focus down"),
    Key([mod], "k", lazy.layout.up(), desc="Move focus up"),
    Key([mod], "space", lazy.layout.next(),
        desc="Move window focus to other window"),
    # Move windows between left/right columns or move up/down in current stack.
    # Moving out of range in Columns layout will create new column.
    Key([mod, "shift"], "h", lazy.layout.shuffle_left(),
        desc="Move window to the left"),
    Key([mod, "shift"], "l", lazy.layout.shuffle_right(),
        desc="Move window to the right"),
    Key([mod, "shift"], "j", lazy.layout.shuffle_down(), desc="Move window down"),
    Key([mod, "shift"], "k", lazy.layout.shuffle_up(), desc="Move window up"),
    # Grow windows. If current window is on the edge of screen and direction
    # will be to screen edge - window would shrink.
    Key([mod, "control"], "h", lazy.layout.grow_left(),
        desc="Grow window to the left"),
    Key([mod, "control"], "l", lazy.layout.grow_right(),
        desc="Grow window to the right"),
    Key([mod, "control"], "j", lazy.layout.grow_down(), desc="Grow window down"),
    Key([mod, "control"], "k", lazy.layout.grow_up(), desc="Grow window up"),
    Key([mod], "n", lazy.layout.normalize(), desc="Reset all window sizes"),
    # Toggle between split and unsplit sides of stack.
    # Split = all windows displayed
    # Unsplit = 1 window displayed, like Max layout, but still with
    # multiple stack panes
    Key(
        [mod, "shift"],
        "Return",
        lazy.layout.toggle_split(),
        desc="Toggle between split and unsplit sides of stack",
    ),
    Key([mod], "Return", lazy.spawn(terminal), desc="Launch terminal"),
    # Toggle between different layouts as defined below
    Key([mod], "Tab", lazy.next_layout(), desc="Toggle between layouts"),
    Key([mod], "q", lazy.window.kill(), desc="Kill focused window"),
    Key([mod, "shift"], "r", lazy.reload_config(), desc="Reload the config"),
    Key([mod], "x", lazy.shutdown(), desc="Shutdown Qtile"),
    # Key([mod], "d", lazy.spawncmd(), desc="Spawn a command using a prompt widget"),
    Key([mod], "d", lazy.spawn("dmenu_run"), desc="launch dmenu"),
    # Adjust brightness up
    Key([], "XF86MonBrightnessUp", lazy.spawn("brightnessctl set +10%")),

    # Adjust brightness down
    Key([], "XF86MonBrightnessDown", lazy.spawn("brightnessctl set 10%-")),
    # reboot
    Key([mod], "z", lazy.spawn("reboot"),
        desc="rebooting the system instantly"),
    # running the monitor screen layout scripts 
    Key([mod, "shift"], "s", lazy.spawn("bash /home/darkxx/.screenlayout/monitor.sh")),

]


groups = []

group_names = ["1", "2", "3", "4", "5", "6",]
group_labels = ["Ⅰ", "Ⅱ", "Ⅲ", "Ⅳ ", "Ⅴ", "Ⅵ ",]
group_layouts = ["monadtall", "monadtall", "monadtall",
                 "monadtall", "monadtall", "monadtall",]


for i in range(len(group_names)):
    groups.append(
        Group(
            name=group_names[i],
            layout=group_layouts[i].lower(),
            label=group_labels[i],
        ))
for i in groups:
    keys.extend([
        Key([mod], i.name, lazy.group[i.name].toscreen()),
        Key([mod], "Tab", lazy.screen.next_group()),
        Key([mod, "shift"], "Tab", lazy.screen.prev_group()),
        Key(["mod1"], "Tab", lazy.screen.next_group()),
        Key(["mod1", "shift"], "Tab", lazy.screen.prev_group()),

        Key([mod, "shift"], i.name, lazy.window.togroup(
            i.name), lazy.group[i.name].toscreen()),
    ])


layouts = [
    layout.Columns(border_focus_stack=["#d75f5f", "#8f3d3d"], border_width=4),
    layout.Max(),
    # Try more layouts by unleashing below layouts.
    # layout.Stack(num_stacks=2 , border_focus="#fc05ec",border_normal="#9e8d9d",border_width=2),
    # layout.Bsp(),
    layout.Matrix(),
    layout.MonadTall(border_focus="#fc05ec",
                     border_normal="#9e8d9d", border_width=2, margin=7),
    # layout.MonadWide(),
    # layout.RatioTile(border_focus="#fc05ec", border_normal="#9e8d9d",border_width=2),
    layout.Tile(),
    # layout.TreeTab(),
    # layout.VerticalTile(),
    # layout.Zoomy(),
]

widget_defaults = dict(
    font="JetBrains Mono",
    fontsize=12,
    padding=1,
)
extension_defaults = widget_defaults.copy()

# Create a TextBox widget as a separator
separator_widget = widget.TextBox(
    text="|",
    fontsize=14,
    padding=5,
    foreground="#ffc0cb",
    background="#1e1e2e"
)
sep3 = widget.TextBox(
    text="--]",
    fontsize=14,
    padding=5,
    foreground="#ffc0cb",
    background="#1e1e2e"
)
sep2 = widget.TextBox(
    text="[--",
    fontsize=14,
    padding=5,
    foreground="#ffc0cb",
    background="#1e1e2e"
)

screens = [
    Screen(
        top=bar.Bar(
            [
                widget.Image(
                    filename="/home/darkxx/custom_walls/ifinity.png",
                    scale=True
                ),
                widget.GroupBox(),
                separator_widget,
                widget.Prompt(),
                separator_widget,
                sep2,                                             
                widget.WindowName(),
                widget.Chord(
                    chords_colors={
                        "launch": ("#ff0000", "#ffffff"),
                    },
                    name_transform=lambda name: name.upper(),
                ),
                # widget.TextBox("default config", name="default"),
                # widget.TextBox("Press &lt;M-r&gt; to spawn", foreground="#d75f5f"),
                # NB Systray is incompatible with Wayland, consider using StatusNotifier instead
                # widget.StatusNotifier(),
                 sep3,
                separator_widget,
                widget.PulseVolume(),
                separator_widget,
                widget.TextBox(text=get_wifi_status()),
                widget.Net(interface="wlan0"),
                separator_widget,
                # DiskUsage(),
                separator_widget,
                CPUGraph(),
                separator_widget,
                ExternalScriptWidget(script_path="~/..config/i3/scripts/battery1"),
                separator_widget,
                widget.Clock(format="%H:%M %p"),
                separator_widget,
                widget.CurrentLayout(),
                separator_widget,
                widget.Systray(),
            ],
            22,
            # border_width=[2, 0, 2, 0],  # Draw top and bottom borders
            # border_color=["ff00ff", "000000", "ff00ff", "000000"]  # Borders are magenta
            background="#1e1e2e"
        )
    ),
]

# Drag floating layouts.
mouse = [
    Drag([mod], "Button1", lazy.window.set_position_floating(),
         start=lazy.window.get_position()),
    Drag([mod], "Button3", lazy.window.set_size_floating(),
         start=lazy.window.get_size()),
    Click([mod], "Button2", lazy.window.bring_to_front()),
]

dgroups_key_binder = None
dgroups_app_rules = []  # type: list
follow_mouse_focus = True
bring_front_click = False
cursor_warp = False
floating_layout = layout.Floating(
    float_rules=[
        # Run the utility of `xprop` to see the wm class and name of an X client.
        *layout.Floating.default_float_rules,
        Match(wm_class="confirmreset"),  # gitk
        Match(wm_class="makebranch"),  # gitk
        Match(wm_class="maketag"),  # gitk
        Match(wm_class="ssh-askpass"),  # ssh-askpass
        Match(title="branchdialog"),  # gitk
        Match(title="pinentry"),  # GPG key password entry
    ]
)
auto_fullscreen = True
focus_on_window_activation = "smart"
reconfigure_screens = True

# If things like steam games want to auto-minimize themselves when losing
# focus, should we respect this or not?
auto_minimize = True

# When using the Wayland backend, this can be used to configure input devices.
wl_input_rules = None

# XXX: Gasp! We're lying here. In fact, nobody really uses or cares about this
# string besides java UI toolkits; you can see several discussions on the
# mailing lists, GitHub issues, and other WM documentation that suggest setting
# this string if your java app doesn't work correctly. We may as well just lie
# and say that we're a working one by default.
#
# We choose LG3D to maximize irony: it is a 3D non-reparenting WM written in
# java that happens to be on java's whitelist.
wmname = "LG3D"
# wallaper setting using the ntriogen program
subprocess.Popen(["nitrogen", "--restore"])
