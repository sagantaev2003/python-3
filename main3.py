import random
import sys
import msvcrt
from datetime import datetime

# --- Функции для консоли ---
def get_key():
    return msvcrt.getch().decode("utf-8").lower()

def clear_console():
    sys.stdout.write("\033[2J\033[H")
    sys.stdout.flush()

# --- Эмодзи карта ---
EMOJI_MAP = {
    "#": "🟦",  # стена
    ".": "⚪",  # точка
    "P": "😋",  # Pac-Man
    " ": "⬛",  # пустое
    "G": "👻"   # призрак
}

# --- Инициализация карты ---
RAW_MAP = [
    "############################",
    "#............##............#",
    "#.####.#####.##.#####.####.#",
    "#.####.#####.##.#####.####.#",
    "#..........................#",
    "#.####.##.########.##.####.#",
    "#......##....##....##......#",
    "######.#####.##.#####.######",
    "#..........................#",
    "#..........######..........#",
    "#.######...####....######..#",
    "#..........................#",
    "#.####.##.########.##.####.#",
    "#.####.##....##....##.####.#",
    "#......######.##.######....#",
    "#..........................#",
    "#.####.#####.##.#####.####.#",
    "#............##............#",
    "#............##............#",
    "############################",
]

field = [list(row) for row in RAW_MAP]

# --- Координаты персонажей ---
pacman_x, pacman_y = 1, 1
field[pacman_x][pacman_y] = "P"

# Призраки
ghosts = [(1, 24), (17, 12), (17, 18)]
for gx, gy in ghosts:
    field[gx][gy] = "G"

score = 0
game_over = False

# --- Отображение поля ---
def print_field():
    clear_console()
    for row in field:
        print("".join(EMOJI_MAP.get(cell, cell) for cell in row))
    
    # Счёт Pac-Man
    print(f"Счет: {score}")
    
    # Счётчик оставшихся точек
    remaining_dots = sum(row.count(".") for row in field)
    print(f"Осталось точек: {remaining_dots}")

    # Подсказка управления
    print("\nУправление: W - движение вверх, A - движение влево, S - движение вниз, D - движение вправо, Q - выход из игры ")


# --- Движение Pac-Man ---
def move_pacman(dx, dy):
    global pacman_x, pacman_y, score, game_over
    new_x, new_y = pacman_x + dx, pacman_y + dy
    target = field[new_x][new_y]
    if target != "#":
        if target == ".":
            score += 1
        elif target == "G":
            game_over = True
        field[pacman_x][pacman_y] = " "
        pacman_x, pacman_y = new_x, new_y
        field[pacman_x][pacman_y] = "P"

# --- Движение призраков ---
def move_ghosts():
    global ghosts, game_over
    new_positions = []
    for gx, gy in ghosts:
        directions = [(-1,0),(1,0),(0,-1),(0,1)]
        random.shuffle(directions)
        for dx, dy in directions:
            nx, ny = gx+dx, gy+dy
            if field[nx][ny] in [" ", "."]:
                field[gx][gy] = " "
                if (nx, ny) == (pacman_x, pacman_y):
                    game_over = True
                field[nx][ny] = "G"
                new_positions.append((nx, ny))
                break
        else:
            new_positions.append((gx, gy))
    ghosts[:] = new_positions

# --- Сохранение результата ---
def save_result(player_name, score, result):
    with open("results.txt", "a", encoding="utf-8") as f:
        now = datetime.now().strftime("%Y-%m-%d %H:%M")
        f.write(f"[{now}] Игрок: {player_name} | Очки: {score} | Результат: {result}\n")

# --- Основной игровой цикл ---
print('Добро пожаловать в нашу игру "Pacman". Разработчик: Сагантай Адиль CS-204(s)')
player_name = input("Введите имя игрока: ")

while not game_over:
    print_field()
    key = get_key()
    if key == "w":
        move_pacman(-1, 0)
    elif key == "s":
        move_pacman(1, 0)
    elif key == "a":
        move_pacman(0, -1)
    elif key == "d":
        move_pacman(0, 1)
    elif key == "q":
        game_over = True
    move_ghosts()
    # Проверка победы
    if all(cell != "." for row in field for cell in row):
        game_over = True
        result_text = "Все точки собраны! Победа!"
        break
else:
    result_text = "Вас поймал призрак! Поражение!"

print_field()
print(result_text)
save_result(player_name, score, result_text)
