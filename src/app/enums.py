import enum


class EnumMeta(enum.EnumMeta):
    """Makes using 'string in Enum' possible."""

    def __contains__(cls, item):
        return item in cls.__members__ or item in [
            e._value_ for e in PersonPermissions._member_map_.values()
        ]


class State(enum.Enum, metaclass=EnumMeta):
    """Enum for all brazilian states."""

    AC = "Acre"
    AL = "Alagoas"
    AP = "Amapá"
    AM = "Amazonas"
    BA = "Bahia"
    CE = "Ceará"
    DF = "Distrito Federal"
    ES = "Espírito Santo"
    GO = "Goiás"
    MA = "Maranhão"
    MT = "Mato Grosso"
    MS = "Mato Grosso do Sul"
    MG = "Minas Gerais"
    PA = "Pará"
    PB = "Paraíba"
    PR = "Paraná"
    PE = "Pernambuco"
    PI = "Piauí"
    RJ = "Rio de Janeiro"
    RN = "Rio Grande do Norte"
    RS = "Rio Grande do Sul"
    RO = "Rondônia"
    RR = "Roraima"
    SC = "Santa Catarina"
    SP = "São Paulo"
    SE = "Sergipe"
    TO = "Tocantins"


class PersonPermissions(enum.Enum, metaclass=EnumMeta):
    """Enum for all person types."""

    Professor = "professor"
    Student = "aluno"
    Responsible = "responsavel"
