import unittest

from solution import EventBookingSystemImpl


class TestLevel2(unittest.TestCase):

    def setUp(self):
        """
        Cria um sistema novo antes de cada teste.
        """
        self.system = EventBookingSystemImpl()

        # Usuários utilizados nos testes
        self.system.add_user(1, "Alice")
        self.system.add_user(2, "Bob")
        self.system.add_user(3, "Charlie")

        # Eventos utilizados nos testes
        self.system.add_event(
            100,
            "Python Conference",
            10
        )

        self.system.add_event(
            200,
            "Statistics Workshop",
            5
        )

    # =========================================================
    # TESTES — create_booking
    # =========================================================

    def test_create_booking_valid(self):
        """Uma reserva válida deve ser criada."""
        result = self.system.create_booking(
            1000,
            1,
            100,
            3
        )

        self.assertTrue(result)

        self.assertEqual(
            self.system.bookings,
            [
                {
                    "booking_id": 1000,
                    "user_id": 1,
                    "event_id": 100,
                    "seats": 3,
                    "status": "active"
                }
            ]
        )

    def test_create_booking_decreases_available_seats(self):
        """Criar uma reserva deve diminuir os lugares disponíveis."""
        self.system.create_booking(
            1000,
            1,
            100,
            3
        )

        event = self.system.get_event(100)

        self.assertEqual(
            event["available"],
            7
        )

    def test_create_booking_with_exact_available_seats(self):
        """É permitido reservar exatamente todos os lugares disponíveis."""
        result = self.system.create_booking(
            1000,
            1,
            100,
            10
        )

        self.assertTrue(result)

        event = self.system.get_event(100)

        self.assertEqual(
            event["available"],
            0
        )

    def test_create_booking_duplicate_booking_id(self):
        """Booking ID duplicado deve ser rejeitado."""
        self.assertTrue(
            self.system.create_booking(
                1000,
                1,
                100,
                3
            )
        )

        result = self.system.create_booking(
            1000,
            2,
            100,
            2
        )

        self.assertFalse(result)

        # Apenas a primeira reserva deve existir.
        self.assertEqual(
            len(self.system.bookings),
            1
        )

        # Os lugares também não devem ser alterados.
        event = self.system.get_event(100)

        self.assertEqual(
            event["available"],
            7
        )

    def test_create_booking_nonexistent_user(self):
        """Usuário inexistente deve impedir a reserva."""
        result = self.system.create_booking(
            1000,
            999,
            100,
            2
        )

        self.assertFalse(result)

        self.assertEqual(
            len(self.system.bookings),
            0
        )

        self.assertEqual(
            self.system.get_event(100)["available"],
            10
        )

    def test_create_booking_nonexistent_event(self):
        """Evento inexistente deve impedir a reserva."""
        result = self.system.create_booking(
            1000,
            1,
            999,
            2
        )

        self.assertFalse(result)

        self.assertEqual(
            len(self.system.bookings),
            0
        )

    def test_create_booking_zero_seats(self):
        """Reserva com zero lugares deve ser rejeitada."""
        result = self.system.create_booking(
            1000,
            1,
            100,
            0
        )

        self.assertFalse(result)

        self.assertEqual(
            len(self.system.bookings),
            0
        )

        self.assertEqual(
            self.system.get_event(100)["available"],
            10
        )

    def test_create_booking_negative_seats(self):
        """Reserva com quantidade negativa deve ser rejeitada."""
        result = self.system.create_booking(
            1000,
            1,
            100,
            -5
        )

        self.assertFalse(result)

        self.assertEqual(
            len(self.system.bookings),
            0
        )

        self.assertEqual(
            self.system.get_event(100)["available"],
            10
        )

    def test_create_booking_more_seats_than_available(self):
        """Não deve ser possível reservar mais lugares que os disponíveis."""
        result = self.system.create_booking(
            1000,
            1,
            100,
            11
        )

        self.assertFalse(result)

        self.assertEqual(
            len(self.system.bookings),
            0
        )

        self.assertEqual(
            self.system.get_event(100)["available"],
            10
        )

    def test_create_booking_when_event_is_full(self):
        """Não deve ser possível criar reserva quando não há lugares."""
        self.system.create_booking(
            1000,
            1,
            100,
            10
        )

        result = self.system.create_booking(
            1001,
            2,
            100,
            1
        )

        self.assertFalse(result)

        self.assertEqual(
            len(self.system.bookings),
            1
        )

        self.assertEqual(
            self.system.get_event(100)["available"],
            0
        )

    def test_create_multiple_bookings(self):
        """Várias reservas válidas devem funcionar."""
        self.assertTrue(
            self.system.create_booking(
                1000,
                1,
                100,
                3
            )
        )

        self.assertTrue(
            self.system.create_booking(
                1001,
                2,
                100,
                2
            )
        )

        self.assertTrue(
            self.system.create_booking(
                1002,
                3,
                100,
                1
            )
        )

        self.assertEqual(
            len(self.system.bookings),
            3
        )

        self.assertEqual(
            self.system.get_event(100)["available"],
            4
        )

    def test_multiple_bookings_same_user_same_event(self):
        """
        O enunciado não proíbe múltiplas reservas do mesmo
        usuário para o mesmo evento.
        """
        self.assertTrue(
            self.system.create_booking(
                1000,
                1,
                100,
                2
            )
        )

        self.assertTrue(
            self.system.create_booking(
                1001,
                1,
                100,
                3
            )
        )

        self.assertEqual(
            len(self.system.bookings),
            2
        )

        self.assertEqual(
            self.system.get_event(100)["available"],
            5
        )

    def test_invalid_booking_does_not_modify_state(self):
        """
        Uma reserva inválida não deve alterar o estado
        do sistema.
        """
        self.system.create_booking(
            1000,
            1,
            100,
            3
        )

        bookings_before = list(self.system.bookings)
        available_before = self.system.get_event(100)["available"]

        result = self.system.create_booking(
            1001,
            999,
            100,
            5
        )

        self.assertFalse(result)

        self.assertEqual(
            self.system.bookings,
            bookings_before
        )

        self.assertEqual(
            self.system.get_event(100)["available"],
            available_before
        )

    # =========================================================
    # TESTES — cancel_booking
    # =========================================================

    def test_cancel_booking_valid(self):
        """Uma reserva existente deve poder ser cancelada."""
        self.system.create_booking(
            1000,
            1,
            100,
            3
        )

        result = self.system.cancel_booking(1000)

        self.assertTrue(result)

    def test_cancel_booking_changes_status(self):
        """O status da reserva deve mudar para cancelled."""
        self.system.create_booking(
            1000,
            1,
            100,
            3
        )

        self.system.cancel_booking(1000)

        self.assertEqual(
            self.system.bookings[0]["status"],
            "cancelled"
        )

    def test_cancel_booking_returns_seats(self):
        """Cancelar deve devolver os lugares ao evento."""
        self.system.create_booking(
            1000,
            1,
            100,
            3
        )

        self.assertEqual(
            self.system.get_event(100)["available"],
            7
        )

        self.system.cancel_booking(1000)

        self.assertEqual(
            self.system.get_event(100)["available"],
            10
        )

    def test_cancel_nonexistent_booking(self):
        """Reserva inexistente deve retornar False."""
        result = self.system.cancel_booking(9999)

        self.assertFalse(result)

    def test_cancel_already_cancelled_booking(self):
        """Uma reserva já cancelada não pode ser cancelada novamente."""
        self.system.create_booking(
            1000,
            1,
            100,
            3
        )

        self.assertTrue(
            self.system.cancel_booking(1000)
        )

        result = self.system.cancel_booking(1000)

        self.assertFalse(result)

        # Os lugares não podem ser devolvidos novamente.
        self.assertEqual(
            self.system.get_event(100)["available"],
            10
        )

    def test_cancel_does_not_affect_other_bookings(self):
        """Cancelar uma reserva não deve afetar as outras."""
        self.system.create_booking(
            1000,
            1,
            100,
            3
        )

        self.system.create_booking(
            1001,
            2,
            100,
            2
        )

        self.system.cancel_booking(1000)

        self.assertEqual(
            self.system.bookings[0]["status"],
            "cancelled"
        )

        self.assertEqual(
            self.system.bookings[1]["status"],
            "active"
        )

        # Apenas os 3 lugares da primeira reserva voltam.
        self.assertEqual(
            self.system.get_event(100)["available"],
            8
        )

    def test_cancel_booking_does_not_delete_booking(self):
        """
        Cancelar uma reserva deve alterar seu status,
        não removê-la da lista.
        """
        self.system.create_booking(
            1000,
            1,
            100,
            3
        )

        self.system.cancel_booking(1000)

        self.assertEqual(
            len(self.system.bookings),
            1
        )

        self.assertEqual(
            self.system.bookings[0]["booking_id"],
            1000
        )

    # =========================================================
    # TESTES — get_user_bookings
    # =========================================================

    def test_get_user_bookings(self):
        """Deve retornar as reservas do usuário."""
        self.system.create_booking(
            1000,
            1,
            100,
            2
        )

        self.system.create_booking(
            1001,
            1,
            200,
            1
        )

        result = self.system.get_user_bookings(1)

        self.assertEqual(
            len(result),
            2
        )

    def test_get_user_bookings_only_specific_user(self):
        """Não deve retornar reservas de outros usuários."""
        self.system.create_booking(
            1000,
            1,
            100,
            2
        )

        self.system.create_booking(
            1001,
            2,
            100,
            3
        )

        result = self.system.get_user_bookings(1)

        self.assertEqual(
            len(result),
            1
        )

        self.assertEqual(
            result[0]["user_id"],
            1
        )

    def test_get_user_bookings_includes_cancelled(self):
        """Reservas canceladas também devem aparecer."""
        self.system.create_booking(
            1000,
            1,
            100,
            2
        )

        self.system.cancel_booking(1000)

        result = self.system.get_user_bookings(1)

        self.assertEqual(
            len(result),
            1
        )

        self.assertEqual(
            result[0]["status"],
            "cancelled"
        )

    def test_get_user_bookings_sorted_by_booking_id(self):
        """As reservas devem ser ordenadas por booking_id."""
        self.system.create_booking(
            3000,
            1,
            100,
            1
        )

        self.system.create_booking(
            1000,
            1,
            200,
            1
        )

        self.system.create_booking(
            2000,
            1,
            100,
            1
        )

        result = self.system.get_user_bookings(1)

        self.assertEqual(
            [booking["booking_id"] for booking in result],
            [1000, 2000, 3000]
        )

    def test_get_user_bookings_empty(self):
        """Usuário sem reservas deve retornar lista vazia."""
        result = self.system.get_user_bookings(1)

        self.assertEqual(
            result,
            []
        )

    def test_get_user_bookings_nonexistent_user(self):
        """
        Um usuário inexistente não possui reservas,
        portanto deve retornar lista vazia.
        """
        result = self.system.get_user_bookings(999)

        self.assertEqual(
            result,
            []
        )

    def test_get_user_bookings_after_cancel_and_new_booking(self):
        """
        Deve incluir tanto reservas canceladas quanto ativas,
        mantendo a ordenação.
        """
        self.system.create_booking(
            3000,
            1,
            100,
            2
        )

        self.system.cancel_booking(3000)

        self.system.create_booking(
            1000,
            1,
            100,
            3
        )

        self.system.create_booking(
            2000,
            1,
            200,
            1
        )

        result = self.system.get_user_bookings(1)

        self.assertEqual(
            [booking["booking_id"] for booking in result],
            [1000, 2000, 3000]
        )

        self.assertEqual(
            [booking["status"] for booking in result],
            ["active", "active", "cancelled"]
        )


if __name__ == "__main__":
    unittest.main()