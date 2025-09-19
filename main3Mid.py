import random
import sys
import msvcrt
from datetime import datetime 
import csv
import os

# функция
def get_key():
    return msvcrt.getch().decode("utf-8").lower()

def clear_console():
    sys.stdout.write("\033[2J\033[H")
    sys.stdout.flush()

# эмодзи карта
EMOJI_MAP = {
    "#": "🟦",  # стена
    ".": "⚪",  # точка
    "P": "😋",  # пакман
    " ": "⬛",  # пустое
    "G": "👻",  # призрак
    "L": "❤️",  # жизнь
    "F": "🍒"   # бонусный фрукт
}

# загрузка карта
def load_map(file_name):
    with open(file_name, "r", encoding="utf-8") as f:
        return [list(line.strip()) for line in f.readlines()]

# сохранить результат
def save_result(player_name, score, result):
    now = datetime.now().strftime("%Y-%m-%d %H:%M")
    # txt
    with open("results.txt", "a", encoding="utf-8") as f:
        f.write(f"[{now}] Игрок: {player_name} | Очки: {score} | Результат: {result}\n")
    # csv
    with open("results.csv", "a", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)
        writer.writerow([player_name, score, result, now])

# меню
def print_menu():
    clear_console()
    print("=== Pac-Man ===")
    print("1. Начать игру")
    print("2. Рекорды")
    print("3. Выход")

def show_records():
    clear_console()
    print("=== Рекорды ===")
    if os.path.exists("results.csv"):
        with open("results.csv", encoding="utf-8") as f:
            for line in f:
                print(line.strip())
    else:
        print("Рекорды пока отсутствуют.")
    input("Нажмите Enter для возврата в меню...")

# игровое поле из файла
def start_game(player_name):
    field = load_map("map.txt")

    pacman_pos = [1,1]
    field[pacman_pos[0]][pacman_pos[1]] = "P"

    ghosts = [[1,len(field[0])-2],[len(field)-2,2]]
    for gx,gy in ghosts:
        field[gx][gy] = "G"

    score = 0
    lives = 3
    game_over = False
    pause = False
    step_counter = 0
    bonus_timer = 0
    bonus_pos = None

    def print_field():
        clear_console()
        for row in field:
            print("".join(EMOJI_MAP.get(cell,cell) for cell in row))
        print(f"Счет: {score} | Жизни: {lives}")
        remaining_dots = sum(row.count(".") for row in field)
        print(f"Осталось точек: {remaining_dots}")
        print("\nУправление: W A S D - движение, Q - выход, P - пауза")

    def move_pacman(dx,dy):
        nonlocal score,lives,pacman_pos,game_over
        new_x = (pacman_pos[0]+dx)%len(field)
        new_y = (pacman_pos[1]+dy)%len(field[0])
        target = field[new_x][new_y]
        if target != "#":
            if target == ".":
                score += 1
            elif target == "L":
                lives += 1
            elif target == "F":
                score += 50
            elif target == "G":
                lives -=1
                if lives<=0:
                    game_over=True
            field[pacman_pos[0]][pacman_pos[1]] = " "
            pacman_pos = [new_x,new_y]
            field[new_x][new_y] = "P"

    def move_ghosts():
        nonlocal game_over,lives
        new_positions=[]
        for gx,gy in ghosts:
            directions=[(-1,0),(1,0),(0,-1),(0,1)]
            random.shuffle(directions)
            for dx,dy in directions:
                nx=(gx+dx)%len(field)
                ny=(gy+dy)%len(field[0])
                if field[nx][ny] in [" ", ".","L","F"]:
                    field[gx][gy]=" "
                    if [nx,ny]==pacman_pos:
                        lives-=1
                        if lives<=0:
                            game_over=True
                    field[nx][ny]="G"
                    new_positions.append([nx,ny])
                    break
            else:
                new_positions.append([gx,gy])
        ghosts[:] = new_positions

    # игровой цикл
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
        elif key=="w":
            move_pacman(-1,0)
        elif key=="s":
            move_pacman(1,0)
        elif key=="a":
            move_pacman(0,-1)
        elif key=="d":
            move_pacman(0,1)

        move_ghosts()

        # бонус фрукты
        step_counter += 1
        if step_counter%10==0 and bonus_pos is None:
            empty_cells=[[i,j] for i,row in enumerate(field) for j,c in enumerate(row) if c==" "]
            if empty_cells:
                bonus_pos=random.choice(empty_cells)
                field[bonus_pos[0]][bonus_pos[1]]="F"
                bonus_timer=30
        if bonus_pos:
            bonus_timer-=1
            if bonus_timer<=0:
                field[bonus_pos[0]][bonus_pos[1]]=" "
                bonus_pos=None

        # победа если все точки собраны
        if all(cell not in ["."] for row in field for cell in row):
            game_over=True
            result_text="Победа!"
            break
    else:
        result_text="Поражение!"

    print_field()
    print("\n" + result_text)  
    save_result(player_name,score,result_text)

# главное меню
while True:
    print_menu()
    choice = get_key()
    if choice=="1":
        clear_console()
        print('Добро пожаловать в нашу игру "Pacman". Разработчик: Сагантай Адиль CS-204(s)')
        player_name=input("Введите имя игрока: ")
        start_game(player_name)
        input("\nНажмите Enter для выхода в меню...")
    elif choice=="2":
        show_records()
    elif choice=="3":
        break
