import numpy as np
import matplotlib.pyplot as plt
from scipy.signal import argrelextrema

# 生成随机的 CCI 数据
np.random.seed(0)
data = np.random.randint(-150, 150, size=100)

# 找到极大值和极小值
maxima = argrelextrema(data, np.greater)
minima = argrelextrema(data, np.less)

# 创建图形
fig, ax = plt.subplots()

# 绘制 CCI 数据
ax.plot(data, color='blue')

# 在极大值和极小值处标注 CCI 值
for max in maxima[0]:
    ax.annotate(str(data[max]), (max, data[max]))
for min in minima[0]:
    ax.annotate(str(data[min]), (min, data[min]))

# 在高度为 100，-100 和 0 的位置画出水平线
ax.axhline(100, color='red', linestyle='--')
ax.axhline(-100, color='red', linestyle='--')
ax.axhline(0, color='black', linestyle='-')

# 在这个区间画出背景线框
ax.axhspan(-100, 100, facecolor='green', alpha=0.1)

plt.show()
