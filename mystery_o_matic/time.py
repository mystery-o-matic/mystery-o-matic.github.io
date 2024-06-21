from datetime import timedelta

class Time:
    seconds = 0
    def __parse_time(self, t):
        """
        Converts a time string in the format "hh:mm" to seconds.

        Parameters:
        t (str): The time string to be parsed.

        Returns:
        int: The time in seconds.
        """
        h, m = map(int, t.split(":"))
        return h * 3600 + m * 60

    def __init__(self, time):
        if isinstance(time, int):
            self.seconds = time
        elif isinstance(time, str):
            self.seconds = self.__parse_time(time)
        else:
            print(time, type(time))
            raise ValueError("Invalid time format")

    def __print_time(self, t):
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

    def __str__(self):
        return self.__print_time(self.seconds)