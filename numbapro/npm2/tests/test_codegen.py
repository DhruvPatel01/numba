import dis
import itertools
from pprint import pprint
from numbapro.npm2.symbolic import SymbolicExecution
from numbapro.npm2.typing import Infer
from numbapro.npm2 import types, functions
from numbapro.npm2.codegen import CodeGen, ImpLib
from numbapro.npm2.compiler import compile
from .support import testcase, main


def foo(a, b):
    sum = a
    for i in range(b):
        sum += i
        i = 132
        i = 321
    return sum

@testcase
def test_codegen():
    dis.dis(foo)
    se = SymbolicExecution(foo)
    se.interpret()

    for blk in se.blocks:
        print blk

    funclib = functions.get_builtin_function_library()

    args = {'a': types.int32, 'b': types.int32}
    return_type = types.int32

    infer = Infer(func = se.func,
                  blocks = se.blocks,
                  args = args,
                  return_type = return_type,
                  funclib = funclib)
    infer.infer()

    for blk in se.blocks:
        print blk


    implib = ImpLib(funclib)
    implib.populate_builtin()

    cg = CodeGen(func = se.func,
                 blocks = se.blocks,
                 args = args,
                 return_type = return_type,
                 implib = implib)

    cg.codegen()

    print cg.lmod

@testcase
def test_compile():
    cfoo = compile(foo, types.int32, [types.int32, types.int32])
    print foo(12, 32)
    print cfoo(12, 32)

if __name__ == '__main__':
    main()
