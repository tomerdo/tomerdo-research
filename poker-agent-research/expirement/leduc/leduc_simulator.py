from leduc.leduc_game import LeducGame
from leduc.leduc_agent import LeducAgent

num_of_rounds = 1000
num_of_simulation = 10


def simulate_game(num_of_rounds):
    player1 = LeducAgent('player1', 100)
    player2 = LeducAgent('player2', 100)
    game = LeducGame(player1, player2)
    for i in range(num_of_rounds):
        if player1.money <= 0 or player2.money <= 0:
            break
        game.play_round(i)
    print(f'after {i} round player {player1.name} with {player1.money}$ and {player2.name} with {player2.money}$')
    return player1.money, player2.money


if __name__ == '__main__':
    player1_sum = 0
    player2_sum = 0
    for _ in range(num_of_simulation):
        player1_money, player2_money = simulate_game(num_of_rounds)
        player1_sum += player1_money
        player2_sum += player2_money
    print(f'after {num_of_simulation} simulations first player average profit is {player1_sum / num_of_simulation}$ '
          f'and second player average profit is {player2_sum / num_of_simulation}$')
