from typing import Union

from enums import State
from utils import assert_instance, assert_regex, regexes, remove_symbols


class Address:
    def __init__(self, state: Union[State, str], city: str, cep: str, address: str):
        if isinstance(state, str) and state in State:
            state = State[state]

        assert_instance(state, State)
        assert_regex(cep, regexes.cep)

        self.state = state
        self.city = city.title().strip()
        self.cep = remove_symbols(cep)
        self.address = address.strip()


class City:
    def __init__(self, state: Union[State, str], city: str):
        if isinstance(state, str) and state in State:
            state = State[state]

        assert_instance(state, State)

        self.state = state
        self.city = city.title().strip()
