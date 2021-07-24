import os

def allow_pkgs():
    """
    使用该方法返回包含该文件夹下的所有包的列表
    """
    names = os.listdir(os.path.dirname(os.path.abspath(__file__)))
    pkgs = []

    for name in names:
        if '__init__' in name:
            continue

        if '.py' not in name:
            continue

        pkgs.append(name.replace('.py',''))

    return pkgs


"""
__all__ 变量中包含的所有包会被自动导入
"""
__all__ = allow_pkgs()
