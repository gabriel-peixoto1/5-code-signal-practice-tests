import unittest

from solution import EventBookingSystemImpl


class TestLevel4(unittest.TestCase):

    def setUp(self):
        """
        Cria um sistema novo antes de cada teste.
        """

        self.system = EventBookingSystemImpl()

        # Usuários
        self.system.add_user(1, "Alice")
        self.system.add_user(2, "Bob")
        self.system.add_user(3, "Charlie")
        self.system.add_user(4, "David")

        # Eventos
        self.system.add_event(
            100,
            "Python Conference",
            5
        )

        self.system.add_event(
            200,
            "Statistics Workshop",
            10
        )

    # =========================================================
    # TESTES — join_waitlist
    # =========================================================

    def test_join_waitlist_valid(self):
        """
        Usuário existente deve conseguir entrar na fila
        de um evento lotado.
        """

        self.system.create_booking(
            1000,
            1,
            100,
            5
        )

        result = self.system.join_waitlist(
            2,
            100
        )

        self.assertTrue(result)

        self.assertEqual(
            self.system.get_waitlist(100),
            [2]
        )

    def test_join_waitlist_multiple_users(self):
        """
        Vários usuários devem poder entrar na fila.
        """

        self.system.create_booking(
            1000,
            1,
            100,
            5
        )

        self.assertTrue(
            self.system.join_waitlist(2, 100)
        )

        self.assertTrue(
            self.system.join_waitlist(3, 100)
        )

        self.assertTrue(
            self.system.join_waitlist(4, 100)
        )

        self.assertEqual(
            self.system.get_waitlist(100),
            [2, 3, 4]
        )

    def test_join_waitlist_preserves_fifo_order(self):
        """
        A fila deve preservar a ordem de chegada.
        """

        self.system.create_booking(
            1000,
            1,
            100,
            5
        )

        self.system.join_waitlist(4, 100)
        self.system.join_waitlist(2, 100)
        self.system.join_waitlist(3, 100)

        self.assertEqual(
            self.system.get_waitlist(100),
            [4, 2, 3]
        )

    def test_join_waitlist_nonexistent_user(self):
        """
        Usuário inexistente não pode entrar na fila.
        """

        self.system.create_booking(
            1000,
            1,
            100,
            5
        )

        result = self.system.join_waitlist(
            999,
            100
        )

        self.assertFalse(result)

        self.assertEqual(
            self.system.get_waitlist(100),
            []
        )

    def test_join_waitlist_nonexistent_event(self):
        """
        Evento inexistente deve rejeitar a entrada na fila.
        """

        result = self.system.join_waitlist(
            1,
            999
        )

        self.assertFalse(result)

    def test_join_waitlist_event_not_full(self):
        """
        Usuário não pode entrar na fila se o evento
        ainda possuir lugares disponíveis.
        """

        # Capacidade = 5
        # Reserva = 3
        # Available = 2
        self.system.create_booking(
            1000,
            1,
            100,
            3
        )

        result = self.system.join_waitlist(
            2,
            100
        )

        self.assertFalse(result)

        self.assertEqual(
            self.system.get_waitlist(100),
            []
        )

    def test_join_waitlist_event_exactly_full(self):
        """
        Quando available == 0, o usuário pode entrar na fila.
        """

        self.system.create_booking(
            1000,
            1,
            100,
            5
        )

        event = self.system.get_event(100)

        self.assertEqual(
            event["available"],
            0
        )

        result = self.system.join_waitlist(
            2,
            100
        )

        self.assertTrue(result)

    def test_join_waitlist_duplicate(self):
        """
        O mesmo usuário não pode entrar duas vezes
        na mesma fila.
        """

        self.system.create_booking(
            1000,
            1,
            100,
            5
        )

        self.assertTrue(
            self.system.join_waitlist(2, 100)
        )

        result = self.system.join_waitlist(
            2,
            100
        )

        self.assertFalse(result)

        self.assertEqual(
            self.system.get_waitlist(100),
            [2]
        )

    def test_join_waitlist_user_with_active_booking(self):
        """
        Usuário que já possui uma reserva ativa no evento
        não pode entrar na fila.
        """

        self.system.create_booking(
            1000,
            1,
            100,
            5
        )

        result = self.system.join_waitlist(
            1,
            100
        )

        self.assertFalse(result)

        self.assertEqual(
            self.system.get_waitlist(100),
            []
        )

    def test_join_waitlist_after_cancelled_booking(self):
        """
        Uma reserva cancelada não é mais uma reserva ativa.
        Portanto, o usuário pode entrar na fila se o evento
        estiver cheio.
        """

        self.system.create_booking(
            1000,
            1,
            100,
            5
        )

        self.system.cancel_booking(1000)

        # O evento deixou de estar cheio, então deve falhar.
        result = self.system.join_waitlist(
            1,
            100
        )

        self.assertFalse(result)

    def test_join_waitlist_does_not_modify_bookings(self):
        """
        Entrar na fila não deve criar nem alterar reservas.
        """

        self.system.create_booking(
            1000,
            1,
            100,
            5
        )

        bookings_before = list(self.system.bookings)

        self.system.join_waitlist(
            2,
            100
        )

        self.assertEqual(
            self.system.bookings,
            bookings_before
        )

    def test_join_waitlist_does_not_change_available_seats(self):
        """
        Entrar na fila não deve alterar available.
        """

        self.system.create_booking(
            1000,
            1,
            100,
            5
        )

        available_before = self.system.get_event(100)["available"]

        self.system.join_waitlist(
            2,
            100
        )

        available_after = self.system.get_event(100)["available"]

        self.assertEqual(
            available_before,
            0
        )

        self.assertEqual(
            available_after,
            0
        )

    # =========================================================
    # TESTES — leave_waitlist
    # =========================================================

    def test_leave_waitlist_valid(self):
        """
        Usuário que está na fila deve conseguir sair.
        """

        self.system.create_booking(
            1000,
            1,
            100,
            5
        )

        self.system.join_waitlist(
            2,
            100
        )

        result = self.system.leave_waitlist(
            2,
            100
        )

        self.assertTrue(result)

        self.assertEqual(
            self.system.get_waitlist(100),
            []
        )

    def test_leave_waitlist_nonexistent_user(self):
        """
        Usuário que não está na fila deve resultar em False.
        """

        self.system.create_booking(
            1000,
            1,
            100,
            5
        )

        result = self.system.leave_waitlist(
            999,
            100
        )

        self.assertFalse(result)

    def test_leave_waitlist_user_not_waiting(self):
        """
        Usuário existente, mas que não está na fila,
        deve resultar em False.
        """

        self.system.create_booking(
            1000,
            1,
            100,
            5
        )

        result = self.system.leave_waitlist(
            2,
            100
        )

        self.assertFalse(result)

        self.assertEqual(
            self.system.get_waitlist(100),
            []
        )

    def test_leave_waitlist_twice(self):
        """
        Sair da fila duas vezes deve resultar em False
        na segunda tentativa.
        """

        self.system.create_booking(
            1000,
            1,
            100,
            5
        )

        self.system.join_waitlist(
            2,
            100
        )

        self.assertTrue(
            self.system.leave_waitlist(
                2,
                100
            )
        )

        result = self.system.leave_waitlist(
            2,
            100
        )

        self.assertFalse(result)

        self.assertEqual(
            self.system.get_waitlist(100),
            []
        )

    def test_leave_waitlist_preserves_other_users(self):
        """
        Remover uma pessoa não deve alterar a posição
        das outras, exceto pelo deslocamento natural da fila.
        """

        self.system.create_booking(
            1000,
            1,
            100,
            5
        )

        self.system.join_waitlist(2, 100)
        self.system.join_waitlist(3, 100)
        self.system.join_waitlist(4, 100)

        self.system.leave_waitlist(
            3,
            100
        )

        self.assertEqual(
            self.system.get_waitlist(100),
            [2, 4]
        )

    def test_leave_middle_user_preserves_fifo_order(self):
        """
        Remover um usuário do meio da fila deve preservar
        a ordem relativa dos demais.
        """

        self.system.create_booking(
            1000,
            1,
            100,
            5
        )

        self.system.join_waitlist(2, 100)
        self.system.join_waitlist(3, 100)
        self.system.join_waitlist(4, 100)

        self.system.leave_waitlist(
            3,
            100
        )

        self.assertEqual(
            self.system.get_waitlist(100),
            [2, 4]
        )

    # =========================================================
    # TESTES — get_waitlist
    # =========================================================

    def test_get_waitlist(self):
        """
        Deve retornar os IDs dos usuários na fila.
        """

        self.system.create_booking(
            1000,
            1,
            100,
            5
        )

        self.system.join_waitlist(2, 100)
        self.system.join_waitlist(3, 100)

        result = self.system.get_waitlist(100)

        self.assertEqual(
            result,
            [2, 3]
        )

    def test_get_waitlist_preserves_order(self):
        """
        get_waitlist deve preservar a ordem de chegada.
        """

        self.system.create_booking(
            1000,
            1,
            100,
            5
        )

        self.system.join_waitlist(4, 100)
        self.system.join_waitlist(2, 100)
        self.system.join_waitlist(3, 100)

        result = self.system.get_waitlist(100)

        self.assertEqual(
            result,
            [4, 2, 3]
        )

    def test_get_waitlist_empty(self):
        """
        Evento sem usuários na fila deve retornar [].
        """

        result = self.system.get_waitlist(100)

        self.assertEqual(
            result,
            []
        )

    def test_get_waitlist_nonexistent_event(self):
        """
        Evento inexistente deve retornar [].
        """

        result = self.system.get_waitlist(999)

        self.assertEqual(
            result,
            []
        )

    def test_get_waitlist_after_user_leaves(self):
        """
        Usuário removido não deve mais aparecer na fila.
        """

        self.system.create_booking(
            1000,
            1,
            100,
            5
        )

        self.system.join_waitlist(2, 100)
        self.system.join_waitlist(3, 100)

        self.system.leave_waitlist(2, 100)

        result = self.system.get_waitlist(100)

        self.assertEqual(
            result,
            [3]
        )

    # =========================================================
    # TESTES — independência entre eventos
    # =========================================================

    def test_waitlists_are_independent(self):
        """
        A fila de um evento não deve interferir na fila
        de outro evento.
        """

        # Lotar os dois eventos
        self.system.create_booking(
            1000,
            1,
            100,
            5
        )

        self.system.create_booking(
            1001,
            2,
            200,
            10
        )

        self.system.join_waitlist(
            3,
            100
        )

        self.system.join_waitlist(
            4,
            200
        )

        self.assertEqual(
            self.system.get_waitlist(100),
            [3]
        )

        self.assertEqual(
            self.system.get_waitlist(200),
            [4]
        )

    def test_joining_waitlist_for_one_event_does_not_affect_another(self):
        """
        Uma entrada na fila de um evento não deve alterar
        a fila de outro evento.
        """

        self.system.create_booking(
            1000,
            1,
            100,
            5
        )

        self.system.create_booking(
            1001,
            2,
            200,
            10
        )

        self.system.join_waitlist(
            3,
            100
        )

        self.assertEqual(
            self.system.get_waitlist(200),
            []
        )


if __name__ == "__main__":
    unittest.main()