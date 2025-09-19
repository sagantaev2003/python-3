import random
import sys
import msvcrt
import os

#  функция
def get_key():
    return msvcrt.getch().decode("utf-8").lower()

def clear_console():
    sys.stdout.write("\033[2J\033[H")
    sys.stdout.flush()

# эмодзи карта
EMOJI_MAP = {
    "#": "🟦",  # стена
    ".": "⚪",  # точка
    "P1": "😋", # пакман 1
    "P2": "😎", # пакман2
    " ": "⬛",  # пустое
    "G": "👻"   # призрак
}

# загрузка карта
def load_map(file_name):
    with open(file_name, "r", encoding="utf-8") as f:
        return [list(line.strip()) for line in f.readlines()]

# сохранение результат
from datetime import datetime
def save_result(player_name, score, result):
    now = datetime.now().strftime("%Y-%m-%d %H:%M")
    with open("results.txt", "a", encoding="utf-8") as f:
        f.write(f"[{now}] Игрок: {player_name} | Очки: {score} | Результат: {result}\n")

# игровое поле
def start_game(player1, player2):
    field = load_map("map.txt")
    pac1_pos = [1,1]
    pac2_pos = [len(field)-2,len(field[0])-2]
    field[pac1_pos[0]][pac1_pos[1]]="P1"
    field[pac2_pos[0]][pac2_pos[1]]="P2"

    ghosts=[[1,len(field[0])-2],[len(field)-2,2]]
    for gx,gy in ghosts:
        field[gx][gy]="G"

    score1=0
    score2=0
    mission_points=50
    game_over=False
    pause=False
    mission_done=False  # сообщение о миссия

    def print_field():
        clear_console()
        for row in field:
            display_row=""
            for c in row:
                if c=="P1":
                    display_row+=EMOJI_MAP["P1"]
                elif c=="P2":
                    display_row+=EMOJI_MAP["P2"]
                else:
                    display_row+=EMOJI_MAP.get(c,c)
            print(display_row)
        print(f"{player1}: {score1} очков | {player2}: {score2} очков")
        remaining_dots = mission_points - (score1 + score2)
        print(f"Осталось точек до миссии: {max(remaining_dots,0)}")
        if mission_done:
            print(" Миссия выполнена! Продолжайте собирать точки!")
        print("Управление: W A S D - Игрок 1, I J K L - Игрок 2, Q - выход, P - пауза")

    def move_pacman(pos, dx, dy):
        nonlocal score1, score2, pac1_pos, pac2_pos
        new_x=(pos[0]+dx)%len(field)
        new_y=(pos[1]+dy)%len(field[0])
        target=field[new_x][new_y]
        if target!="#":
            if target==".":
                if pos==pac1_pos: score1+=1
                else: score2+=1
            elif target=="G":
                if pos==pac1_pos: score1=max(score1-5,0)
                else: score2=max(score2-5,0)
            field[pos[0]][pos[1]]=" "
            pos[0],pos[1]=new_x,new_y
            if pos==pac1_pos: field[new_x][new_y]="P1"
            else: field[new_x][new_y]="P2"

    def move_ghosts():
        new_positions=[]
        for gx,gy in ghosts:
            directions=[(-1,0),(1,0),(0,-1),(0,1)]
            random.shuffle(directions)
            for dx,dy in directions:
                nx=(gx+dx)%len(field)
                ny=(gy+dy)%len(field[0])
                if field[nx][ny] in [" ", "."]:
                    field[gx][gy]=" "
                    if [nx,ny]==pac1_pos:
                        score1=max(score1-5,0)
                    if [nx,ny]==pac2_pos:
                        score2=max(score2-5,0)
                    field[nx][ny]="G"
                    new_positions.append([nx,ny])
                    break
            else:
                new_positions.append([gx,gy])
        ghosts[:] = new_positions

    while not game_over:
        print_field()
        key=get_key()
        if key=="p":
            pause=not pause
        if pause:
            continue
        if key=="q":
            game_over=True
            result_text="Выход"
            break
        elif key in ["w","a","s","d"]:
            if key=="w": move_pacman(pac1_pos,-1,0)
            elif key=="s": move_pacman(pac1_pos,1,0)
            elif key=="a": move_pacman(pac1_pos,0,-1)
            elif key=="d": move_pacman(pac1_pos,0,1)
        elif key in ["i","j","k","l"]:
            if key=="i": move_pacman(pac2_pos,-1,0)
            elif key=="k": move_pacman(pac2_pos,1,0)
            elif key=="j": move_pacman(pac2_pos,0,-1)
            elif key=="l": move_pacman(pac2_pos,0,1)

        move_ghosts()

        if score1+score2>=mission_points and not mission_done:
            mission_done=True  # вкл флаг для сообщения
    print_field()
    result_text="Игра окончена!"
    print(result_text)
    save_result(player1, score1, result_text)
    save_result(player2, score2, result_text)

# главное меню
while True:
    clear_console()
    print("=== Pac-Man ===")
    print("1. Начать игру")
    print("2. Рекорды")
    print("3. Выход")
    choice=get_key()
    if choice=="1":
        clear_console()
        print('Добро пожаловать в игру "Pacman" на одной клавиатуре. Разработчик: Сагантай Адиль CS-204(s)')
        player1=input("Имя игрока 1: ")
        player2=input("Имя игрока 2: ")
        start_game(player1,player2)
    elif choice=="2":
        clear_console()
        if os.path.exists("results.txt"):
            with open("results.txt", encoding="utf-8") as f:
                for line in f:
                    print(line.strip())
        else:
            print("Рекорды пока отсутствуют.")
        input("Нажмите Enter для возврата в меню...")
    elif choice=="3":
        break
