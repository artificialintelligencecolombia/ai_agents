def calculate_average(numbers):
    total = 0
    for num in numbers:
        total += num
    return total / len(numbers)


def get_user_name(user):
    return user["name"].upper()


def add_item(item, items=[]):
    items.append(item)
    return items


def get_last_three(items):
    return [items[i] for i in range(1, 4)]

result = calculate_average([])
print(result)

user = {"username": "dmaldonado"}
print(get_user_name(user))

print(add_item("a"))
print(add_item("b"))

print(get_last_three([10, 20]))
