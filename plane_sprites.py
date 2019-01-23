import random
import pygame

# 屏幕大小常量(全部大写，单词之间用下划线连接)
SCREEN_RECT = pygame.Rect(0, 0, 480, 700)

# 刷新帧率
FRAME_PER_SEC = 60

# 创建敌机的定时器常量
CREATE_ENEMY_EVENT = pygame.USEREVENT

# 英雄发射子弹事件常量
HERO_FIRE_EVENT = pygame.USEREVENT + 1


class GameSprite(pygame.sprite.Sprite):
    """飞机大战游戏精灵"""

    def __init__(self, image_name, speed=1):

        # 重写__init__()方法时需要调用父类的初始化方法，保证父类的初始化完成
        super().__init__()

        self.image = pygame.image.load(image_name)
        self.rect = self.image.get_rect()
        self.speed = speed

    def update(self):

        # 在屏幕垂直方向上移动
        self.rect.y += self.speed


class Background(GameSprite):
    """游戏背景精灵"""

    def __init__(self, is_alt=False):
        super().__init__("./images/background.png")

        if is_alt:
            self.rect.y = -self.rect.height

    def update(self):

        # 调用父类的方法实现
        super().update()

        # 交替轮换
        if self.rect.y >= SCREEN_RECT.height:
            self.rect.y = -self.rect.height


class Enemy(GameSprite):

    def __init__(self):
        # 调用父类方法，创建敌机，同时制定敌机图片
        super().__init__("./images/enemy"+str(random.randint(1, 3)) +".png")

        # 随机速度
        self.speed = random.randint(1, 3)
        # 随机位置
        self.rect.bottom = 0
        self.rect.x = random.randint(0, SCREEN_RECT.width - self.rect.width)

    def update(self):
        # 调用父类方法， 保持敌机飞行方向
        super().update()

        if self.rect.y >= SCREEN_RECT.height:

            # kill方法可将精灵从精灵组中移出，精灵自动被销毁
            self.kill()

    # 可用于判断判断是否释放内存
    # def __del__(self):
    #     print("移出内存 %s" %self.rect)

    # def destroy(self):
    #     pass


class Bullet(GameSprite):
    def __init__(self):
        super().__init__("./images/bullet1.png", -2)

    def update(self):
        super().update()

        if self.rect.bottom < 0:
            self.kill()


class Hero(GameSprite):
    def __init__(self):
        super().__init__("./images/me1.png")

        # 初始位置
        self.rect.centerx = SCREEN_RECT.centerx
        self.rect.bottom = SCREEN_RECT.height - 120

        # 创建子弹的精灵组
        self.bullets = pygame.sprite.Group()

    def update(self):
        self.rect.y -= 0

        # 左右移动
        self.rect.x += self.speed

        # 控制飞行范围
        if self.rect.x < 0:
            self.rect.x = 0
        elif self.rect.right > SCREEN_RECT.right:
            self.rect.right = SCREEN_RECT.right

    def fire(self):
        # 每次只发射一颗子弹
        # bullet = Bullet()
        #
        # bullet.rect.bottom = self.rect.y - 20
        # bullet.rect.centerx = self.rect.centerx
        #
        # self.bullets.add(bullet)

        # 每次发射3颗子弹
        for i in (0, 1, 2):

            bullet = Bullet()

            bullet.rect.bottom = self.rect.y - 20 * i
            bullet.rect.centerx = self.rect.centerx

            self.bullets.add(bullet)