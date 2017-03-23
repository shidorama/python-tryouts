import os
from json import load


class Helper():
    def __load_fixtures(self):
        """Loads fixtures from json file with the same name as current test file and puts it into __data property

        :return:
        """
        filename = os.path.abspath(__file__)[:-3]
        try:
            with open('%s.json' % filename, 'r') as fp:
                self.__data = load(fp)
        except IOError:
            self.__data = {}

    def __get_data(self):
        """Provides fixture data for caller method

        :return: fixture data
        :rtype: any
        """
        caller_name = inspect.stack()[1][3]
        if caller_name in self.__data:
            return self.__data[caller_name]
        return {}
