from connection import Connection
from models import City
from utils import assert_instance, assert_regex, regexes


class Ticket:
    @staticmethod
    def fetch_by_buyer_join_party_city(buyer: id) -> list:
        assert_regex(buyer, regexes.cpf, "cpf")

        query = """
            SELECT data_horario, nome, preço, cidade, estado
            FROM ingresso as I, festa as F, residencia as R
            WHERE I.festa = F.id AND I.comprador = %s AND F.moradia = R.id
            ORDER BY data_horario DESC;
        """
        return Connection().exec_commit(query, buyer, cb=lambda cur: cur.fetchall())


class Party:
    @staticmethod
    def fetch_future_by_city_join_address(city: City) -> list:
        assert_instance(city, City)

        query = """
            SELECT F.id, data_horario, nome, preço, endereço, open_bar
            FROM festa as F, residencia as R
            WHERE F.data_horario > NOW() AND F.moradia = R.id
                  AND R.cidade = %s AND R.estado = %s
                  AND F.n_ingressos_total > F.n_ingressos_vendidos
            ORDER BY data_horario ASC;
        """
        return Connection().exec_commit(
            query, city.city, city.state.name, cb=lambda cur: cur.fetchall()
        )
