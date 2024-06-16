from datetime import timedelta

def parse_time(t):
    """
    Converts a time string in the format "hh:mm" to seconds.

    Parameters:
    t (str): The time string to be parsed.

    Returns:
    int: The time in seconds.
    """
    h, m = map(int, t.split(":"))
    return h * 3600 + m * 60


def print_time(t):
    """
    Converts a given time in seconds to a formatted string representation.

    Args:
        t (int): The time in seconds.

    Returns:
        str: The formatted time string in the format "hours:minutes".
    """
    clock = timedelta(seconds=t)
    h, m, s = str(clock).split(":")
    return h + ":" + m
