import tkinter as tk
import random
from tkinter import PhotoImage


# --------------------------------------------------


# Ensure High DPI awareness on Windows
try:
    from ctypes import windll
    windll.shcore.SetProcessDpiAwareness(1)
except:
    pass


# --------------------------------------------------



class SnakeGame:
    def __init__(self, master):
        self.master = master
        self.master.title("Snake Game")
        self.master.geometry("400x450")
        self.master.resizable(False, False)

        self.canvas = tk.Canvas(self.master, bg="black", width=400, height=400)
        self.canvas.pack()

        self.score_label = tk.Label(self.master, text="Score: 0", font=("Arial", 16))
        self.score_label.pack()

        self.snake = [(100, 100), (90, 100), (80, 100)]
        self.snake_direction = "Right"
        self.food = None
        self.create_food()

        self.score = 0
        self.game_over = False

        self.master.bind("<KeyPress>", self.change_direction)

        self.update()


    def create_food(self):
        x = random.randint(0, 39) * 10
        y = random.randint(0, 39) * 10
        self.food = (x, y)
        self.canvas.create_oval(x, y, x + 10, y + 10, fill="red", tags="food")


    def move_snake(self):
        head = self.snake[0]
        if self.snake_direction == "Right":
            new_head = (head[0] + 10, head[1])
        elif self.snake_direction == "Left":
            new_head = (head[0] - 10, head[1])
        elif self.snake_direction == "Up":
            new_head = (head[0], head[1] - 10)
        elif self.snake_direction == "Down":
            new_head = (head[0], head[1] + 10)

        self.snake.insert(0, new_head)

        if new_head == self.food:
            self.score += 1
            self.score_label.config(text=f"Score: {self.score}")
            self.canvas.delete("food")
            self.create_food()
        else:
            self.snake.pop()

        if (new_head[0] < 0 or new_head[0] >= 400 or
            new_head[1] < 0 or new_head[1] >= 400 or
            new_head in self.snake[1:]):
            self.game_over = True


    def change_direction(self, event):
        key = event.keysym
        if (key == "Right" and not self.snake_direction == "Left"):
            self.snake_direction = key
        elif (key == "Left" and not self.snake_direction == "Right"):
            self.snake_direction = key
        elif (key == "Up" and not self.snake_direction == "Down"):
            self.snake_direction = key
        elif (key == "Down" and not self.snake_direction == "Up"):
            self.snake_direction = key


    def draw_snake(self):
        self.canvas.delete("snake")
        for segment in self.snake:
            self.canvas.create_rectangle(segment[0], segment[1],
                                         segment[0] + 10, segment[1] + 10,
                                         fill="green", tags="snake")


    def update(self):
        if not self.game_over:
            self.move_snake()
            self.draw_snake()
            self.master.after(100, self.update)
        else:
            self.canvas.create_text(200, 200, text="Game Over!", 
                                    font=("Arial", 24), fill="white")


if __name__ == "__main__":
    root = tk.Tk()
    logo = PhotoImage(file="logo.png")
    root.iconphoto(False, logo)
    game = SnakeGame(root)
    root.mainloop()
