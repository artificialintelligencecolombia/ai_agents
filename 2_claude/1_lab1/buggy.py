def calculate_average(numbers):
    if not numbers:
        return 0.0
    total = 0
    for num in numbers:
        total += num
    return total / len(numbers)


def get_user_name(user):
    name = user.get("name")
    if name is None:
        return ""
    return name.upper()


def add_item(item, items=None):
    if items is None:
        items = []
    items.append(item)
    return items


def get_last_three(items):
    return items[-3:]

result = calculate_average([])
print(result)

user = {"username": "dmaldonado"}
print(get_user_name(user))

print(add_item("a"))
print(add_item("b"))

print(get_last_three([10, 20]))
