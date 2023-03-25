import csv
import arcade
import time





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

        """ partie graphique """
        self.set_update_rate(1/200)
        self.screen_x = screen_x
        self.screen_y = screen_y
        self.camera_x = 0   # position x de la camera 
        self.camera_y = 0   # position y de la camera
        self.zoom = 1  # zoom de la caméra

        self.mouse_pos_x = 0    # position x de la souris
        self.mouse_pos_y = 0    # position y de la souris

        """ partie technique """

        self.pause = True
        self.debug_mode = False
        self.timer = 0
        self.step_per_sec = 2

        """ partie moteur """


        self.activecells = {(0.0,0.0): (0.0,0.0),(1.0,0.0): (1.0,0.0),(2.0,0.0): (2.0,0.0)}
        file = "InfGroth"
        self.loadMap(__file__[:-17] + f"Maps/{file}.csv")

        savefile = 'Save1'
        self.savePath = __file__[:-17] + f"Maps/{savefile}.csv"



    def on_draw(self):
        startTime = time.perf_counter()

        arcade.start_render()

        Xe,Ye = Physical_Screen.orgin_from_center_phy(self.camera_x, self.camera_y  , self.zoom, self.screen_x , self.screen_y ) 
        for cellule in self.activecells.values():
            pos_x , pos_y = Physical_Screen.to_screen(Xe,Ye, cellule[0] , cellule[1],self.zoom)
            width  =  self.zoom 
            height =  self.zoom 
            arcade.draw_rectangle_filled(pos_x, pos_y, width , height , (255,255,255))
            
        arcade.draw_text(" steps/s : " + str( round(self.step_per_sec , 2) ) , 30 , self.screen_y - 50 , (160 , 180 ,90))



        print(f"draw new frame : {round((time.perf_counter()-startTime) *1000 , 1)} ms")



    def on_update(self, delta_time: float):
        # print("self.activecells" , len(self.activecells))
        
        self.timer += delta_time
        if self.timer > 1/self.step_per_sec and not self.pause:
            self.timer = self.timer %  (1/self.step_per_sec)

            self.calculateNewFrame()



    def calculateNewFrame(self):
        startTime = time.perf_counter()
        

        # détermine toute les cellules à calculer
        CellsToCalculate = {}
        for cellCoordinates in self.activecells.values(): 
            CellsToCalculate[cellCoordinates] = cellCoordinates

            aroundCoordinates = self.getAroundCoordinates(cellCoordinates) 
            for Coo in aroundCoordinates :
                CellsToCalculate[Coo] = Coo


        newFrame = {}
        
        # print(len(CellsToCalculate))
        for cell in CellsToCalculate.values():
            # print(cell , self.getNeighborsCount(cell) , self.activecells.get(cell) is not None) 
            

            neighbors = self.getNeighborsCount(cell)
            wasactive = self.activecells.get(cell) is not None

            if  (2 > neighbors) or (neighbors > 3) : # meurent d'isolation ou de surpopulation 
                pass
            elif wasactive and neighbors == 2 :  # si il y avais déja une cellule et qu'elle a deux voisins, elle reste en vie
                newFrame[cell] = cell
            elif wasactive and neighbors == 3 :  # si il y avais déja une cellule et qu'elle a deux voisins, elle reste en vie
                newFrame[cell] = cell
            elif neighbors == 3 :                # si une cellule a 3 voisine, elle nait
                newFrame[cell] = cell

        self.activecells = {}
        self.activecells = newFrame

        print(f"Calculate new frame : {round((time.perf_counter()-startTime) *1000 , 1)} ms")
           

    def getAroundCoordinates(self , cellCoordinates):
        x,y = cellCoordinates[0] , cellCoordinates[1]
        return ( (x-1 , y+1) , (x,y+1) , (x+1,y+1) , (x-1,y) , (x+1,y) , (x-1,y-1) , (x,y-1) , (x+1,y-1))


    def getNeighborsCount(self , cellCoordinates) :
        count = 0

        for AroundCoo in self.getAroundCoordinates(cellCoordinates) :
            if self.activecells.get(AroundCoo) is not None :
                count += 1

        return count



    def loadMap(self , path):
        self.activecells = {}

        with open(path, newline='') as csvfile:
            reader = csv.reader(csvfile, delimiter=',')
            for row in reader:
                valuestuple  = (float(row[0]), float(row[1]))
                self.activecells[valuestuple] = valuestuple



    def SaveMap(self , path):
        with open(path, 'w' , newline='') as csvfile:
            writer = csv.writer(csvfile, delimiter=',')
            
            for cell in self.activecells.values():
                writer.writerow(cell)

        print("Saved Successfully !")





    def on_key_press(self, key: int, modifiers: int):

        def signe(x) :
            if x >= 0  : return 1
            else : return -1

        if key == arcade.key.SPACE :
            self.pause = not(self.pause)

        if key == arcade.key.RIGHT :
            self.step_per_sec *= 1.5

        if key == arcade.key.LEFT :
            self.step_per_sec /= 1.5

        if key == arcade.key.E :

            Xe,Ye = Physical_Screen.orgin_from_center_phy(self.camera_x, self.camera_y  , self.zoom, self.screen_x , self.screen_y ) 
            x , y = Physical_Screen.to_physic( Xe , Ye , self.mouse_pos_x , self.mouse_pos_y , self.zoom)

            signe_x = signe(x)
            signe_y = signe(y)
            cell_x = int( abs(x) + .5) * signe_x
            cell_y = int( abs(y) + .5) * signe_y
            cell = (cell_x , cell_y )

            if self.activecells.get(cell) is None :
                self.activecells[cell] = cell
            else :
                del self.activecells[cell]

        if key == arcade.key.R :
            self.activecells = {}

        if key == arcade.key.S :
            self.SaveMap(self.savePath)


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






if __name__ == '__main__':
    screen_x = 800
    screen_y = 800
    window = MyWindow()
    arcade.run()