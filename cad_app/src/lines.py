from .points import Point
import numpy as np

# 2つのPointインスタンスを結ぶLineクラスを定義
# Lineインスタンスはその長さも計算
class Line:
    def __init__(self, point1, point2):
        self.point1 = point1
        self.point2 = point2
        self.length = self.calculate_length()

    # Lineインスタンスの長さを計算するメソッド
    def calculate_length(self):
        return np.sqrt((self.point1.x - self.point2.x) ** 2 + (self.point1.y - self.point2.y) ** 2)