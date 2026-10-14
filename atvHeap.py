
class Paciente:
    def __init__(self, cpf, nome_completo, cartao_sus, tipo_atendimento, idade):
        self.cpf = cpf
        self.nome_completo = nome_completo
        self.cartao_sus = cartao_sus
        self.tipo_atendimento = tipo_atendimento
        self.idade = idade


class HeapAtendimentos:
    def __init__(self):
        self.heap = []

    # Insere o paciente no Max-Heap
    def cadastrar_atendimento_dia(self, cpf, nome, cartao_sus, tipo_atendimento, idade):
        paciente = Paciente(cpf, nome, cartao_sus, tipo_atendimento, idade)
        self.heap.append(paciente)

        i = len(self.heap) - 1

        while i > 0:
            pai = (i - 1) // 2

            if self.heap[i].idade > self.heap[pai].idade:
                self.heap[i], self.heap[pai] = self.heap[pai], self.heap[i]
                i = pai
            else:
                break

        print("\nPaciente adicionado à agenda com sucesso!")

    # Consulta a raiz do Heap
    def quem_eh_o_proximo(self):
        if not self.heap:
            print("\nA agenda está vazia.")
            return None

        paciente = self.heap[0]

        print("\n===== PRÓXIMO PACIENTE =====")
        print(f"Nome: {paciente.nome_completo}")
        print(f"CPF: {paciente.cpf}")
        print(f"Idade: {paciente.idade} anos")

        return paciente

    # Reorganiza o Max-Heap
    def heapify(self, i):
        tamanho = len(self.heap)

        while True:
            maior = i
            esquerda = 2 * i + 1
            direita = 2 * i + 2

            if esquerda < tamanho and self.heap[esquerda].idade > self.heap[maior].idade:
                maior = esquerda

            if direita < tamanho and self.heap[direita].idade > self.heap[maior].idade:
                maior = direita

            if maior == i:
                break

            self.heap[i], self.heap[maior] = self.heap[maior], self.heap[i]
            i = maior

    # Remove o paciente de maior idade
    def remover_paciente_prioritario(self):
        if not self.heap:
            print("\nA agenda está vazia.")
            return None

        removido = self.heap[0]

        if len(self.heap) == 1:
            self.heap.pop()
        else:
            self.heap[0] = self.heap.pop()
            self.heapify(0)

        print(f"\nPaciente chamado: {removido.nome_completo}")
        print(f"Idade: {removido.idade} anos")

        return removido

    # Exibe a estrutura atual do Heap
    def exibir_agenda(self):
        if not self.heap:
            print("\nA agenda está vazia.")
            return

        print("\n===== HEAP DE ATENDIMENTOS =====")

        for i, paciente in enumerate(self.heap):
            print(
                f"Posição {i} | {paciente.nome_completo} | "
                f"CPF: {paciente.cpf} | Idade: {paciente.idade}"
            )

    # NOVO: Heap Sort em uma cópia do vetor
    def heap_sort(self):
        copia = self.heap.copy()

        def ajustar_heap(vetor, tamanho, i):
            while True:
                maior = i
                esquerda = 2 * i + 1
                direita = 2 * i + 2

                if esquerda < tamanho and vetor[esquerda].idade > vetor[maior].idade:
                    maior = esquerda

                if direita < tamanho and vetor[direita].idade > vetor[maior].idade:
                    maior = direita

                if maior == i:
                    break

                vetor[i], vetor[maior] = vetor[maior], vetor[i]
                i = maior

        n = len(copia)

        # Constrói o Max-Heap na cópia
        for i in range(n // 2 - 1, -1, -1):
            ajustar_heap(copia, n, i)

        # Heap Sort: gera ordem crescente
        for fim in range(n - 1, 0, -1):
            copia[0], copia[fim] = copia[fim], copia[0]
            ajustar_heap(copia, fim, 0)

        # Inverte para obter ordem decrescente
        copia.reverse()
        return copia

    # NOVO: imprime os pacientes ordenados
    def imprimir_agenda_ordenada(self):
        pacientes = self.heap_sort()

        if not pacientes:
            print("\nA agenda está vazia.")
            return

        print("\n===== AGENDA POR ORDEM DE IDADE =====")

        for posicao, paciente in enumerate(pacientes, start=1):
            print(
                f"{posicao}º - {paciente.nome_completo} | "
                f"CPF: {paciente.cpf} | Idade: {paciente.idade}"
            )

    # NOVO: informa quantas pessoas faltam
    def falta_quantos(self, cpf):
        pacientes = self.heap_sort()

        for posicao, paciente in enumerate(pacientes):
            if paciente.cpf == cpf:
                return posicao

        return None


def main():
    agenda = HeapAtendimentos()

    while True:
        print("\n======================================")
        print("       AGENDA PRIORITÁRIA - UBS")
        print("======================================")
        print("1 - Cadastrar atendimento")
        print("2 - Consultar próximo paciente")
        print("3 - Atender paciente prioritário")
        print("4 - Exibir Heap")
        print("5 - Imprimir agenda ordenada por idade")
        print("6 - Consultar quantas pessoas faltam")
        print("7 - Sair")
        print("======================================")

        opcao = input("Escolha uma opção: ")

        if opcao == "1":
            cpf_texto = input("CPF (11 dígitos): ")

            if not cpf_texto.isdigit() or len(cpf_texto) != 11:
                print("CPF inválido!")
                continue

            cpf = int(cpf_texto)
            nome = input("Nome completo: ")

            cartao_sus = input("Cartão SUS (15 dígitos): ")

            if not cartao_sus.isdigit() or len(cartao_sus) != 15:
                print("Cartão SUS inválido!")
                continue

            print("\n1 - Triagem")
            print("2 - Vacinação")
            print("3 - Consulta Agendada")

            tipo = input("Tipo de atendimento: ")

            tipos = {
                "1": "Triagem",
                "2": "Vacinação",
                "3": "Consulta Agendada"
            }

            if tipo not in tipos:
                print("Tipo inválido!")
                continue

            try:
                idade = int(input("Idade: "))
                if idade < 0:
                    print("Idade inválida!")
                    continue
            except ValueError:
                print("Digite uma idade válida!")
                continue

            agenda.cadastrar_atendimento_dia(
                cpf, nome, cartao_sus, tipos[tipo], idade
            )

        elif opcao == "2":
            agenda.quem_eh_o_proximo()
            input("\nPressione Enter para voltar ao menu...")

        elif opcao == "3":
            agenda.remover_paciente_prioritario()
            input("\nPressione Enter para voltar ao menu...")

        elif opcao == "4":
            agenda.exibir_agenda()
            input("\nPressione Enter para voltar ao menu...")

        elif opcao == "5":
            agenda.imprimir_agenda_ordenada()
            input("\nPressione Enter para voltar ao menu...")

        elif opcao == "6":
            cpf_texto = input("Digite o CPF do paciente: ")

            if not cpf_texto.isdigit() or len(cpf_texto) != 11:
                print("CPF inválido!")
                continue

            quantidade = agenda.falta_quantos(int(cpf_texto))

            if quantidade is None:
                print("\nPaciente não encontrado na agenda.")
            else:
                print(f"\nFaltam {quantidade} pessoa(s) antes desse paciente.")

            input("\nPressione Enter para voltar ao menu...")

        elif opcao == "7":
            print("\nSistema encerrado.")
            break

        else:
            print("\nOpção inválida!")


if __name__ == "__main__":
    main()
