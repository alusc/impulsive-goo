import pygame
import random


# ============================== OBJETS ==============================

from gl0bals import *
from screen import *
from block import *
from entity import *
from player import *
from enemy1 import *
from enemy2 import *
from enemy3 import *
from weapon import *
from projectile import *
from mist import *
from level0 import *
from level1 import *

# ==================================================================================================================================

def game_initialize():

	global screen, level, TAB, player, weapon, FONT, clock, over, wave

	# ============================== INITIALISATION ==============================

	pygame.init()


	# ========== FENETRE

	screen = Screen()


	# ========== NIVEAU

	# séléction du niveau
	if Globals.level == 0:
		level = Level0()
	elif Globals.level == 1:	
		level = Level1()
	elif Globals.level == 2: # /!\ n'existe pas
		level = Level2() # /!\ n'existe pas

	TAB = level.TAB # tableau de 1 et 0 du niveau
	player = level.player # initialisation du joueur
	weapon = level.weapon # initialisation de l'arme

	# créer tout les blocs de l'environnement
	for i in range(0,len(TAB)):
		for j in range(0,len(TAB[0])):
			if TAB[i][j]==1:
				# est ajouté à la liste de tout les blocs
				Globals.blocks.append( Block( (j * Globals.RATIO , i * Globals.RATIO) ) )


	# ========== TEXTE

	pygame.font.init()
	FONT = pygame.font.Font("./ressources/FFFFORWA.TTF", 15)


	# ========== HORLOGE

	Globals.counter = 0
	clock = pygame.time.Clock()


	# ========== JEU

	over = False
	wave = 0



# ==================================================================================================================================

