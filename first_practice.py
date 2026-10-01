"""
    Написать выражение (one-liner, используя list comprehension),
    которое вернет список имен (только имена) тех пользователей, 
    которым 18 лет и больше, и у которых обязательно указан email. 
    Если возраст не указан, считаем, что пользователь несовершеннолетний.
"""

users: list[dict] = [
    {"name": "Alice", "age": 25, "email": "alice@example.com"},
    {"name": "Bob", "age": 17},
    {"name": "Charlie", "age": 30, "email": "charlie@example.com"},
    {"name": "David", "email": "david@example.com"}
]

result: list = [
    user["name"] for user in users
    if user.get("age", 0) >= 18
    and "email" in user
]

print(result)

#tests
assert "Charlie" in result
assert "Bob" not in result
