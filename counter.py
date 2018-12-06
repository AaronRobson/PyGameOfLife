#!/usr/bin/python


class Counter():
    def __init__(self, startNum=None):
        self.Reset(startNum)

    def Reset(self, startNum=None):
        if startNum is None:
            startNum = 0

        self._value = int(startNum)

    def Inc(self):
        self._value += 1

    @property
    def value(self):
        return self._value

    def __call__(self):
        return self.value

    def __int__(self):
        return self.value

    def __str__(self):
        return str(self.value)

    def __repr__(self):
        return '%s(%d)' % (self.__class__.__name__, self.value)


if __name__ == "__main__":
    print('"Counter" support unit.')
    input('\nPress Enter to Close:')
