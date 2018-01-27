from tkinter import *
import random
import time

tk=Tk()
tk.title("Table Tennis")
tk.resizable(0,0)
canvas= Canvas(tk, height=900,width=900)
canvas.pack()
tk.update()

class Ball:
    def __init__ (self,canvas,color,size):
        self.color = color
        self.canvas=canvas
        self.canvas_height = self.canvas.winfo_height()
        self.canvas_width = self.canvas.winfo_width()
        self.ball_shape = self.canvas.create_oval(0,0,size,size, fill=self.color,outline='blue')
        self.canvas.move(self.ball_shape,.5*self.canvas_width-(.5*size), .5*self.canvas_height)
        speeds = [-4,-2,2,4]
        self.x = random.choice(speeds)
        self.y = random.choice(speeds)
        self.canvas.bind_all('<Button-2>', self.change_color)
        self.hit_ceiling = False
        self.hit_floor = False
        self.game_started = False
        self.canvas.bind_all('<KeyPress-Return>', self.begin_game)
    def move(self):
        self.canvas.move(self.ball_shape,self.x,self.y)
        self.ball_pos=self.canvas.coords(self.ball_shape)
        self.paddle_pos = paddle.canvas.coords(paddle.paddle_shape)
        self.paddle2_pos = paddle2.canvas.coords(paddle2.paddle2_shape)
        if self.ball_pos[0] <= 0:
            self.x=7
        if self.ball_pos[2] >= self.canvas_width:
            self.x = -7
        if self.ball_pos[1] <= 0:
            self.y=7
        if self.ball_pos[3] >= self.canvas_height:
            self.y=-7

        if self.ball_pos[2] >= self.paddle_pos[0] and self.ball_pos[0] <= self.paddle_pos[2] \
           and self.ball_pos[3] >= self.paddle_pos[1] and self.ball_pos[1] <= self.paddle_pos[3]:
            self.y = -7
            self.x += paddle.x
            messages.score_for_p1()            
        if self.ball_pos[2] >= self.paddle2_pos[0] and self.ball_pos[0] <= self.paddle2_pos[2] \
           and self.ball_pos[3] >= self.paddle2_pos[1] and self.ball_pos[1] <= self.paddle2_pos[3]:
            self.y = 7
            self.x += paddle2.x
            messages.score_for_p2()

        if self.ball_pos[1] <= 0:
            self.hit_ceiling = True
        if self.ball_pos[3] >= self.canvas_height:
            self.hit_floor = True
    def change_color(self,event):
        colors=['blue','orange','gold','red','green','brown','grey','pink','purple','white']
        color_choice = random.choice(colors)
        self.canvas.itemconfig(self.ball_shape, fill=color_choice)
    def begin_game(self,event):
        if event.keysym == 'Return':
            messages.game_start_messages()
            self.game_started = True
                        
class Paddle:
    def __init__(self,canvas,color,length):
        self.color = color
        self.length = length
        self.canvas = canvas
        self.canvas_width=self.canvas.winfo_width()
        self.paddle_shape = self.canvas.create_rectangle(0,0,self.length,20,fill=self.color, \
                                                         outline='black')
        self.canvas.move(self.paddle_shape, (self.canvas_width*.5)-(.5*self.length), 820)
        self.canvas.bind_all('<Button-1>', self.change_color)
        self.canvas.bind_all('<KeyPress-Right>', self.move_right)
        self.canvas.bind_all('<KeyPress-Left>', self.move_left)
        self.x = 4
        self.y = 0
        self.started = False
    def change_color(self,event):
        colors=['blue','orange','gold','red','green','brown','grey','pink','purple','white']
        color_choice = random.choice(colors)
        self.canvas.itemconfig(self.paddle_shape, fill=color_choice)
    def move(self):
        self.canvas.move(self.paddle_shape,self.x,self.y)
        self.paddle_pos=self.canvas.coords(self.paddle_shape)
        if self.paddle_pos[0] <= 0:
            self.x=2
        if self.paddle_pos[2] >= self.canvas_width:
            self.x=-2
    def move_right(self,event):
        if event.keysym == 'Right':
            self.x=5
    def move_left(self,event):
        if event.keysym == 'Left':
            self.x=-5

