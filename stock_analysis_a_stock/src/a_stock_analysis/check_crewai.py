import crewai
print('BaseTool' in dir(crewai))
print(dir(crewai))

try:
    # 尝试从不同位置导入BaseTool
    from crewai import BaseTool
    print("成功从crewai导入BaseTool")
except ImportError:
    try:
        from crewai.tools import BaseTool
        print("成功从crewai.tools导入BaseTool")
    except ImportError:
        try:
            from crewai.utilities import BaseTool
            print("成功从crewai.utilities导入BaseTool")
        except ImportError:
            print("无法导入BaseTool")

# 查看crewai的子模块
try:
    import pkgutil
    print("crewai的子模块:")
    for _, name, _ in pkgutil.iter_modules(crewai.__path__):
        print(f"- {name}")
except Exception as e:
    print(f"获取子模块时出错: {e}")