import copy
from typing import Iterable

# Dictionary evaluates string values for in-referencing among values
class DynamicDict(dict):

    def __getitem__(self, key):
        value = super(DynamicDict, self).__getitem__(key)
        return eval(value, self) if isinstance(value, str) else value

    def values(self):
        values = list(super(DynamicDict, self).values())

        result = []
        for value in values:
            try:
                result.append(eval(str(value), self))
            except NameError:
                result.append(value)
            except Exception as e:
                print(e)

        return result

def test_dyna_dict():
    testing_values = DynamicDict(
        valid = DynamicDict(
            minimum=0,                
            midpoint=1000,
            maximum=10000000,
            above_min='minimum + 1',
            below_max='maximum - 1',
        ),
        invalid= DynamicDict(
        
            negative=-1,
            non_integer='abc'
        )
    )

    assert testing_values['valid']['minimum'] + 1 == testing_values['valid']['above_min'], "Failed to evaluate dictionary value"

if __name__ == '__main__':
    test_dyna_dict()
