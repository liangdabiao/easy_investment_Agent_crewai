import akshare as ak
import inspect

# 查找所有与板块相关的函数
funcs = []
for name, obj in inspect.getmembers(ak):
    if inspect.isfunction(obj) and ('sector' in name or '板块' in name):
        funcs.append(name)

print('可用的板块相关函数:', funcs)

# 特别检查是否有与同花顺板块相关的函数
ths_funcs = []
for name, obj in inspect.getmembers(ak):
    if inspect.isfunction(obj) and ('ths' in name):
        ths_funcs.append(name)

print('可用的同花顺相关函数:', ths_funcs)