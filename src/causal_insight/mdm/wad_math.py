SCALE = 10**18  # 1e18 fixed-point


def to_wad(x: float) -> int:
    return int(x * SCALE)


def from_wad(x: int) -> float:
    return x / SCALE


def wad_add(a: int, b: int) -> int:
    return a + b


def wad_sub(a: int, b: int) -> int:
    return a - b


def wad_mul(a: int, b: int) -> int:
    # (a * b) / SCALE
    return (a * b) // SCALE


def wad_div(a: int, b: int) -> int:
    # (a * SCALE) / b
    return (a * SCALE) // b


def wad_avg(a: int, b: int) -> int:
    return (a + b) // 2


def wad_vec_avg(v1, v2):
    return [(x + y) // 2 for x, y in zip(v1, v2)]
