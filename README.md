# funclist
Rust inspired method chaining for lists in Python.

Functional programming concepts in Rust allow for the chaining of multiple methods. It also has useful methods for iteration built into iterators as standard. Let's say we want to find the multiple of every pair in the vector, and then only keep those that are multiples of two. For example: 

```rust
pub fn main() {
    let v: Vec<i32> = (0..100).collect();
    let out: Vec<i32> = v
        .windows(2)
        .map(|x| x[0] * x[1])
        .filter(|x| x % 2 == 0)
        .collect();

    println!("{:?}", out);
}
```

Concise - and there's no additional memory allocations. Unfortunately, most python list operations operate inplace and don't allow for chaining. For example, to copy the Rust example:

```python
from itertools import tee

l = list(range(100))

def pairwise(iterable):
    "Util: s -> (s0,s1), (s1,s2), (s2, s3), ..."
    a, b = tee(iterable)
    next(b, None)
    return list(zip(a, b))
  
pairs = pairwise(l)
out = [x * y for x, y in pairs]
final = [i for i in out if i % 2 == 0]
```

This is a slightly naive implementation, and we could remove some of the intermediate allocation:

```python
from itertools import tee

l = list(range(100))

def pairwise(iterable):
    "Util: s -> (s0,s1), (s1,s2), (s2, s3), ..."
    a, b = tee(iterable)
    next(b, None)
    return list(zip(a, b))

out = [
    i for i in [
        x * y for x, y in pairwise(l)
      ] if i % 2 == 0
  ]
```

This is probably the fastest and most efficient way of doing this in Python - but it's completely unreadable. Enter `funclist`.

Let's implement the same function using `funclist`:

```python
from funclist import funclist

out = funclist(range(100)).windows(2).map(lambda x: x[0] * x[1]).filter(lambda x: x % 2 == 0)
```

I find this style easier to read and easier to understand what the intermediate computations are actually doing. Enjoy!