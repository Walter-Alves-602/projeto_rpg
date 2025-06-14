from random import randint
from typing import overload, Union

class DiceRoller:
    @staticmethod
    def roll_by_params(num_sides: int, num_dice: int=1, mod: int=0) -> int:
        """
        Rola um número específico de dados com um dado número de lados e aplica um modificador.

        Exemplo: roll_dice(6, 2, 3) rola 2d6 e adiciona 3.
        :param num_sides: Número de lados do dado (ex: 6 para d6).
        :param num_dice: Número de dados a rolar (padrão é 1).
        :param mod: Modificador a ser aplicado ao resultado total (padrão é 0).
        :return: Resultado total da rolagem dos dados mais o modificador.
        """
        if num_sides < 1 or num_dice < 1:
            raise ValueError("Number of sides and number of dice must be at least 1.")
        
        total = sum(randint(1, num_sides) for _ in range(num_dice))
        return total + mod
    
    @staticmethod
    def roll_by_notation(dice_notation: str) -> int:
        """
        Rolls dice based on a notation string like 'NdM+X' or 'NdM-X', where:
        - N is the number of dice to roll
        - M is the number of sides on each die
        - X is a modifier to add or subtract from the total roll
        :param dice_notation: String representing the dice roll notation.
        :return: Total result of the dice rolls plus the modifier.
        :raises ValueError: If the notation is invalid.
        :example: "2d6+3" rolls 2 six-sided dice and adds 3 to the total.
        """
        if 'd' not in dice_notation:
            raise ValueError("Invalid dice notation. Use format like 'NdM+X' or 'NdM-X'.")
        
        if "+" in dice_notation or "-" in dice_notation:
            parts = dice_notation.split('+') if '+' in dice_notation else dice_notation.split('-')
            mod = int(parts[1]) if '+' in dice_notation else -int(parts[1])
            dice_part = parts[0]
        else:
            dice_part = dice_notation
            mod = 0
        dice_params = dice_part.split('d')
        if len(dice_params) != 2:
            raise ValueError("Invalid dice notation. Use format like 'NdM+X' or 'NdM-X'.")
        return DiceRoller.roll_by_params(int(dice_params[1]), int(dice_params[0]), mod)
    
    @overload
    @staticmethod
    def roll( num_sides: int, num_dice: int = 1, mod: int = 0) -> int:
        """
        Rola um número específico de dados com um dado número de lados e aplica um modificador.

        Exemplo: roll_dice(6, 2, 3) rola 2d6 e adiciona 3.
        :param num_sides: Número de lados do dado (ex: 6 para d6).
        :param num_dice: Número de dados a rolar (padrão é 1).
        :param mod: Modificador a ser aplicado ao resultado total (padrão é 0).
        :return: Resultado total da rolagem dos dados mais o modificador.
        """
        ...
    @overload
    @staticmethod
    def roll( dice_notation: str) -> int:
        """
        Rola dados com base em uma notação de string (ex: 'NdM+X', 'NdM-X').

        Exemplo: roll_dice("2d6+3") rola 2 dados de 6 lados e adiciona 3.
        :param dice_notation: String representando a notação da rolagem de dados.
        :return: Resultado total da rolagem dos dados.
        :raises ValueError: Se a notação for inválida.
        """
        ...
    
    @staticmethod
    def roll( arg1: Union[int, str], num_dice: int = 1, mod: int = 0) -> int:
        """Rola dados com base em parâmetros ou em uma string de notação.
        :param arg1: O número de lados do dado (int) ou uma string de notação de dados (str).
        :param num_dice: Número de dados a rolar (o padrão é 1).
        :param mod: Modificador a ser aplicado ao resultado total da rolagem (o padrão é 0).
        :return: Resultado total da rolagem dos dados mais o modificador."""
        if isinstance(arg1, int):
            return DiceRoller.roll_by_params(arg1, num_dice, mod)
        elif isinstance(arg1, str):
            return DiceRoller.roll_by_notation(arg1)
            
if __name__ == "__main__":
    print(DiceRoller.roll_by_params(6, 2, 3))  # Rolls 2 six-sided dice and adds 3
    print(DiceRoller.roll_by_notation("2d6+3"))  # Rolls 2 six-sided dice and adds 3
    print(DiceRoller.roll_by_notation("2d6-3"))
    print(DiceRoller.roll("2d6"))  # Rolls 2 six-sided dice with no modifier
    print(DiceRoller.roll(6, 2, 3))  # Rolls 2 six-sided dice and adds 3
