import copy


class Counter:
    def __init__(self, start_state):
        self.state = start_state

    def get(self):
        result = copy.deepcopy(self.state)

        temp = bytearray(self.state)

        index = len(temp) - 1

        while index >= 0:
            temp[index] = (temp[index] + 1) % 256
            if temp[index] != 0:
                break
            index -= 1

        self.state = bytes(temp)

        return result
