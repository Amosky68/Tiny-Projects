import math
from tkinter import W
import arcade
import random


screen_x = 800
screen_y = 800



class Physical_Screen():    # gere le changement de repère (physique a l'écran / écran a physique)

    """ Calcul de l'espace Physique -> Espace Ecrab 

    Xe: Coordonnées debut écran dans l'espace physique
    X : Coordonnées dans l'espace physique
    X': Coordonnées dans l'espace ecran


    Phy->Ecran : X'=(X-Xe)*Zoom
    Ecran->Phy : X=(X'/Zoom + Xe)
    """

    # Calcul les coordonnées dans le repere ecran (depuis les coordonnées dans le repère physique)
    def to_screen(Xe,Ye,X,Y,Zoom):
        return (X-Xe)*Zoom, (Y-Ye)*Zoom

    # Calcul les coordonnées dans le repere Physique (depuis les coordonnées dans le repère écran)
    def to_physic(Xe,Ye,X,Y,Zoom):
        return X/Zoom+Xe,Y/Zoom+Ye

    # Calcul origine de l'écran connaissant les coordonnées physique du milieu et le zoom
    def orgin_from_center_phy(X,Y,Zoom,bordure_x,bordure_y):
        return X-bordure_x/(2*Zoom),Y-bordure_y/(2*Zoom)




class MyWindow(arcade.Window):


    def __init__(self):
        super().__init__(screen_x, screen_y, "Game of life" , resizable=True)

        self.screen_x = screen_x
        self.screen_y = screen_y

        self.camera_x = 0   # position x de la camera 
        self.camera_y = 0   # position y de la camera
        self.zoom = 1  # zoom de la caméra

        self.mouse_pos_x = 0    # position x de la souris
        self.mouse_pos_y = 0    # position y de la souris


        self.grid = [(0,0)]     # list of active cells (with coordonates)


        self.pause = True
        self.debug_mode = False

        self.timer = 0
        self.step_per_sec = 2




    def on_draw(self):

        arcade.start_render()

        Xe,Ye = Physical_Screen.orgin_from_center_phy(self.camera_x, self.camera_y  , self.zoom, self.screen_x , self.screen_y ) 


        for cellule in self.grid:
            pos_x , pos_y = Physical_Screen.to_screen(Xe,Ye, cellule[0] , cellule[1],self.zoom)

            width  =  self.zoom 
            height =  self.zoom 
            
            arcade.draw_rectangle_filled(pos_x, pos_y, width , height , (255,255,255))
            


        arcade.draw_text(" steps/s : " + str( round(self.step_per_sec , 2) ) , 30 , self.screen_y - 50 , (160 , 180 ,90))
                    
        



    def on_update(self, delta_time: float): 

        self.timer -= self.step_per_sec * delta_time 


        if self.timer < 0 :
            step_missing = int( -self.timer + 1)

            self.timer += step_missing

            for i in range( step_missing ) :

                if not ( self.pause ) :

                    
                    to_calculate = self.get_blocks_to_change(self.grid)
                    previous_grid = self.grid.copy()
                    self.grid[:] = [] 

                    print(len(to_calculate))

                    for value in to_calculate :
                        new_cell = ( value[0] , value[1] )
                        
                        if ( value[2] < 2 ) or ( value[2] > 3 ) :   # on ajoute rien si la cellule meurt 
                            pass

                        elif value[2] == 2 :                # si il y avais déja la cellule et que cette dernière a deux voisin on l'ajoute 
                            if new_cell in previous_grid :
                                self.grid.append(new_cell)

                        elif value[2] == 3 :            # si une case a trois voisins, elle nait 
                            self.grid.append(new_cell)
                        


    def get_blocks_to_change(self, grid) :

        blocks_coordonates_list = []
        output_list = []

        # calcul les coordonées de toutes les cases à calculer 

        for value in grid :
            x = value[0]
            y = value[1]
            neighbors_coordonates = [ (x+1, y+1) , (x, y+1) , (x-1, y+1) , (x+1, y) , (x, y) , (x-1, y) , (x+1, y-1) , (x, y-1) , (x-1, y-1)]
            
            for i in neighbors_coordonates :
                if i not in blocks_coordonates_list :
                    blocks_coordonates_list.append(i)


        # calcul le nombre de voision pour chaque cellule
        for value in blocks_coordonates_list :
            x = value[0]
            y = value[1]
            
            neighbors_number = self.get_number_of_neightbors(self.grid ,x , y)

            output_list.append( (x , y , neighbors_number) )


        return output_list

                        

    def get_number_of_neightbors(self , grid , x , y) :

        total = 0
        for values in grid :
            x2 = values[0]
            y2 = values[1]
            distance = self.distance(x , x2 , y , y2)

            if ( distance < 2 ) and ( distance != 0 ):
                total += 1

        return total



    def on_mouse_press(self, x: float, y: float, button: int, modifiers: int):
        

        pass



    def on_key_press(self, key: int, modifiers: int):

        if key == arcade.key.SPACE :
            self.pause = not(self.pause)

        if key == arcade.key.RIGHT :
            self.step_per_sec *= 1.5

        if key == arcade.key.LEFT :
            self.step_per_sec /= 1.5

        if key == arcade.key.E :

            Xe,Ye = Physical_Screen.orgin_from_center_phy(self.camera_x, self.camera_y  , self.zoom, self.screen_x , self.screen_y ) 
            x , y = Physical_Screen.to_physic( Xe , Ye , self.mouse_pos_x , self.mouse_pos_y , self.zoom)


            signe_x = self.signe(x)
            signe_y = self.signe(y)

            cell_x = int( abs(x) + .5) * signe_x
            cell_y = int( abs(y) + .5) * signe_y

            cell = (cell_x , cell_y )

            if cell in self.grid :
                self.grid.remove(cell)

            elif cell not in self.grid :
                self.grid.append(cell)

        if key == arcade.key.R :
            self.grid = []



    def on_mouse_scroll(self, x, y, scroll_x, scroll_y):  # réduit / augmente le niveau de zoom si on scroll vers le bas ou vers le haut
        if scroll_y > 0 : 
            self.zoom /= 0.92   # rapproche la camera 
        elif scroll_y < 0 :
            self.zoom *= 0.92   # éloigne la caméra



    def on_mouse_drag(self, x, y, dx, dy, buttons, modifiers):  #   modifie la valeur du centre de l'écran 
        self.camera_x -= dx / self.zoom                         #   dans les coordonées physique en fonction 
        self.camera_y -= dy / self.zoom                         #   du déplacement de la souris 



    def on_mouse_motion(self, x: float, y: float, dx: float, dy: float):

        self.mouse_pos_x = x    # coordonées x de la souris 
        self.mouse_pos_y = y    # coordonées y de la souris 



    def on_resize(self, width: float, height: float):
        
        super().on_resize(width, height)

        self.screen_x = width
        self.screen_y = height



    def distance(self, x1 , x2 , y1 , y2):
        return math.sqrt( (x2 - x1)*(x2 - x1) + (y2 - y1)*(y2 - y1) )



    def signe(self, x) :
        if x >= 0  : return 1
        else : return -1



window = MyWindow()
arcade.run()