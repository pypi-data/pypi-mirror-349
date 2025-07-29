from inspect import currentframe, getframeinfo
from ast import parse, unparse

# 控制是否打印的全局變數
_PRINT_ENABLED = True

def offpp():
    """禁用 pp 和 pps 的打印輸出"""
    global _PRINT_ENABLED
    _PRINT_ENABLED = False

def onpp():
    """啟用 pp 和 pps 的打印輸出"""
    global _PRINT_ENABLED
    _PRINT_ENABLED = True

# pp
def pp(*args):
    if not _PRINT_ENABLED:
        return
    
    # 抓呼叫這個函數的那一行程式碼
    frame = currentframe().f_back
    code_context = getframeinfo(frame).code_context
    if not code_context:
        for arg in args:
            print(arg)
        return

    code_line = code_context[0].strip()
    
    try:
        # 解析 AST 拿到呼叫 pp 裡面的參數原始碼
        tree = parse(code_line)
        call = tree.body[0].value  # 假設這行是一個 expression
        arg_sources = [unparse(arg) for arg in call.args]
    except Exception:
        # fallback
        arg_sources = [f'arg{i}' for i in range(len(args))]

    for name, value in zip(arg_sources, args):
        print(f"{name}: {value}")

# pps
def pps(*args):
    if not _PRINT_ENABLED:
        return
    
    # 抓呼叫這個函數的那一行程式碼
    frame = currentframe().f_back
    code_context = getframeinfo(frame).code_context
    if not code_context:
        for arg in args:
            try:
                print(f"{arg.shape}")
            except AttributeError:
                print(f"{arg} has no shape attribute")
        return

    code_line = code_context[0].strip()
    
    try:
        # 解析 AST 拿到呼叫 pps 裡面的參數原始碼
        tree = parse(code_line)
        call = tree.body[0].value  # 假設這行是一個 expression
        arg_sources = [unparse(arg) for arg in call.args]
    except Exception:
        # fallback
        arg_sources = [f'arg{i}' for i in range(len(args))]

    for name, value in zip(arg_sources, args):
        try:
            print(f"{name}'s shape: {value.shape}")
        except AttributeError:
            print(f"{name} has no shape attribute")