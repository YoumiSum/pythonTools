from functools import wraps
from inspect import getfullargspec


def paramcheck(func):
    @wraps(func)
    def inner(*args, **kwargs):
        func_args = getfullargspec(func)
        youmi = dict(kwargs)
        youmi.update({func_args[0][index]: args[index] for index in range(len(args))})

        annotations = dict(func_args[-1])
        for key in annotations.keys():
            if key == "return":
                continue
            if youmi.get(key) is None:
                continue

            assert isinstance(youmi.get(key), annotations.get(key)), f"\n{key} must be {annotations.get(key)}, but get ({youmi.get(key)}, {type(youmi.get(key))})"

        del youmi
        del annotations

        return func(*args, **kwargs)

    return inner


def deserted(func):

    @wraps(func)
    def inner(*args, **kwargs):
        print(f"\033[1;31mWARNING: this function({str(func).split(' ')[1]}) will be delete in future\033[0m")
        return func(*args, **kwargs)
    return inner


if __name__ == '__main__':
    """
        使用示例：如下列所示：self和right都没有进行校验，因为其没有加 :类型
            而其余有加的都会进行验证
    """
    class Test(object):

        @paramcheck
        def __init__(self, name: str = None, left: float = -1.0, right=-1.0):
            print(left)
            print(right)

        @deserted
        def del_test(self):
            print("AA")


