import copy
import random
import sys
from time import perf_counter

"""
Tres en raya con Minimax
"""
class TicTacToe:
    """
    Esta clase implementa el algoritmo minimax para
    llevar a cabo un juego de tres en raya como matriz
    """
    # Siempre inicia el jugador que elija la "X"
    X = "X"     # Extremo max
    O = "O"     # Extremo min
    EMPTY = None
    def initial_state(self):
        """
        Inicializar el estado del juego
        """
        return [[self.EMPTY, self.EMPTY, self.EMPTY],
                [self.EMPTY, self.EMPTY, self.EMPTY],
                [self.EMPTY, self.EMPTY, self.EMPTY]]

    def player(self, board):
        """
        Retorna al jugador con el turno para jugar
        """
        x_count = sum(row.count(self.X) for row in board)
        o_count = sum(row.count(self.O) for row in board)

        if x_count > o_count: # Como 'X' siempre inicia entonces si lleva mayor cantidad de turnos, significa que va 'O'
            return self.O
        else:
            return self.X

    def actions(self, board):
      """
      Retorna un conjunto de posibles movimientos (fila,columna) según el estado actual del tablero
      """
      actions_set = set()

      for row in range(3):
          for col in range(3):
              if board[row][col] == self.EMPTY:
                  actions_set.add((row, col))

      return actions_set

    def result(self, board, action):
        """
        Retorna el tablero resultante del movimiento que se recibe
        """
        if board[action[0]][action[1]] is not self.EMPTY:
            raise Exception("Movimiento no es válido")

        new_board = copy.deepcopy(board)  # Crear una copia independiente a la variable de tablero original
        new_board[action[0]][action[1]] = self.player(board)  # player va a retornar el jugador del turno actual y se asginará a la casilla del tablero
        return new_board

    def winner(self, board):
        """
        Retorna el ganador del juego si no hay empate
        """
        for player in [self.X, self.O]:
            # Revisar filas, columnas y diagonales
            if any(all(board[i][j] == player for j in range(3)) for i in range(3)) or \
              any(all(board[i][j] == player for i in range(3)) for j in range(3)) or \
              all(board[i][i] == player for i in range(3)) or \
              all(board[i][2 - i] == player for i in range(3)):
                return player
        return None

    def terminal(self, board):
        """
        Retorna True si el juego terminó, False en caso contrario
        """
        # Un juego ha terminado si la función winner retorna a algún jugador o 
        # si ninguna casilla está vacía (empate)
        return self.winner(board) is not None or all(board[i][j] is not self.EMPTY for i in range(3) for j in range(3))

    def utility(self, board):
        """
        Retorna 1 si X ganó, -1 si O ganó, 0 empate
        """
        winner = self.winner(board)
        if winner == self.X:
            return 1
        elif winner == self.O:
            return -1
        else:
            return 0
          
    def minimax(self, board):
        """
        Retorna el movimiento óptimo para el jugador activo
        """
        if self.terminal(board):
            return None

        if self.player(board) == self.X:
            return self.max_value(board)[1]
        else:
            return self.min_value(board)[1]

    def max_value(self, board):
        """
        Función recursiva que devuelve el valor máximo de una acción de 
        todas las acciones posibles en el estado actual
        """
        if self.terminal(board):  # Verificar si el juego ha terminado
            return self.utility(board), None

        max_value = float('-inf')
        max_actions = []

        for action in self.actions(board):
            value, _ = self.min_value(self.result(board, action))
            if value > max_value:
                max_value = value
                max_actions = [action]
            elif value == max_value:  # Si hay movimientos con el mismo puntaje, se agrega a la lista de acciones
                max_actions.append(action)

        # Se elige aleatoriamente alguna de las acciones con los mayores puntajes
        # Si solo hay una con el valor máximo, solo esa se podrá elegir
        return max_value, random.choice(max_actions)

    def min_value(self, board):
        """
        Función recursiva que devuelve el valor mínimo de una acción de 
        todas las acciones posibles en el estado actual
        """
        if self.terminal(board):  # Verificar si el juego ha terminado
            return self.utility(board), None

        min_value = float('inf')
        min_actions = []

        for action in self.actions(board):
            value, _ = self.max_value(self.result(board, action))
            if value < min_value:
                min_value = value
                min_actions = [action]
            elif value == min_value:  # Si hay movimientos con el mismo puntaje, se agrega a la lista de acciones
                min_actions.append(action)

        # Se elige aleatoriamente alguna de las acciones con los menores puntajes
        # Si solo hay una con el valor mínimo, solo esa se podrá elegir
        return min_value, random.choice(min_actions)


"""
Clase para ejecutar el juego
"""

