---

# **FuckPy**

A fun, expressive, and experimental Python framework designed to push the boundaries of the language with unique syntax and functionality through operator overloading and creative abstractions.

## **Features**

- **`switch`**: Minimalistic switch-case functionality using `>>`.
- **`microFor`**: An alternative to `for` loops using `<<`.
- **`FPipe`**: A functional pipeline operator (`|`) for chaining transformations.
- **`FMath`**: Flexible math operations that adapt to numbers and strings.
- **`CondChain`**: Conditional chains with `if_`, `elif_`, and `else_`.
- **`BoolExpr`**: Object-based Boolean algebra for expressive logical expressions.
- **`QBuilder`**: An SQL query builder with Pythonic chaining.
- **`FuncChain`**: Functional chains with both `|` and `>>`.
- **`FEval`**: Lazy evaluations with chained computations.
- **`StateMachine`**: State management with `>>` transitions.
- **`ReactiveVar`**: Reactive programming with variable watchers.

---

## **Installation**

1. Clone the repository:
   ```bash
   git clone https://github.com/automatick/fuckpy.git
   ```
2. Navigate to the project directory:
   ```bash
   cd fuckpy
   ```
3. Install the required dependencies (if any).

---

## **Quick Examples**

### **Switch-Case**
```python
from main import switch, default

switch(7) >> {
    5: lambda: print("is 5"),
    10: lambda: print("is 10"),
    default: lambda: print("not found"),
}
```

---

### **Pipeline**
```python
from main import FPipe

result = (
    FPipe(5)
    | (lambda x: x * 2)
    | (lambda x: x + 10)
    | (lambda x: f"Result is: {x}")
).result()

print(result)  # Result is: 20
```

---

### **Query Builder**
```python
from main import QBuilder

query = (
    QBuilder()
    .select("*")
    .from_("products")
    .where("price > 1000")
    .and_("stock > 0")
    .or_("category = 'electronics'")
    .order_by("price", "DESC")
    .limit(10)
)

print(query)  # SELECT * FROM products WHERE price > 1000 AND stock > 0 OR category = 'electronics' ORDER BY price DESC LIMIT 10;
```

---

### **State Machine**
```python
from main import State, StateMachine

idle = State("idle", lambda: print("Entering idle state."))
working = State("working", lambda: print("Entering working state."))

machine = StateMachine(idle) >> working
```

---

## **Why FuckPy?**

**FuckPy** is not just a library—it's a playground for experimenting with Python's advanced features like operator overloading, functional programming, and DSL creation. While it might not be suited for production, it offers a creative space for developers to explore and learn.

---

## **Contributing**

Feel free to fork the project, create pull requests, or suggest features. This is a community-driven project for Python enthusiasts!

---

## **License**

MIT License. See `LICENSE` file for details.

---
