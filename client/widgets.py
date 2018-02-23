import abc
import pygame
from itertools import takewhile

class Widget(metaclass=abc.ABCMeta):

    @abc.abstractmethod
    def draw(self):
        pass

    @abc.abstractmethod
    def erase(self):
        pass

class Button(Widget, metaclass=abc.ABCMeta):

    @abc.abstractmethod
    def draw(self):
        pass

    @abc.abstractmethod
    def erase(self):
        pass
    
    @abc.abstractmethod
    def mouse_click(self):
        pass

#draws image with opacity
def blit_alpha(display, source, location, opacity):
    #negative = set(map(lambda x: -1*x, location))
    x = location[0]
    y = location[1]
    temp = pygame.Surface((source.get_width(), source.get_height())).convert()
    temp.blit(display, (-x, -y))
    temp.blit(source, (0, 0))
    temp.set_alpha(opacity)        
    display.blit(temp, location)

class TakeSeatButton(Button):

    def __init__(self, position, seat_number, client):
        self.position = position
        self.seat_number = seat_number
        self.image = pygame.image.load("images/take.png")
        self.parent = client
        self.kind = 'seat button'

    def draw(self):
        mouse = pygame.mouse.get_pos()
        click = pygame.mouse.get_pressed()
        
        x, y = self.position
        w, h = self.image.get_rect().size

        self.erase()
        if x+w>mouse[0]>x and y+h>mouse[1]>y:
            self.parent.display.blit(self.image, self.position)
            if(click[0]==1):
                self.parent.last_clicked_button = self
        else:
            blit_alpha(self.parent.display, self.image, self.position, 210)
                
    def erase(self):
        self.parent.display.blit(self.parent.bg, self.position, pygame.Rect(self.position, self.image.get_rect().size))

    def mouse_click(self):
        self.parent.sender.take_seat(self.parent.address, self.seat_number)

class CheckButton(Button):

    def __init__(self, position, client):
        self.position = position
        self.image = pygame.image.load("images/check.png")
        self.parent = client
        self.kind = 'bet button'

    def draw(self):
        mouse = pygame.mouse.get_pos()
        click = pygame.mouse.get_pressed()
        
        x, y = self.position
        w, h = self.image.get_rect().size

        self.erase()
        if x+w>mouse[0]>x and y+h>mouse[1]>y:
            self.parent.display.blit(self.image, self.position)
            if(click[0]==1):
                self.parent.last_clicked_button = self
        else:
            blit_alpha(self.parent.display, self.image, self.position, 210)
                
    def erase(self):
        self.parent.display.blit(self.parent.bg, self.position, pygame.Rect(self.position, self.image.get_rect().size))

    def mouse_click(self):
        self.parent.sender.check()

class FoldButton(Button):

    def __init__(self, position, client):
        self.position = position
        self.image = pygame.image.load("images/fold.png")
        self.parent = client
        self.kind = 'bet button'

    def draw(self):
        mouse = pygame.mouse.get_pos()
        click = pygame.mouse.get_pressed()
        
        x, y = self.position
        w, h = self.image.get_rect().size

        self.erase()
        if x+w>mouse[0]>x and y+h>mouse[1]>y:
            self.parent.display.blit(self.image, self.position)
            if(click[0]==1):
                self.parent.last_clicked_button = self
        else:
            blit_alpha(self.parent.display, self.image, self.position, 210)
                
    def erase(self):
        self.parent.display.blit(self.parent.bg, self.position, pygame.Rect(self.position, self.image.get_rect().size))

    def mouse_click(self):
        self.parent.sender.fold()

class CallButton(Button):

    def __init__(self, position, call_value, client):
        self.position = position
        self.image = pygame.image.load("images/call.png")
        self.call_value = call_value
        self.parent = client
        self.kind = 'bet button'

        image_size = self.image.get_rect().size
        self.label = client.myfont.render(str(round(call_value)), True, (255,255,255))
        l_size = self.label.get_rect().size

        x, y = position
        label_x = x + image_size[0]/2 - l_size[0]/2
        label_y = y + image_size[1]/2
        self.label_position = (label_x, label_y)
        
        
    def draw(self):
        mouse = pygame.mouse.get_pos()
        click = pygame.mouse.get_pressed()
        
        x, y = self.position
        w, h = self.image.get_rect().size

        self.erase()
        if x+w>mouse[0]>x and y+h>mouse[1]>y:
            self.parent.display.blit(self.image, self.position)
            if(click[0]==1):
                self.parent.last_clicked_button = self
        else:
            blit_alpha(self.parent.display, self.image, self.position, 210)

        self.parent.display.blit(self.label, self.label_position)
                
    def erase(self):
        self.parent.display.blit(self.parent.bg, self.position, pygame.Rect(self.position, self.image.get_rect().size))

    def mouse_click(self):
        self.parent.sender.call(self.call_value)
    
