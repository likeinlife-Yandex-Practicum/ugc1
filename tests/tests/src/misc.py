import random
from string import ascii_letters


def generate_string(length: int) -> str:
    return ''.join(random.choices(ascii_letters, k=length))


def generate_resolution_pair() -> tuple:
    from_, to_ = random.choices(['144', '360', '720', '1080'], k=2)

    return from_, to_
