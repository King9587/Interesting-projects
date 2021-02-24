
import random
import pygame

# 屏幕大小的常量
SCREEN_RECT = pygame.Rect(0, 0, 480, 700)
# 创建敌机的事件
CREATE_ENEMY_EVENT = pygame.USEREVENT
# 英雄飞机发射子弹的事件
HERO_FIRE_EVENT = pygame.USEREVENT + 1


class GameSprite(pygame.sprite.Sprite):
    """游戏主类——继承自pygame.sprite.Sprite"""

    def __init__(self, image_name, speed=1):
        # 调用父类的初始化方法
        super().__init__()
        # 定义属性
        self.image = pygame.image.load(image_name)
        self.rect = self.image.get_rect()
        self.speed = speed

    def update(self):
        # 在屏幕的垂直方向向下移动
        self.rect.y += self.speed


class BackGround(GameSprite):
    """背景类，继承自GameSprite"""

    def __init__(self, is_alt=False):
        # 调用父类方法创建精灵对象
        super().__init__("./游戏素材/background.png")
        # 判断是否为背景图像2，若是则改变初始坐标位置
        if is_alt:
            self.rect.bottom = 0

    def update(self):
        # 调用父类方法——向下移动
        super().update()
        if self.rect.y >= SCREEN_RECT.height:
            self.rect.bottom = 0


class Enemy(GameSprite):
    """敌机精灵类，继承自GameSprite"""

    def __init__(self):
        # 随机抽取敌机
        number = random.randint(1, 3)
        if number == 1:
            # 调用父类方法创建精灵对象
            super().__init__("./游戏素材/enemy1.png")
            # 随机抽取出场位置
        elif number == 2:
            # 调用父类方法创建精灵对象
            super().__init__("./游戏素材/enemy2.png")
        elif number == 3:
            # 调用父类方法创建精灵对象
            super().__init__("./游戏素材/enemy3_n1.png")

        # 随机抽取出场位置
        self.rect.x = random.randrange(
            0, (SCREEN_RECT.width - self.rect.width), 1)
        # 随机抽取出场速度
        self.speed = random.randint(1, 3)
        # 初始位置应该在游戏主窗口的上方
        self.rect.bottom = 0

    def update(self):
        # 调用父类方法——向下移动
        super().update()
        # 判断是否飞出屏幕，是则释放
        if self.rect.y >= SCREEN_RECT.height:
            self.kill()


class Hero(GameSprite):
    """英雄飞机类，继承自GameSprite"""

    def __init__(self):
        # 设置速度为0
        super().__init__("./游戏素材/me1.png", speed=0)
        # 位于游戏主窗口的中央
        self.rect.centerx = SCREEN_RECT.centerx
        self.rect.bottom = SCREEN_RECT.height - 10
        # 创建子弹精灵组
        self.bullet_group = pygame.sprite.Group()

    def update(self):
        # 英雄飞机在水平方向移动且不能移出边界
        if self.rect.x < 0:
            self.rect.x = 0
        elif self.rect.right > SCREEN_RECT.width:
            self.rect.right = SCREEN_RECT.width
        else:
            self.rect.x += self.speed

    def fire(self):
        """英雄飞机发射子弹"""
        for i in (0, 1, 2):
            # 创建子弹精灵
            bullet = Bullet()
            # 设定子弹精灵的位置，应该与英雄飞机的正上方中央发射
            bullet.rect.y = self.rect.y - 2 * i * bullet.rect.height
            bullet.rect.centerx = self.rect.centerx
            # 子弹精灵加入精灵组
            self.bullet_group.add(bullet)


class Bullet(GameSprite):
    """子弹类，继承自GameSprite"""

    def __init__(self):
        super().__init__("./游戏素材/bullet1.png", speed=-3)

    def update(self):
        # 调用父类方法——向下移动
        super().update()
        # 判断子弹是否飞出屏幕，是则释放
        if self.rect.bottom <= 0:
            self.kill()
