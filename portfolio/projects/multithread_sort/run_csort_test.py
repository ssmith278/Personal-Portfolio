import sys
import unittest
from run_csort import spawn_and_sort, get_random_arr
from utils.dynamicdict import DynamicDict

class TestRandomGenerator(unittest.TestCase):

    LENGTH_KEY = 'length'    
    RANGE_KEY = 'range'

    VALID_KEY = 'valid'
    INVALID_KEY = 'invalid'

    def common_setup(self):

        self.testing_values = DynamicDict(
            length = DynamicDict(
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
            ),
            range = DynamicDict(
                valid = DynamicDict(
                    minimum=-sys.maxsize,
                    negative_midpoint=-1000,
                    below_zero=-1,
                    zero=0,
                    above_zero=1,
                    midpoint=1000,
                    maximum=sys.maxsize,
                    above_min='minimum + 1',
                    below_max='maximum - 1',
                ),
                invalid= DynamicDict(                                    
                    non_integer='abc',
                    num_list = [1,2],
                    num_tuple = (1,2)
                )
            ),
        )

    def test_length_valid_input(self):

        try:
            self.testing_values
        except AttributeError:
            self.common_setup()

        valid_testing_values = self.testing_values[self.LENGTH_KEY][self.VALID_KEY].values()
        print('Testing length with values: {}'.format(valid_testing_values))
        
        for value in valid_testing_values:

            self.test_arr = get_random_arr(value)
            self.assertEqual(len(self.test_arr), value)

    def test_length_invalid_input(self):

        try:
            self.testing_values
        except AttributeError:
            self.common_setup()

        invalid_testing_values = self.testing_values[self.LENGTH_KEY][self.INVALID_KEY].values()
        print('Testing length with values: {}'.format(invalid_testing_values))    

        for value in invalid_testing_values:
            self.assertRaises(ValueError, get_random_arr, value)            
        

    def test_range_valid_input(self):
        
        try:
            self.testing_values
        except AttributeError:
            self.common_setup()

        valid_testing_values = self.testing_values[self.RANGE_KEY][self.VALID_KEY].values()

        default_length = self.testing_values[self.LENGTH_KEY][self.VALID_KEY]['midpoint']

        for min_value in valid_testing_values:
            for max_value in valid_testing_values:

                if min_value >= max_value:
                    continue

                self.test_arr = get_random_arr(default_length, min_value, max_value)

                # Check all values greater than or equal to min value
                self.assertGreaterEqual(min(self.test_arr), min_value)

                # Check all values less than or equal to max value
                self.assertLessEqual(max(self.test_arr), max_value)


    def test_min(self):
        pass



class TestInputBoundaries(unittest.TestCase):

    def common_setup(self):
        pass

    def test_lower(self):
        pass

if __name__ == '__main__':
    unittest.main()