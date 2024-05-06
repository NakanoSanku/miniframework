#!/usr/bin/python
# -*- coding: UTF-8 -*-
from abc import ABC, abstractmethod

from minicv import Images


class Template(ABC):

    @abstractmethod
    def __init__(self) -> None:
        """模板参数"""

    @abstractmethod
    def match(self, image):
        """匹配方法"""

    @abstractmethod
    def __str__(self) -> str:
        """模板描述"""


class ImageTemplate(Template):
    def __init__(self, templatePath: str, describe: str = None, threshold: float = 0.9, region: list = None,
                 level: int = None) -> None:
        """找图模板

        Args:
            templatePath (str): 模板图片路径
            describe (str, optional): 描述信息. Defaults to None.
            threshold (float, optional): 图片相似度. Defaults to 0.9.
            region (list, optional): 找图范围. Defaults to None.
            level (int, optional): 图像金字塔等阶. Defaults to None.
        """
        self.templatePath = templatePath
        self.describe = describe or templatePath.split("/")[-1].split("\\")[-1].split('.')[0]
        self.template = Images.read(templatePath, 0)
        self.threshold = threshold
        self.region = region
        self.level = level

    def match(self, image):
        """灰度匹配"""
        return Images.findImage(image, self.template, self.threshold, self.region, self.level)

    def match_color(self, image, colorThreshold: int = 4):
        """原图匹配"""
        result = self.match(image)
        if result:
            color = Images.getPixel(self.template, 0, 0)
            x_min, y_min = result[0:2]
            region = [x_min, y_min, x_min + 10, y_min + 10]
            if not Images.findColor(image, color, region, colorThreshold):
                result = None
        return result

    def __str__(self) -> str:
        return self.describe


class MultiColorsTemplate(Template):
    def __init__(self, firstColor: str, colors: list, describe: str = None, region: list | None = None,
                 threshold: int = 4) -> None:
        """多点找色模板

        Args:
            firstColor (str): 第一个点颜色值
            colors (list): [(dx,dy,color)]
            describe (str, optional): 描述. Defaults to None.
            region (list | None, optional): 找色范围. Defaults to None.
            threshold (int, optional): 颜色相似度. Defaults to 4.
        """
        self.firstColor = firstColor
        self.colors = colors
        self.region = region
        self.threshold = threshold
        self.describe = describe or firstColor

    def match(self, image):
        return Images.findMultiColors(image, self.firstColor, self.colors, self.region, self.threshold)

    def __str__(self) -> str:
        return self.describe
