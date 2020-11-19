class mainGameScreen:
    def __init__(self, game_display):
        self.frame = game_display
        self.flag = True
        self.score = 0
        self.lives = 3
        self.win = 0
        self.load_data()

    def load_data(self):
        with open ("Highscore.txt", "w") as g:
            try:
                self.highscore = init(g.read())
            except:
                self.highscore = 0

    def respawn(self):
        self.player = Player(100, 460)
    
    """
    def __update__(self):
        # Gravedad en plataformas
        self.player.falling = True
        for platform in self.platforms:
            if self.player.rect.colliderect(platform.rect):
                self.player.falling = False
                break
            elif self.player.rect.colliderect(platform.rect):
                self.respawn()
                self.lives -= 1
        self.player.__update__()

        if self.score > self.highscore:
            self.highscore = self.score
            with open("HighScore.txt", "w") as g:
                g.write(str(self.score))
            with open("SalonFama.txt", "a") as f:
                f.write("Mario: " + str(self.score) + "\n")

    def __draw__(self):
        backGroundImage = pygame.image.load("images/")

    """"

    def events(self, event):
        keys = pygame.key.get_pressed()

        if keys[pygame.K_LEFT]:
            x -= vel

        if keys[pygame.K_RIGHT]:
            x += vel

        if keys[pygame.K_UP]:
            y -= vel

        if keys[pygame.K_DOWN]:
            y += vel





        
        

        
        

