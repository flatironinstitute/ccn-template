""""Hello World!" python function
"""


def hello_world_func(word):
    """
    Prints a greeting message with the specified word.

    Parameters
    ----------
    word : str
        The word to include in the greeting message.

    Returns
    -------
    None
        This function doesn't return anything.

    """
    print(f"Hello {word}!")
    return


if __name__ == "__main__":
    hello_world_func("World")
