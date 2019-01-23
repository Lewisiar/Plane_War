import pygame
from plane_sprites import *

#Git say hello!
#bye~~
class PlaneGame(object):
    """飞机大战主程序"""

    # 初始化
    def __init__(self):
        # 创建游戏窗口
        self.screen = pygame.display.set_mode(SCREEN_RECT.size)

        # 创建时钟
        self.clock = pygame.time.Clock()

        # 调用私有方法，精灵和精灵组的创建
        self.__create_sprites()

        # 设置定时器事件 创建敌机 1s & 发射子弹 0.5s
        pygame.time.set_timer(CREATE_ENEMY_EVENT, 800) # 第二个参数是设置定时器时间 单位是ms
        pygame.time.set_timer(HERO_FIRE_EVENT, 500)

    def __create_sprites(self):

        # 创建背景精灵
        bg1 = Background()
        bg2 = Background(is_alt=True)

        self.back_group = pygame.sprite.Group(bg1, bg2)

        # 创建敌机精灵组
        self.enemy_group = pygame.sprite.Group()

        # 创建英雄机精灵
        self.hero = Hero()
        self.hero_group = pygame.sprite.Group(self.hero)

    def start_game(self):
        while True:

            # 设置刷新帧率
            self.clock.tick(FRAME_PER_SEC)

            # 事件监听
            self.__event_handle()

            # 碰撞检测
            self.__check_collide()

            # 更新/绘制精灵（组）
            self.__update_sprites()

            # 更新显示
            pygame.display.update()

    def __event_handle(self):
        for event in pygame.event.get():

            # 检测是否退出游戏
            if event.type == pygame.QUIT:
                self.__game_over()
            elif event.type == CREATE_ENEMY_EVENT:
                # print("敌机出现")
                # 创建精灵
                enemy = Enemy()
                # 添加进精灵组
                self.enemy_group.add(enemy)
            elif event.type == HERO_FIRE_EVENT:
                self.hero.fire()

            # 该方法需要松开键盘 才能算一次按键事件
            # elif event.type == pygame.KEYDOWN and event.key == pygame.K_RIGHT:
            #     print("向右飞行！")

        # 使用键盘提供的方法获取键盘按键 - 按键元组
        keys_pressed = pygame.key.get_pressed()

        # 判断元组中对应的按键索引值 1
        if keys_pressed[pygame.K_RIGHT]:
            self.hero.speed = 2
        elif keys_pressed[pygame.K_LEFT]:
            self.hero.speed = -2
        else:
            self.hero.speed = 0

    def __check_collide(self):
        # 子弹摧毁敌机
        pygame.sprite.groupcollide(self.hero.bullets, self.enemy_group, True, True)
        # print(destroy_list)
        # if len(destroy_dict) > 0:
        #     pass
        # 敌机摧毁英雄
        enemies = pygame.sprite.spritecollide(self.hero, self.enemy_group, True, False)

        if len(enemies) > 0:
            self.hero.kill()
            self.__game_over()

    def __update_sprites(self):
        self.back_group.update()
        self.back_group.draw(self.screen)

        self.enemy_group.update()
        self.enemy_group.draw(self.screen)

        self.hero_group.update()
        self.hero_group.draw(self.screen)

        self.hero.bullets.update()
        self.hero.bullets.draw(self.screen)

    @staticmethod
    def __game_over():
        print("游戏结束!")

        pygame.quit()
        exit()


if __name__ == '__main__':
    # 创建游戏对象
    game =  PlaneGame()

    # 启动游戏
    game.start_game()
