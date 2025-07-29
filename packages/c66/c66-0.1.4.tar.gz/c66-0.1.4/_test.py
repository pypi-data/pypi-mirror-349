# 範例使用方式
from src.c66 import pp, pps, onpp, offpp

a = 10
b = "hello"
import numpy as np
c = np.array([1, 2, 3])

print("--- 初始狀態 (預設啟用) ---")
pp(a, b)
pps(c)

print("\n--- 關閉打印 ---")
offpp()
pp(a, b) # 這些將不會打印
pps(c)  # 這些將不會打印

print("\n--- 開啟打印 ---")
onpp()
pp(a, b) # 這些將再次打印
pps(c)  # 這些將再次打印

print("\n--- 再次關閉 ---")
offpp()
pp(a + 5, b + " world") # 這些將不會打印