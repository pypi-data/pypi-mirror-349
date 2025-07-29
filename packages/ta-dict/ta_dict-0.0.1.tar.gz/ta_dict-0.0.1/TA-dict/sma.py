# ta_dict/ma.py

def simple_moving_average(data, period):
    """Compute the simple moving average (SMA).

    Args:
        data (list or iterable): A sequence of prices (floats or ints).
        period (int): Number of periods to average over.

    Returns:
        list: SMA values. The first (period - 1) values will be None.
    """
    if period < 1:
        raise ValueError("Period must be a positive integer.")
    if len(data) < period:
        return [None] * len(data)
    
    sma = [None] * (period - 1)
    for i in range(period - 1, len(data)):
        window = data[i - period + 1:i + 1]
        sma.append(sum(window) / period)
    return sma
