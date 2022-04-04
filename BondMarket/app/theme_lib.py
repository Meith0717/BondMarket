from dataclasses  import dataclass

@dataclass
class theme:
    name        : str
    bg_color    : str
    fg_color    : str
    lb_color    : str
    ttk_theme   : str

LIGHT = theme(
        name='LIGHT', 
        bg_color=None, 
        fg_color='black', 
        lb_color='#f0f0f0', 
        ttk_theme='xpnative'
        )

DARK = theme(
        name='DARK', 
        bg_color='#424242', 
        fg_color='white', 
        lb_color='#424242', 
        ttk_theme='black'
        )