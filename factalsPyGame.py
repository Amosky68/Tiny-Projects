import pygame
from time import perf_counter
import numpy
from arcade import lerp
from math import floor
from multiprocessing import process





class Fractal():
    

    def __init__(self , complexNumber : complex) -> None:
        self.ComplexNumber = complexNumber
        self.Maxiteration = 30



    def calculatePointsFromBounds(self , Bounds :  tuple):

        centerX , centerY , Width , Heigth = Bounds
        pointA = (centerX-Width , centerY+Heigth )
        pointB = (centerX+Width , centerY-Heigth )
        return pointA,pointB



    def get_julia(self,  ScreenShape : tuple ,  Bounds : tuple) :

        """
        ArrayShape : (X,Y)  \            
        Complex Number from julia set 
        Bounds : (centerX , centerY , Width , Heigth ) \n
        \n
        This fonction return a 2dArray filled with the time taken to know the nature of the value 
        (stable or not)
        """
        screenX , screenY = ScreenShape
        IterrationArray = numpy.ndarray(ScreenShape)

        points = self.calculatePointsFromBounds(Bounds)

        for x in range(screenX) :
            for y in range(screenY) :

                IterrationArray[x][y] = self.get_time_Taken(points , (x,y) , ScreenShape)

        return IterrationArray

        

    def get_time_Taken(self , points , pixelPosition , ScreenShape) :
        """
        points[0] = firts pixel on the top left 
        points[1] = second pixel on the bottom right 
        pixelPosition = position of the pixel based on the Pygame coordinates system 
        """

        screenX , screenY = ScreenShape
        planX  =  lerp(points[0][0] , points[1][0] , pixelPosition[0]/screenX)
        planY  =  lerp(points[0][1] , points[1][1] , pixelPosition[1]/screenY)
        Value = complex(planX , planY)
        # print(Value)

        i = 0
        
        while ( abs(Value) < 4 ) and ( i < self.Maxiteration ) : 

            Value = Value * Value + self.ComplexNumber
            # print(Value)
            i += 1

        return i

            







class Game:
    def __init__(self, screen):
        self.screen = screen
        self.running = True
        self.clock = pygame.time.Clock()
        self.pixelArray = pygame.PixelArray(self.screen)

        
        self.fractal = Fractal(0)
        self.fractal.Maxiteration = 100
        # for i in range(1080) :
        #     print( self.fractal.get_time_Taken( points = ( (-2,2) , (2,-2) )  , pixelPosition= (i,360) , ScreenShape=self.screen.get_size())  , (i,0))
        self.calculateJulia( -1 , 0 )
        


    def handling_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:   # 
                self.running = False


            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_a :   # if a is pressed we re-generate the julia set
                    self.calculateJulia( 0  ,  0 )

    


    def calculateJulia(self , real , imag):
        print("calculating Fractal...")
        self.fractal.ComplexNumber = complex(real , imag)

        start = perf_counter()
        screenX , screenY = self.screen.get_size()

        Bounds = ( 0 , 0 , 1.5 , 1.5 ) # Centre de l'écran , largeur , hauteur
        Julia_Values = self.fractal.get_julia(self.screen.get_size() , Bounds )

        print("drawing The Julia set")

        self.draw_Julia(screenX , screenY , Julia_Values)


        print(f"done in {perf_counter() - start} seconds ")




    def draw_Julia(self , screenX , screenY , Julia_Values) :

        for x in range(screenX) :
            for y in range(screenY) :
                self.pixelArray[x][y] = self.get_color(Julia_Values[x][y] , maxValue = self.fractal.Maxiteration)



    def get_color(self, value , maxValue):

        Colors = [(1, 0, 144,255) , (206, 205, 0,255) , (0,0,0,255)]
        t = value/(maxValue+1) * (len(Colors) - 1)
        newColor = [0,0,0,255]

        for rgba in range(4):

            ft = floor(t)
            value1 = Colors[ ft ][rgba]
            value2 = Colors[ ft + 1][rgba]

            newColor[rgba] = lerp( value1 , value2 , t - ft )

        return tuple(newColor)



    def update(self):
        
        
        # print(f"done in {perf_counter() - start} seconds ")
        # self.pixelArray[0][719] = pygame.Color('purple')
        # print(pygame.Color('purple'))
        
        pass



    def display(self):
        pygame.display.update()



    def run(self):
        while self.running:
            self.handling_events()
            self.update()
            self.display()
            self.clock.tick(60)




pygame.init()
screen = pygame.display.set_mode((1220, 920))
game = Game(screen)
game.run()

pygame.quit()