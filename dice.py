import random
import time
import getpass
import hashlib


HASHED_PASSWORD = "b109f3bbbc244eb82441917ed06d618b9008dd09b3befd1b5e07394c706a8bb980b1d7785e5976ec049b46df5f1326af5a2ea6d103fd07c95385ffab0cacbc86"
USERS = ('User1', 'User2', 'User3', 'User4', 'User5')

def login(max_attempts=5):
    attempts = 0
    while attempts < max_attempts:
        username = input('What is your username? ')
        password = getpass.getpass('What is your password? ')

        # [OPTIONAL] add a salt
        if username not in USERS or HASHED_PASSWORD != hashlib.sha512(password.encode()).hexdigest():
            print('Something went wrong, try again')
            attempts += 1
            continue

        print(f'Welcome, {username} you have been successfully logged in.')
        return username
    print("Too many tries, exiting")
    exit()

if __name__ == '__main__':
    user = login()

def roll():
    die1 = random.randint(1, 6)
    die2 = random.randint(1, 6)
    change = 10 if (die1 + die2) % 2 == 0 else -5
    points = die1 + die2 + change
    if die1 == die2:
        points += random.randint(1, 6)
    return points


def game(user1, user2):
    player1_points = 0
    player2_points = 0
    for i in range(1,5):
        player1_points += roll()
        print(f'After this round {user1} you now have: {player1_points} Points')
        time.sleep(1)
        player2_points += roll()
        print(f'After this round {user2} you now have: {player2_points} Points')
        time.sleep(1)

    player1_tiebreaker = 0
    player2_tiebreaker = 0
    if player1_points == player2_tiebreaker:
        while player1_tiebreaker == player2_tiebreaker:
            player1_tiebreaker = random.randint(1,6)
            player2_tiebreaker = random.randint(1,6)

    player1_win = (player1_points + player1_tiebreaker) > (player2_points, player2_tiebreaker)
    return (player1_points, player1_win), (player2_points, not player2_win)


def add_winner(winner):
    with open('Winner.txt', 'a') as f:
        f.write('{winner[0]},{winner[1]}\n')


def get_leaderboard():
    with open('Leaderboard.txt', 'r') as f:
        return [line.replace('\n','') for line in f.readlines()]


def update_leaderboard(leaderboard, winner):
    for idx, item in enumerate(leaderboard):
        if item.split(', ')[1] == winner[1] and int(item.split(', ')[0]) < int(winner[0]):
                leaderboard[idx] = '{}, {}'.format(winner[0], winner[1])
        else:
            pass
    leaderboard.sort(reverse=True)


def save_leaderboard(leaderboard):
    with open('Leaderboard.txt', 'w') as f:
        for item in leaderboard:
            f.write(f'{item}\n')


def main():
    user1 = login()
    user2 = login()
    (player1, player1_win), (player2, player2_win) = game(user1, user2)
    if player1_win:
        winner = (player1, user1)
    else:
        winner = (player2, user2)
    print('Well done, {winner[1]} you won with {winner[0]} Points')
    add_winner(winner)
    leaderboard = get_leaderboard()
    update_leaderboard(leaderboard, winner)
    save_leaderboard(leaderboard)


if __name__ == '__main__':
    main()
