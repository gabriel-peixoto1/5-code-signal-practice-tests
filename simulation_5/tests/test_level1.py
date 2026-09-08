import unittest

from solution import EventBookingSystemImpl


class TestLevel1(unittest.TestCase):

    def setUp(self):
        """
        Cria um sistema novo antes de cada teste.
        Assim, um teste não interfere no outro.
        """
        self.system = EventBookingSystemImpl()

    # =========================================================
    # TESTES — add_user
    # =========================================================

    def test_add_user_valid(self):
        """Usuário válido deve ser adicionado."""
        result = self.system.add_user(1, "Alice")

        self.assertTrue(result)

        self.assertEqual(
            self.system.users,
            [
                {
                    "user_id": 1,
                    "name": "Alice"
                }
            ]
        )

    def test_add_multiple_users(self):
        """Vários usuários válidos devem ser adicionados."""
        self.assertTrue(
            self.system.add_user(1, "Alice")
        )

        self.assertTrue(
            self.system.add_user(2, "Bob")
        )

        self.assertTrue(
            self.system.add_user(3, "Charlie")
        )

        self.assertEqual(len(self.system.users), 3)

    def test_duplicate_user_id(self):
        """ID de usuário duplicado deve ser rejeitado."""
        self.assertTrue(
            self.system.add_user(1, "Alice")
        )

        result = self.system.add_user(1, "Bob")

        self.assertFalse(result)

        # O segundo usuário não deve ter sido adicionado.
        self.assertEqual(len(self.system.users), 1)

        self.assertEqual(
            self.system.users[0],
            {
                "user_id": 1,
                "name": "Alice"
            }
        )

    def test_non_sequential_user_ids(self):
        """IDs não precisam ser sequenciais."""
        self.assertTrue(
            self.system.add_user(100, "Alice")
        )

        self.assertTrue(
            self.system.add_user(7, "Bob")
        )

        self.assertTrue(
            self.system.add_user(999, "Charlie")
        )

        self.assertEqual(len(self.system.users), 3)

    def test_user_data_is_stored_correctly(self):
        """O dicionário do usuário deve possuir os campos corretos."""
        self.system.add_user(42, "Gabriel")

        user = self.system.users[0]

        self.assertEqual(user["user_id"], 42)
        self.assertEqual(user["name"], "Gabriel")

        self.assertEqual(
            set(user.keys()),
            {"user_id", "name"}
        )

    # =========================================================
    # TESTES — add_event
    # =========================================================

    def test_add_event_valid(self):
        """Evento válido deve ser adicionado."""
        result = self.system.add_event(
            100,
            "Python Conference",
            50
        )

        self.assertTrue(result)

        self.assertEqual(
            self.system.events,
            [
                {
                    "event_id": 100,
                    "name": "Python Conference",
                    "capacity": 50,
                    "available": 50
                }
            ]
        )

    def test_add_multiple_events(self):
        """Vários eventos válidos devem ser adicionados."""
        self.assertTrue(
            self.system.add_event(100, "Python", 50)
        )

        self.assertTrue(
            self.system.add_event(200, "Statistics", 30)
        )

        self.assertTrue(
            self.system.add_event(300, "Data Science", 20)
        )

        self.assertEqual(len(self.system.events), 3)

    def test_duplicate_event_id(self):
        """ID de evento duplicado deve ser rejeitado."""
        self.assertTrue(
            self.system.add_event(100, "Python", 50)
        )

        result = self.system.add_event(
            100,
            "Another Event",
            20
        )

        self.assertFalse(result)

        # O evento original deve permanecer intacto.
        self.assertEqual(len(self.system.events), 1)

        self.assertEqual(
            self.system.events[0],
            {
                "event_id": 100,
                "name": "Python",
                "capacity": 50,
                "available": 50
            }
        )

    def test_event_capacity_zero(self):
        """Capacity igual a zero deve ser rejeitada."""
        result = self.system.add_event(
            100,
            "Invalid Event",
            0
        )

        self.assertFalse(result)

        self.assertEqual(len(self.system.events), 0)

    def test_event_capacity_negative(self):
        """Capacity negativa deve ser rejeitada."""
        result = self.system.add_event(
            100,
            "Invalid Event",
            -10
        )

        self.assertFalse(result)

        self.assertEqual(len(self.system.events), 0)

    def test_event_capacity_one(self):
        """Capacity igual a 1 é válida."""
        result = self.system.add_event(
            100,
            "Small Event",
            1
        )

        self.assertTrue(result)

        self.assertEqual(
            self.system.events[0]["capacity"],
            1
        )

        self.assertEqual(
            self.system.events[0]["available"],
            1
        )

    def test_non_sequential_event_ids(self):
        """IDs de eventos não precisam ser sequenciais."""
        self.assertTrue(
            self.system.add_event(500, "Event A", 10)
        )

        self.assertTrue(
            self.system.add_event(2, "Event B", 20)
        )

        self.assertTrue(
            self.system.add_event(9999, "Event C", 30)
        )

        self.assertEqual(len(self.system.events), 3)

    def test_event_data_is_stored_correctly(self):
        """O evento deve possuir exatamente os dados especificados."""
        self.system.add_event(
            42,
            "Python Workshop",
            25
        )

        event = self.system.events[0]

        self.assertEqual(
            set(event.keys()),
            {
                "event_id",
                "name",
                "capacity",
                "available"
            }
        )

        self.assertEqual(event["event_id"], 42)
        self.assertEqual(event["name"], "Python Workshop")
        self.assertEqual(event["capacity"], 25)
        self.assertEqual(event["available"], 25)

    # =========================================================
    # TESTES — get_event
    # =========================================================

    def test_get_existing_event(self):
        """get_event deve retornar o evento existente."""
        self.system.add_event(
            100,
            "Python Conference",
            50
        )

        result = self.system.get_event(100)

        self.assertEqual(
            result,
            {
                "event_id": 100,
                "name": "Python Conference",
                "capacity": 50,
                "available": 50
            }
        )

    def test_get_nonexistent_event(self):
        """Evento inexistente deve retornar None."""
        result = self.system.get_event(999)

        self.assertIsNone(result)

    def test_get_event_among_multiple_events(self):
        """Deve retornar o evento correto quando existem vários."""
        self.system.add_event(
            100,
            "Python",
            50
        )

        self.system.add_event(
            200,
            "Statistics",
            30
        )

        self.system.add_event(
            300,
            "Data Science",
            20
        )

        result = self.system.get_event(200)

        self.assertEqual(
            result,
            {
                "event_id": 200,
                "name": "Statistics",
                "capacity": 30,
                "available": 30
            }
        )

    def test_get_event_does_not_modify_state(self):
        """Consultar um evento não deve modificar o sistema."""
        self.system.add_event(
            100,
            "Python",
            50
        )

        before = list(self.system.events)

        self.system.get_event(100)

        after = self.system.events

        self.assertEqual(before, after)

    # =========================================================
    # TESTES — interação entre os métodos
    # =========================================================

    def test_users_and_events_are_independent(self):
        """Adicionar usuários não deve alterar os eventos e vice-versa."""
        self.system.add_user(1, "Alice")

        self.system.add_event(
            100,
            "Python",
            50
        )

        self.assertEqual(
            self.system.users,
            [
                {
                    "user_id": 1,
                    "name": "Alice"
                }
            ]
        )

        self.assertEqual(
            self.system.events,
            [
                {
                    "event_id": 100,
                    "name": "Python",
                    "capacity": 50,
                    "available": 50
                }
            ]
        )

    def test_invalid_event_does_not_change_state(self):
        """Evento inválido não deve alterar a lista de eventos."""
        self.system.add_event(
            100,
            "Python",
            50
        )

        before = list(self.system.events)

        self.system.add_event(
            200,
            "Invalid",
            0
        )

        self.assertEqual(
            self.system.events,
            before
        )

    def test_invalid_duplicate_user_does_not_change_state(self):
        """Usuário duplicado não deve alterar o estado."""
        self.system.add_user(1, "Alice")

        before = list(self.system.users)

        self.system.add_user(1, "Bob")

        self.assertEqual(
            self.system.users,
            before
        )


if __name__ == "__main__":
    unittest.main()