import simplegui
import random

# initialize globals - pos and vel encode vertical info for paddles
WIDTH = 600
HEIGHT = 400       
BALL_RADIUS = 20
PAD_WIDTH = 8
PAD_HEIGHT = 80
HALF_PAD_WIDTH = PAD_WIDTH / 2
HALF_PAD_HEIGHT = PAD_HEIGHT / 2
LEFT = False
RIGHT = True
ball_vel=[0,0]
ball_pos=[WIDTH/2,HEIGHT/2]

# initialize ball_pos and ball_vel for new bal in middle of table
# if direction is RIGHT, the ball's velocity is upper right, else upper left

def spawn_ball(direction):
    global ball_pos
    global ball_vel,LEFT,RIGHT 
    # these are vectors stored as lists
    ball_vel[0]+=(0.05)*ball_vel[0]
    #ball_vel[1]+=(0.05)*ball_vel[1]
    ball_pos=[WIDTH/2,HEIGHT/2]
    if direction==RIGHT:
        ball_vel[0]=-ball_vel[0]
    else:
        ball_vel[0]=-ball_vel[0]
          
    

# define event handlers
def new_game():
    global paddle1_pos, paddle2_pos, paddle1_vel, paddle2_vel,ball_pos,RIGHT  # these are numbers
    global score1, score2 # these are ints
    paddle1_pos=HEIGHT/2
    paddle2_pos=HEIGHT/2
    paddle1_vel=0
    paddle2_vel=0
    score1=0
    score2=0
    ball_vel[0]=random.randrange(1,7)
    ball_vel[1]=random.randrange(1,3)   

    spawn_ball(RIGHT)

def draw(canvas):
    global score1, score2, paddle1_pos, paddle2_pos, ball_pos, ball_vel,LEFT,RIGHT
 
        
    # draw mid line and gutters
    canvas.draw_line([WIDTH / 2, 0],[WIDTH / 2, HEIGHT], 1, "White")
    canvas.draw_line([PAD_WIDTH, 0],[PAD_WIDTH, HEIGHT], 1, "White")
    canvas.draw_line([WIDTH - PAD_WIDTH, 0],[WIDTH - PAD_WIDTH, HEIGHT], 1, "White")
        
    # update ball
    ball_pos[0]+=ball_vel[0]
    ball_pos[1]+=ball_vel[1]  
    # draw ball
    canvas.draw_circle(ball_pos,BALL_RADIUS,5,"white","white") 
        
    # update paddle's vertical position, keep paddle on the screen
    if paddle1_pos+paddle1_vel>=HALF_PAD_HEIGHT and paddle1_pos+paddle1_vel<=HEIGHT-HALF_PAD_HEIGHT:
        paddle1_pos+=paddle1_vel
    if paddle2_pos+paddle2_vel>=HALF_PAD_HEIGHT and paddle2_pos+paddle2_vel<=HEIGHT-HALF_PAD_HEIGHT:
        paddle2_pos+=paddle2_vel
    
    # draw paddles
    canvas.draw_polygon([[0,paddle1_pos-HALF_PAD_HEIGHT],
                        [0,paddle1_pos+HALF_PAD_HEIGHT],
                        [PAD_WIDTH-4,paddle1_pos-HALF_PAD_HEIGHT],
                        [PAD_WIDTH-4,paddle1_pos+HALF_PAD_HEIGHT]],
                        8,"white","white")
    canvas.draw_polygon([[WIDTH-PAD_WIDTH+4,paddle2_pos-HALF_PAD_HEIGHT],
                        [WIDTH-PAD_WIDTH+4,paddle2_pos+HALF_PAD_HEIGHT],
                        [WIDTH,paddle2_pos-HALF_PAD_HEIGHT],
                        [WIDTH,paddle2_pos+HALF_PAD_HEIGHT]],
                        8,"white","white")
    
    # determine whether paddle and ball collide 
    if ball_pos[1]+BALL_RADIUS==HEIGHT or ball_pos[1]-BALL_RADIUS==0:
            ball_vel[1]=-ball_vel[1]
    if ball_pos[1]>=paddle1_pos-HALF_PAD_HEIGHT and ball_pos[1]<=paddle1_pos+HALF_PAD_HEIGHT and ( ball_pos[0]-BALL_RADIUS<=PAD_WIDTH):
            ball_vel[0]=-ball_vel[0]
    elif ( ball_pos[0]-BALL_RADIUS<=PAD_WIDTH) :
        RIGHT==True
        LEFT=False
        score2+=1
        spawn_ball(RIGHT)
    if ball_pos[1]>=paddle2_pos-HALF_PAD_HEIGHT and ball_pos[1]<=paddle2_pos+HALF_PAD_HEIGHT and (ball_pos[0]+BALL_RADIUS>=WIDTH-PAD_WIDTH):      
            ball_vel[0]=-ball_vel[0]
    elif (ball_pos[0]+BALL_RADIUS>=WIDTH-PAD_WIDTH):
        LEFT=True
        RIGHT=False
        score1+=1
        spawn_ball(LEFT)
  
          
    # draw scores
    canvas.draw_text("PLAYER 1",[80,50],20,"white")
    canvas.draw_text("PLAYER 2",[400,50],20,"white")
    canvas.draw_text(str(score1),[120,80],20,"white")
    canvas.draw_text(str(score2),[440,80],20,"white")

    if score1==15:
        canvas.draw_text("PLAYER 1 WINS!!",[100,300],50,"red")
        new_game()
    elif score2==15:
        canvas.draw_text("PLAYER 2 WINS!!",[100,300],50,"red")
        new_game()
    
def keydown(key):
    global paddle1_vel, paddle2_vel
    if key==simplegui.KEY_MAP["w"]:
        paddle1_vel=-7
    if key==simplegui.KEY_MAP["s"]:
        paddle1_vel=7
    if key==simplegui.KEY_MAP["up"]:
        paddle2_vel=-3
    if key==simplegui.KEY_MAP["down"]:
        paddle2_vel=3    
   
def keyup(key):
    global paddle1_vel, paddle2_vel
    if key==simplegui.KEY_MAP["w"]:
        paddle1_vel=0
    if key==simplegui.KEY_MAP["s"]:
        paddle1_vel=0
    if key==simplegui.KEY_MAP["up"]:
        paddle2_vel=0
    if key==simplegui.KEY_MAP["down"]:
        paddle2_vel=0
def reset():
    new_game()
def start():
    new_game()
# create frame
frame = simplegui.create_frame("Pong", WIDTH, HEIGHT)
frame.set_draw_handler(draw)
frame.set_keydown_handler(keydown)
frame.set_keyup_handler(keyup)
frame.add_button("RESET",reset,100)

# start frame
new_game()
frame.start()
