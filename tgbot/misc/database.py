from faker import Faker
import random


async def get_users_data():
    fake = Faker()
    Faker.seed(0)

    ids = [num for num in range(1, 101)]
    names = [fake.first_name() for _ in range(100)]
    last_name = [fake.last_name() for _ in range(100)]
    phone_numbers = [fake.phone_number() for _ in range(100)]
    addresses = [fake.address() for _ in range(100)]
    orders_sum = [random.randint(100, 1000) for _ in range(100)]

    return tuple(zip(ids, names, last_name, phone_numbers, addresses, orders_sum))
