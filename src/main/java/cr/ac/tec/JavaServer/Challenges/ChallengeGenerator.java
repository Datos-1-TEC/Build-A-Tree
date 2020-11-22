package cr.ac.tec.JavaServer.Challenges;
import cr.ac.tec.JavaServer.TokensPrototype.*;

import java.util.Random;

public class ChallengeGenerator {
    private String[] challengeList = {"BST", "AVL", "SPLAY", "BTREE"};
    private String challenge;
    private CloneFactory cloneFactory = new CloneFactory();
    private Diamond bstToken = new Diamond();
    private Circle avlToken = new Circle();
    private Rectangle bToken = new Rectangle();
    private Triangle splayToken = new Triangle();
    private Random r =  new Random();

    //Metodo para generar los tokens
    public void challengeSelector() {
        int randomTree = r.nextInt(challengeList.length-1);
        if (randomTree == 0){
            this.challenge = challengeList[randomTree];
            if (this.challenge == "BST"){
                
            }

        }
    }

    //Método para parsear esos tokens a JSON

    //Método para pasear JSON a String

    
}
