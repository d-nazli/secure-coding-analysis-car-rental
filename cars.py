from database import get_all_cars


def list_cars():
    cars = get_all_cars()
    result = []

    for c in cars:
        if c[4] == 1:
            result.append(c)
        else:
            pass

    return result
