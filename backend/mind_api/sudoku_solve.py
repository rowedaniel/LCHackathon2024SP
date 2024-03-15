from sqlalchemy.orm import Session

from .crud import (get_all_elements, get_all_possible_products,
                   get_operation_by_parents)
from .schemas import Element


def check_table(table: list[list[list[int]]]) -> bool:
    n = len(table)

    # check rows
    for c in range(n):
        row = [table[r][c] for r in range(n)]
        if [] in row:
            # no possibilities
            return False
        row_trim = [elem[0] for elem in row if len(elem) == 1]
        if len(set(row_trim)) != len(row_trim):
            # repeated element
            return False

    # check cols
    for r in range(n):
        col = [table[r][c] for c in range(n)]
        if [] in col:
            # no possibilities
            return False
        col_trim = [elem[0] for elem in row if len(elem) == 1]
        if len(set(col_trim)) != len(row_trim):
            # repeated element
            return False

    return True


def reduce_table(table: list[list[list[int]]], identity: int) -> bool:
    """reduce product table of a group in-place"""
    n = len(table)

    changed = False

    # make sure group rules hold
    for a in range(n):
        for b in range(n):
            # uniqueness of inverses
            if len(table[a][b]) == 1 or len(table[b][a]) == 1:
                if table[a][b] == [identity] or table[b][a] == [identity]:
                    entry_1 = table[a][b]
                    entry_2 = table[b][a]
                    intersection = list(set(entry_1).intersection(set(entry_2)))

                    if len(intersection) < len(entry_1) or len(intersection) < len(
                        entry_2
                    ):
                        changed = True

                    table[a][b] = intersection
                    table[b][a] = intersection



            for c in range(n):

                # associativity
                if len(table[a][b]) == 1 and len(table[b][c]) == 1:
                    ab = table[a][b][0]
                    bc = table[b][c][0]

                    entry_1 = table[ab][c]
                    entry_2 = table[a][bc]
                    intersection = list(set(entry_1).intersection(set(entry_2)))

                    if len(intersection) < len(entry_1) or len(intersection) < len(
                        entry_2
                    ):
                        changed = True

                    table[ab][c] = intersection
                    table[a][bc] = intersection

                # uniqueness of identity
                if (
                    len(table[b][c]) == 1
                    and len(table[a][table[b][c][0]]) == 1
                    and table[a][table[b][c][0]][0] == c
                ) or (
                    len(table[a][b]) == 1
                    and len(table[table[a][b][0]][c]) == 1
                    and table[table[a][b][0]][c][0] == c
                ):
                    # abc=c -> ab=e
                    entry_1 = table[a][b]
                    entry_2 = [identity]
                    intersection = list(set(entry_1).intersection(set(entry_2)))

                    if len(intersection) < len(entry_1) or len(intersection) < len(
                        entry_2
                    ):
                        changed = True

                    table[a][b] = intersection

                if (
                    len(table[b][c]) == 1
                    and len(table[a][table[b][c][0]]) == 1
                    and table[a][table[b][c][0]][0] == a
                ) or (
                    len(table[a][b]) == 1
                    and len(table[table[a][b][0]][c]) == 1
                    and table[table[a][b][0]][c][0] == a
                ):
                    # abc=a -> bc=e
                    entry_1 = table[b][c]
                    entry_2 = [identity]
                    intersection = list(set(entry_1).intersection(set(entry_2)))

                    if len(intersection) < len(entry_1) or len(intersection) < len(
                        entry_2
                    ):
                        changed = True

                    table[b][c] = intersection

    # make sure sudoku rules are followed
    for r in range(n):
        for c in range(n):
            if len(table[r][c]) != 1:
                continue
            singleton = table[r][c][0]

            for r2 in range(n):
                if r2 == r:
                    continue
                row = [elem for elem in table[r2][c]]
                table[r2][c] = [elem for elem in row if elem != singleton]
                if len(row) > len(table[r2][c]):
                    changed = True

            for c2 in range(n):
                if c2 == c:
                    continue
                col = [elem for elem in table[r][c2]]
                table[r][c2] = [elem for elem in col if elem != singleton]
                if len(col) > len(table[r][c2]):
                    changed = True
    return changed


def construct_table(db: Session, elements: list[Element]) -> list[list[list[int]]]:
    table = [[[] for _ in elements] for _ in elements]
    for row, left in enumerate(elements):
        for col, right in enumerate(elements):
            possible_products = [
                elem.id for elem in get_all_possible_products(db, left.id, right.id)
            ]

            table[row][col] = [
                i for i, elem in enumerate(elements) if elem.id in possible_products
            ]

            # no possible new products
            if len(table[row][col]) == 0:
                # check for existing products
                prod = get_operation_by_parents(db, left.id, right.id)
                if prod is not None:
                    table[row][col] = [
                        i for i, elem in enumerate(elements) if elem.id == prod.child
                    ]
    return table


def copy_table(table: list[list[list[int]]]) -> list[list[list[int]]]:
    return [[[elem for elem in col] for col in row] for row in table]


def verify_table_options(
    db: Session,
    table: list[list[list[int]]],
    elements: list[Element],
    parent_left: int,
    parent_right: int,
) -> tuple[list[int], list[list[list[int]]]]:

    table_orig = table
    good_options = []
    good_tables = []

    lefts = [i for i, elem in enumerate(elements) if elem.id == parent_left]
    rights = [i for i, elem in enumerate(elements) if elem.id == parent_right]
    identities = [i for i, elem in enumerate(elements) if elem.order == 1]
    if len(lefts) != 1 or len(rights) != 1 or len(identities) != 1:
        return []
    row = lefts[0]
    col = rights[0]
    identity = identities[0]

    for i in table_orig[row][col]:
        good = True

        table = copy_table(table_orig)
        table[row][col] = [i]

        while reduce_table(table, identity):
            if not check_table(table):
                good = False
                break
        if good:
            good_options.append(i)
            good_tables.append(table)
    return good_options, good_tables
