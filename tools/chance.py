import random
def chance(num):
    if random.randint(1, num) == 1:
        return True
    return False