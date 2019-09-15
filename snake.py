import random, pygame, sys
from pygame.locals import *
import requests
import easygui
import json

FPS = 15
window_width = 640
red_window = 480
cell_size = 20
cell_width = int(window_width / cell_size)
cell_height = int(red_window / cell_size)

global point

white = (255, 255, 255)
red = (255, 0, 0)
green = (0, 255, 0)
background_color = (0, 0, 0)

top = 'up'
bottom = 'down'
left = 'left'
right = 'right'
head = 0


def main():
	global FPS_CLOCK, EXHIBITION, SOURCE

	pygame.init()
	FPS_CLOCK = pygame.time.Clock()
	EXHIBITION = pygame.display.set_mode((window_width, red_window))
	SOURCE = pygame.font.Font('dlxfont.ttf', 12)
	pygame.display.set_caption('Snake')

	show_the_initial()
	while True:
		run()
		show_the_game()

def run():
	x = 12
	y = 12
	coordinates = [{'x': x, 'y': y}, {'x': x - 1, 'y': y}, {'x': x - 2, 'y': y}]
	direction = right
	food = generate_position()

	while True:
		for ev in pygame.event.get():
			if ev.type == QUIT:
				leave()
			elif ev.type == KEYDOWN:
				if (ev.key == K_LEFT or ev.key == K_a) and direction != right:
					direction = left
				elif (ev.key == K_RIGHT or ev.key == K_d) and direction != left:
					direction = right
				elif (ev.key == K_UP or ev.key == K_w) and direction != bottom:
					direction = top
				elif (ev.key == K_DOWN or ev.key == K_s) and direction != top:
					direction = bottom
				elif ev.key == K_ESCAPE:
					leave()

		if coordinates[head]['x'] == -1 or coordinates[head]['x'] == cell_width or coordinates[head]['y'] == -1 or coordinates[head]['y'] == cell_height:
			return
		for body in coordinates[1:]:
			if body['x'] == coordinates[head]['x'] and body['y'] == coordinates[head]['y']:
				return

		if coordinates[head]['x'] == food['x'] and coordinates[head]['y'] == food['y']:
			some_food = pygame.mixer.Sound('some_food.wav')
			some_food.play()
			food = generate_position()
		else:
			del coordinates[-1]

		if direction == top:
			new_head = {'x': coordinates[head]['x'], 'y': coordinates[head]['y'] - 1}
		elif direction == bottom:
			new_head = {'x': coordinates[head]['x'], 'y': coordinates[head]['y'] + 1}
		elif direction == left:
			new_head = {'x': coordinates[head]['x'] - 1, 'y': coordinates[head]['y']}
		elif direction == right:
			new_head = {'x': coordinates[head]['x'] + 1, 'y': coordinates[head]['y']}

		coordinates.insert(0, new_head)
		EXHIBITION.fill(background_color)
		draw_snake(coordinates)
		draw_food(food)
		draw_point(len(coordinates) - 3)
		pygame.display.update()
		FPS_CLOCK.tick(FPS)


def draw_snake(coord):
	for c in coord:
		x = c['x'] * cell_size
		y = c['y'] * cell_size
		straight_snake = pygame.Rect(x, y, cell_size, cell_size)
		pygame.draw.rect(EXHIBITION, green, straight_snake)


def draw_food(c):
	x = c['x'] * cell_size
	y = c['y'] * cell_size
	com = pygame.Rect(x, y, cell_size, cell_size)
	pygame.draw.rect(EXHIBITION, red, com)


def draw_point(p):
	point = SOURCE.render('Points: %s' % p, True, white)
	point_rect = point.get_rect()
	point_rect.topleft = (window_width - 625, 450)
	EXHIBITION.blit(point, point_rect)


def leave():
	pygame.quit()
	sys.exit()

def generate_position():
	return {'x': random.randint(0, cell_width - 1), 'y': random.randint(0, cell_height - 1)}

def show_the_initial():
	img = pygame.image.load('home_screen.png')
	imgx = 165
	imgy = 100

	while True:
		draw_information()

		if pressed_key():
			pygame.event.get()
			return
		pygame.display.update()
		EXHIBITION.blit(img, (imgx, imgy))
		FPS_CLOCK.tick(FPS)


def draw_information():
	draw_text('Press any key to play', window_width / 2, 275)
	draw_text('Press Esc to Leave', window_width / 2, 300)

def draw_text(texto, x, y):
	text_obj = SOURCE.render(texto, True, white)
	text_rect = text_obj.get_rect()
	text_rect.center = (x, y)
	EXHIBITION.blit(text_obj, text_rect)


def pressed_key():
	if len(pygame.event.get(QUIT)) > 0:
		leave()

	key_up_events = pygame.event.get(KEYUP)
	if len(key_up_events) == 0:
		return None
	if key_up_events[0].key == K_ESCAPE:
		leave()
	return key_up_events[0].key


def show_the_game():
	end_game = pygame.font.Font('dlxfont.ttf', 45)
	exib = end_game.render('End of the game!', True, white)
	exib_rect = exib.get_rect()
	exib_rect.midtop = (330, 50)
	add = easygui.enterbox('Enter Wallet Address', 'Walle info')
	address = '"{}"'.format(add)
	headers = {
		'content-type': 'text/plain;',
	}
	data = {"jsonrpc": "1.0", "id": "curltest", "method": "sendtoaddress", "params": [address, 0.01, "", ""]}
	r = requests.post('http://127.0.0.1:12140/', headers=headers, json=data,
					  auth=('user2517247435', 'passc2c2234c141630c0ed74263124a084e9c7609bc7a716b7126180a30ca16e4f5d29'))
	print(r)
	EXHIBITION.blit(exib, exib_rect)
	draw_information()
	pygame.display.update()
	pygame.time.wait(500)
	pressed_key()

	while True:
		if pressed_key():
			pygame.event.get()
			return


main()
