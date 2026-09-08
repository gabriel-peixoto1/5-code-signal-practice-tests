import unittest

from solution import EventBookingSystemImpl


class TestLevel3(unittest.TestCase):

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
            10
        )

        self.system.add_event(
            200,
            "Statistics Workshop",
            20
        )

        self.system.add_event(
            300,
            "Data Science Meetup",
            5
        )

    # =========================================================
    # TESTES — get_event_bookings
    # =========================================================

    def test_get_event_bookings(self):
        """
        Deve retornar as reservas ativas de um evento.
        """

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

        result = self.system.get_event_bookings(100)

        self.assertEqual(
            len(result),
            2
        )

        self.assertEqual(
            result,
            [
                {
                    "booking_id": 1000,
                    "user_id": 1,
                    "event_id": 100,
                    "seats": 3,
                    "status": "active"
                },
                {
                    "booking_id": 1001,
                    "user_id": 2,
                    "event_id": 100,
                    "seats": 2,
                    "status": "active"
                }
            ]
        )

    def test_get_event_bookings_only_specific_event(self):
        """
        Não deve retornar reservas pertencentes a outros eventos.
        """

        self.system.create_booking(
            1000,
            1,
            100,
            3
        )

        self.system.create_booking(
            1001,
            2,
            200,
            4
        )

        result = self.system.get_event_bookings(100)

        self.assertEqual(
            len(result),
            1
        )

        self.assertEqual(
            result[0]["event_id"],
            100
        )

    def test_get_event_bookings_excludes_cancelled(self):
        """
        Reservas canceladas não devem aparecer.
        """

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

        result = self.system.get_event_bookings(100)

        self.assertEqual(
            len(result),
            1
        )

        self.assertEqual(
            result[0]["booking_id"],
            1001
        )

        self.assertEqual(
            result[0]["status"],
            "active"
        )

    def test_get_event_bookings_sorted_by_booking_id(self):
        """
        As reservas devem ser ordenadas por booking_id crescente,
        independentemente da ordem em que foram criadas.
        """

        self.system.create_booking(
            3000,
            1,
            100,
            1
        )

        self.system.create_booking(
            1000,
            2,
            100,
            2
        )

        self.system.create_booking(
            2000,
            3,
            100,
            1
        )

        result = self.system.get_event_bookings(100)

        self.assertEqual(
            [booking["booking_id"] for booking in result],
            [1000, 2000, 3000]
        )

    def test_get_event_bookings_nonexistent_event(self):
        """
        Evento inexistente deve retornar lista vazia.
        """

        result = self.system.get_event_bookings(999)

        self.assertEqual(
            result,
            []
        )

    def test_get_event_bookings_without_bookings(self):
        """
        Evento existente sem reservas deve retornar lista vazia.
        """

        result = self.system.get_event_bookings(100)

        self.assertEqual(
            result,
            []
        )

    def test_get_event_bookings_after_all_bookings_cancelled(self):
        """
        Se todas as reservas forem canceladas, nenhuma deve aparecer.
        """

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

        self.system.cancel_booking(1000)
        self.system.cancel_booking(1001)

        result = self.system.get_event_bookings(100)

        self.assertEqual(
            result,
            []
        )

    # =========================================================
    # TESTES — get_event_occupancy
    # =========================================================

    def test_get_event_occupancy_empty_event(self):
        """
        Evento sem reservas deve ter ocupação igual a 0.0.
        """

        result = self.system.get_event_occupancy(100)

        self.assertEqual(
            result,
            0.0
        )

        self.assertIsInstance(
            result,
            float
        )

    def test_get_event_occupancy_partial(self):
        """
        3 lugares ocupados de uma capacidade de 10
        devem resultar em 0.3.
        """

        self.system.create_booking(
            1000,
            1,
            100,
            3
        )

        result = self.system.get_event_occupancy(100)

        self.assertEqual(
            result,
            0.3
        )

    def test_get_event_occupancy_multiple_bookings(self):
        """
        A ocupação deve considerar a soma dos lugares
        de todas as reservas ativas.
        """

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

        result = self.system.get_event_occupancy(100)

        self.assertEqual(
            result,
            0.5
        )

    def test_get_event_occupancy_full_event(self):
        """
        Evento completamente ocupado deve retornar 1.0.
        """

        self.system.create_booking(
            1000,
            1,
            100,
            10
        )

        result = self.system.get_event_occupancy(100)

        self.assertEqual(
            result,
            1.0
        )

    def test_get_event_occupancy_after_cancellation(self):
        """
        Cancelamento deve diminuir a ocupação.
        """

        self.system.create_booking(
            1000,
            1,
            100,
            8
        )

        self.assertEqual(
            self.system.get_event_occupancy(100),
            0.8
        )

        self.system.cancel_booking(1000)

        self.assertEqual(
            self.system.get_event_occupancy(100),
            0.0
        )

    def test_get_event_occupancy_cancelled_booking_not_counted(self):
        """
        Uma reserva cancelada não deve contribuir para a ocupação,
        mesmo permanecendo em self.bookings.
        """

        self.system.create_booking(
            1000,
            1,
            100,
            4
        )

        self.system.create_booking(
            1001,
            2,
            100,
            2
        )

        self.system.cancel_booking(1000)

        result = self.system.get_event_occupancy(100)

        self.assertEqual(
            result,
            0.2
        )

    def test_get_event_occupancy_nonexistent_event(self):
        """
        Evento inexistente deve retornar 0.0.
        """

        result = self.system.get_event_occupancy(999)

        self.assertEqual(
            result,
            0.0
        )

        self.assertIsInstance(
            result,
            float
        )

    def test_get_event_occupancy_different_capacity(self):
        """
        A ocupação deve ser calculada em relação à capacidade
        de cada evento.
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
            5
        )

        occupancy_event_100 = self.system.get_event_occupancy(100)
        occupancy_event_200 = self.system.get_event_occupancy(200)

        self.assertEqual(
            occupancy_event_100,
            0.5
        )

        self.assertEqual(
            occupancy_event_200,
            0.25
        )

    # =========================================================
    # TESTES — get_most_popular_event
    # =========================================================

    def test_get_most_popular_event_single_event_with_bookings(self):
        """
        Com apenas um evento com reservas, ele deve ser retornado.
        """

        self.system.create_booking(
            1000,
            1,
            100,
            4
        )

        result = self.system.get_most_popular_event()

        self.assertEqual(
            result,
            100
        )

    def test_get_most_popular_event_by_occupied_seats(self):
        """
        O evento com maior quantidade de lugares ocupados
        deve ser retornado.
        """

        self.system.create_booking(
            1000,
            1,
            100,
            3
        )

        self.system.create_booking(
            1001,
            2,
            200,
            7
        )

        self.system.create_booking(
            1002,
            3,
            300,
            2
        )

        result = self.system.get_most_popular_event()

        self.assertEqual(
            result,
            200
        )

    def test_get_most_popular_event_multiple_bookings(self):
        """
        A popularidade deve considerar a soma dos lugares
        ocupados em todas as reservas ativas.
        """

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
            4
        )

        self.system.create_booking(
            1002,
            3,
            200,
            5
        )

        result = self.system.get_most_popular_event()

        # Evento 100 = 7 lugares
        # Evento 200 = 5 lugares
        self.assertEqual(
            result,
            100
        )

    def test_get_most_popular_event_ignores_cancelled_bookings(self):
        """
        Reservas canceladas não devem contar para determinar
        o evento mais popular.
        """

        self.system.create_booking(
            1000,
            1,
            100,
            8
        )

        self.system.create_booking(
            1001,
            2,
            200,
            5
        )

        self.system.cancel_booking(1000)

        result = self.system.get_most_popular_event()

        self.assertEqual(
            result,
            200
        )

    def test_get_most_popular_event_tie_alphabetical(self):
        """
        Em caso de empate na quantidade de lugares ocupados,
        deve vencer o evento cujo nome vem primeiro
        alfabeticamente.
        """

        # Python Conference = 5 lugares
        self.system.create_booking(
            1000,
            1,
            100,
            5
        )

        # Data Science Meetup = 5 lugares
        self.system.create_booking(
            1001,
            2,
            300,
            5
        )

        result = self.system.get_most_popular_event()

        # "Data Science Meetup" < "Python Conference"
        self.assertEqual(
            result,
            300
        )

    def test_get_most_popular_event_tie_with_multiple_events(self):
        """
        Deve aplicar o desempate alfabético quando três eventos
        possuem a mesma quantidade de lugares ocupados.
        """

        self.system.create_booking(
            1000,
            1,
            100,
            2
        )

        self.system.create_booking(
            1001,
            2,
            200,
            2
        )

        self.system.create_booking(
            1002,
            3,
            300,
            2
        )

        result = self.system.get_most_popular_event()

        # Ordem alfabética:
        # Data Science Meetup
        # Python Conference
        # Statistics Workshop
        self.assertEqual(
            result,
            300
        )

    def test_get_most_popular_event_zero_bookings_are_candidates(self):
        """
        Eventos sem reservas continuam sendo candidatos válidos.
        """

        result = self.system.get_most_popular_event()

        # Todos possuem 0 lugares ocupados.
        # "Data Science Meetup" é alfabeticamente menor.
        self.assertEqual(
            result,
            300
        )

    def test_get_most_popular_event_all_zero_after_cancellation(self):
        """
        Se todas as reservas forem canceladas, todos os eventos
        terão 0 lugares ocupados e o desempate deve ser aplicado.
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
            5
        )

        self.system.cancel_booking(1000)
        self.system.cancel_booking(1001)

        result = self.system.get_most_popular_event()

        self.assertEqual(
            result,
            300
        )

    def test_get_most_popular_event_no_events(self):
        """
        Se não houver eventos, deve retornar None.
        """

        system = EventBookingSystemImpl()

        result = system.get_most_popular_event()

        self.assertIsNone(result)

    def test_get_most_popular_event_same_event_after_cancellation(self):
        """
        O evento mais popular deve ser recalculado corretamente
        após um cancelamento.
        """

        self.system.create_booking(
            1000,
            1,
            100,
            8
        )

        self.system.create_booking(
            1001,
            2,
            200,
            5
        )

        self.assertEqual(
            self.system.get_most_popular_event(),
            100
        )

        self.system.cancel_booking(1000)

        self.assertEqual(
            self.system.get_most_popular_event(),
            200
        )


if __name__ == "__main__":
    unittest.main()