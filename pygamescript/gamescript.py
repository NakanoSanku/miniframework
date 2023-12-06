from minicv import Images
from minidevice import ADBtouch, DroidCast, MiniDevice, Minicap, Minitouch
from template import Template, ImageTemplate
from typing import Optional


class GameScript(MiniDevice):
    def __init__(self, serial=None, capMethod: ADBtouch | Minicap | DroidCast = None,
                 touchMethod: ADBtouch | Minitouch = None, screenshotTimeout=30) -> None:
        super().__init__(serial, capMethod, touchMethod, screenshotTimeout)

    def screenshot(self):
        """get cv2.Mat format image"""
        return Images.bytes2opencv(self.screenshot_raw())

    def saveScreenshot(self, path: str = './screenshot.png'):
        """save screenshot to path"""
        with open(path, 'wb') as file:
            file.write(self.screenshot_raw())

    def find(self, template: Template, isColor: bool = False, colorThreshold: int = 4):
        """find template on the device's screen

        Args:
            template (Template): 模板 ImageTemplate ColorsTemplate OcrTemplate
            isColor  (bool): 是否找色 Default to False.
            colorThreshold (int): 颜色相似度 0~255 Default to 4.

        Returns:
            result: 是否匹配到
        """
        screenshot = self.screenshot()
        if isinstance(template, ImageTemplate):
            return template.match_color(screenshot, colorThreshold) if isColor else template.match(screenshot)
        else:
            return template.match(screenshot)

    def findAndOperate(self, template: Template, operate, operateParams: Optional[dict] = None):
        """find template on the device's screen ,operate the device

        Args:
            template (Template): 模板
            operate (function): 操作方法
            operateParams: 操作方法参数 默认{”result“ : result} 当然你可以设置自定义result

        Returns:
            result: 是否找到模板 会传递给operate函数
        """
        result = self.find(template)
        if result:
            operateParams = operateParams or {}
            operateParams.setdefault("result", result)
            operate(**operateParams)
        return result