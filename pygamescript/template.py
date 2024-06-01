#!/usr/bin/python
# -*- coding: UTF-8 -*-
from abc import ABC, abstractmethod

from minicv import Images


class Template(ABC):
    """抽象模板类，用于定义模板的基本方法和属性"""

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
    """图像模板类，用于在图像中查找与模板图像相似的区域"""

    def __init__(self, template_path: str, describe: str = None, threshold: float = 0.9, region: list = None,
                 level: int = None) -> None:
        """初始化图像模板

        Args:
            template_path (str): 模板图像的路径
            describe (str, optional): 模板的描述信息. Defaults to None.
            threshold (float, optional): 匹配的相似度阈值. Defaults to 0.9.
            region (list, optional): 匹配的区域范围. Defaults to None.
            level (int, optional): 图像金字塔的层级. Defaults to None.
        """
        self.template_path = template_path
        self.describe = describe or template_path.split("/")[-1].split("\\")[-1].split('.')[0]
        self.template = None
        self.threshold = threshold
        self.region = region
        self.level = level

    def match(self, image):
        """匹配图像与模板的相似度

        Args:
            image (): 需要匹配的图像

        Returns:
            bool: 是否找到匹配区域
        """
        if self.template is None:
            self.template = Images.read(self.template_path)
        return Images.findImage(image, self.template, self.threshold, self.region, self.level)

    def __str__(self) -> str:
        return self.describe


class ImageColorTemplate(ImageTemplate):
    """图像颜色模板类，用于在图像中查找与模板颜色相似的区域"""

    def __init__(self, template_path: str, describe: str = None, threshold: float = 0.9, region: list = None,
                 level: int = None, color_threshold: int = 4) -> None:
        """初始化图像颜色模板

        Args:
            template_path (str): 模板图像的路径
            describe (str, optional): 模板的描述信息. Defaults to None.
            threshold (float, optional): 匹配的相似度阈值. Defaults to 0.9.
            region (list, optional): 匹配的区域范围. Defaults to None.
            level (int, optional): 图像金字塔的层级. Defaults to None.
            color_threshold (int, optional): 颜色相似度的阈值. Defaults to 4.
        """
        super().__init__(template_path, describe, threshold, region, level)
        self.color_threshold = color_threshold

    def match(self, image):
        """匹配图像与模板颜色的相似度

        Args:
            image (): 需要匹配的图像

        Returns:
            bool: 是否找到匹配区域
        """
        if self.template is None:
            self.template = Images.read(self.template_path)
        result = super().match(image)
        if result:
            color = Images.getPixel(self.template, 0, 0)
            x_min, y_min = result[0:2]
            region = [x_min, y_min, x_min + 10, y_min + 10]
            if not Images.findColor(image, color, region, self.color_threshold):
                result = None
        return result

    def __str__(self) -> str:
        return self.describe


class MultiColorsTemplate(Template):
    """多点颜色模板类，用于在图像中查找与多个颜色点相似的区域"""

    def __init__(self, first_color: str, colors: list, describe: str = None, region: list | None = None,
                 threshold: int = 4) -> None:
        """初始化多点颜色模板

        Args:
            first_color (str): 第一个点的颜色值
            colors (list): 包含多个颜色点的列表，每个点为(dx, dy, color)
            describe (str, optional): 模板的描述信息. Defaults to None.
            region (list, optional): 匹配的区域范围. Defaults to None.
            threshold (int, optional): 颜色相似度的阈值. Defaults to 4.
        """
        self.first_color = first_color
        self.colors = colors
        self.region = region
        self.threshold = threshold
        self.describe = describe or first_color

    def match(self, image):
        """匹配图像与模板多个颜色点的相似度

        Args:
            image (): 需要匹配的图像

        Returns:
            bool: 是否找到匹配区域
        """
        return Images.findMultiColors(image, self.first_color, self.colors, self.region, self.threshold)

    def __str__(self) -> str:
        return self.describe
