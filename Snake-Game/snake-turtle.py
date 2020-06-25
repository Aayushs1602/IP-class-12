# import os
# import sys
import time
import random as r
import turtle as t

"""Creating Screen"""
win = t.Screen()
win.title("Snake Game")
win.setup(width=600, height=600)
win.bgcolor("green")
win.tracer(0)

"""Sake Head"""
Head = t.Turtle()
Head.speed(0)
Head.penup()
Head.direction = "stop"
Head.goto(0, 0)
Head.shape("square")
Head.color("black")

# food
food = t.Turtle()
food.penup()
food.goto(0, 100)
food.shape("circle")
food.color("red")

# writing the score
pen = t.Turtle()
pen.penup()
pen.goto(0, 260)
pen.speed(0)
pen.hideturtle()
pen.shape("circle")
pen.color("white")
pen.write("Score: 0  High Score: 0", align="center", font=("courior", 24, "normal"))

# varaibles
parts = []
score = 0
high_score = 0
delay = 0.1


def go_up():
    if Head.direction != "down":
        Head.direction = 'up'


def go_down():
    if Head.direction != "up":
        Head.direction = 'down'


def go_left():
    if Head.direction != "right":
        Head.direction = 'left'


def go_right():
    if Head.direction != "left":
        Head.direction = 'right'


def move():
    if Head.direction == "up":
        y = Head.ycor()
        Head.sety(y + 20)
    if Head.direction == "down":
        y = Head.ycor()
        Head.sety(y - 20)
    if Head.direction == "left":
        x = Head.xcor()
        Head.setx(x - 20)
    if Head.direction == "right":
        x = Head.xcor()
        Head.setx(x + 20)


"""Keyboard binding"""
win.listen()
win.onkeypress(go_up, 'w')
win.onkeypress(go_down, 's')
win.onkeypress(go_left, 'a')
win.onkeypress(go_right, 'd')

while True:
    win.update()

    # checking for collisions
    if Head.xcor() > 290 or Head.xcor() < -290 or Head.ycor() > 290 or Head.ycor() < -290:
        time.sleep(1)
        Head.goto(0, 0)
        Head.direction = "stop"

        for segment in parts:
            segment.goto(1000, 1000)

        parts.clear()

        delay = 0.1
        score = 0

        pen.clear()
        pen.write("Score: {}  High Score: {}".format(score, high_score), align="center", font=("courior", 24, "normal"))

    if Head.distance(food) < 20:
        # moves the food to random position
        x_f = r.randint(-290, 290)
        y_f = r.randint(-290, 290)
        food.goto(x_f, y_f)

        new_part = t.Turtle()
        new_part.penup()
        new_part.speed(0)
        new_part.shape("square")
        new_part.color("grey")
        parts.append(new_part)
        delay -= 0.001
        score += 10
        if high_score < score:
            high_score = score

        pen.clear()
        pen.write("Score: {}  High Score: {}".format(score, high_score), align="center", font=("courior", 24, "normal"))

    for i in range(len(parts)-1, 0, -1):
        i_x = parts[i-1].xcor()
        i_y = parts[i-1].ycor()
        parts[i].goto(i_x, i_y)

    if len(parts) > 0:
        h_x = Head.xcor()
        h_y = Head.ycor()
        parts[0].goto(h_x, h_y)

    move()

    for segment in parts:
        if segment.distance(Head) < 20:
            time.sleep(1)
            Head.goto(0, 0)
            Head.direction = "stop"

            for segments in parts:
                segments.goto(1000, 1000)

            parts.clear()

            delay = 0.1
            score = 0

            pen.clear()
            pen.write(f"Score: {score}  High Score: {high_score}", align="center", font=("courior", 24, "normal"))

    time.sleep(delay)

# noinspection PyUnreachableCode
win.mainloop()
