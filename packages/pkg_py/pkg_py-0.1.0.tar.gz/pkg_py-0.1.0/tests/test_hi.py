from pkg_py.hi import say_hello

def test_hi_no_name():
    assert say_hello() == "Hello Bro !"

def test_hi_with_name():
    assert say_hello("John") == "Hello John"