def game_body():

	global screen, level, TAB, player, weapon, FONT, clock, over, wave


	# ======================================== EVENTS

	for event in pygame.event.get():
		if event.type == pygame.QUIT:
			Globals.launched = False

	if over:
		Globals.ecran = "select"
	

	keys = pygame.key.get_pressed()

	# ======================================== FENETRE

	# quitter
	if keys[pygame.K_ESCAPE]:
		Globals.launched = False

	# plein écran
	if keys[pygame.K_F11] and screen.fullscreen==False:
		screen.surface = pygame.display.set_mode(screen.resolution, pygame.FULLSCREEN)
		pygame.mouse.set_visible(False)
		screen.fullscreen = True
	elif keys[pygame.K_F11] and screen.fullscreen==True:
		screen.surface = pygame.display.set_mode(screen.resolution)
		pygame.mouse.set_visible(True)
		screen.fullscreen = False


	# ======================================== VAGUES

	for i in range(0, len(level.waves)):
		# début de la transition
		if wave == i and Globals.enemies == []:
			Globals.transition -= 1
			weapon = None
			player.weaponized = False
			# brouillard indicateur des positions ennemies
			if Globals.transition == Globals.TRANSITION -1:
				level.pre_waves[i](level)
			# initialisation de la prochaine vague
			if Globals.transition == 0:
				wave = i+1
				level.waves[i](level)
				player = level.player
				weapon = level.weapon
				Globals.mists = []
				Globals.transition = Globals.TRANSITION


	# ======================================== ENNEMIES (GLOBAL)

	for enemy in Globals.enemies:

		# joueur touché
		if player.rect.colliderect(enemy.rect) and not player.hurted:
			player.heart -= 1
			player.hurted = True
			player.invincible_counter = player.INVINCIBLE
			# game over
			if player.heart == 0:
				over = True
				player.heart = player.HEART

		# out of bounds
		if enemy.killed or enemy.rect.top > screen.resolution[1]:

			del Globals.enemies[Globals.enemies.index(enemy)]

			if enemy in Globals.enemies1:
				del Globals.enemies1[Globals.enemies1.index(enemy)]

			elif enemy in Globals.enemies2:
				del Globals.enemies2[Globals.enemies2.index(enemy)]

			elif enemy in Globals.enemies3:
				del Globals.enemies3[Globals.enemies3.index(enemy)]


	# ====================================== ENNEMIES 1

	for enemy in Globals.enemies1:

		# déplacement gauche
		if enemy.rect.x > player.rect.x:
			enemy.move(-random.uniform(0.05, 0.1), 0) # vitesse aléatoire

		# déplacement droit
		if enemy.rect.x < player.rect.x:
			enemy.move(random.uniform(0.05, 0.1), 0) # vitesse aléatoire

		# saut
		if enemy.onground and not enemy.isjump:
			enemy.isjump = True
			enemy.vy_index = len(enemy.vy)//random.randint(3,6) # rang de vélocité d'impulsion initiale
		if enemy.isjump:
			enemy.jump()

		# gravité
		if not enemy.isjump:
			enemy.gravity()


	# ======================================== ENNEMIES 2

	for enemy in Globals.enemies2:

		# déplacement gauche
		if Globals.counter%480 <= 120:
			enemy.last_move = "left"
			enemy.move(-enemy.v_fixed, 0)

		# déplacement droit
		if 240 < Globals.counter%480 <= 360 :
			enemy.last_move = "right"
			enemy.move(enemy.v_fixed, 0)

		# gravité
		if not enemy.isjump:
			enemy.gravity()

		# tir
		if Globals.counter%180 == 0 and not enemy.killed:
			Projectile(enemy.rect.x, enemy.rect.y, player.rect.x + player.width/2, player.rect.y + player.height/2)


	# ====================================== ENNEMIES 3

	for enemy in Globals.enemies3:

		if not enemy.killed:
			# tir horizontal
			if Globals.counter%40 == 0 and player.rect.top >= enemy.rect.top and player.rect.bottom <= enemy.rect.bottom:
				# tir à gauche
				if (player.rect.right <= enemy.rect.left):
					Projectile(enemy.rect.x + enemy.width/2, enemy.rect.y + enemy.width/2, enemy.rect.x, enemy.rect.y + enemy.width/2)
				# tir à droite
				elif (player.rect.left >= enemy.rect.right):
					Projectile(enemy.rect.x + enemy.width/2, enemy.rect.y + enemy.width/2, enemy.rect.x + enemy.width, enemy.rect.y + enemy.width/2)
			# tir polydirectionnel
			elif Globals.counter%180 == 0:
				Projectile(enemy.rect.x + enemy.width/2, enemy.rect.y + enemy.width/2, enemy.rect.x, enemy.rect.y)
				Projectile(enemy.rect.x + enemy.width/2, enemy.rect.y + enemy.width/2, enemy.rect.x + enemy.width/2, enemy.rect.y)
				Projectile(enemy.rect.x + enemy.width/2, enemy.rect.y + enemy.width/2, enemy.rect.x + enemy.width, enemy.rect.y)
				Projectile(enemy.rect.x + enemy.width/2, enemy.rect.y + enemy.width/2, enemy.rect.x + enemy.width, enemy.rect.y + enemy.width/2)
				Projectile(enemy.rect.x + enemy.width/2, enemy.rect.y + enemy.width/2, enemy.rect.x + enemy.width, enemy.rect.y + enemy.width)
				Projectile(enemy.rect.x + enemy.width/2, enemy.rect.y + enemy.width/2, enemy.rect.x + enemy.width /2, enemy.rect.y + enemy.width)
				Projectile(enemy.rect.x + enemy.width/2, enemy.rect.y + enemy.width/2, enemy.rect.x, enemy.rect.y + enemy.width)
				Projectile(enemy.rect.x + enemy.width/2, enemy.rect.y + enemy.width/2, enemy.rect.x, enemy.rect.y + enemy.width/2)


	# ======================================== PROJECTILES

	for projectile in Globals.projectiles:
		# déplacement
		projectile.move_single_axis()
		# out of bounds
		if projectile.rect.left > screen.resolution[0] or projectile.rect.right < 0 or projectile.rect.bottom < 0 or projectile.rect.top > screen.resolution[1]:
			del Globals.projectiles[Globals.projectiles.index(projectile)]


	# ======================================== JOUEUR

	# out of bounds
	if player.rect.y > screen.resolution[1]:
		Globals.launched = False

	# déplacement gauche
	if keys[pygame.K_LEFT]:
		if not(keys[pygame.K_RIGHT]):
			player.last_move = "left"
		player.move(-player.v_fixed, 0)

	# déplacement droit
	if keys[pygame.K_RIGHT]:
		if not(keys[pygame.K_LEFT]):
			player.last_move = "right"
		player.move(player.v_fixed, 0)

	# saut
	if keys[pygame.K_SPACE] and player.onground and not player.isjump:
		player.isjump = True
		player.vy_index = len(player.vy)//6 # rang de vélocité d'impulsion initiale
	if player.isjump:
		player.jump()

	# gravité
	if not player.isjump:
		player.gravity()

	# frappe
	if player.weaponized and keys[pygame.K_x] and player.cooldown_counter == 0:
		player.hit()
		player.cooldown_counter = player.COOLDOWN + 1
	if player.cooldown_counter > 0:
		player.cooldown_counter -= 1

	# touché
	if player.hurted and player.invincible_counter > 0:
		player.invincible_counter -= 1
	elif player.hurted and player.invincible_counter == 0:
		player.hurted = False

	# ======================================== ARME

	if weapon != None and player.rect.colliderect(weapon.rect):
		player.weaponized = True

	# changement d'apparence du joueur
	if player.weaponized:
		player.sprites_right = [ pygame.image.load("./ressources/goodoo_gold/1.png"),
								pygame.image.load("./ressources/goodoo_gold/2.png") ]
		player.sprites_left = [ pygame.image.load("./ressources/goodoo_gold/3.png"),
								pygame.image.load("./ressources/goodoo_gold/4.png") ]
	else:
		player.sprites_right = [ pygame.image.load("./ressources/goodoo_white/1.png"),
								pygame.image.load("./ressources/goodoo_white/2.png") ]
		player.sprites_left = [ pygame.image.load("./ressources/goodoo_white/3.png"),
								pygame.image.load("./ressources/goodoo_white/4.png") ]


	# ======================================== GAME OVER

	# défaite d'un niveau
	if player.heart <= 0:
		over = True
		# écran de game over




