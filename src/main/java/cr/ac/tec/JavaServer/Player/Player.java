package cr.ac.tec.JavaServer.Player;

import cr.ac.tec.JavaServer.Challenges.Trees.AVLTree;
import cr.ac.tec.JavaServer.Challenges.Trees.BTree;
import cr.ac.tec.JavaServer.Challenges.Trees.BinarySearchTree;
import cr.ac.tec.JavaServer.Challenges.Trees.SplayTree;


public class Player {
    private int ID;
    private int lives = 3;
    //Agregar atributo Reto actual
    private BinarySearchTree myBST;
    private AVLTree myAVL;
    private SplayTree mySplay;
    private BTree myBTree; 
    private int score;
    public Player(int ID, int lives, int score) {
            this.ID = ID;
            this.lives = lives;
            this.score = score;
            
        }
    public Player(int iD,int lives){
        this.ID = iD;
        this.lives = lives;
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

    public int getScore() {
        return score;
    }

    public void setScore(int score) {
        this.score = score;
    }

    public BinarySearchTree getMyBST() {
        return myBST;
    }

    public void setMyBST(BinarySearchTree myBST) {
        this.myBST = myBST;
    }

    public AVLTree getMyAVL() {
        return myAVL;
    }

    public void setMyAVL(AVLTree myAVL) {
        this.myAVL = myAVL;
    }

    public SplayTree getMySplay() {
        return mySplay;
    }

    public void setMySplay(SplayTree mySplay) {
        this.mySplay = mySplay;
    }

    public BTree getMyBTree() {
        return myBTree;
    }

    public void setMyBTree(BTree myBTree) {
        this.myBTree = myBTree;
    }
    

}
