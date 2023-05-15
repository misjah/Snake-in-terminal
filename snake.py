import curses
import random
import time

# set up the game window
screen = curses.initscr()
curses.curs_set(0)
screen_height, screen_width = screen.getmaxyx()
game_window = curses.newwin(screen_height - 1, screen_width - 1, 0, 0)
game_window.keypad(True)
game_window.timeout(100)
curses.cbreak()  # disable input buffering

# set up the initial snake and food positions
snake_x = screen_width // 4
snake_y = screen_height // 2
snake = [[snake_y, snake_x], [snake_y, snake_x - 1], [snake_y, snake_x - 2]]
food = [screen_height // 2, screen_width // 2]
game_window.addch(food[0], food[1], curses.ACS_PI)

# set up initial direction
direction = curses.KEY_RIGHT

# set up initial score
score = 0

# main game loop
while True:
    # get user input
    next_direction = game_window.getch()
    if next_direction in [curses.KEY_LEFT, curses.KEY_RIGHT, curses.KEY_UP, curses.KEY_DOWN]:
        direction = next_direction
    elif next_direction == ord('p'):
        while True:
            pause_key = game_window.getch()
            if pause_key == ord('p'):
                break

    # move the snake
    new_head = [snake[0][0], snake[0][1]]
    if direction == curses.KEY_RIGHT:
        new_head[1] += 1
    elif direction == curses.KEY_LEFT:
        new_head[1] -= 1
    elif direction == curses.KEY_UP:
        new_head[0] -= 1
    elif direction == curses.KEY_DOWN:
        new_head[0] += 1
    snake.insert(0, new_head)

    # check if the snake has hit the wall or itself
    if snake[0][0] in [0, screen_height - 1] or snake[0][1] in [0, screen_width - 1] or snake[0] in snake[1:]:
        curses.endwin()
        print("Game Over!")
        print(f"Your score is: {score}")
        break

    # check if the snake has eaten the food
    if snake[0] == food:
        score += 10  # increment the score
        food = None
        while food is None:
            new_food = [random.randint(1, screen_height - 2), random.randint(1, screen_width - 2)]
            food = new_food if new_food not in snake else None
        game_window.addch(food[0], food[1], curses.ACS_PI)
    else:
        tail = snake.pop()
        game_window.addch(tail[0], tail[1], ' ')

    # draw the snake
    for i, point in enumerate(snake):
        if i == 0:
            game_window.addch(point[0], point[1], curses.ACS_CKBOARD)
        else:
            game_window.addch(point[0], point[1], curses.ACS_BLOCK)

    # update the screen
    game_window.refresh()

    # pause briefly before next iteration
    time.sleep(0.1)
# created by ChatGPT
