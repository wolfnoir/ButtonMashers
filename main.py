import pygame as pg
import random

# Set up dimensions for screen, and other constants.
# Image position constants.
SCREEN_WIDTH = 1920
SCREEN_HEIGHT = 1080
SPRITE_WIDTH = 333
SPRITE_HEIGHT = 366
KEY_BOX_WH = 150
COUNTER_BOX_WH = 90
BACKGROUND_MOD = 0.8
PLAYER_MOD_W = 527
PLAYER_MOD_H = 900
BACKGROUND_IMG_COORD = (194, 110)
RED_END = (200, 300)
BLUE_END = (1300, 300)
# Other constants.
FRAMES_PER_SECOND = 60
WIN_NUMBER = 50
# Colors.
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
BLUE = (0, 0, 255)
# Counter for scores of players
p1Counter = 0
p2Counter = 0

#boolean to play the game over music only once
gameOverMusic = False

# Create variables to keep track of game state and game difficulty.
gameState = "START"
hardMode = False

# Set up pygame, screen, clock, text, and more fundamental components.
pg.init()
pg.mixer.init()
pg.font.init()
pg.display.set_caption('ButtonMashers - an SBUHacks Game')
screen = pg.display.set_mode((0, 0), pg.FULLSCREEN)
clock = pg.time.Clock()
gameFont = pg.font.SysFont('Roboto Black', 42)
winConditionFont = pg.font.SysFont('Friday13', 48)
roundOverFont = pg.font.SysFont('Impact', 120)
countdownFont = pg.font.SysFont('Friday13', 100)

# Load images.
# Load background images such as the title screen, main background, and victory screens.
titleScreenImage = pg.transform.scale(pg.image.load('img/ButtonMashers_Title_Screen_Difficulty.jpg'),
	(int(SCREEN_WIDTH * BACKGROUND_MOD), int(SCREEN_HEIGHT * BACKGROUND_MOD))).convert_alpha()
backgroundScreenImage = pg.transform.scale(pg.image.load('img/ButtonMashers_Background_Screen.jpg'),
	(int(SCREEN_WIDTH * BACKGROUND_MOD), int(SCREEN_HEIGHT * BACKGROUND_MOD)))
victoryImageRed = pg.transform.scale(pg.image.load('img/ButtonMashers_Victory_Red.jpg'),
	(int(SCREEN_WIDTH * BACKGROUND_MOD), int(SCREEN_HEIGHT * BACKGROUND_MOD)))
victoryImageBlue = pg.transform.scale(pg.image.load('img/ButtonMashers_Victory_Blue.jpg'),
	(int(SCREEN_WIDTH * BACKGROUND_MOD), int(SCREEN_HEIGHT * BACKGROUND_MOD)))
