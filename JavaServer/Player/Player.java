package JavaServer.Player;

import JavaServer.TokensPrototype.Token;

public class Player {
    private int ID;
    private int lives = 3;
    //Agregar atributo Reto actual
    private Token currentToken;
    private int score;
    private int time; 
    public Player(int iD, int lives, Token currentToken, int score, int time) {
            ID = iD;
            this.lives = lives;
            this.currentToken = currentToken;
            this.score = score;
            this.time = time;
        }
        
    public int getID() {
        return ID;
    }

    public void setID(int iD) {
        ID = iD;
    }

    public int getLives() {
        return lives;
    }

    public void setLives(int lives) {
        this.lives = lives;
    }

    public Token getCurrentToken() {
        return currentToken;
    }

    public void setCurrentToken(Token currentToken) {
        this.currentToken = currentToken;
    }

    public int getScore() {
        return score;
    }

    public void setScore(int score) {
        this.score = score;
    }

    public int getTime() {
        return time;
    }

    public void setTime(int time) {
        this.time = time;
    }

    
    

}
