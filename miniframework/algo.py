import random

import numpy as np


class CurveGenerate:

    @staticmethod
    def bezier_curve(startX, startY, endX, endY, duration):
        def bezier(screenPoint, offset):
            p0, p1, p2, p3 = screenPoint
            cx = 3 * (p1['x'] - p0['x'])
            bx = 3 * (p2['x'] - p1['x']) - cx
            ax = p3['x'] - p0['x'] - cx - bx
            cy = 3 * (p1['y'] - p0['y'])
            by = 3 * (p2['y'] - p1['y']) - cy
            ay = p3['y'] - p0['y'] - cy - by
            t = np.arange(0, 1, 0.08)  # 使用 numpy 的 arange 函数生成浮点数步长的范围
            tSquared = t * t
            tCubed = tSquared * t
            x = ax * tCubed + bx * tSquared + cx * t + p0['x']
            y = ay * tCubed + by * tSquared + cy * t + p0['y']
            return [(int(px), int(py)) for px, py in zip(x, y)]

        def smlMove(qx, qy, zx, zy):
            slidingPath = []
            point = [
                {'x': qx, 'y': qy},
                {'x': random.randint(qx - 100, qx + 100), 'y': random.randint(qy, qy + 50)},
                {'x': random.randint(zx - 100, zx + 100), 'y': random.randint(zy, zy + 50)},
                {'x': zx, 'y': zy}
            ]
            slidingPath.extend(bezier(point, 0.08))
            return slidingPath

        return smlMove(startX, startY, endX, endY)


class RandomPointGenerate:

    @staticmethod
    def normal_distribution(region):
        """基于正太分布生成随机点

        Args:
            region (list): [xMin, yMin, xMax, yMax]

        Returns:
            point (tuple): (x,y)
        """
        xMin, yMin, xMax, yMax = region
        w = xMax - xMin
        h = yMax - yMin
        centerX = xMin + w / 2
        centerY = yMin + h / 2
        while True:
            x = round(np.random.normal(centerX, w / 6))
            y = round(np.random.normal(centerY, h / 6))
            if xMin <= x <= xMax and yMin <= y <= yMax:
                break
        return x, y
