from .points import Point
import numpy as np

# 2つのPointインスタンスを結ぶLineクラスを定義
# Lineインスタンスはその長さも計算
class Line:
    def __init__(self, p1, p2):
        self.p1 = p1
        self.p2 = p2
        self.length = self.calculate_length()

    # Lineインスタンスの長さを計算するメソッド
    def calculate_length(self):
        return np.sqrt((self.p1.x - self.p2.x) ** 2 + (self.p1.y - self.p2.y) ** 2)