from src.calc.calc import add


def test_add():
    print("Testing add function")
    assert add(1, 2) == 3
    