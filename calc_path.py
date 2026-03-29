#!/usr/bin/env python

import itertools
from typing import Iterator, Tuple

restriction: dict = {
    "H": ["P", "C", "G"],
    "P": ["H", "M", "G"],
    "M": ["P", "C", "G"],
    "C": ["H", "M", "G"],
    "G": ["H", "P", "M", "C"],
}

distance: dict = {
    "H_P": 50,
    "H_C": 80,
    "H_G": 40,
    "P_M": 68,
    "P_G": 28,
    "M_C": 92,
    "M_G": 58,
    "C_G": 70,
}


def possible_permutation() -> Iterator[Tuple[str, ...]]:
    letters = ("H", "P", "M", "C", "G")
    for perm in itertools.permutations(letters):
        if perm[0] == "H":
            yield perm


def constrains(mylist: list[tuple]) -> bool:
    # handle empty list defensively
    if not mylist:
        return False
    # base case: single element
    if len(mylist) == 1:
        return True
    first, second = mylist[0], mylist[1]
    try:
        allowed = restriction.get(first, ())
        if second in allowed:
            return constrains(mylist[1:])
        return False
    except Exception as e:
        # convert unexpected errors into a clear ValueError
        raise ValueError("unexpected error while checking constraints") from e


def calculate_distance(mylist: list[tuple]) -> float:
    mydistance = 0.0
    try:
        for count in range(5):
            try:
                value = distance[f"{mylist[count]}_{mylist[count + 1]}"]
            except KeyError:
                value = distance[f"{mylist[count + 1]}_{mylist[count]}"]
            mydistance += value
    except IndexError:
        # list too short; raise a clearer error
        raise ValueError("mylist must contain at least 6 elements") from None
    return mydistance


def main() -> None:
    results = []
    for perm in possible_permutation():
        if not constrains(perm) or perm[-1] == "M":
            continue
        results.append(perm + ("H",))

    for item in results:
        distance = calculate_distance(item)
        print(f"{item}: {distance}")


if __name__ == "__main__":
    main()
