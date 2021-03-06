import datetime
import re

from enums import State

# accepted boolean-like strings
AFFIRMATIVE_RESPONSES = ["true", "y", "yes", "s", "sim"]
NEGATIVE_RESPONSES = ["false", "n", "no", "não", "nao"]


class regexes:
    """Various utilities regexes to validate data."""

    cep = re.compile(r"^(\d{5})-?(\d{3})$")
    cpf = re.compile(r"^(\d{3})\.?(\d{3})\.?(\d{3})\-?(\d{2})$")
    date = re.compile(r"\d{2}/\d{2}/19\d{2}|\d{2}/\d{2}/20\d{2}")
    name = re.compile(r"^\w{2,}\s\w{2,}[\w\s]*$")
    single_name = re.compile(r"^[\w\s]*$")
    rg = re.compile(r"^(\d{1,2})\.?(\d{3})\.?(\d{3})-?(\d{1}|X|x)$")


def assert_regex(string: str, regex: re.Pattern, name: str = "") -> None:
    """
    Raise an error if a given string does not match a given pattern.

    Parameters
    ----------
    string: str
        The string to be tested.
    regex: re.Pattern
        The pattern to test `string` against.
    name: str (default '')
        The string's name to be specified in the error message.
    """
    if not regex.match(string):
        raise ValueError(f"'{name or string}' is invalid.")


def assert_instance(variable: any, _class: object, name: str = "") -> None:
    """
    Raise an error if a given variable isn't an instance of a given class.

    Parameters
    ----------
    variable: any
        The variable to be tested.
    _class: object
        The class that `variable` should be an instance of.
    name: str (default '')
        The variable's name to be specified in the error message.
    """
    if not isinstance(variable, _class):
        raise ValueError(f"'{name or variable}' has an invalid type.")


def assert_value(a: any, b: any, name: str = "") -> None:
    """
    Raise an error if a given variable isn't equal to another.

    Parameters
    ----------
    a, b: any
        The variables to be compared.
    name: str (default '')
        `a`'s name to be specified in the error message.
    """
    if a != b:
        raise ValueError(f"'{name}' is invalid ({a} doesn't match {b}).")


def remove_symbols(string: str) -> str:
    """Remove everything that's not a letter nor a number from the given string."""
    return re.sub(r"[^a-zA-Z0-9]", "", string)


def prompt(
    text: str,
    validate: callable = None,
    err: str = "Input inválido, tente novamente.",
) -> str:
    """
    Prompt user for input and only returns when the input is valid.

    Parameters
    ----------
    text: str
        Input prompt.
    validate: function = None
        Validator for the input - if none is provided, all input is considered
        valid. It should receive a string to validate as parameter and return a
        bool.
    err: str = "Input inválido, tente novamente."
        Error message in case validation fails.

    Returns
    -------
    str: the user's validated input.
    """
    if not text.endswith("\n"):
        text += " "

    r = input(text)
    if validate:
        is_valid = validate(r)
        while not is_valid:
            r = input(f"\n{err} {text}")
            is_valid = validate(r)

    return r


def prompt_continue(leading: str = "\n") -> None:
    """Prompt user to press Enter to continue."""
    input(leading + "Aperte ENTER para continuar. ")


def prompt_menu(
    options: list[str],
    leading_text: str = "Selecione uma das opções do menu a seguir para continuar.\n\n",
    trailing_text: str = "\n\nPara selecionar, insira apenas o número da opção. Input:",
) -> int:
    """
    Prompt user to choose an option from the menu and returns the option's
    index.

    Parameters
    ----------
    options: list[str]
        Menu optons in order. Indexing them (e.g. "1. Options ...") is not
        necessary and will be done automatically.
    leading_text: str
        Text that'll precede the list of options.
    trailint_text: str
        Text that'll proceed the list of options an precede the user's input.

    Returns
    -------
    int: the chosen option's index (`0, ..., len(options)`).
    """
    if not (options and isinstance(options, list)):
        return None

    n_options = len(options)
    options = "\n".join([f"{i+1}. {o}" for i, o in enumerate(options)])

    text = (
        leading_text
        + ("\n\n" if leading_text and not leading_text.endswith("\n") else "")
        + options
        + trailing_text
    )

    def validate(option: str):
        """Validate the user input for the menu."""
        if option.endswith("."):
            option = option[:-1]
        return option.isdigit() and int(option) <= n_options

    r = prompt(text, validate)

    return int(r.replace(".", "")) - 1


def format(target: any, type: str = "") -> str:
    """Format the input according to the specified type (only required for CEP and RG)."""
    if isinstance(target, datetime.date):
        return target.strftime(
            "%d/%m/%Y" + (", %Hh%M" if type == "data_horario" else "")
        )

    if isinstance(target, list):
        return ", ".join(target) if target else "-"

    if target in State:
        return State[target].value

    if isinstance(target, State):
        return target.value

    if isinstance(target, str) and target.startswith("$"):
        return f"R{target.replace(',','<DOT>').replace('.', ',').replace('<DOT>','.')}"

    cpf = regexes.cpf.match(target)
    if cpf:
        _1, _2, _3, _4 = cpf.groups()
        return f"{_1}.{_2}.{_3}-{_4}"

    cep = regexes.cep.match(target)
    if cep and type.upper() == "CEP":
        _1, _2 = cep.groups()
        return f"{_1}-{_2}"

    rg = regexes.rg.match(target)
    if rg and type.upper() == "RG":
        _1, _2, _3, _4 = rg.groups()
        return f"{_1}.{_2}.{_3}-{_4}"

    return target


def validate_date(date: str) -> bool:
    """Check if a given date is valid in the format DD/MM/YYYY."""
    if not regexes.date.match(date):
        return False

    day, month, year = [int(string) for string in date.split("/")]
    if not (day and month and year) or day > 31 or month > 12:
        return False

    current_year = datetime.date.today().year
    if year >= current_year:
        return False

    return True


def validate_bool(boolean: str) -> bool:
    """Check if a given string can be parsed to boolean."""
    return boolean in AFFIRMATIVE_RESPONSES + NEGATIVE_RESPONSES


def parse_bool(boolean: str) -> bool:
    """Parse a given string to boolean."""
    if boolean.lower() in AFFIRMATIVE_RESPONSES:
        return True

    elif boolean.lower() in NEGATIVE_RESPONSES:
        return False


def validate_float(number: str) -> bool:
    """Check if a given string is a float number."""
    return number.replace(".", "", 1).isdigit() or number.replace(",", "", 1).isdigit()


def parse_float(number: str) -> float:
    """Parse a given string to float."""
    return float(number.replace(",", "."))


def loop_display_data(data: list[any], display_fn: callable, prop: str = None) -> None:
    """
    If the given data has at least one item, loop thrugh the list and call the
    display function for each one, followed by a <Continue> prompt. Otherwise,
    display a "no results found" message.

    Parameters
    ----------
    data: list[T]
        A dataset.
    display_fn: function(data_item: T, index: int) -> None
        Function that will be called for each item in `data`. The item as well
        as it's index will be passed as arguments.
    prop: str
        The property's name. If passed, a warning will be printed saying the
        functionality is a work in proggress.
    """
    if not data:
        print("\nNenhum resultado encontrado.")
        prompt_continue()
    else:
        if prop:
            print(
                "\nNo momento ainda não é possível ver as informações de cada "
                + f"{prop} com mais detalhes, mas essa funcionalidade está em "
                + "desenvolvimento!"
            )

        for index, data_item in enumerate(data):
            display_fn(data_item, index)
            prompt_continue()
