from pygame import *
mixer.pre_init(44100, -16, 1, 512)
mixer.init()
mixer.music.load('a5230bf64dffcb6.mp3')
mixer.music.play()
mixer.music.set_volume(0.3)
sound = mixer.Sound('2.ogg')


class GameSprite(sprite.Sprite):
    def __init__(self, player_image, player_x , player_y , size_x , size_y):
        super().__init__()
        self.image = transform.scale(image.load(player_image), (size_x , size_y))
        self.rect = self.image.get_rect()
        self.rect.x = player_x
        self.rect.y = player_y
    def reset(self):
        window.blit(self.image, self.rect)




class Player(GameSprite):
    def __init__(self, player_image , player_x , player_y , size_x , size_y ,  player_speed):
        super().__init__(player_image , player_x , player_y , size_x , size_y, )
        self.speed = player_speed
        self.lives = 3


    def update(self):
        keys = key.get_pressed()
        if keys[K_LEFT] and self.rect.x > 0:
            self.rect.x -= self.speed
            self.image = transform.rotate(self.image , 270) 
        if keys[K_RIGHT] and self.rect.x < 620:
            self.rect.x += self.speed
        if keys[K_UP] and self.rect.y > 0:
            self.rect.y -= self.speed
        if keys[K_DOWN] and self.rect.y < 420:
            self.rect.y += self.speed


    def fire(self):
        bullet = Bullet('weapon.png' , self.rect.right , self.rect.centery , 10 , 15 , 10 )
        bullets.add(bullet)
           






class Bullet(GameSprite):
    def __init__(self, player_image , player_x , player_y , size_x , size_y ,  player_speed):
        super().__init__(player_image , player_x , player_y , size_x , size_y, )
        self.speed = player_speed



    def update(self):
        self.rect.x += self.speed
        if self.rect.x > 710:
            self.kill()



        barriers_hit = sprite.spritecollide(self, barriers, False)
        for barrier in barriers_hit:
            self.kill()  
        
    
        




class Enemy(GameSprite):
    direction = 'left'
    def __init__(self, player_image , player_x , player_y , size_x , size_y ,  player_speed):
        super().__init__(player_image , player_x , player_y , size_x , size_y, )
        self.speed = player_speed



    def update(self): 
        if self.rect.x <= 400:
            self.direction = 'right'
        if self.rect.x >= 650:
            self.direction = 'left'
        if self.direction == 'left':
            self.rect.x -= self.speed
        else:
            self.rect.x += self.speed


         
    






win_width = 700
win_height = 500
display.set_caption('Пакмен')
window = display.set_mode((win_width , win_height)) 
background = transform.scale(image.load('galaxy_1.jpg'), (700,500))


barriers = sprite.Group()


bullets = sprite.Group()
w1 = GameSprite('platform_h.png', win_width / 2 - win_width / 3, win_height / 2 , 300 , 50)
w2 = GameSprite('platform_v.png', 370, 100 , 50 , 400)


barriers.add(w1)
barriers.add(w2)



monsters = sprite.Group()


Ghost =  Player('hero.png', 5, win_height - 80, 80, 80, 5)
enemy = Enemy('enemy.png', win_width - 80 , 180 , 80 , 80, 20 )
final_sprite = GameSprite('game-over_1.png', win_width - 85, win_height - 100 , 80 , 80)

monsters.add(enemy)

finish = False
clock = time.Clock()
run = True 
while run:
    keys = key.get_pressed()

    for e in event.get( ):
        if e.type == QUIT:
            run = False
        elif e.type == KEYDOWN:
            if e.key == K_SPACE:
                sound.play()
                Ghost.fire() 
        

    if not finish:
            window.blit(background,(0,0))
            



            barriers.draw(window)


            
            
            final_sprite.reset()
            Ghost.reset()
            bullets.draw(window)
            bullets.update()

            Ghost.update()
            sprite.groupcollide(monsters, bullets , True , True)
            monsters.draw(window)
            monsters.update()

            touched = sprite.spritecollide(Ghost , barriers , False)
            for platform in touched:
                if platform.rect.x > Ghost.rect.x and keys[K_RIGHT]:
                    Ghost.rect.x -= 20
                if platform.rect.x < Ghost.rect.x and keys[K_LEFT]:
                    Ghost.rect.x += 20
                if platform.rect.y < Ghost.rect.y and keys[K_UP]:
                    Ghost.rect.y += 20
                if platform.rect.y > Ghost.rect.y and keys[K_DOWN]:
                    Ghost.rect.y -= 20



            if  sprite.spritecollide(Ghost , monsters , False ):
                finish = True
                img = image.load('yoda_113476792_orig_.jpg')
                cago = img.get_width() // img.get_height()
                window.blit(transform.scale(img ,(win_height * cago , win_height)), (0,0))
                display.update()
                time.delay(2000)
                run = False            


    




            if sprite.collide_rect(Ghost , final_sprite):
                finish = True
                img = image.load('hitriy-getsbi_67346318_orig_.jpg')
                window.blit(transform.scale(img ,(win_width , win_height)),(0,0))
    display.update()
    clock.tick(30)
