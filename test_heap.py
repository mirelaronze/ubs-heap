
import unittest
from contextlib import redirect_stdout
from io import StringIO

from atvHeap import HeapAtendimentos


class TestHeapAtendimentos(unittest.TestCase):

    def setUp(self):
        self.agenda = HeapAtendimentos()

        pacientes = [
            (50000000000, "Ana", 35),
            (30000000000, "João", 67),
            (70000000000, "Maria", 42),
            (20000000000, "Carlos", 81),
            (40000000000, "Beatriz", 59)
        ]

        for cpf, nome, idade in pacientes:
            with redirect_stdout(StringIO()):
                self.agenda.cadastrar_atendimento_dia(
                    cpf, nome, "123456789012345",
                    "Consulta Agendada", idade
                )

    def test_cadastro(self):
        self.assertEqual(len(self.agenda.heap), 5)
        self.assertEqual(self.agenda.heap[0].idade, 81)

    def test_proximo_paciente(self):
        with redirect_stdout(StringIO()):
            paciente = self.agenda.quem_eh_o_proximo()

        self.assertEqual(paciente.nome_completo, "Carlos")

    def test_remocao(self):
        with redirect_stdout(StringIO()):
            removido = self.agenda.remover_paciente_prioritario()

        self.assertEqual(removido.idade, 81)
        self.assertEqual(len(self.agenda.heap), 4)
        self.assertEqual(self.agenda.heap[0].idade, 67)

    def test_heapify(self):
        self.agenda.heap[0], self.agenda.heap[-1] = (
            self.agenda.heap[-1], self.agenda.heap[0]
        )
        self.agenda.heapify(0)
        self.assertEqual(self.agenda.heap[0].idade, 81)

    def test_heap_sort(self):
        ordenados = self.agenda.heap_sort()
        idades = [paciente.idade for paciente in ordenados]

        self.assertEqual(idades, [81, 67, 59, 42, 35])

    def test_heap_original_preservado(self):
        antes = self.agenda.heap.copy()
        self.agenda.heap_sort()

        self.assertEqual(self.agenda.heap, antes)

    def test_falta_quantos(self):
        self.assertEqual(self.agenda.falta_quantos(20000000000), 0)
        self.assertEqual(self.agenda.falta_quantos(30000000000), 1)
        self.assertEqual(self.agenda.falta_quantos(50000000000), 4)

    def test_paciente_inexistente(self):
        self.assertIsNone(self.agenda.falta_quantos(99999999999))

    def test_agenda_vazia(self):
        vazia = HeapAtendimentos()

        self.assertEqual(vazia.heap_sort(), [])
        self.assertIsNone(vazia.falta_quantos(12345678900))

        with redirect_stdout(StringIO()):
            self.assertIsNone(vazia.quem_eh_o_proximo())
            self.assertIsNone(vazia.remover_paciente_prioritario())

    def test_imprimir_agenda(self):
        saida = StringIO()

        with redirect_stdout(saida):
            self.agenda.imprimir_agenda_ordenada()

        self.assertIn("Carlos", saida.getvalue())
        self.assertIn("Ana", saida.getvalue())

    def test_exibir_heap(self):
        saida = StringIO()

        with redirect_stdout(saida):
            self.agenda.exibir_agenda()

        self.assertIn("HEAP DE ATENDIMENTOS", saida.getvalue())


if __name__ == "__main__":
    unittest.main()
