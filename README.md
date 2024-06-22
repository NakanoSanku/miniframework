# pygamescript 自动化脚本库
## 1. 简介
pygamescript是一个用于自动化游戏的Python库，它提供了多种功能，如屏幕截图、模板匹配、随机点击、曲线滑动等。这个库可以与minicv和minidevice库结合使用，以实现更复杂的自动化任务。
## 2. 安装
首先需要安装[minicv](https://github.com/NakanoSanku/minicv)和[minidevice](https://github.com/NakanoSanku/minidevice)库,再安装[pygamescript]()：
```bash
pip install minicv mindeivce 
```
```bash
pip install miniframework
```
## 3. 类和方法
### 3.1  Instance类
- **属性**:
  - `debug`: 布尔值，用于控制是否打印调试信息。
  - `debug_result_list`: 列表，用于存储调试结果。
- **构造函数**:
  - `__init__(self, serial=None, screenshot_method=None, touch_method=None, screenshot_timeout=30, debug=False)`: 初始化GameScript对象，设置设备连接参数和调试模式。
    - serial: 设备的序列号，用于连接设备。当使用minidevice内置方案时，并且screenshot_method, touch_method存在不是实例的时候
    - screenshot_method 基于[minidevice](https://github.com/NakanoSanku/minidevice)的截图方法，可以是实例,当使用minidevice内置方案时，可以直接传入截图类
    - touch_method 基于[minidevice](https://github.com/NakanoSanku/minidevice)的触控方法，可以是实例,当使用minidevice内置方案时，可以直接传入触控类
    - debug: 布尔值，用于控制是否打印调试信息。调试信息包括各种方法的耗时信息。find方法的结果信息是否存储到debug_result_list中。
- **方法**:
  - **基础方法**
    - `screenshot(self)`: 获取设备的屏幕截图，返回OpenCV格式的图片。
    - `click(self, x, y, duration)`: 执行点击操作。
    - `swipe(self, points, duration)`: 执行滑动操作。
    - `save_screenshot(self, path: str = './screenshot.png')`: 将屏幕截图保存到指定路径。
  - **基于[防封策略](miniframework/algo.py)的操作方法**
    - `range_random_click(self, result: tuple | list, duration=None, random_point_generate_algo=RandomPointGenerate.normal_distribution)`: 在指定范围内生成随机点击点并点击。
    - `curve_swipe(self, start_x, start_y, end_x, end_y, duration, curve_generate_algo=CurveGenerate.bezier_curve)`: 执行曲线滑动操作。
  - **基于[Template](#32-template类)的方法**
    - `find(self, template: Template)`: 在设备屏幕上查找模板，返回是否找到匹配的模板。
    - `find_and_operate(self, template: Template, operate, operate_params: dict = None)`: 查找模板并在找到时执行操作。
    - `find_and_click(self, template: Template, result: tuple | list = None, duration=None, random_point_generate_algo=None)`: 查找模板并在找到时执行点击操作。

### 3.2 Template类
模板类用于描述模板图像，包括模板图像路径、模板名称和匹配模式

[Template类说明文档](docs/template.md)
- `Template` 抽象类
  - `ImageTemplate` 灰度图像模板类
  - `ImageColorTemplate` 原图像模板类
  - `MultiColorTemplate` 多点找色模板类

## 4. 示例
以下是一个简单的示例，展示了如何使用GameScript库进行屏幕截图和模板匹配：

```python
from minidevice import DroidCast, MiniTouch
from miniframework.template import ImageTemplate
from miniframework.GameScript import GameScript

test = GameScript(serial="127.0.0.1:16384", screenshot_method=DroidCast, touch_method=MiniTouch, debug=True)
test.find_and_click(ImageTemplate(r"C:\Users\KateT\Desktop\QQ截图20240601161121.png", "测试"))
time.sleep(0.8)
test.find(ImageTemplate(r"C:\Users\KateT\Desktop\QQ截图20240601161121.png", "测试"))
```
这个示例首先创建了一个GameScript对象，然后使用`find_and_click`方法查找并点击一个模板。之后，使用`find`方法再次查找该模板。
## 5. 注意事项