class Runner:
    def __init__(self):
        self.tic_tac_toe = TicTacToe()
        self.user = None
        self.board = self.tic_tac_toe.initial_state()
        self.ai_turn = False

    def run_game(self):
        while True:
            # El usuario elige un jugador
            random=self.choose_player()
            if random:
                self.random_oponent_test()
            else:
                while True:
                    if self.user is None:
                        break
                    self.print_board()
                    self.play_game()
            
    def random_oponent_test(self):
        test_scenarios=[self.tic_tac_toe.X,self.tic_tac_toe.O,None]
        msg="\nEjecutando 500 pruebas del escenario: "
        # las columnas son: P1, P2, Empates
        # Las Filas: Random - Minmax
        #            Minmax - Random
        #            Minmax - Minmax
        scenario_stadistics=[["Random - Minmax", 0,0,0],
                             ["Minmax - Random", 0,0,0],
                             ["Minmax - Minmax", 0,0,0]]
        winner = None
    
        for i,test in enumerate(test_scenarios):
            scenario_func = self.play_game_AI if test is None else self.play_game_random
            match i:
                case 0:
                    print(msg, "Random - Minmax")
                case 1:
                    print(msg, "Minmax - Random")
                case 2:
                    print(msg, "Minmax - Minmax")
            for j in range(500):
                print(f"\n------------ Prueba #{j+1} ------------")
                self.user = self.tic_tac_toe.X if test is None else test
                while True:
                    if self.user is None:
                        match(winner):
                            case self.tic_tac_toe.X:
                                scenario_stadistics[i][1] += 1
                            case self.tic_tac_toe.O:
                                scenario_stadistics[i][2] += 1
                            case None:
                                scenario_stadistics[i][3] += 1
                        break
                    #self.print_board()
                    winner = scenario_func()

        self.test_stadistics(scenario_stadistics)
    

    def print_board(self):
        # Imprimir el tablero de juego
        for row in self.board:
            print(" | ".join(cell if cell is not None else " " for cell in row))
            print("-" * 9)

    def test_stadistics(self,scenario_stadistics):
        print("\nPruebas terminadas... Imprimiendo resultados...\n")
        print("{:<17} {:<8} {:<8} {:<8}".format("Estilo de juego","P1 Gana", "P2 Gana", "Empate"))
        for stats in scenario_stadistics:
            scenario,p1,p2,draw=stats
            print("{:<17} {:<8} {:<8} {:<8}".format(scenario,p1,p2,draw))

    def choose_player(self):
        print("Tres en raya")
        print("Elija un jugador:")
        print("1. X")
        print("2. O")
        print("3. Prueba contra Aleatorio")
        print("0. Salir")

        while True:
            choice = input("Ingrese su respuesta: ")
            if choice == "1":
                self.user = self.tic_tac_toe.X
                return False
            elif choice == "2":
                self.user = self.tic_tac_toe.O
                return False
            elif choice == "3":
                return True
            elif choice == "0":
                sys.exit()
            else:
                print("Debe elegir opción 1 o 2")

    def play_game(self):
        # Si es el turno del usuario, obtener el input
        if self.user == self.tic_tac_toe.player(self.board):
            self.get_user_move()
        # Si es el turno de la IA, ejecutar algoritmo minimax
        else:
            self.make_ai_move()

        # Verificar si el juego ha terminado
        if self.tic_tac_toe.terminal(self.board):
            self.print_board()
            winner = self.tic_tac_toe.winner(self.board)
            if winner is not None:
                print(f"Game over. {winner} es el ganador!")
            else:
                print("Game over. Es un empate!")
            self.reset_game()

    def play_game_random(self):
        # Si es el turno del oponente aleatorio se elige una pos aleatoria
        if self.user == self.tic_tac_toe.player(self.board):
            self.get_random_move()
        # Si es el turno de la IA, ejecutar algoritmo minimax
        else:
            self.make_ai_move()

        # Verificar si el juego ha terminado
        if self.tic_tac_toe.terminal(self.board):
            self.print_board()
            winner = self.tic_tac_toe.winner(self.board)
            if winner is not None:
                print(f"Game over. {winner} es el ganador!")
                self.reset_game()
                return winner
            else:
                print("Game over. Es un empate!")
                self.reset_game()
                return None
            

    def play_game_AI(self):
        # La IA juega contra si misma
        self.make_ai_move()

        # Verificar si el juego ha terminado
        if self.tic_tac_toe.terminal(self.board):
            self.print_board()
            winner = self.tic_tac_toe.winner(self.board)
            if winner is not None:
                print(f"Game over. {winner} es el ganador!")
                self.reset_game()
                return winner
            else:
                print("Game over. Es un empate!")
                self.reset_game()
                return None

    def get_user_move(self):
        print(f"Es tu turno, {self.user}")
        while True:
            try:
                move = input("Ingrese su movimiento (fila,col): ")
                row, col = map(int, move.split(","))
                if 0 <= row <= 2 and 0 <= col <= 2:
                    if self.board[row][col] is None:
                        self.board = self.tic_tac_toe.result(self.board, (row, col))
                        break
                    else:
                        print("Esta celda ya está ocupada. Intente de nuevo.")
                else:
                    print("El número de fila y columna deben ser entre 0 y 2.")
            except (ValueError, IndexError):
                print("Valor incorrecto. Debe ingresar números entre 0 y 2, separados por una coma.")

    def get_random_move(self):
        print(f"El oponente aleatorio va ser su movimiento")

        empty_spaces = []

        for i,row in enumerate(self.board):
            for j,element in enumerate(row):
                if element is None:
                    empty_spaces.append((i,j))
        
        random_pos = random.choice(empty_spaces)

        self.board = self.tic_tac_toe.result(self.board, random_pos) 

    def make_ai_move(self):
        print("La IA va a hacer un movimiento\n")
        move = self.tic_tac_toe.minimax(self.board)
        self.board = self.tic_tac_toe.result(self.board, move)

    def reset_game(self):
        self.user = None
        self.board = self.tic_tac_toe.initial_state()

if __name__ == "__main__":
    runner = Runner()
    runner.run_game()