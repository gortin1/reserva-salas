import unittest
import requests

class TestReserva(unittest.TestCase):

    def test_001_cria_reserva(self):
        response1 = requests.post('http://localhost:5002/reservas', json={
            "turma_id": 1,
            "sala": "101",
            "data": "2025-05-25",
            "hora_inicio": "08:00",
            "hora_fim": "10:00"
        })

        response2 = requests.post('http://localhost:5002/reservas', json={
            "turma_id": 2,
            "sala": "102",
            "data": "2025-05-25",
            "hora_inicio": "09:00",
            "hora_fim": "11:00"
        })

        self.assertEqual(response1.status_code, 201)
        self.assertIn("Reserva adicionada com sucesso.", response1.text)
        self.assertEqual(response2.status_code, 201)
        self.assertIn("Reserva adicionada com sucesso.", response2.text)

    def test_002_lista_reservas(self):
        response = requests.get('http://localhost:5002/reservas')
        if response.status_code == 404:
            self.fail("Erro 404 - Não há reservas no servidor")
        try:
            lista = response.json()
        except:
            self.fail("Não retornou JSON na listagem de reservas")
        self.assertIsInstance(lista, list)

    def test_003_reserva_por_id(self):
        reserva_id = requests.get('http://localhost:5002/reservas/1')
        dict_retornado = reserva_id.json()
        self.assertEqual(type(dict_retornado), dict)
        self.assertIn('sala', dict_retornado)
        self.assertEqual(dict_retornado['sala'], '101')

    def test_004_edita_reserva(self):
        requests.post('http://localhost:5002/reservas', json={
            "turma_id": 1,
            "sala": "103",
            "data": "2025-05-27",
            "hora_inicio": "10:00",
            "hora_fim": "12:00"
        })

        reserva_id_antes = requests.get('http://localhost:5002/reservas/3')
        self.assertEqual(reserva_id_antes.json()['sala'], "103")

        requests.put(f'http://localhost:5002/reservas/3', json={
            "turma_id": 1,
            "sala": "104",
            "data": "2025-06-01",
            "hora_inicio": "10:00",
            "hora_fim": "12:00"
        })

        reserva_id_depois = requests.get(f'http://localhost:5002/reservas/3')
        reserva_json = reserva_id_depois.json()
        self.assertEqual(reserva_json['sala'], "104")
        self.assertEqual(reserva_json['data'], "2025-06-01")

    def test_005_deleta_reserva(self):
        requests.post('http://localhost:5002/reservas', json={
            "turma_id": 1,
            "sala": "105",
            "data": "2025-05-28",
            "hora_inicio": "13:00",
            "hora_fim": "15:00"
        })


        requests.delete(f'http://localhost:5002/reservas/4')
        
        response_check = requests.get('http://localhost:5002/reservas/4')
        self.assertEqual(response_check.status_code, 404)


def runTests():
    suite = unittest.defaultTestLoader.loadTestsFromTestCase(TestReserva)
    unittest.TextTestRunner(verbosity=2, failfast=True).run(suite)

if __name__ == '__main__':
    runTests()
