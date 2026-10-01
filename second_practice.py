"""Написать класс CycleList, который инициализируется обычным списком."""


class CycleList(list):
    """Кастомный список"""

    def __getitem__(self, index):
        """Переопределение индекса для зацикливания"""
        index = index % len(self)
        return super().__getitem__(index)

    def __iter__(self): # pylint: disable=useless-parent-delegation
        """Явное переопределение для безопасности в PyPy / Jython"""
        return super().__iter__()


# Ожидаемое поведение:
init_items: list = [1, 2, 3]

cl = CycleList(init_items)

print(f"длина cl: {len(cl)}")
print(f"cl[0]: {cl[0]}") # 1
print(f"cl[3]: {cl[3]}") # 1 (пошло по кругу)
print(f"cl[5]: {cl[5]}") # 3

print('---начало цикла---')
for item in cl:
    print(item)
print('---конец цикла---')


print(f"строковое представление: {str(cl)}")

# тесты
assert len(cl) == len(init_items)
assert cl[6] == 1
assert cl[7] != 1

