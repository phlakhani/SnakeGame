## snake game   will create tkinter window then we put canvas in that window to create app

import tkinter as tk
from PIL import Image, ImageTk
from random import randint

MOVE_INCREMENT=20
moves_per_second=5
GAME_SPEED = 1000//moves_per_second    # use integer division(//) bcoz tkinter function after() doesnt accept float argument

class snake(tk.Canvas):     # snake class in now become canvas that we will put inside window

    def __init__(self):
        super().__init__(width=650, height=650, background="linen", highlightthickness=1)

        self.snake_positions = [(100,100), (80,100), (60,100)]
        self.food_positions = self.set_new_food_positions()
        self.score=0
        self.direction="right"
        self.bind_all("<Key>",self.on_key_press)    ## when any key is pressed from keyboard, on_key_press() fun is called




        self.load_asset()
        self.create_objects()    # used to place object(image) in app window
        self.after(75, self.perform_actions)
    def load_asset(self):
        try:
            self.snake_body_image = Image.open("./asset/snake.png")     # open image n give it to snake_body_image variable
            self.snake_body = ImageTk.PhotoImage(self.snake_body_image)    # ImageTk place image in tk app

            self.food_image = Image.open("./asset/food.png")  # open image n give it to snake_body_image variable
            self.food = ImageTk.PhotoImage(self.food_image)  # ImageTk place image in tk app
        except IOError as error:
            print(error)
            root.destroy()   # will close window

    def create_objects(self):
        self.create_text(150,20,text=f"Score:{self.score}   Speed:{moves_per_second}",
                         tag="score", fill="#f00a3d", font=("TkDefaultFont", 14))

        for x_postion, y_position in self.snake_positions:
            self.create_image(x_postion, y_position, image=self.snake_body, tag="snake")  # create_image method of canvas to put image on canvas
        self.create_image(*self.food_positions, image=self.food, tag="food")
        self.create_rectangle(40,30,640,640, outline="#20acfa")

    def move_snake(self):
        head_x_position, head_y_position= self.snake_positions[0]

        if self.direction == "Right":
            new_head_position = (head_x_position + MOVE_INCREMENT, head_y_position)
            self.snake_positions = [new_head_position] + self.snake_positions[:-1]
        elif self.direction == "Left":
            new_head_position = (head_x_position - MOVE_INCREMENT, head_y_position)
            self.snake_positions = [new_head_position] + self.snake_positions[:-1]
        elif self.direction == "Down":
            new_head_position = (head_x_position, head_y_position + MOVE_INCREMENT)
            self.snake_positions = [new_head_position] + self.snake_positions[:-1]
        elif self.direction == "Up":
            new_head_position = (head_x_position, head_y_position - MOVE_INCREMENT)
            self.snake_positions = [new_head_position] + self.snake_positions[:-1]


        for segment, position in zip(self.find_withtag("snake"), self.snake_positions):  # pick element from canvas n move to another position we give
            self.coords(segment, position)

    def perform_actions(self):
        if self.check_collision():
            self.end_game()
            return

        self.check_food_collision()
        self.move_snake()

        self.after(GAME_SPEED, self.perform_actions)


    def check_collision(self):
        head_x_position, head_y_position = self.snake_positions[0]
        return (
            head_x_position in (40,640) or
            head_y_position in (40,640) or
            (head_x_position, head_y_position) in self.snake_positions[1:]
            )

    def check_food_collision(self):
        if self.snake_positions[0] == self.food_positions:
            self.score += 1
            self.snake_positions.append(self.snake_positions[-1])
            self.create_image(*self.snake_positions[-1], image=self.snake_body, tag="snake")   # to grow snake

            if self.score % 10 == 0:     # every time score reaches multiple of 10 speed got increases
                global moves_per_second
                moves_per_second += 2
                global GAME_SPEED
                GAME_SPEED=1000//moves_per_second
            score=self.find_withtag("score")
            self.itemconfigure(score, text=f"Score:{self.score}   Speed:{moves_per_second}", tag="score")
            # this above method will allow to change or update properties by using tag  of the objects we created before

            self.food_positions = self.set_new_food_positions()
            self.coords(self.find_withtag("food"), self.food_positions)
            #print(GAME_SPEED)

    def set_new_food_positions(self):
        while True:
            x_position= randint(3,31) * MOVE_INCREMENT      # random x position from 60 to 620
            y_position = randint(3, 31) * MOVE_INCREMENT    # random y position from 60 to 620
            food_position=(x_position,y_position)

            if food_position not in self.snake_positions:      # new food should not be inside the snake
                return food_position

    def end_game(self):
        self.delete(tk.ALL)    # will delete everything in window including canvas
        self.create_text(
            self.winfo_height()/2,
            self.winfo_width()/2,
            text=f"Boom! GAME OVER Your Score: {self.score}",
            fill="#000",
            font=("TkDefaultFont", 25)
        )  # text in center

    def on_key_press(self, e):
        new_direction = e.keysym
        all_directions = ("Right", "Left", "Up", "Down")
        opposite_direction = ({"Up", "Down"}, {"Right", "Left"})
        if (new_direction in all_directions and
            {new_direction, self.direction} not in opposite_direction
        ):
            self.direction = new_direction







root =tk.Tk()   # will create main application window
root.title("Snake Game")
root.resizable(False, False)    # can't resize app window of width & height


board=snake()     # we create canvas
board.pack()    # pack() used to put any element into other element in tkinter, here we put canvas into tkinter main window
root.mainloop()   # will allow app to display
