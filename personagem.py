from modificadores_raca import MODIFICADORES_RACA


class ModificadorRacaAdapter:
    def obter_modificadores(self, raca):
        return MODIFICADORES_RACA.get(raca, {})


class Personagem:
    def __init__(
        self,
        nome,
        jogador,
        raca,
        classe,
        nivel,
        forca,
        destreza,
        constituicao,
        inteligencia,
        sabedoria,
        carisma,
    ):
        self.nome = nome
        self.jogador = jogador
        self.raca = raca
        self.classe = classe
        self.nivel = nivel

        self.atributos = {
            "forca": forca,
            "destreza": destreza,
            "constituicao": constituicao,
            "inteligencia": inteligencia,
            "sabedoria": sabedoria,
            "carisma": carisma,
        }
        #iplementar a logica de hp
        self.pontos_de_vida_max = 0
        self.pontos_de_vida_atual = 0 #
        self.pontos_de_experiencia = 0

        self.inventario = []


        self.modificadores_raca = self.calcular_modificadores_raca()
        # Aplicando os modificadores de raça
        for atributo in self.atributos:
            if atributo in self.modificadores_raca:
                self.atributos[atributo] += self.modificadores_raca[atributo]

    def calcular_modificadores_raca(self):
        return ModificadorRacaAdapter.obter_modificadores(self, self.raca)
    
    #inventario
    def adicionar_item_inventario(self, item):
        self.inventario.append(item)

    def remover_item_inventario(self, item):
        if item in self.inventario:
            self.inventario.remove(item)
        else:
            print(f"Item {item} não encontrado no inventário.")


if __name__ == "__main__":
    # Exemplo de como criar um personagem
    meu_personagem = Personagem(
        nome="Tordek",
        jogador="Você",
        raca="Anão da Colina",
        classe="Guerreiro",
        nivel=1,
        forca=15,
        destreza=10,
        constituicao=14,
        inteligencia=8,
        sabedoria=12,
        carisma=9,
    )

    print(f"Nome: {meu_personagem.nome}")
    print(f"Raça: {meu_personagem.raca}")
    print(f"Força: {meu_personagem.atributos['forca']}")
    print(f"Destreza: {meu_personagem.atributos['destreza']}")
    print(f"Constituição: {meu_personagem.atributos['constituicao']}")
