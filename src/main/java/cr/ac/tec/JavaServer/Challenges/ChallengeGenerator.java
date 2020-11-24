package cr.ac.tec.JavaServer.Challenges;
import cr.ac.tec.JavaServer.Challenges.Trees.BinarySearchTree;
import cr.ac.tec.JavaServer.Challenges.Trees.SinglyLinkedList;
import cr.ac.tec.JavaServer.TokensPrototype.*;

import java.util.Random;

public class ChallengeGenerator {
    private String[] challengeList = {"BST", "AVL", "SPLAY", "BTREE"};
    private String challenge;
    private CloneFactory cloneFactory = new CloneFactory();
    private Diamond bstToken = new Diamond();
    private SinglyLinkedList<Diamond> bstTokensList = new SinglyLinkedList<>();
    private Circle avlToken = new Circle();
    private SinglyLinkedList<Diamond> avlTokensList = new SinglyLinkedList<>();
    private Rectangle bToken = new Rectangle();
    private SinglyLinkedList<Diamond> bTokensList = new SinglyLinkedList<>();
    private Triangle splayToken = new Triangle();
    private SinglyLinkedList<Diamond> splayTokensList = new SinglyLinkedList<>();
    private Random r =  new Random();
    private BinarySearchTree myBST = new BinarySearchTree();

    //Metodo para generar los tokens
    public void challengeSelector() {
        int randomTree = r.nextInt(challengeList.length-1);
        if (true){
            this.challenge = challengeList[0];
            if (this.challenge == "BST"){
                this.myBST = myBST.createBST();
                int listLength = this.myBST.getKeysList().getLength();
                mainTokens(this.challenge, listLength, this.myBST.getKeysList());
                System.out.println("El valor del token en 0 es : " + this.bstTokensList.getElementAt(0).getValue());
            }

        }
    }
    //Metodo para generar lista de tokens principales pertenecientes al reto 
    public void mainTokens(String tokenType, int length, SinglyLinkedList<Integer> valuesList){
        CloneFactory tokenMaker = new CloneFactory();
        int index = 0;
        if (tokenType == "BST" ){
            while(length>0){
                Diamond clonedDiamond = (Diamond)tokenMaker.getToken(bstToken);
                clonedDiamond.setValue(valuesList.getElementAt(index));
                this.bstTokensList.add(clonedDiamond);
                length --;
                index ++;
            }
        }

        
    }

    //Método para parsear esos tokens a JSON

    //Método para pasear JSON a String
    public static void main(String[] args) {
        ChallengeGenerator myChGenerator = new ChallengeGenerator();
        myChGenerator.challengeSelector();
    }
    
}
