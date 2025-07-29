# TA-dict

**TA-dict** is a lightweight and fast technical analysis library written in pure Python. It is designed for speed and simplicity, working directly with nested dictionaries — no `pandas`, no `numpy`, and **no C-based dependencies**.

## 🔍 Why TA-dict?

Most technical analysis libraries in Python are built on top of heavy libraries like `pandas` or use C extensions to boost performance. TA-dict takes a different approach:

- 🚀 **Pure Python only** – no external or C-based dependencies
- 🧠 Uses standard nested `dict` structures
- 📈 Designed for speed and minimal memory usage
- 🧩 Easily extensible for new indicators

## 📊 Input Data Format

TA-dict functions operate on data structured as nested dictionaries. For example, a candle dataset should look like this:

```python
data = {
    1: {'date': '2025/06/20', 'Open': 1.0001, 'High': 1.0003, 'Low': 1.0000, 'Close': 1.0002, 'Volume': 1000},
    2: {'date': '2025/06/21', 'Open': 1.0002, 'High': 1.0004, 'Low': 1.0001, 'Close': 1.0003, 'Volume': 1500},
    # ...
}
