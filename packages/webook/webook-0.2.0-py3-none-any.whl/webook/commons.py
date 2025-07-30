def in_groups(arr: list, n: int) -> list[list]:
    return [arr[i::n] for i in range(n)]