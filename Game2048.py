import math
import arcade
import random


screen_x = 800
screen_y = 900



class MyWindow(arcade.Window):


    def __init__(self):
        super().__init__(screen_x, screen_y, "Balls colliding")


        self.board = [[0,0,0,0],
                      [0,0,0,0],
                      [0,0,0,0],
                      [0,0,0,0]]


        self.mouse_x = 0
        self.mouse_y = 0
        self.game_over = False
        self.score = 0
        self.has_said_well_played = False
        self.well_played_counter = 0

        self.color_with_number = {"2" : (215,200,180)  ,  "4" : (236, 222, 144)  ,  "8" : (223, 180, 136)  ,  "16" : (223, 145, 113)  , "32" : (250, 129, 131) ,
        "64" : (250, 108, 140)  ,  "128" : (250, 86, 106)  ,  "256" : (250, 59, 146)  ,  "512" : (180, 27, 91)  , "1024" :  (160, 16, 43) , "2048" : (255, 130, 2)
        , "4096" : (180,100,0) , "8192" : (100,50,0) , "16384" : (0,0,0)}


        self.create_random_number(self.board)



    def on_draw(self):

        arcade.start_render()
        arcade.set_background_color(arcade.color.WHEAT)

        
        # déssine la couleur derniere les cases 
        for line_index,lines in enumerate(self.board) :
            for rows_index,values in enumerate(lines) :
                if values != 0 :
                    arcade.draw_rectangle_filled(200*rows_index + 100 , 700 - 200*line_index , 200 , 200 , self.color_with_number[str(values)])


        for i in range(5):
            arcade.draw_line(i*200 , 800 , i*200 , 0 , (0,0,0) , 10)
            arcade.draw_line(0 , i*200 , 800 , i*200, (0,0,0) , 10)


        for line_index,lines in enumerate(self.board) :
            for rows_index,values in enumerate(lines) :
                if values != 0 and values <= 2048 :
                    arcade.draw_text(str(values), 200*rows_index + 100 , 700 - 200*line_index , color=(0,0,0) , font_size=40 , anchor_x="center" , anchor_y="center")
                elif values > 2048 :
                    arcade.draw_text(str(values), 200*rows_index + 100 , 700 - 200*line_index , color=(255,255,255) , font_size=40 , anchor_x="center" , anchor_y="center")


        if self.game_over :
            arcade.draw_text("Game Over !" , 400 , 850 , (0,0,0) , font_size=40 , anchor_x="center" , anchor_y="center")

        arcade.draw_text("Score : " + str(self.score) , 40 , 850 , (0,0,0) , font_size=16 , anchor_x="left" , anchor_y="center")


        for line_index,lines in enumerate(self.board) :
            for rows_index,values in enumerate(lines) :
                if values >= 2048 and not self.has_said_well_played:
                    self.has_said_well_played = True
                    self.well_played_counter = 5
                    
        if self.well_played_counter > 0 :
            arcade.draw_text("Well Played !" , 400 , 850 , (0,0,0) , font_size=40 , anchor_x="center" , anchor_y="center")

        

    def on_update(self, delta_time: float):
        self.well_played_counter -= delta_time



    def on_key_press(self, symbol: int, modifiers: int):

        changed = False

        if symbol == arcade.key.DOWN :
            changed = self.compress(self.board , 0)
            if self.merge(self.board,0) :
                changed = True   
            self.compress(self.board , 0)

            if changed :
                self.create_random_number(self.board)


        if symbol == arcade.key.LEFT :
            changed = self.compress(self.board , 1)
            if self.merge(self.board,1) :
                changed = True
            self.compress(self.board , 1)

            if changed :
                self.create_random_number(self.board)


        if symbol == arcade.key.UP :
            changed = self.compress(self.board , 2)
            if self.merge(self.board,2) :
                changed = True
            self.compress(self.board , 2)

            if changed :
                self.create_random_number(self.board)


        if symbol == arcade.key.RIGHT :
            changed = self.compress(self.board , 3)
            if self.merge(self.board,3) :
                changed = True
            self.compress(self.board , 3)

            if changed :
                self.create_random_number(self.board)


        if symbol == arcade.key.R :
            self.setup()



        if self.check_for_game_over(self.board) :
            self.game_over = True

        

    def compress(self,Board,direction : int):

        # direction : 0 -> down | 1 -> left | 2 -> up | 3 -> right

        has_compressed = False

        if direction == 0 :
            for i in range(3) :
                for line_index,lines in enumerate(Board) :
                    for rows_index,value in enumerate(lines) :
                        if line_index < 3 and Board[line_index+1][rows_index] == 0 and Board[line_index][rows_index] != 0:
                            Board[line_index][rows_index] = 0
                            Board[line_index+1][rows_index] = value
                            has_compressed = True


        if direction == 1 :
            for i in range(3) :
                for line_index,lines in enumerate(Board) :
                    for rows_index,value in enumerate(lines) :
                        if rows_index > 0 and Board[line_index][rows_index-1] == 0 and Board[line_index][rows_index] != 0:
                            Board[line_index][rows_index] = 0
                            Board[line_index][rows_index-1] = value
                            has_compressed = True

        
        if direction == 2 :
            for i in range(3) :
                for line_index,lines in enumerate(Board) :
                    for rows_index,value in enumerate(lines) :
                        if line_index > 0 and Board[line_index-1][rows_index] == 0 and Board[line_index][rows_index] != 0 :
                            Board[line_index][rows_index] = 0
                            Board[line_index-1][rows_index] = value
                            has_compressed = True


        if direction == 3 :
            for i in range(3) :
                for line_index,lines in enumerate(Board) :
                    for rows_index,value in enumerate(lines) :
                        if rows_index < 3 and Board[line_index][rows_index+1] == 0 and Board[line_index][rows_index] != 0:
                            Board[line_index][rows_index] = 0
                            Board[line_index][rows_index+1] = value
                            has_compressed = True

        return has_compressed



    def check_for_game_over(self,Board):


        is_game_over = True

        for i in range(3) :
            for line_index,lines in enumerate(Board) :
                for rows_index,value in enumerate(lines) :
                    if line_index < 3 and Board[line_index+1][rows_index] == 0 :
                        is_game_over = False

                    if rows_index > 0 and Board[line_index][rows_index-1] == 0 :
                        is_game_over = False

                    if line_index > 0 and Board[line_index-1][rows_index] == 0 :
                        is_game_over = False

                    if rows_index < 3 and Board[line_index][rows_index+1] == 0 :
                        is_game_over = False

        
        for rows in range(4) :
            for lines in range(3,0,-1):
                if Board[lines-1][rows] == Board[lines][rows] and Board[lines][rows] != 0 :
                    is_game_over = False

        
        for rows in range(3) :
            for lines in range(4):
                if Board[lines][rows+1] == Board[lines][rows] and Board[lines][rows] != 0 :
                    is_game_over = False

        
        for rows in range(4) :
            for lines in range(3):
                if Board[lines+1][rows] == Board[lines][rows] and Board[lines][rows] != 0 :
                    is_game_over = False


        for rows in range(3,0,-1) :
            for lines in range(4):
                if Board[lines][rows-1] == Board[lines][rows] and Board[lines][rows] != 0 :
                    is_game_over = False
        
        return is_game_over



    def merge(self,Board,direction : int):

        # direction : 0 -> down | 1 -> left | 2 -> up | 3 -> right
        has_merged = False

        if direction == 0 :
            for rows in range(4) :
                for lines in range(3,0,-1):
                    if Board[lines-1][rows] == Board[lines][rows] and Board[lines][rows] != 0 :
                        Board[lines-1][rows] = 0
                        Board[lines][rows] *= 2
                        self.score += Board[lines][rows]
                        has_merged = True


        if direction == 1 :
            for rows in range(3) :
                for lines in range(4):
                    if Board[lines][rows+1] == Board[lines][rows] and Board[lines][rows] != 0 :
                        Board[lines][rows+1] = 0
                        Board[lines][rows] *= 2 
                        self.score += Board[lines][rows]
                        has_merged = True


        if direction == 2 :
            for rows in range(4) :
                for lines in range(3):
                    if Board[lines+1][rows] == Board[lines][rows] and Board[lines][rows] != 0 :
                        Board[lines+1][rows] = 0
                        Board[lines][rows] *= 2 
                        self.score += Board[lines][rows]
                        has_merged = True
                        

        if direction == 3 :
            for rows in range(3,0,-1) :
                for lines in range(4):
                    if Board[lines][rows-1] == Board[lines][rows] and Board[lines][rows] != 0 :
                        Board[lines][rows-1] = 0
                        Board[lines][rows] *= 2 
                        self.score += Board[lines][rows]
                        has_merged = True
        
        return has_merged



    def create_random_number(self,Board):
        case_possible = []

        for line_index,lines in enumerate(self.board) :
            for rows_index,values in enumerate(lines) :
                if values == 0 :
                    case_possible.append((line_index,rows_index))

        if len(case_possible) == 0 :
            self.game_over = True

        rand = random.randint(0,len(case_possible) - 1)
        
        if random.random() > .9 :
            case_value = 4
        else :
            case_value = 2

        Board[case_possible[rand][0]][case_possible[rand][1]] = case_value



    def setup(self):

        self.board = [[0,0,0,0],
                      [0,0,0,0],
                      [0,0,0,0],
                      [0,0,0,0]]


        self.game_over = False
        self.score = 0

        self.create_random_number(self.board)




window = MyWindow()
arcade.run()