# Create sprites for Fighter 1.
p1SpriteIdle = pg.transform.scale(pg.image.load('img/Fighter_Red_Idle.png'),  (SPRITE_WIDTH, SPRITE_HEIGHT))
p1SpriteAttack = pg.transform.scale(pg.image.load('img/Fighter_Red_Attack.png'),  (SPRITE_WIDTH, SPRITE_HEIGHT))
p1SpriteDamage = pg.transform.scale(pg.image.load('img/Fighter_Red_Damage.png'),  (SPRITE_WIDTH, SPRITE_HEIGHT))
# Create sprites for Fighter 2.
p2SpriteIdle = pg.transform.scale(pg.image.load('img/Fighter_Blue_Idle.png'),  (SPRITE_WIDTH, SPRITE_HEIGHT))
p2SpriteAttack = pg.transform.scale(pg.image.load('img/Fighter_Blue_Attack.png'),  (SPRITE_WIDTH, SPRITE_HEIGHT))
p2SpriteDamage = pg.transform.scale(pg.image.load('img/Fighter_Blue_Damage.png'),  (SPRITE_WIDTH, SPRITE_HEIGHT))
# Create images for Red and Blue Key boxes.
redKeyBox = pg.transform.scale(pg.image.load('img/ButtonMashers_Key_Red.png'), (KEY_BOX_WH, KEY_BOX_WH))
blueKeyBox = pg.transform.scale(pg.image.load('img/ButtonMashers_Key_Blue.png'), (KEY_BOX_WH, KEY_BOX_WH))
# Create images for red and blue score boxes.
redCounterBox = pg.transform.scale(pg.image.load('img/ButtonMashers_Key_Red.png'), (COUNTER_BOX_WH, COUNTER_BOX_WH))
blueCounterBox = pg.transform.scale(pg.image.load('img/ButtonMashers_Key_Blue.png'), (COUNTER_BOX_WH, COUNTER_BOX_WH))
# Create images for Red and Blue victory poses.
redWins = pg.transform.scale(pg.image.load('img/Red_Victory.png'), (int(PLAYER_MOD_W * 0.75), int(PLAYER_MOD_H * 0.75)))
redLoses = pg.transform.scale(pg.image.load('img/Red_Loss.png'), (int(PLAYER_MOD_W * 0.75), int(PLAYER_MOD_H * 0.75)))
blueWins = pg.transform.scale(pg.image.load('img/Blue_Victory.png'), (int(PLAYER_MOD_W * 0.75), int(PLAYER_MOD_H * 0.75)))
blueLoses = pg.transform.scale(pg.image.load('img/Blue_Loss.png'), (int(PLAYER_MOD_W * 0.75), int(PLAYER_MOD_H * 0.75)))

# Create sounds that will play over music.
hitEffect = pg.mixer.Sound('sound/hitSFX.wav')
buttonMashersVoice = pg.mixer.Sound('sound/buttonMashersVoice.wav')
countdownVoice = pg.mixer.Sound('sound/countdownVoice.wav')
redWinsVoice = pg.mixer.Sound('sound/redWinsVoice.wav')
blueWinsVoice = pg.mixer.Sound('sound/blueWinsVoice.wav')
noContestVoice = pg.mixer.Sound('sound/noContestVoice.wav')

# Load title screen music.
pg.mixer.music.load('sound/titleMusic.wav')

# Play initial music and sounds.
buttonMashersVoice.play()
pg.time.delay(1500)
pg.mixer.music.play()

# Set up timers and state, along with other miscellaneous things.
startPressed = False
pg.time.set_timer(pg.USEREVENT+1, 50)
screenIntensity = 200

# Declare Win condition counter.
winCondition = "Fifty Points to Win"

