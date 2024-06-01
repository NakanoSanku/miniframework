from pygamescript import GameScript, ImageTemplate, MultiColorsTemplate
from minidevice import DroidCast, MaaTouch, ADBCap, MiniCap

d = GameScript(serial="127.0.0.1:16384", debug=debug)
#
# d.screenshot()
# d.click(100,100,5000)

test = MultiColorsTemplate("#e0bb75",
                           [[18, 5, "#e2bf85"], [178, 6, "#744d3c"], [186, 3, "#e53b2a"], [336, 1, "#98412d"],
                            [352, 7, "#e03f13"], [351, 19, "#181e12"], [353, -2, "#f9802d"]],threshold=26
                           )
ts = d.screenshot()
d.saveScreenshot()
# print(test.match(ts))
