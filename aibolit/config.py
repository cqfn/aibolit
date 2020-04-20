from aibolit.metrics.entropy.entropy import Entropy as M1
from aibolit.metrics.ncss.ncss import NCSSMetric as M2
from aibolit.metrics.spaces.SpaceCounter import IndentationCounter as M3
from aibolit.patterns.assert_in_code.assert_in_code import AssertInCode as P1
from aibolit.patterns.classic_setter.classic_setter import ClassicSetter as P2
from aibolit.patterns.empty_rethrow.empty_rethrow import EmptyRethrow as P3
from aibolit.patterns.er_class.er_class import ErClass as P4
from aibolit.patterns.force_type_casting_finder.force_type_casting_finder import ForceTypeCastingFinder as P5
from aibolit.patterns.if_return_if_detection.if_detection import CountIfReturn as P6
from aibolit.patterns.implements_multi.implements_multi import ImplementsMultiFinder as P7
from aibolit.patterns.instanceof.instance_of import InstanceOf
from aibolit.patterns.many_primary_ctors.many_primary_ctors import ManyPrimaryCtors
from aibolit.patterns.method_chaining.method_chaining import MethodChainFind
from aibolit.patterns.multiple_try.multiple_try import MultipleTry
from aibolit.patterns.non_final_attribute.non_final_attribute import NonFinalAttribute
from aibolit.patterns.null_check.null_check import NullCheck
from aibolit.patterns.partial_synchronized.partial_synchronized import PartialSync
from aibolit.patterns.redundant_catch.redundant_catch import RedundantCatch
from aibolit.patterns.return_null.return_null import ReturnNull
from aibolit.patterns.string_concat.string_concat import StringConcatFinder
from aibolit.patterns.supermethod.supermethod import SuperMethod
from aibolit.patterns.this_finder.this_finder import ThisFinder
from aibolit.patterns.var_decl_diff.var_decl_diff import VarDeclarationDistance
from aibolit.patterns.var_middle.var_middle import VarMiddle


CONFIG = {
    "patterns": [
        {"name": "Asserts", "code": "P1", "make": lambda: P1()},
        {"name": "Setters", "code": "P2", "make": lambda: P2()},
        {"name": "Empty Rethrow", "code": "P3", "make": lambda: P3()},
        {"name": "Prohibited class name", "code": "P4", "make": lambda: P4()},
        {"name": "Force Type Casting Finder", "code": "P5", "make": lambda: P5()},
        {"name": "Count If Return", "code": "P6", "make": lambda: P6()},
        {"name": "Implements Multi Finder", "code": "P7", "make": lambda: P7()},
    ],
    "metrics": [
        {"name": "Entropy", "code": "M1", "make": lambda: M1()},
        {"name": "NCSS", "code": "M2", "make": lambda: M2()},
        {"name": "Indentation counter: Right total variance", "code": "M3", "make": lambda: M3(right_var=True)},
        {"name": "Indentation counter: Left total variance", "code": "P7", "make": lambda: M3(left_var=True)},
        {"name": "Indentation counter: Right max variance", "code": "P7", "make": lambda: M3(max_right=True)},
        {"name": "Indentation counter: Left max variance", "code": "P7", "make": lambda: M3(max_left=True)},
    ],
    "target": {

    }
}
