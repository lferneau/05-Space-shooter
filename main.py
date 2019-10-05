import sys, logging, os, random, math, open_color, arcade
import pyglet

version = (3,7)
assert sys.version_info >= version, "This script requires at least Python {0}.{1}".format(version[0],version[1])

logging.basicConfig(format='[%(filename)s:%(lineno)d] %(message)s', level=logging.DEBUG)
logger = logging.getLogger(__name__)

SCREEN_WIDTH = 2000
SCREEN_HEIGHT = 600
MARGIN = 30
SCREEN_TITLE = "Space War"

NUM_ENEMIES = 5
STARTING_LOCATION = (400,100)
BULLET_DAMAGE = 10
ENEMY_HP = 100
HIT_SCORE = 10
KILL_SCORE = 110



class Bullet(arcade.Sprite):
    def __init__(self, position, velocity, damage):
        ''' 
        initializes the bullet
        Parameters: position: (x,y) tuple
            velocity: (dx, dy) tuple
            damage: int (or float)
        '''
        super().__init__("assets/new_bullet.png", 0.5)
        (self.center_x, self.center_y) = position
        (self.dx, self.dy) = velocity
        self.damage = damage

    def update(self):
        '''
        Moves the bullet
        '''
        self.center_x += self.dx
        self.center_y += self.dy


    
class Player(arcade.Sprite):
    def __init__(self):
        super().__init__("assets/DurrrSpaceShip.png", 0.5)
        (self.center_x, self.center_y) = STARTING_LOCATION

class Enemy(arcade.Sprite):
    def __init__(self, position):
        '''
        initializes a UFO enemy
        Parameter: position: (x,y) tuple
        '''
        super().__init__("assets/Nave.png", 0.5)
        self.hp = ENEMY_HP
        (self.center_x, self.center_y) = position


        


class Window(arcade.Window):
    
    
    def __init__(self, width, height, title):
        super().__init__(width, height, title)
        file_path = os.path.dirname(os.path.abspath(__file__))
        os.chdir(file_path)

        self.set_mouse_visible(True)
        arcade.set_background_color(open_color.black)
        self.bullet_list = arcade.SpriteList()
        self.enemy_list = arcade.SpriteList()
        self.player = Player()
        self.score = 0


    def setup(self):
        '''
        Set up enemies
        '''
        for i in range(NUM_ENEMIES):
            x = 265 * (i+1) + 40
            y = 500
            enemy = Enemy((x,y))
            self.enemy_list.append(enemy) 
        song = pyglet.media.load('bensound-scifi.mp3')
        song.play()
        pyglet.app.run()   

    def update(self, delta_time):
        self.bullet_list.update()
        for e in self.enemy_list:
            damage = arcade.check_for_collision_with_list(e, self.bullet_list)
            for d in damage:
                e.hp -= d.damage
                d.kill()
                if e.hp <= 0:
                    self.score += KILL_SCORE
                    e.kill()
                else:
                    self.score += HIT_SCORE
                if e.hp == 0:
                    song = pyglet.media.load('victory.wav')
                    song.play()
                
         

    def on_draw(self):
        arcade.start_render()
        arcade.draw_text(str(self.score), 20, SCREEN_HEIGHT - 40, open_color.white, 16)
        self.player.draw()
        self.bullet_list.draw()
        self.enemy_list.draw()
        if len(self.enemy_list) == 0:
            arcade.draw_text('YOU ARE VICTORIOUS!', 375, SCREEN_HEIGHT - 60, open_color.red_2, 24)
            arcade.draw_text('THANKS FOR PLAYING!', 375, SCREEN_HEIGHT - 100, open_color.red_2, 24)
        #if len(self.enemy_list) == 0:
            #import pyglet
            #song = pyglet.media.load('victory.wav')
            #song.play()
            #pyglet.app.run()
        #I was trying to get this to work, but it would keep repeating the track indefinetely from the start

    def on_mouse_motion(self, x, y, dx, dy):
        '''
        The player moves left and right with the mouse
        '''
        self.player.center_x = x


    def on_mouse_press(self, x, y, button, modifiers):
        if len(self.enemy_list) >= 1:    
            if button == arcade.MOUSE_BUTTON_LEFT:
                x = self.player.center_x
                y = self.player.center_y + 15
                bullet = Bullet((x,y),(0,10),BULLET_DAMAGE)
                self.bullet_list.append(bullet)
            import pyglet
            song = pyglet.media.load('laser_sound.wav')
            song.play()
            pyglet.app.run()



def main():
    window = Window(SCREEN_WIDTH, SCREEN_HEIGHT, SCREEN_TITLE)
    window.setup()
    arcade.run()
    


if __name__ == "__main__":
    main()