"""Dark-mode helpers shared by the CATG and STM editor dialogs.

The dialogs are written with light-theme colours (pastel section backgrounds,
dark grey text, light borders).  When QGIS is running a dark theme these helpers
translate those colours so the dialogs stay readable:

* light backgrounds / borders  -> dark equivalents (hue kept, muted)
* dark text colours            -> light equivalents
* mid-tone and saturated colours (button fills, white button text) unchanged
"""

import colorsys
import re

from qgis.PyQt.QtGui import QColor
from qgis.PyQt.QtWidgets import QWidget

_STYLE_PROP = "_dark_theme_css"

_DECL_RE = re.compile(
    r"(?<![\w-])(?P<prop>background-color|background|border(?:-[a-z-]+)?|"
    r"gridline-color|outline|color)(?P<sep>\s*:\s*)(?P<val>[^;}\"]+)"
)
_COLOR_RE = re.compile(
    r"#(?P<hex>[0-9a-fA-F]{6}|[0-9a-fA-F]{3})\b"
    r"|rgb\(\s*(?P<r>\d+)\s*,\s*(?P<g>\d+)\s*,\s*(?P<b>\d+)\s*\)"
)


def is_dark(widget: QWidget) -> bool:
    """True when the widget's current palette is a dark theme."""
    return widget.palette().window().color().lightness() < 128


def _to_hls(r: int, g: int, b: int):
    return colorsys.rgb_to_hls(r / 255.0, g / 255.0, b / 255.0)


def _from_hls(h: float, lum: float, s: float):
    r, g, b = colorsys.hls_to_rgb(h, lum, s)
    return round(r * 255), round(g * 255), round(b * 255)


def _darken(r: int, g: int, b: int):
    """Map a light background/border colour to a dark one."""
    h, lum, s = _to_hls(r, g, b)
    if lum <= 0.6:
        return r, g, b
    return _from_hls(h, 0.12 + (1.0 - lum) * 0.6, s * 0.5)


def _lighten(r: int, g: int, b: int):
    """Map a dark text colour to a light one."""
    h, lum, s = _to_hls(r, g, b)
    if lum >= 0.45:
        return r, g, b
    return _from_hls(h, 0.9 - lum * 0.6, s)


def adapt_color(color: QColor, dark: bool) -> QColor:
    """Dark-mode equivalent of a light background QColor."""
    if not dark:
        return color
    r, g, b = _darken(color.red(), color.green(), color.blue())
    return QColor(r, g, b)


def adapt_stylesheet(css: str, dark: bool) -> str:
    """Rewrite the colours in a stylesheet / inline style for dark mode."""
    if not dark or not css:
        return css

    def _recolor(match):
        is_text = match.group("prop") == "color"
        fn = _lighten if is_text else _darken

        def _sub(cm):
            if cm.group("hex"):
                hx = cm.group("hex")
                if len(hx) == 3:
                    hx = "".join(ch * 2 for ch in hx)
                rgb = tuple(int(hx[i:i + 2], 16) for i in (0, 2, 4))
                new = fn(*rgb)
                return "#%02x%02x%02x" % new
            rgb = (int(cm.group("r")), int(cm.group("g")), int(cm.group("b")))
            return "rgb(%d,%d,%d)" % fn(*rgb)

        return (
            match.group("prop") + match.group("sep")
            + _COLOR_RE.sub(_sub, match.group("val"))
        )

    return _DECL_RE.sub(_recolor, css)


def retheme(root: QWidget, dark: bool) -> None:
    """Adapt the stylesheets of root and all its descendants for dark mode.

    Safe to call repeatedly: stylesheets already adapted are left alone, and a
    stylesheet set afterwards by the application is adapted again.
    """
    if not dark:
        return
    for w in [root] + root.findChildren(QWidget):
        css = w.styleSheet()
        if not css or css == w.property(_STYLE_PROP):
            continue
        new = adapt_stylesheet(css, True)
        w.setProperty(_STYLE_PROP, new)
        if new != css:
            w.setStyleSheet(new)
