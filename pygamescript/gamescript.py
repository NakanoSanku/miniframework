from minicv import Images
from minidevice import ADBtouch, DroidCast, MiniDevice, Minicap, Minitouch
from pygamescript.template import Template, ImageTemplate
from typing import Optional
import numpy as np
from pygamescript.algo import CurveGenerate,RandomPointGenerate
import random

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


    def rangeRandomClick(self,result:tuple|list,duration = None,randomPointGenerateAlgo=RandomPointGenerate.normalDistribution):
        if len(result) == 2:
            x,y =result
        elif len(result) == 4:
            x,y=randomPointGenerateAlgo(result)
        else:
            raise ValueError(f"{result} is No Correct Value")
        if duration is None:
            randomI = round(np.random.normal(0, 30))
            duration = random.randint(200,350) if randomI > 80 else  random.randint(80,120)
        self.click(x,y,duration)

    def curveSwipe(self,startX, startY, endX, endY, duration,curveGenerateAlgo=CurveGenerate.BezierCurve):
        points = curveGenerateAlgo(startX, startY, endX, endY, duration)
        self.swipe(points,duration)
        

    def findAndClick(self,template: Template,result:tuple|list = None,duration = None,randomPointGenerateAlgo=None):
        clickParams = {}
        if result:
            clickParams["result"] = result
        if randomPointGenerateAlgo:
            clickParams["randomPointGenerateAlgo"] = randomPointGenerateAlgo
        if duration:
            clickParams["duration"] = duration
        return self.findAndOperate(template,self.rangeRandomClick,clickParams)