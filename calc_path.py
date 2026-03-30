#!/usr/bin/env python

import itertools
from typing import Iterator, Tuple

restriction: dict[str, tuple[str, ...]] = {
    "H": ("P", "C", "G"),
    "P": ("H", "M", "G"),
    "M": ("P", "C", "G"),
    "C": ("H", "M", "G"),
    "G": ("H", "P", "M", "C"),
}

distance: dict[str, float] = {
    "H_P": 50.0,
    "H_C": 80.0,
    "H_G": 40.0,
    "P_M": 68.0,
    "P_G": 28.0,
    "M_C": 92.0,
    "M_G": 58.0,
    "C_G": 70.0,
}


def possible_permutation() -> Iterator[Tuple[str, ...]]:
    letters: tuple[str, ...] = ("H", "P", "M", "C", "G")
    for perm in itertools.permutations(letters):
        if perm[0] == "H" and perm[-1] != "M":
            yield perm


def constrains(route: tuple[str, ...]) -> bool:
    # handle empty list defensively
    if not route:
        return False
    # base case: single element
    if len(route) == 1:
        return True
    first, second = route[0], route[1]
    try:
        allowed_next_hop_for_first = restriction.get(first, ())
        if second in allowed_next_hop_for_first:
            return constrains(route[1:])
        return False
    except Exception as e:
        # convert unexpected errors into a clear ValueError
        raise ValueError("unexpected error while checking constraints") from e


def calculate_distance(route: tuple[str, ...]) -> float:
    accumulator: float = 0.0
    try:
        for count in range(5):
            try:
                value = distance[f"{route[count]}_{route[count + 1]}"]
            except KeyError:
                value = distance[f"{route[count + 1]}_{route[count]}"]
            accumulator += value
    except IndexError:
        # list too short; raise a clearer error
        raise ValueError("mylist must contain at least 6 elements") from None
    return accumulator


def main() -> None:
    routes: list[tuple[*tuple[str, ...]]] = []
    for route in possible_permutation():
        if not constrains(route):
            continue
        routes.append(route + ("H",))

    for route in routes:
        distance = calculate_distance(route)
        print(f"{route}: {distance}")


if __name__ == "__main__":
    main()
