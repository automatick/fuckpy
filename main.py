from typing import Any, Callable, Iterable, Union

default: str = "default"

class switch:
    def __init__(self, var: Any) -> None:
        self.var = var

    def __rshift__(self, cases: dict[Any, Callable]):
        case = cases.get(self.var, cases.get("default"))
        if case:
            case()
        else:
            print(f"Case {self.var} not found")

class microFor:
    def __init__(self, items: Iterable) -> None:
        self.items = items

    def __lshift__(self, func: Callable[[Any], None]) -> None:
        for item in self.items:
            func(item)


class FPipe:
    def __init__(self, value: Any) -> None:
        self.value = value

    def __or__(self, func: Callable[[Any], Any]) -> "FPipe":
        return FPipe(func(self.value))

    def result(self) -> Any:
        return self.value


class FMath:
    def __init__(self, value: Union[int, float, str]) -> None:
        self.value = value

    def __add__(self, other: Any) -> "FMath":
        if isinstance(self.value, str):
            return FMath(self.value + str(other))
        return FMath(self.value + other)

    def __mul__(self, other: Any) -> "FMath":
        if isinstance(self.value, str):
            return FMath(self.value * other)
        return FMath(self.value * other)

    def __sub__(self, other: Any) -> "FMath":
        if isinstance(self.value, str):
            return FMath(self.value.replace(str(other), ""))
        return FMath(self.value - other)

    def __truediv__(self, other: Any) -> "FMath":
        if isinstance(self.value, str):
            parts = self.value.split(str(other))
            return FMath(parts if len(parts) > 1 else self.value)
        return FMath(self.value / other)

    def __str__(self) -> str:
        return str(self.value)

    def __repr__(self) -> str:
        return f"LazyMath({self.value})"

class CondChain:
    def __init__(self, value: Any) -> None:
        self.value = value
        self.executed = False

    def if_(self, condition: Callable[[Any], bool], action: Callable[[], None]) -> "CondChain":
        if not self.executed and condition(self.value):
            action()
            self.executed = True
        return self

    def elif_(self, condition: Callable[[Any], bool], action: Callable[[], None]) -> "CondChain":
        return self.if_(condition, action)

    def else_(self, action: Callable[[], None]) -> None:
        if not self.executed:
            action()

class BoolExpr:
    def __init__(self, value: bool) -> None:
        self.value = value

    def __and__(self, other: "BoolExpr") -> "BoolExpr":
        return BoolExpr(self.value and other.value)

    def __or__(self, other: "BoolExpr") -> "BoolExpr":
        return BoolExpr(self.value or other.value)

    def __invert__(self) -> "BoolExpr":
        return BoolExpr(not self.value)

    def __xor__(self, other: "BoolExpr") -> "BoolExpr":
        return BoolExpr(self.value ^ other.value)

    def eval(self) -> bool:
        return self.value

    def apply(self, func: Callable[[bool], bool]) -> "BoolExpr":
        return BoolExpr(func(self.value))

    def __str__(self) -> str:
        return f"BoolExpression({self.value})"

    def __repr__(self) -> str:
        return str(self)

class QBuilder:
    def __init__(self):
        self.query = ""

    def select(self, *fields: str) -> "QBuilder":
        self.query += f"SELECT {', '.join(fields)} "
        return self

    def from_(self, table: str) -> "QBuilder":
        self.query += f"FROM {table} "
        return self

    def where(self, condition: str) -> "QBuilder":
        self.query += f"WHERE {condition} "
        return self

    def and_(self, condition: str) -> "QBuilder":
        self.query += f"AND {condition} "
        return self

    def or_(self, condition: str) -> "QBuilder":
        self.query += f"OR {condition} "
        return self

    def order_by(self, field: str, direction: str = "ASC") -> "QBuilder":
        self.query += f"ORDER BY {field} {direction} "
        return self

    def limit(self, n: int) -> "QBuilder":
        self.query += f"LIMIT {n} "
        return self

    def subquery(self, subquery: "QBuilder", alias: str) -> "QBuilder":
        self.query += f"({str(subquery)[:-1]}) AS {alias} "
        return self

    def __str__(self) -> str:
        return self.query.strip() + ";"

    def __repr__(self) -> str:
        return str(self)


class FuncChain:
    def __init__(self, value: Any) -> None:
        self.value = value

    def __or__(self, func: Callable[..., Any]) -> "FuncChain":
        def wrapper(value: Any, *args, **kwargs):
            return func(value, *args, **kwargs)

        return FuncChain(wrapper(self.value))

    def __rshift__(self, func: Callable[..., Any]) -> "FuncChain":
        def wrapper(value: Any, *args, **kwargs):
            return func(value, *args, **kwargs)

        return FuncChain(wrapper(self.value))

    def __str__(self) -> str:
        return str(self.value)

    def __repr__(self) -> str:
        return f"FuncChain({self.value})"

    def result(self) -> Any:
        return self.value

