from datetime import datetime
from typing import List, Union

from enums import PersonRole
from utils import regexes, remove_symbols


class Person:
    def __init__():
        pass

    def __init__(
        self,
        cpf: str,
        rg: str,
        name: str,
        birthdate: Union[datetime, str],
        roles: Union[List[PersonRole], PersonRole],
    ):
        if type(roles) == list and len(
            [el for el in roles if type(el) != PersonRole]
        ):
            raise ValueError("'roles' must be a PersonRole.")
        elif not regexes.cpf.match(cpf):
            raise ValueError("'cpf' is invalid.")
        elif not regexes.rg.match(rg):
            raise ValueError("'rg' is invalid.")
        elif type(birthdate) != datetime and type(birthdate) != str:
            raise ValueError("'birthdate' must be a datetime or date-like string.")

        if type(roles) == PersonRole:
            roles = [roles]
        elif type(birthdate) == str:
            birthdate = datetime.strptime(birthdate, '%d/%m/%Y')

        self.__cpf = remove_symbols(cpf)
        self.__rg = remove_symbols(rg)
        self.__name = name
        self.__birthdate = birthdate
        self.__roles = roles

    def get_cpf(self) -> str:
        return self.__cpf

    def get_rg(self) -> str:
        return self.__rg

    def get_name(self) -> str:
        return self.__name

    def get_birthdate(self) -> datetime:
        return self.__birthdate

    def get_birthdate_str(self) -> str:
        return self.__birthdate.strftime("%d/%m/%Y")

    def get_roles(self) -> List[PersonRole]:
        return self.__roles