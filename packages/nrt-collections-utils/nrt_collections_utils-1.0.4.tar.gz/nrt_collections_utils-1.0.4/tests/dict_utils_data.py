

get_value_data = [
    ({'a': 1}, 'a', None, 1),
    ({'a': 1}, ['a'], None, 1),
    ({'a': 1}, ['a', 'b'], None, None),
    ({'a': 1}, ['a', 'b'], 'Test', 'Test'),
    ({'a': {'b': 4}}, ['a', 'b'], None, 4),
    ({'a': {'b': [1, 2]}}, ['a', 'b'], None, [1, 2]),
    ({'a': {'b': [1, 2]}}, ['a', 'b', 'c'], None, None),
]