class FEval:
    def __init__(self, func: Callable[[], Any]) -> None:
        self.func = func

    def __add__(self, other: "FEval") -> "FEval":
        return FEval(lambda: self.func() + other.func())

    def __mul__(self, other: "FEval") -> "FEval":
        return FEval(lambda: self.func() * other.func())

    def __sub__(self, other: "FEval") -> "FEval":
        return FEval(lambda: self.func() - other.func())

    def __truediv__(self, other: "FEval") -> "FEval":
        return FEval(lambda: self.func() / other.func())

    def then(self, action: Callable[[Any], Any]) -> "FEval":
        return FEval(lambda: action(self.func()))

    def eval(self) -> Any:
        return self.func()

    def __repr__(self) -> str:
        return f"LazyEval({self.func})"

class State:
    def __init__(self, name: str, action: Callable[[], None]):
        self.name = name
        self.action = action

    def enter(self):
        self.action()


class StateMachine:
    def __init__(self, initial: State) -> None:
        self.current = initial
        self.current.enter()
        self.transitions = {}

    def add_transition(self, from_state: State, to_state: State, action: Callable[[], None]) -> None:
        self.transitions[(from_state.name, to_state.name)] = action

    def __rshift__(self, next_state: State) -> "StateMachine":
        transition = self.transitions.get((self.current.name, next_state.name))
        if transition:
            transition()
        self.current = next_state
        self.current.enter()
        return self

class ReactiveVar:
    def __init__(self, initial_value: Any, on_change: Callable[[Any, Any], None] = None):
        self._value = initial_value
        self._on_change = on_change

    @property
    def value(self) -> Any:
        return self._value

    @value.setter
    def value(self, new_value: Any) -> None:
        old_value = self._value
        self._value = new_value
        if self._on_change:
            self._on_change(old_value, new_value)

    def __add__(self, other: Any) -> "ReactiveVar":
        return ReactiveVar(self._value + other)

    def __sub__(self, other: Any) -> "ReactiveVar":
        return ReactiveVar(self._value - other)

    def __mul__(self, other: Any) -> "ReactiveVar":
        return ReactiveVar(self._value * other)

    def __truediv__(self, other: Any) -> "ReactiveVar":
        return ReactiveVar(self._value / other)

    def bind(self, callback: Callable[[Any, Any], None]) -> None:
        self._on_change = callback

    def __str__(self) -> str:
        return str(self._value)

    def __repr__(self) -> str:
        return f"ReactiveVar({self._value})"

if __name__ == "__main__":
    idk: None = switch(7) >> {
        5: lambda: print("is 5"),
        10: lambda: print("is 10"),
        default: lambda: print("not found")
    }

    idk: None = microFor(range(5)) << (
        lambda x: print(f"hello world {x}")
    )

    idk: None = (
        FPipe(5)
        | (lambda x: x * 2)
        | (lambda x: x + 10)
        | (lambda x: f"Result is: {x}")
    ).result()

    CondChain(10) \
        .if_(lambda v: v < 5, lambda: print("Less than 5")) \
        .elif_(lambda v: v == 10, lambda: print("Equal to 10")) \
        .elif_(lambda v: v > 15, lambda: print("Greater than 15")) \
        .else_(lambda: print("Something else"))

    a = BoolExpr(True)
    b = BoolExpr(False)

    print((a & b).eval())  # False
    print((a | b).eval())  # True
    print((~a).eval())     # False
    print((a ^ b).eval())  # True

    expr = BoolExpr(True) & (BoolExpr(False) | ~BoolExpr(False))
    print(expr.eval())  # True

    expr_with_func = BoolExpr(True).apply(lambda x: not x) & BoolExpr(True)
    print(expr_with_func.eval())

    query = QBuilder() \
        .select("*") \
        .from_("products") \
        .where("price > 1000") \
        .and_("stock > 0") \
        .or_("category = 'electronics'") \
        .order_by("price", "DESC") \
        .limit(10)
    print(query)

    a_eval = FEval(lambda: 10)
    b_eval = FEval(lambda: 20)

    sum_eval = a_eval + b_eval
    product_eval = a_eval * b_eval

    print(sum_eval.eval())  # 30
    print(product_eval.eval())  # 200

    x = 5
    x_eval = FEval(lambda: x * 2)
    x = 10
    print(x_eval.eval())  # 20

    chain_eval = FEval(lambda: 10 + 20).then(lambda result: result * 2)
    print(chain_eval.eval())  # 60