class Paddle2:
    def __init__(self,canvas,color,length):
        self.color = color
        self.length = length
        self.canvas = canvas
        self.canvas_width=self.canvas.winfo_width()
        self.paddle2_shape = self.canvas.create_rectangle(0,0,self.length,20,fill=self.color, \
                                                         outline='black')
        self.canvas.move(self.paddle2_shape, (self.canvas_width*.5)-(.5*self.length), 60)
        self.canvas.bind_all('<Button-3>', self.change_color)
        self.canvas.bind_all('<KeyPress-d>', self.move_right)
        self.canvas.bind_all('<KeyPress-a>', self.move_left)
        self.x = 4
        self.y = 0
    def change_color(self,event):
        colors=['blue','orange','gold','red','green','brown','grey','pink','purple','white']
        color_choice = random.choice(colors)
        self.canvas.itemconfig(self.paddle2_shape, fill=color_choice)
    def move(self):
        self.canvas.move(self.paddle2_shape,self.x,self.y)
        self.paddle2_pos=self.canvas.coords(self.paddle2_shape)
        if self.paddle2_pos[0] <= 0:
            self.x=2
        if self.paddle2_pos[2] >= self.canvas_width:
            self.x=-2
    def move_right(self,event):
        if event.keysym == 'd':
            self.x=5
    def move_left(self,event):
        if event.keysym == 'a':
            self.x=-5

class Messages:
    def __init__(self,canvas):
        self.canvas = canvas
        self.instructions1 = self.canvas.create_text(450,450,text='Click Mouse Buttons to change color,', \
                                                     font=('arial',20))
        self.instructions2 = self.canvas.create_text(450,500, text = 'then hit "Enter" when ready...', \
                                                     font=('arial',20))
        self.game_on = self.canvas.create_text(450,450,text="BEGIN!",font = ("gothic", 40), \
                                     fill='red',state='hidden',)
        self.canvas_height = self.canvas.winfo_height()
        self.canvas_width = self.canvas.winfo_width()
        self.p1_score=0
        self.p2_score=0
        self.p1_score_line1 = self.canvas.create_text(.9*self.canvas_width,.95*self.canvas_height, \
                                                 text="PLAYER 1 SCORE", font=('arial',10),fill='red',state='hidden')
        self.p1_score_line2 = self.canvas.create_text(.9*self.canvas_width,.98*self.canvas_height, \
                                                  text =self.p1_score,font=('arial',10),fill='red',state='hidden')
        self.p2_score_line1 = self.canvas.create_text(.1*self.canvas_width,.02*self.canvas_height, \
                                                 text="PLAYER 1 SCORE", font=('arial',10),fill='blue',state='hidden')
        self.p2_score_line2 = self.canvas.create_text(.1*self.canvas_width,.05*self.canvas_height, \
                                                  text =self.p1_score,font=('arial',10),fill='blue',state='hidden')


    def game_start_messages(self):
        self.canvas.itemconfig(self.instructions1, state='hidden')
        self.canvas.itemconfig(self.instructions2, state='hidden')
        tk.update()
        time.sleep(0.5)
        self.canvas.itemconfig(self.game_on,state = 'normal')
        tk.update()
        time.sleep(1)
        self.canvas.itemconfig(self.game_on, state='hidden')
        self.canvas.itemconfig(self.p1_score_line1,state = 'normal')
        self.canvas.itemconfig(self.p1_score_line2,state = 'normal')
        self.canvas.itemconfig(self.p2_score_line1,state = 'normal')
        self.canvas.itemconfig(self.p2_score_line2,state = 'normal')
    def score_for_p1(self):
        self.p1_score= self.p1_score + 50
        self.canvas.itemconfig(self.p1_score_line2,text= self.p1_score)
    def score_for_p2(self):
        self.p2_score = self.p2_score + 50
        self.canvas.itemconfig(self.p2_score_line2,text = self.p2_score)
    def player1_wins(self):
        p1_win_message= canvas.create_text(450,450, text='Player 1 Wins! :D', font=('arial', 40), fill='red')
        for x in range(0,40):
            colors=['blue','orange','gold','red','green','brown','grey','pink','purple','white']
            color_choice = random.choice(colors)
            paddle.canvas.itemconfig(paddle.paddle_shape, fill=color_choice)
            tk.update()
            time.sleep(0.02)
    def player2_wins(self):
        p2_win_message = canvas.create_text(450,450, text='Player 2 Wins! :D', font=('arial', 40), fill='blue')                          
        for x in range(0,20):
            paddle2.canvas.itemconfig(paddle2.paddle2_shape, state='hidden')
            tk.update()
            time.sleep(0.02)
            paddle2.canvas.itemconfig(paddle2.paddle2_shape, state='normal')
            tk.update()
            time.sleep(0.02)


paddle = Paddle(canvas,color='purple',length=200)
paddle2 = Paddle2(canvas,color='orange',length=200)
ball = Ball(canvas,color='pink',size=50)
messages = Messages(canvas)


while 1:
    if ball.hit_ceiling == False and ball.hit_floor == False and ball.game_started == True:
        paddle.move()
        paddle2.move()
        ball.move()
    tk.update_idletasks()
    tk.update()
    time.sleep(.01)   
    if ball.hit_ceiling == True:
        messages.player1_wins()
        break
    if ball.hit_floor == True:
        messages.player2_wins()
        break
    
