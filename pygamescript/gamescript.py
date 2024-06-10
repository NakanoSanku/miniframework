import functools
import random
import time

import numpy as np
from loguru import logger
from minicv import Images
from minidevice import MiniDevice

from pygamescript.algo import RandomPointGenerate, CurveGenerate
from pygamescript.template import Template


def _performance_test(func):
    """装饰器：测量函数执行时间"""

    @functools.wraps(func)
    def wrapper(self, *args, **kwargs):
        if self.debug:
            start_time = time.time()
            result = func(self, *args, **kwargs)
            end_time = time.time()
            elapsed_time = end_time - start_time
            logger.debug(f"Function {func.__name__} executed in {elapsed_time:.6f} seconds")
            return result
        else:
            return func(self, *args, **kwargs)

    return wrapper


class GameScript:
    debug = False

    def __init__(self, serial=None, screenshot_method=None, touch_method=None, screenshot_timeout=30, debug=False):
        self.__device = MiniDevice(serial, screenshot_method, touch_method, screenshot_timeout)
        self.__current_screenshot = self.screenshot()
        self.debug = debug
        self.debug_result_list = []

    @_performance_test
    def screenshot(self):
        """获取设备的屏幕截图，返回OpenCV格式的图片"""
        raw = self.__device.screenshot_raw()
        data = Images.bytes2opencv(raw)
        return data

    @_performance_test
    def save_screenshot(self, path: str = './screenshot.png'):
        """将屏幕截图保存到指定路径"""
        self.__device.save_screenshot(path)

    @_performance_test
    def find(self, template: Template):
        """在设备屏幕上查找模板

        Args:
            template (Template): 模板对象，可以是ImageTemplate, MultiColorsTemplate或OcrTemplate,ImageColorTemplate

        Returns:
            result: 是否找到匹配的模板
        """
        screenshot = self.screenshot()
        result = template.match(screenshot)
        logger.debug("Find Template:{} Result: {}".format(template, result))
        if self.debug and result:
            self.debug_result_list.append(
                {
                    "template": template,
                    "result": result,
                    "screenshot": screenshot
                })
        return result

    @_performance_test
    def find_and_operate(self, template: Template, operate, operate_params: dict = None):
        """查找模板并在找到时执行操作

        Args:
            template (Template): 模板对象
            operate: 操作函数
            operate_params (dict): 操作函数的参数

        Returns:
            result: 是否找到匹配的模板
        """
        result = self.find(template)
        if result:
            operate_params = operate_params or {}
            operate_params.setdefault("result", result)
            operate(**operate_params)
        return result

    @_performance_test
    def range_random_click(self, result: tuple | list, duration=None,
                           random_point_generate_algo=RandomPointGenerate.normal_distribution):
        """在指定范围内生成随机点击点并点击

        Args:
            result (tuple | list): 点击区域的坐标，可以是(x, y)或(x1, y1, x2, y2)
            duration (int): 点击持续时间，默认为None，即随机生成
            random_point_generate_algo: 随机点生成算法，默认为RandomPointGenerate.normal_distribution

        Raises:
            ValueError: 如果result的格式不正确

        """
        if len(result) == 2:
            x, y = result
        elif len(result) == 4:
            x, y = random_point_generate_algo(result)
        else:
            raise ValueError(f"{result} is No Correct Value")
        if duration is None:
            randomI = round(np.random.normal(0, 30))
            duration = random.randint(200, 350) if randomI > 80 else random.randint(80, 120)
        self.click(x, y, duration)

    @_performance_test
    def curve_swipe(self, start_x, start_y, end_x, end_y, duration, curve_generate_algo=CurveGenerate.bezier_curve):
        """执行曲线滑动操作

        Args:
            start_x (int): 起始点X坐标
            start_y (int): 起始点Y坐标
            end_x (int): 结束点X坐标
            end_y (int): 结束点Y坐标
            duration (int): 滑动持续时间
            curve_generate_algo: 曲线生成算法，默认为CurveGenerate.bezier_curve

        Returns:
            None
        """
        points = curve_generate_algo(start_x, start_y, end_x, end_y, duration)
        self.swipe(points, duration)

    @_performance_test
    def find_and_click(self, template: Template, result: tuple | list = None, duration=None,
                       random_point_generate_algo=None):
        """查找模板并在找到时执行点击操作

        Args:
            template (Template): 模板对象
            result (tuple | list): 点击区域的坐标，可以是(x, y)或(x1, y1, x2, y2)
            duration (int): 点击持续时间，默认为None，即随机生成
            random_point_generate_algo: 随机点生成算法，默认为None

        Returns:
            result: 是否找到匹配的模板
        """
        clickParams = {}
        if result:
            clickParams["result"] = result
        if random_point_generate_algo:
            clickParams["random_point_generate_algo"] = random_point_generate_algo
        if duration:
            clickParams["duration"] = duration
        return self.find_and_operate(template, self.range_random_click, clickParams)

    @_performance_test
    def click(self, x: int, y: int, duration: int = 100):
        self.__device.click(x, y, duration)

    @_performance_test
    def swipe(self, points: list[tuple[int]], duration: int = 300):
        self.__device.swipe(points, duration)


if __name__ == '__main__':
    from minidevice import DroidCast, MiniTouch
    from pygamescript.template import ImageTemplate, ImageColorTemplate

    test = GameScript(serial="127.0.0.1:16384", screenshot_method=DroidCast, touch_method=MiniTouch, debug=True)
    test.find_and_click(ImageTemplate(r"C:\Users\KateT\Desktop\QQ截图20240601161121.png", "测试"))
    time.sleep(0.8)
    test.find(ImageColorTemplate(r"C:\Users\KateT\Desktop\QQ截图20240601161121.png", "测试"))
