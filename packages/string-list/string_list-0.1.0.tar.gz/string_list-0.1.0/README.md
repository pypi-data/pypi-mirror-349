# string-list

**Tiny but powerful string <-> list manipulation utilities for Python.**

`string-list` is a lightweight Python package designed to help you quickly and cleanly convert between strings, lists, sets, and more. It’s perfect for handling user input, CSV-style values, or transforming semi-structured data with minimal fuss.

---

## ✨ Features

* ✅ Cleanly split strings into lists (with optional whitespace trimming)
* ✅ Join lists/sets into delimited strings (with optional quoting)
* ✅ Handle unknown input types (`str`, `int`, `list`) and normalize them
* ✅ Case-insensitive set merging with capitalization preference
* ✅ Dictionary enumeration with string keys for config-friendly output

---

## 📦 Installation

```bash
pip install string-list
```

> Then in your Python code:

```python
from string_list import list_from_string
```

---

## 🔧 Usage Examples

### 📌 `list_from_string()`

Split a string into a list with optional trimming:

```python
from string_list import list_from_string

list_from_string("a,b,c")                    # ['a', 'b', 'c']
list_from_string(" a , b , c ", strip=True)  # ['a', 'b', 'c']
list_from_string("1|2|3", delim="|")         # ['1', '2', '3']
```

---

### 📌 `string_from_list()`

Join a list or set into a string:

```python
from string_list import string_from_list

string_from_list(['a', 'b', 'c'])                     # "a,b,c"
string_from_list({'x', 'y'}, quoted=True)             # "'x','y'"
string_from_list([1, 2, 3], delim='|')                # "1|2|3"
string_from_list(['x', None, 'y'])                    # "x,y"
```

---

### 📌 `list_from_any()`

Convert a `str`, `int`, or `list` into a list of strings or integers:

```python
from string_list import list_from_any

list_from_any("10,20,30", return_items_as_int=True)  # [10, 20, 30]
list_from_any(123)                                   # ['123']
list_from_any(['1', '2'])                            # ['1', '2']
```

---

### 📌 `case_insensitive_update()`

Merge two sets while ensuring case-insensitive uniqueness and preferring title-case:

```python
from string_list import case_insensitive_update

base = {"Film", "Movie"}
new = {"film", "Cinema"}
case_insensitive_update(base, new)  # {'Film', 'Movie', 'Cinema'}
```

---

### 📌 `str_enumerate()`

Enumerate any string/list into a dictionary with **string keys** (great for config files or JSON):

```python
from string_list import str_enumerate

str_enumerate("apple,banana", start=1)
# {'1': 'apple', '2': 'banana'}

str_enumerate(["x", "y"])
# {'0': 'x', '1': 'y'}
```

---

## 🧪 Running Tests

If cloning the repo locally:

```bash
pip install -r requirements-dev.txt
pytest tests/
```

---

## 📝 License

MIT Licensed – free to use, share, and modify.

---

## 🙌 Contributing

If you have improvements or new utility functions to add, feel free to open a pull request!
