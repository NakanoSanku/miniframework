
# 图像处理模板类
## 1. 抽象模板类 (Template)
抽象模板类 `Template` 定义了模板的基本方法和属性。它包含三个抽象方法：
- `__init__`: 初始化模板参数。
- `match`: 匹配方法，用于比较模板与目标图像的相似度。
- `__str__`: 返回模板的描述信息。
## 2. 灰度图像模板类 (ImageTemplate)
图像模板类 `ImageTemplate` 继承自 `Template`，用于在图像中查找与模板图像相似的区域。它包含以下属性：
- `template_path`: 模板图像的路径。
- `describe`: 模板的描述信息。
- `threshold`: 匹配的相似度阈值。
- `region`: 匹配的区域范围。
- `level`: 图像金字塔的层级。一般不需要修改。
## 3. 原图像模板类 (ImageColorTemplate)
原图像模板类 `ImageColorTemplate` 继承自 `ImageTemplate`，用于在图像中查找与模板图像相似的区域并且检查图像一个像素点颜色值是否相似。它包含以下额外属性：
- `color_threshold`: 颜色相似度的阈值。
## 4. 多点颜色模板类 (MultiColorsTemplate)
多点颜色模板类 `MultiColorsTemplate` 继承自 `Template`，用于在图像中查找与多个颜色点相似的区域。它包含以下属性：
- `first_color`: 第一个点的颜色值。
- `colors`: 包含多个颜色点的列表，每个点为 (dx, dy, color)。
- `region`: 匹配的区域范围。
- `threshold`: 颜色相似度的阈值。
每个类都提供了 `match` 方法来执行匹配操作，并 `__str__` 方法来返回模板的描述信息。