# ==================================================================================================================================

def game_display():

	global screen, level, TAB, player, weapon, FONT, clock, over, wave

	# ======================================== DESSIN DES SURFACES

	# fond
	#screen.surface.fill(Globals.BLACK)
	screen.surface.blit(screen.sprite, (0,0)) # /!\ Chute de fps


	# blocs
	for block in Globals.blocks:
		pygame.draw.rect(screen.surface, Globals.WHITE, block.rect) # hitbox
		#screen.surface.blit(block.sprite, (block.rect.x, block.rect.y) )


	# ennemis
	for enemy in Globals.enemies3:
		if not enemy.killed :
			enemy.animation(enemy.last_move)
			#pygame.draw.rect(screen.surface, Globals.RED, enemy.rect) # hitbox
			screen.surface.blit(enemy.sprite, (enemy.rect.x, enemy.rect.y) )
	for enemy in Globals.enemies2:
		if not enemy.killed :
			enemy.animation(enemy.last_move)
			#pygame.draw.rect(screen.surface, Globals.RED, enemy.rect) # hitbox
			screen.surface.blit(enemy.sprite, (enemy.rect.x, enemy.rect.y) )
	for enemy in Globals.enemies1:
		if not enemy.killed :
			enemy.animation(enemy.last_move)
			#pygame.draw.rect(screen.surface, Globals.RED, enemy.rect) # hitbox
			screen.surface.blit(enemy.sprite, (enemy.rect.x, enemy.rect.y) )


	# arme
	if weapon != None and not player.weaponized:
		#pygame.draw.rect(screen.surface, Globals.YELLOW, weapon.rect) # hitbox
		screen.surface.blit(weapon.sprite, (weapon.rect.x, weapon.rect.y) )

	# brouillard
	for mist in Globals.mists:
		mist.animation()
		#pygame.draw.rect(screen.surface, Globals.PURPLE, mist.rect) # hitbox
		screen.surface.blit(mist.sprite, (mist.rect.x, mist.rect.y) )


	# joueur
	player.animation(player.last_move)
	#pygame.draw.rect(screen.surface, Globals.RED, player.rect) # hitbox
	if not player.hurted:
		screen.surface.blit(player.sprite, (player.rect.x, player.rect.y) )
	elif player.hurted and Globals.counter%4 == 0:
		screen.surface.blit(player.sprite, (player.rect.x, player.rect.y) )
	#pygame.draw.rect(screen.surface, Globals.PURPLE, player.blockcollide) # bloc de collision


	# frappe
	if player.cooldown_counter == player.COOLDOWN and player.last_move == "right":
		screen.surface.blit(player.hit_sprite_right, (player.rect.x, player.rect.y - Globals.RATIO) )
	elif player.cooldown_counter == player.COOLDOWN and player.last_move == "left":
		screen.surface.blit(player.hit_sprite_left, (player.rect.x - Globals.RATIO, player.rect.y - Globals.RATIO) )


	#projectiles
	for projectile in Globals.projectiles:
		projectile.animation()
		#pygame.draw.rect(screen.surface, Globals.RED, projectile.rect) # hitbox
		screen.surface.blit(projectile.sprite, (projectile.rect.x, projectile.rect.y) )

	#texte
	fps_text = FONT.render(f"FPS : { int(clock.get_fps()) }", False, Globals.RED)
	wave_text = FONT.render(f"WAVE : { wave }", False, Globals.RED)
	heart_text = FONT.render(f"HEART : { player.heart }", False, Globals.RED)
	screen.surface.blit(fps_text, (5, 5) )
	screen.surface.blit(wave_text, (5, 30) )
	screen.surface.blit(heart_text, (5, 55) )


	# actualisation de l'écran
	pygame.display.flip()


	# ========== MISE A JOUR

	Globals.counter += 1
	clock.tick(Globals.FPS)