# Main event loop:
while True:
	clock.tick(FRAMES_PER_SECOND)
	# Display title screen image if Spacebar has not been pressed.
	if not startPressed:
		screen.blit(titleScreenImage, BACKGROUND_IMG_COORD)

	# listen for events.
	for event in pg.event.get():
		# Listen for key events.
		if event.type == pg.KEYDOWN:
			# Quit with escape key.
			if event.key == pg.K_ESCAPE:
				quit()
			# Enter 'EASY' mode.
			if event.key == pg.K_1:
				startPressed = True
				hardMode = False
				# Create list of keys and generate the initial keys for both players.
				keysLeft = [pg.K_1, pg.K_2, pg.K_3, pg.K_4, pg.K_5, pg.K_q,
							pg.K_w, pg.K_e, pg.K_r, pg.K_t, pg.K_a, pg.K_s,
							pg.K_d, pg.K_f, pg.K_z, pg.K_x, pg.K_c, pg.K_v]
				keysRight = [pg.K_6, pg.K_7, pg.K_8, pg.K_9, pg.K_0, pg.K_y,
							pg.K_u, pg.K_i, pg.K_o, pg.K_p, pg.K_g,  pg.K_h,
							pg.K_j, pg.K_k, pg.K_l,  pg.K_b, pg.K_n, pg.K_m]
				p1Key = random.choice(keysLeft)
				p2Key = random.choice(keysRight)

				#stop the title screen music
				pg.mixer.music.stop()
				# Load initial sound effect.
				pg.mixer.music.load('sound/gameStartSFX.wav')
				# Play game start sound
				pg.mixer.music.play()

			# Enter 'HARD' mode.
			elif event.key == pg.K_2:
				startPressed = True
				hardMode = True
				# Create list of keys and generate the initial keys for both players.
				keys = [pg.K_1, pg.K_2, pg.K_3, pg.K_4, pg.K_5, pg.K_6,
						pg.K_7, pg.K_8, pg.K_9, pg.K_0, pg.K_a, pg.K_b,
						pg.K_c, pg.K_d, pg.K_e, pg.K_f, pg.K_g, pg.K_h,
						pg.K_i, pg.K_j, pg.K_k, pg.K_l, pg.K_m, pg.K_n,
						pg.K_o, pg.K_p, pg.K_q, pg.K_r, pg.K_s, pg.K_t,
						pg.K_u, pg.K_v, pg.K_w, pg.K_x, pg.K_y, pg.K_z]
				p1Key = random.choice(keys)
				p2Key = random.choice(keys)

				#stop the title screen music
				pg.mixer.music.stop()
				# Load initial sound effect.
				pg.mixer.music.load('sound/gameStartSFX.wav')
				# Play game start sound
				pg.mixer.music.play()	

		# Listen for timer events once SPACEBAR has been pressed.
		elif event.type == pg.USEREVENT+1 and startPressed:
			# Fade out screen.
			if screenIntensity >= 0:
				screen.fill((screenIntensity, screenIntensity, screenIntensity))
			screenIntensity -= 5	
			# Once screen is faded out, display main background image after a short delay.
			if screenIntensity <= 0:
				pg.time.delay(250)
				
				screen.blit(backgroundScreenImage, BACKGROUND_IMG_COORD)
				gameState = "COUNTDOWN"
				# Start a new loop.
				while True:
					if gameState == "COUNTDOWN":
						# Render game background, fighters, key boxes and initial keys to the screen.
						screen.fill(BLACK)
						screen.blit(backgroundScreenImage, BACKGROUND_IMG_COORD)
						screen.blit(p1SpriteIdle, (715, 420))
						screen.blit(p2SpriteIdle, (885, 420))
						screen.blit(redKeyBox, (450, 150))
						screen.blit(redCounterBox, (350, 180))
						screen.blit(blueKeyBox, (1330, 150))	
						screen.blit(blueCounterBox, (1490, 180))
						screen.blit(gameFont.render(str(chr(p1Key)).upper(), True, RED), (510, 200))
						screen.blit(gameFont.render(str(p1Counter), True, BLACK), (380, 200))
						screen.blit(gameFont.render(str(chr(p2Key)).upper(), True, BLUE), (1395, 200))
						screen.blit(gameFont.render(str(p2Counter), True, BLACK), (1520, 200))
						screen.blit(winConditionFont.render(winCondition, True, BLACK), (802, 152))
						screen.blit(winConditionFont.render(winCondition, True, WHITE), (800, 150))

						screen.blit(countdownFont.render("3...2...1...START!", True, BLACK), (707, 242))
						screen.blit(countdownFont.render("3...2...1...START!", True, RED), (705, 240))
						# Update display.
						pg.display.flip()

						countdownVoice.play()
						pg.time.delay(3700)

						#load in the fight music
						pg.mixer.music.load('sound/fightMusic.wav')
						pg.mixer.music.play()

						gameState = "GAME"

						#Handle quitting Python
						for event in pg.event.get():
							# Quit python
							if event.type == pg.QUIT:
								quit()
							# Listen for key events.
							elif event.type == pg.KEYDOWN:
								# Quit with escape key.
								if event.key == pg.K_ESCAPE:
									quit()	

					if gameState == "GAME":						
						# Render game background, fighters, key boxes and initial keys to the screen.
						screen.fill(BLACK)
						screen.blit(backgroundScreenImage, BACKGROUND_IMG_COORD)
						screen.blit(p1SpriteIdle, (715, 420))
						screen.blit(p2SpriteIdle, (885, 420))
						screen.blit(redKeyBox, (450, 150))
						screen.blit(redCounterBox, (350, 180))
						screen.blit(blueKeyBox, (1330, 150))	
						screen.blit(blueCounterBox, (1490, 180))
						screen.blit(gameFont.render(str(chr(p1Key)).upper(), True, RED), (510, 200))
						screen.blit(gameFont.render(str(p1Counter), True, BLACK), (380, 200))
						screen.blit(gameFont.render(str(chr(p2Key)).upper(), True, BLUE), (1395, 200))
						screen.blit(gameFont.render(str(p2Counter), True, BLACK), (1520, 200))
						screen.blit(winConditionFont.render(winCondition, True, BLACK), (802, 152))
						screen.blit(winConditionFont.render(winCondition, True, WHITE), (800, 150))

						#checks to see if win condition is true
						if p1Counter == WIN_NUMBER:
							gameState = "ROUND_OVER"
						if p2Counter == WIN_NUMBER:
							gameState = "ROUND_OVER"

						# Listen for events.
						for event in pg.event.get():
							# Quit python
							if event.type == pg.QUIT:
								quit()
							# Listen for key events.
							elif event.type == pg.KEYDOWN:
								# Quit with escape key.
								if event.key == pg.K_ESCAPE:
									quit()			
								# Handle players hitting the right keys.		
								elif event.key == p1Key: # p1 hits the right key.
									screen.fill(BLACK)
									screen.blit(backgroundScreenImage, BACKGROUND_IMG_COORD)
									screen.blit(p1SpriteAttack, (725, 420))
									screen.blit(p2SpriteDamage, (875, 420))
									hitEffect.play()
									screen.blit(redKeyBox, (450, 150))
									screen.blit(redCounterBox, (350, 180))
									screen.blit(blueKeyBox, (1330, 150))	
									screen.blit(blueCounterBox, (1490, 180))
									screen.blit(gameFont.render(str(chr(p1Key)).upper(), True, RED), (510, 200))
									screen.blit(gameFont.render(str(p1Counter), True, BLACK), (380, 200))
									screen.blit(gameFont.render(str(chr(p2Key)).upper(), True, BLUE), (1395, 200))
									screen.blit(gameFont.render(str(p2Counter), True, BLACK), (1520, 200))
									screen.blit(winConditionFont.render(winCondition, True, BLACK), (802, 152))
									screen.blit(winConditionFont.render(winCondition, True, WHITE), (800, 150))

									p1Counter += 1
									if hardMode:
										p1Key = random.choice(keys)
									else:
										p1Key = random.choice(keysLeft)
									pg.time.delay(25)

								if event.key == p2Key: # p2 hits the right key.
									screen.fill(BLACK)
									screen.blit(backgroundScreenImage, BACKGROUND_IMG_COORD)
									screen.blit(p2SpriteAttack, (875, 420))
									screen.blit(p1SpriteDamage, (725, 420))
									hitEffect.play()
									screen.blit(redKeyBox, (450, 150))
									screen.blit(redCounterBox, (350, 180))
									screen.blit(blueKeyBox, (1330, 150))	
									screen.blit(blueCounterBox, (1490, 180))
									screen.blit(gameFont.render(str(chr(p1Key)).upper(), True, RED), (510, 250))
									screen.blit(gameFont.render(str(chr(p1Key)).upper(), True, RED), (510, 200))
									screen.blit(gameFont.render(str(p1Counter), True, BLACK), (380, 200))
									screen.blit(gameFont.render(str(chr(p2Key)).upper(), True, BLUE), (1395, 200))
									screen.blit(gameFont.render(str(p2Counter), True, BLACK), (1520, 200))
									screen.blit(winConditionFont.render(winCondition, True, BLACK), (817, 152))
									screen.blit(winConditionFont.render(winCondition, True, WHITE), (815, 150))

									p2Counter += 1
									if hardMode:
										p2Key = random.choice(keys)
									else:
										p2Key = random.choice(keysRight)
									pg.time.delay(25)

						# Update display.
						pg.display.flip()

					# Handle the game ending.
					elif gameState == "ROUND_OVER":
						screen.blit(countdownFont.render("VICTORY!", True, BLACK), (787, 242))
						screen.blit(countdownFont.render("VICTORY!", True, WHITE), (785, 240))
						pg.mixer.music.fadeout(2000)
						pg.mixer.music.set_volume(0.8)
						pg.display.flip()
						if p1Counter == WIN_NUMBER and p2Counter < WIN_NUMBER:
							gameState = "VICTORY_RED"
						elif p1Counter < WIN_NUMBER and p2Counter == WIN_NUMBER:
							gameState = "VICTORY_BLUE"
						elif p1Counter == WIN_NUMBER and p2Counter == WIN_NUMBER:
							gameState = "VICTORY_TIE"
						#Handle quitting Python
						for event in pg.event.get():
							# Quit python
							if event.type == pg.QUIT:
								quit()
							# Listen for key events.
							elif event.type == pg.KEYDOWN:
								# Quit with escape key.
								if event.key == pg.K_ESCAPE:
									quit()	

					# Render RED Victory to the screen.
					elif gameState == "VICTORY_RED":
						pg.time.delay(25)
						screen.blit(victoryImageRed, BACKGROUND_IMG_COORD)
						screen.blit(redWins, RED_END)
						screen.blit(blueLoses, BLUE_END)
						
						if gameOverMusic == False:
							pg.mixer.music.load('sound/victorySFX.wav')
							redWinsVoice.play()
							pg.mixer.music.play()
							gameOverMusic = True
						pg.display.flip()

						# Handle events. 
						for event in pg.event.get():
							# Quit python
							if event.type == pg.QUIT:
								quit()
							# Listen for key events.
							elif event.type == pg.KEYDOWN:
								# Quit with escape key.
								if event.key == pg.K_ESCAPE:
									quit()	
								# Start a new game.
								if event.key == pg.K_SPACE:
									p1Counter = 0
									p2Counter = 0
									gameOverMusic == False
									gameState = 'COUNTDOWN'

					# Render BLUE Victory to the screen.	
					elif gameState == "VICTORY_BLUE":
						pg.time.delay(25)
						screen.blit(victoryImageBlue, BACKGROUND_IMG_COORD)
						screen.blit(blueWins, BLUE_END)
						screen.blit(redLoses, RED_END)
						
						if gameOverMusic == False:
							pg.mixer.music.load('sound/victorySFX.wav')
							blueWinsVoice.play()
							pg.mixer.music.play()
							gameOverMusic = True
						pg.display.flip()

						# Handle events. 
						for event in pg.event.get():
							# Quit python
							if event.type == pg.QUIT:
								quit()
							# Listen for key events.
							elif event.type == pg.KEYDOWN:
								# Quit with escape key.
								if event.key == pg.K_ESCAPE:
									quit()	
								# Start a new game.
								if event.key == pg.K_SPACE:
									p1Counter = 0
									p2Counter = 0
									gameOverMusic == False
									gameState = 'COUNTDOWN'	

					# Handle the rare chance of a tie happening.
					elif gameState == "VICTORY_TIE":
						pg.time.delay(25)
						screen.fill(BLACK)
						noContestVoice.play()
						pg.display.flip()
						#Handle quitting Python
						for event in pg.event.get():
							# Quit python
							if event.type == pg.QUIT:
								quit()
							# Listen for key events.
							elif event.type == pg.KEYDOWN:
								# Quit with escape key.
								if event.key == pg.K_ESCAPE:
									quit()	
								# Start a new game.
								if event.key == pg.K_SPACE:
									p1Counter = 0
									p2Counter = 0
									gameOverMusic == False
									gameState = 'COUNTDOWN'	

	# Update display.
	pg.display.flip()