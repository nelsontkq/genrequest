from jsongenerator.jsongenerator import TagReplacer

def test_parse_function_generates_different_every_time():
    x = TagReplacer()
    func = x.parse_function("rand_str(10)")
    assert str(func) != str(func)