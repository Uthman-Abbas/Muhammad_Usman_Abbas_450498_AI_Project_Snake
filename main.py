import tkinter as tk
import random


class SnakeGame:
    def __init__(self, master):
        self.master = master
        self.master.title("Snake Game")
        self.master.geometry("620x650")
        self.master.resizable(False, False)

        self.canvas = tk.Canvas(self.master, bg="black", width=600, height=600)
        self.canvas.pack()

        self.obstacles = [(200, 200), (400, 400), (400, 200), (200, 400),
                          (580, 580), (580, 560), (560, 580),
                          (0, 580), (0, 560), (20, 580),
                          (0, 0), (0, 20), (20, 0),
                          (580, 0), (580, 20), (560, 0)]

        self.game_over = False  # Initialize game_over attribute
        self.enemy_out = False

        self.score = 0  # Initialize score variable
        self.score_label = tk.Label(self.master, text=f"Your Score: {self.score}",
                                    font=("Helvetica", 16), fg="white", bg="white")
        self.score_label.pack()

        self.snake = [(100, 100), (90, 100), (80, 100)]
        self.direction = "Right"
        self.last_direction = None  # Add a variable to store the last direction

        self.enemy_score = 0  # New variable to track enemy snake's score

        self.score_label = tk.Label(self.master, text=f"Your Score: {self.score}",
                                    font=("Helvetica", 16), fg="white", bg="black")
        self.score_label.place(x=10, y=615)

        self.enemy_score_label = tk.Label(self.master, text=f"AI Score: {self.enemy_score}",
                                          font=("Helvetica", 16), fg="white", bg="black")
        self.enemy_score_label.place(x=420, y=615)  # Adjust x and y as needed

        self.enemy_snake = [(500, 500), (510, 500), (520, 500)]  # Initial position for the enemy snake
        self.enemy_direction = "Left"  # Initial direction for the enemy snake
        self.enemy_last_direction = None  # Add a variable to store the last direction for the enemy snake

        self.food = self.create_food()

        self.master.bind("<KeyPress>", self.change_direction)

        self.update()

    def create_food(self):
        while True:
            x = random.randint(0, 29) * 20
            y = random.randint(0, 29) * 20
            food_coords = (x, y)

            # Check if the food overlaps with any obstacle
            overlapping_obstacle = any(
                self.canvas.find_overlapping(x, y, x + 20, y + 20) and
                obstacle in self.obstacles for obstacle in self.canvas.find_withtag("obstacle")
            )

            if not overlapping_obstacle:
                break

        food = self.canvas.create_rectangle(x, y, x + 20, y + 20, fill="red")
        return food

    def move_snake(self):
        head = self.snake[0]
        if self.direction == "Right":
            new_head = (head[0] + 20, head[1])
        elif self.direction == "Left":
            new_head = (head[0] - 20, head[1])
        elif self.direction == "Up":
            new_head = (head[0], head[1] - 20)
        elif self.direction == "Down":
            new_head = (head[0], head[1] + 20)

        self.snake.insert(0, new_head)

        self.snake.pop()

    def move_enemy_snake(self):
        if not self.enemy_out:
            head = self.enemy_snake[0]

            # Calculate Manhattan distance to food
            food_coords = self.canvas.coords(self.food)
            distance_x = food_coords[0] - head[0]
            distance_y = food_coords[1] - head[1]

            # Determine the direction that reduces the distance
            if abs(distance_x) > abs(distance_y):
                if distance_x > 0 and self.enemy_direction != "Left":
                    self.enemy_direction = "Right"
                elif distance_x < 0 and self.enemy_direction != "Right":
                    self.enemy_direction = "Left"
                elif distance_x > 0 and food_coords[0] > head[0] and self.enemy_direction == "Left":
                    self.enemy_direction = "Down"
                    self.master.after(150, self.enemy_direction_right)
                elif distance_x > 0 and food_coords[0] < head[0] and self.enemy_direction == "Left":
                    self.enemy_direction = "Down"
                    self.master.after(150, self.enemy_direction_right)
                elif distance_x < 0 and food_coords[0] < head[0] and self.enemy_direction == "Right":
                    self.enemy_direction = "Up"
                    self.master.after(150, self.enemy_direction_left)
                elif distance_x < 0 and food_coords[0] > head[0] and self.enemy_direction == "Right":
                    self.enemy_direction = "Up"
                    self.master.after(150, self.enemy_direction_left)
            else:
                if distance_y > 0 and self.enemy_direction != "Up":
                    self.enemy_direction = "Down"
                elif distance_y < 0 and self.enemy_direction != "Down":
                    self.enemy_direction = "Up"
                elif distance_y > 0 and food_coords[1] > head[1] and self.enemy_direction == "Up":
                    self.enemy_direction = "Right"
                    self.master.after(150, self.enemy_direction_down)
                elif distance_y < 0 and food_coords[1] < head[1] and self.enemy_direction == "Up":
                    self.enemy_direction = "Left"
                    self.master.after(150, self.enemy_direction_up)
                elif distance_x < 0 and food_coords[1] > head[1] and self.enemy_direction == "Down":
                    self.enemy_direction = "Right"
                    self.master.after(150, self.enemy_direction_up)
                elif distance_x < 0 and food_coords[1] < head[1] and self.enemy_direction == "Down":
                    self.enemy_direction = "Left"
                    self.master.after(150, self.enemy_direction_up)

            new_head = self.calculate_new_head(head, self.enemy_direction)
            if not self.is_obstacle_at_position(new_head):
                self.enemy_snake.insert(0, new_head)
            else:
                # If the next position is an obstacle, choose a different direction
                self.choose_alternative_direction()

            head = self.enemy_snake[0]

            if head == self.canvas.coords(self.food):
                self.enemy_score += 1
                self.enemy_score_label.config(text=f"AI Score: {self.enemy_score}")
                self.enemy_snake.append((0, 0))
                self.canvas.delete(self.food)
                self.food = self.create_food()
            else:
                self.enemy_snake.pop()

    def enemy_direction_right(self):
        self.enemy_direction = "Right"

    def enemy_direction_left(self):
        self.enemy_direction = "Left"

    def enemy_direction_up(self):
        self.enemy_direction = "Up"

    def enemy_direction_down(self):
        self.enemy_direction = "Down"

    def calculate_new_head(self, head, direction):
        if direction == "Right":
            return head[0] + 20, head[1]
        elif direction == "Left":
            return head[0] - 20, head[1]
        elif direction == "Up":
            return head[0], head[1] - 20
        elif direction == "Down":
            return head[0], head[1] + 20
        return head  # Default to current head if direction is not recognized

    def is_obstacle_at_position(self, position):
        # Check if there's an obstacle at the specified position
        obstacles_at_position = self.canvas.find_overlapping(
            position[0], position[1], position[0] + 20, position[1] + 20
        )
        return any(obstacle in self.obstacles for obstacle in obstacles_at_position)

    def choose_alternative_direction(self):
        # Choose an alternative direction if the current one leads to an obstacle
        alternative_directions = [
            "Right", "Left", "Up", "Down", "DownRight", "DownLeft"
        ]
        alternative_directions.remove(self.enemy_direction)
        random.shuffle(alternative_directions)
        for direction in alternative_directions:
            new_head = self.calculate_new_head(self.enemy_snake[0], direction)
            if not self.is_obstacle_at_position(new_head):
                self.enemy_direction = direction
                self.enemy_snake.insert(0, new_head)
                return

    def update(self):
        if self.game_over:
            return

        self.move_snake()
        self.move_enemy_snake()  # Move the enemy snake

        head = self.snake[0]
        enemy_head = self.enemy_snake[0]

        # Check for collision with itself
        if len(self.snake) > 1 and head in self.snake[1:]:
            self.game_over = True
            if self.score > self.enemy_score:
                self.canvas.create_text(300, 300, text=f"You Win!\nYour Score : "
                                                       f"{self.score}\nAI Score : "
                                                       f"{self.enemy_score}", font=("Helvetica", 24),
                                        fill="white")
            elif self.score < self.enemy_score:
                self.canvas.create_text(300, 300, text=f"AI Wins!\nYour Score : "
                                                       f"{self.score}\nAI Score : "
                                                       f"{self.enemy_score}", font=("Helvetica", 24),
                                        fill="white")
            elif self.score == self.enemy_score:
                self.canvas.create_text(300, 300, text=f"Tie!\nYour Score : "
                                                       f"{self.score}\nAI Score : "
                                                       f"{self.enemy_score}", font=("Helvetica", 24),
                                        fill="white")

        if len(self.enemy_snake) > 1 and enemy_head in self.enemy_snake[1:]:
            self.enemy_out = True

        # Check for collision with walls
        if not (0 <= head[0] < 600 and 0 <= head[1] < 600):
            self.game_over = True
            if self.score > self.enemy_score:
                self.canvas.create_text(300, 300, text=f"You Win!\nYour Score : "
                                                       f"{self.score}\nAI Score : "
                                                       f"{self.enemy_score}", font=("Helvetica", 24),
                                        fill="white")
            elif self.score < self.enemy_score:
                self.canvas.create_text(300, 300, text=f"AI Wins!\nYour Score : "
                                                       f"{self.score}\nAI Score : "
                                                       f"{self.enemy_score}", font=("Helvetica", 24),
                                        fill="white")
            elif self.score == self.enemy_score:
                self.canvas.create_text(300, 300, text=f"Tie!\nYour Score : "
                                                       f"{self.score}\nAI Score : "
                                                       f"{self.enemy_score}", font=("Helvetica", 24),
                                        fill="white")

        if not (0 <= enemy_head[0] < 600 and 0 <= enemy_head[1] < 600):
            self.enemy_out = True

        head = self.snake[0]
        if head in self.obstacles:
            self.game_over = True
            if self.score > self.enemy_score:
                self.canvas.create_text(300, 300, text=f"You Win!\nYour Score : "
                                                       f"{self.score}\nAI Score : "
                                                       f"{self.enemy_score}", font=("Helvetica", 24),
                                        fill="white")
            elif self.score < self.enemy_score:
                self.canvas.create_text(300, 300, text=f"AI Wins!\nYour Score : "
                                                       f"{self.score}\nAI Score : "
                                                       f"{self.enemy_score}", font=("Helvetica", 24),
                                        fill="white")
            elif self.score == self.enemy_score:
                self.canvas.create_text(300, 300, text=f"Tie!\nYour Score : "
                                                       f"{self.score}\nAI Score : "
                                                       f"{self.enemy_score}", font=("Helvetica", 24),
                                        fill="white")

        enemy_head = self.enemy_snake[0]
        if enemy_head in self.obstacles:
            self.enemy_out = True

        if self.game_over:
            return

        self.canvas.delete("snake")
        self.canvas.delete("enemy_snake")
        self.canvas.delete("obstacle")

        for obstacle in self.obstacles:
            self.canvas.create_rectangle(
                obstacle[0], obstacle[1], obstacle[0] + 20, obstacle[1] + 20, fill="white", tags="obstacle"
            )
        for segment in self.snake:
            self.canvas.create_rectangle(segment[0], segment[1], segment[0] + 20,
                                         segment[1] + 20, fill="green", tags="snake")
        if not self.enemy_out:
            for segment in self.enemy_snake:
                self.canvas.create_rectangle(segment[0], segment[1], segment[0] + 20,
                                             segment[1] + 20, fill="yellow", tags="enemy_snake")

        self.canvas.delete("food")
        food_coords = self.canvas.coords(self.food)
        if head[0] == food_coords[0] and head[1] == food_coords[1]:
            self.snake.append((0, 0))  # Just to increase the length
            self.score += 1
            self.score_label.config(text=f"Your Score: {self.score}")  # Update the score label
            if self.food:
                self.canvas.delete(self.food)
                self.food = None
            self.food = self.create_food()

        if enemy_head[0] == food_coords[0] and enemy_head[1] == food_coords[1]:
            self.enemy_snake.append((0, 0))  # Just to increase the length
            self.enemy_score += 1
            self.enemy_score_label.config(text=f"AI Score: {self.enemy_score}")  # Update the score label
            if self.food:
                self.canvas.delete(self.food)
                self.food = None
            self.food = self.create_food()

        self.last_direction = self.direction  # Update the last direction
        self.enemy_last_direction = self.enemy_direction  # Update the last direction for the enemy snake

        self.master.after(200, self.update)  # to increase speed decrease the value,
        # this is milliseconds after the snake will move

    def change_direction(self, event):
        if event.keysym == "Right" and not self.last_direction == "Left":
            self.direction = "Right"
        elif event.keysym == "Left" and not self.last_direction == "Right":
            self.direction = "Left"
        elif event.keysym == "Up" and not self.last_direction == "Down":
            self.direction = "Up"
        elif event.keysym == "Down" and not self.last_direction == "Up":
            self.direction = "Down"


if __name__ == "__main__":
    root = tk.Tk()
    game = SnakeGame(root)
    root.mainloop()