from functools import wraps
from inspect import getfullargspec
from collections.abc import Iterable

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

            # 增加整数到浮点数的自动扩展
            if isinstance(youmi.get(key), int) and annotations.get(key) == float:
                continue

            assert isinstance(youmi.get(key), annotations.get(key)), f"\n{key} must be {annotations.get(key)}, but got ({youmi.get(key)}, {type(youmi.get(key))})"

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


@paramcheck
def muti_for_simula(lengths: Iterable = []):
    """
    多层 for 循环模拟器，当你无法确定需要动态的生成for循环套用的次数的时候，可以使用它
    :param lengths: 每个index所对应的长度length
    :return: 生成的索引列表
    """
    indexs = [0 for i in lengths]
    lengths = lengths[::-1]

    # 下面的操作将模拟加法的运算过程
    flag = 0        # 进位标志符
    while True:
        for i, item in enumerate(lengths):
            indexs[i] += flag
            # 对于第一个数字，需要单独的处理，因为它需要进行自增
            if i == 0:
                if indexs[i] >= item - 1:
                    if i == len(indexs) - 1:
                        return None

                    flag = 1
                    indexs[i] = -1
                else:
                    flag = 0

            else:
                if indexs[i] >= item:
                    if i == len(indexs) - 1:
                        return None

                    flag = 1
                    indexs[i] = 0
                else:
                    flag = 0

        indexs[0] += 1
        yield list(indexs[::-1])


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

    """
        for循环模拟器
    """
    for item in muti_for_simula([3, 3]):
        print(item)
        # 结果如下：
        #     [0, 1]
        #     [0, 2]
        #     [1, 0]
        #     [1, 1]
        #     [1, 2]
        #     [2, 0]
        #     [2, 1]
        #     [2, 2]
        #