class Slider(Widget):
    def __init__(self):
        self.WHITE = (255, 255, 255)
        self.TRANS = (1, 1, 1)

        self.val = 0  # start value
        self.maxi = 0  # maximum at slider position right
        self.mini = 0  # minimum at slider position left
        self.xpos = 540  # x-location on screen
        self.ypos = 495 # y-location on screen

        self.hit = False  # the hit attribute indicates slider movement due to mouse interaction

        # button surface #
        self.button_surf = pygame.surface.Surface((20, 20))
        self.button_surf.fill(self.TRANS)
        self.button_surf.set_colorkey(self.TRANS)
        self.button_surf.blit(pygame.image.load("images/slider_button.png"),(0,0))

    def draw(self, screen):
        screen.blit(pygame.image.load("images/table.png"), (self.xpos, self.ypos), pygame.Rect((self.xpos, self.ypos),(120, 25)))
        surf = pygame.surface.Surface((120, 25), pygame.SRCALPHA, 32)
        surf.blit(pygame.image.load("images/slider_scale.png"),(0,8))

        pos = (10+int((self.val-self.mini)/(self.maxi-self.mini)*100), 13)
        self.button_rect = self.button_surf.get_rect(center=pos)
        surf.blit(self.button_surf, self.button_rect)
        self.button_rect.move_ip(self.xpos, self.ypos)  # move of button box to correct screen position

        screen.blit(surf, (self.xpos, self.ypos))
    
    def erase(self):
        pass
    
    def move(self):
        """
        The dynamic part; reacts to movement of the slider button.
        """
        self.val = (pygame.mouse.get_pos()[0] - self.xpos - 10) / 100 * (self.maxi - self.mini) + self.mini
        if self.val < self.mini:
            self.val = self.mini
        if self.val > self.maxi:
            self.val = self.maxi

class Player(Widget):

    def __init__(self, position, seat_number, name, chips, on_move, bet, cards, address, client):
        self.position = position
        self.seat_number = seat_number
        self.name = name
        self.chips = chips
        self.on_move = on_move
        self.parent = client
        self.address = address
        
        self.cards = []
        x, y = client.cards_coord[seat_number]
        for card in cards:
            self.cards.append(PlayerCard((x, y), card, address, client))
            x += 60

        x, y = self.position

        self.name_label = self.parent.myfont.render(self.name, True, pygame.Color('white'))
        l_size = self.name_label.get_rect().size
        self.chips_label = self.parent.myfont.render(str(self.chips)+' $', True, pygame.Color('white'))
        c_size = self.chips_label.get_rect().size

        if(self.seat_number >= 4):
            side = 'left'
            self.l_x = x + 100 - l_size[0]/2
            self.c_x = x + 100 - c_size[0]/2
        else:
            side = 'right'
            self.l_x = x + 50 - l_size[0]/2
            self.c_x = x + 50 - c_size[0]/2

        if(self.on_move):
            color = "green"
        else:
            color = "purple"

        self.l_y = y + 15
        self.c_y = y + 37

        self.image = pygame.image.load("images/"+color+"_"+side+".png")

        self.bet = Chips(client.chips_coord[seat_number], bet, seat_number, client)

    def draw(self):

        self.erase()

        for card in self.cards:
            card.draw()

        self.parent.display.blit(self.image, self.position)
        self.parent.display.blit(self.name_label, (self.l_x, self.l_y))
        self.parent.display.blit(self.chips_label, (self.c_x, self.c_y))
        
        self.bet.draw()
    
    def erase(self):
        for card in self.cards:
            card.erase()
        
        self.bet.erase()
        self.parent.display.blit(self.parent.bg, self.position, pygame.Rect(self.position, self.image.get_rect().size))

class EmptySeat(Widget):

    def __init__(self, position, seat_number, client):
        self.position = position
        self.seat_number = seat_number
        self.image = pygame.image.load("images/empty.png")
        self.parent = client

    def draw(self):
        self.erase()
        blit_alpha(self.parent.display, self.image, self.position, 128)
                
    def erase(self):
        self.parent.display.blit(self.parent.bg, self.position, pygame.Rect(self.position, self.image.get_rect().size))

class Chips(Widget):

    def __init__(self, position, total, seat_number, client):
        self.position = position
        self.parent = client
        self.total = total
        
        self.chips_histogram = self.create_chips_histogram(total)
        columns = self.group_chips()
        
        self.chips = []

        x, y = self.position
        start_y = y
        for column in columns:
            for chips in column:
                for i in range(0,chips[1]):
                    self.chips.append(Chip(chips[0], (x, y), client))
                    y -= 5
            y = start_y
            if(int(seat_number)>=4):
                x -= 22
            else:
                x += 22
        
    def create_chips_histogram(self, total):
        chips = takewhile(lambda x: x<=total, self.parent.chips)
        chips = list(chips)
        chips_hist={}

        for chip in reversed(chips):
            i = 0
            while ((total-chip)>=0):
                total-=chip
                i+=1
                chips_hist[chip]=i #histogram : key chip, value count
            if(total<1):
                break
        
        return chips_hist
    
    def group_chips(self):
        chips = [[],[],[],[]]
        i = 0
        for item in self.chips_histogram.items():
            if(i==4):
                i = 0
            chips[i].append(item)
            i+=1
        return chips

    def draw(self):
        for chip in self.chips:
            chip.draw()
                
    def erase(self):
        for chip in self.chips:
            chip.erase()

class Chip(Widget):

    def __init__(self, count, position, client):
        self.count = count
        self.position = position
        self.parent = client
        self.image = pygame.image.load("images/chips/"+str(count)+".png")

    def draw(self):
        self.parent.display.blit(self.image, self.position)
                
    def erase(self):
        self.parent.display.blit(self.parent.bg, self.position, pygame.Rect(self.position, self.image.get_rect().size))
    
class PlayerCard(Widget):

    def __init__(self, position, card, address, client):
        self.position = position
        self.card = card
        self.parent = client
        
        if client.address == address:
            self.image = pygame.image.load("images/cards/"+card+".png")
        else:
            self.image = pygame.image.load("images/cards/0.png")

    def draw_image_part(self, image, coord, size):
        self.parent.display.blit(image, coord, pygame.Rect((0,0), size))

    def draw(self):
        self.draw_image_part(self.image, self.position, (60,60))
                
    def erase(self):
        self.parent.display.blit(self.parent.bg, self.position, pygame.Rect(self.position, self.image.get_rect().size))
