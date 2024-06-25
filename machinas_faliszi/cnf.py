from typing import Self


def parse(input: str) -> 'Cnf':
    n_clauses = 0
    n_variables = 0
    clauses: list[list[int]] = []

    for line in input.split('\n'):
        match line.split():
            case ['c', *_]:
                pass
            
            case ['p', _, str(n), str(m)]:
                n_clauses = int(m)
                n_variables = int(n)

            case list(clause):
                clauses.append([int(x) for x in clause])

    if len(clauses) < n_clauses:
        pass

    return Cnf(n_variables, n_clauses, clauses)


class Cnf:
    n_variables: int
    clauses: list[list[int]]
    values: dict[int, bool]

    def __init__(self, n_variables: int, clauses: list[list[int]]) -> None:
        self.n_variables = n_variables
        self.clauses = clauses
        self.values = dict()

    def value(self, literal: int) -> bool | None:
        value = self.values.get(abs(literal), None)

        if value is None:
            return None

        return value if literal > 0 else not value

    def is_solved(self) -> bool:
        result = True

        for clause in self.clauses:
            clause_value = False

            for literal in clause:
                literal_value = self.value(literal)

                if literal_value is None:
                    return False

                clause_value |= literal_value

            result &= clause_value

        return result

    def set(self, literal: int, value: bool) -> None:
        self.values[abs(literal)] = value

    def unset(self, literal: int) -> None:
        self.values[abs(literal)] = None

    @staticmethod
    def load(path: str) -> Self:
        with open(path, 'r') as file:
            return parse(file.read())

