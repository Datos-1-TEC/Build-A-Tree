package cr.ac.tec.JavaServer.Challenges;

import cr.ac.tec.JavaServer.Challenges.Trees.AVLTree;
import cr.ac.tec.JavaServer.Challenges.Trees.BTree;
import cr.ac.tec.JavaServer.Challenges.Trees.BinarySearchTree;
import cr.ac.tec.JavaServer.Challenges.Trees.NodeL;
import cr.ac.tec.JavaServer.Challenges.Trees.SinglyLinkedList;
import cr.ac.tec.JavaServer.Challenges.Trees.SplayTree;
import cr.ac.tec.JavaServer.TokensPrototype.*;

import java.util.Random;

/**
 * Esta clase se encarga de generar el reto que se escoja de la lista de
 * árboles, es decir, crea un árbol con cierta cantidad de tokens clasificados
 * en Main Tokens, que pertenecen a los tokens del árbol y Filler Tokens
 * 
 * @author Juan Peña
 * 
 */
public class ChallengeGenerator {
    private String[] challengeList = { "BST", "AVL", "SPLAY", "BTREE" };
    private SinglyLinkedList<String> challengeList2 = new SinglyLinkedList<>();
    private String challenge;
    private String challengeShape;
    private Diamond bstToken = new Diamond();
    private SinglyLinkedList<Token> bstTokensList = new SinglyLinkedList<>();
    private Circle avlToken = new Circle();
    private SinglyLinkedList<Token> avlTokensList = new SinglyLinkedList<>();
    private Rectangle bToken = new Rectangle();
    private SinglyLinkedList<Token> bTokensList = new SinglyLinkedList<>();
    private Triangle splayToken = new Triangle();
    private int order = 0;
    private SinglyLinkedList<Token> splayTokensList = new SinglyLinkedList<>();
    private BinarySearchTree myBST = new BinarySearchTree();
    private AVLTree myAVL = new AVLTree();
    private BTree myBTree = new BTree();
    private SplayTree mySplay = new SplayTree();

    // Metodo para generar los tokens
    /**
     * Este método crea el árbol respectivo, y crea los tokens para ese árbol luego
     * crea 5 tokens de relleno por cada tipo de token restante
     */
    public void challengeSelector() {

        this.challengeList2.add("BST");
        this.challengeList2.add("AVL");
        this.challengeList2.add("SPLAY");
        this.challengeList2.add("BTREE");
        Random r = new Random();
        int randomTree = r.nextInt(4);

        this.challenge = challengeList[randomTree];
        if (this.challenge == "BST") {
            setChallengeShape("Diamond");
            myBST = myBST.createBST();
            int listLength = myBST.getKeysList().getLength();
            mainTokens(this.challenge, listLength, myBST.getKeysList());
            fillingTokens(5, "BST");
            System.out.println("Tree depth: " + myBST.getMaxDepth());
            System.out.println(this.challenge);

        } else if (this.challenge == "AVL") {
            setChallengeShape("Circle");
            
            myAVL.createAVL();
            System.out.println("Cantidad de elementos: " + myAVL.getList().getLength());
            int listLength = myAVL.getList().getLength();
            mainTokens(this.challenge, listLength, myAVL.getList());
            fillingTokens(5, this.challenge);
            System.out.println(this.challenge);

        } else if (this.challenge == "BTREE") {
            setChallengeShape("Rectangle");
            
            myBTree.createB();
            setOrder(myBTree.getOrder()/2);
            int listLength = myBTree.getList().getLength();
            mainTokens(this.challenge, listLength, myBTree.getList());
            fillingTokens(5, this.challenge);
            System.out.println("Orden: " + myBTree.getOrder());
            System.out.println("Niveles: " + myBTree.getLevel());
            System.out.println(this.challenge);

        } else if (this.challenge == "SPLAY") {
            setChallengeShape("Triangle");
            
            mySplay.createSplay();
            int listLength = mySplay.getList().getLength();
            mainTokens(this.challenge, listLength, mySplay.getList());
            fillingTokens(5, this.challenge);
            System.out.println("Cantidad de elementos: " + mySplay.getList().getLength());
            System.out.println(this.challenge);

        }

    }

    /**
     * Metodo para generar lista de tokens principales pertenecientes al reto,
     * 
     * @param tokenType  String que indica cuál es el tipo de token a generar
     * @param length     Longitud de la lista de keys en el árbol
     * @param valuesList Lista de keys en el árbol
     */

    public void mainTokens(String tokenType, int length, SinglyLinkedList<Integer> valuesList) {
        CloneFactory tokenMaker = new CloneFactory();
        int index = 0;
        if (tokenType == "BST") {
            while (length > 0) {
                Diamond clonedDiamond = (Diamond) tokenMaker.getToken(bstToken);
                clonedDiamond.setValue(valuesList.getElementAt(index));
                this.bstTokensList.add(clonedDiamond);
                length--;
                index++;
            }
        }

        else if (tokenType == "AVL") {
            while (length > 0) {
                Circle clonedCircle = (Circle) tokenMaker.getToken(avlToken);
                clonedCircle.setValue(valuesList.getElementAt(index));
                this.avlTokensList.add(clonedCircle);
                length--;
                index++;
            }
        }

        else if (tokenType == "BTREE") {
            while (length > 0) {
                Rectangle clonedRectangle = (Rectangle) tokenMaker.getToken(bToken);
                clonedRectangle.setValue(valuesList.getElementAt(index));
                this.bTokensList.add(clonedRectangle);
                length--;
                index++;
            }
        }

        else if (tokenType == "SPLAY") {
            while (length > 0) {
                Triangle clonedTriangle = (Triangle) tokenMaker.getToken(splayToken);
                clonedTriangle.setValue(valuesList.getElementAt(index));
                this.splayTokensList.add(clonedTriangle);
                length--;
                index++;
            }
        }
    }

    /**
     * Este método se encarga se agregar los keys a la lista de tokens que son de
     * relleno
     * 
     * @param elements         cantidad de tokens que se van a generar
     * @param currentChallenge es el String del reto actual que se usa para indicar
     *                         que no se crearan tokens de ese tipo
     */
    public void fillingTokens(int elements, String currentChallenge) {
        CloneFactory tokenMaker = new CloneFactory();
        int copies = elements;
        SinglyLinkedList<String> myFillers = searchChallenge(currentChallenge, 0);
        int cont = 0;
        while (cont < 3) {

            if (myFillers.getElementAt(cont).equals("BST")) {
                while (copies > 0) {
                    Diamond clonedDiamond = (Diamond) tokenMaker.getToken(bstToken);
                    clonedDiamond.setValue(getRandomNumber(10, 100));
                    this.bstTokensList.add(clonedDiamond);
                    copies--;
                }
                copies = elements;

            } else if (myFillers.getElementAt(cont).equals("AVL")) {
                while (copies > 0) {
                    Circle clonedCircle = (Circle) tokenMaker.getToken(avlToken);
                    clonedCircle.setValue(getRandomNumber(10, 100));
                    this.avlTokensList.add(clonedCircle);
                    copies--;
                }
                copies = elements;

            } else if (myFillers.getElementAt(cont).equals("BTREE")) {
                while (copies > 0) {
                    Rectangle clonedRectangle = (Rectangle) tokenMaker.getToken(bToken);
                    clonedRectangle.setValue(getRandomNumber(10, 100));
                    this.bTokensList.add(clonedRectangle);
                    copies--;
                }
                copies = elements;

            } else if (myFillers.getElementAt(cont).equals("SPLAY")) {
                while (copies > 0) {
                    Triangle clonedTriangle = (Triangle) tokenMaker.getToken(splayToken);
                    clonedTriangle.setValue(getRandomNumber(10, 100));
                    this.splayTokensList.add(clonedTriangle);
                    copies--;
                }
                copies = elements;
            }
            cont++;
        }
    }

    /**
     * Método para sacar el reto actual de la lista que se utilizará para recorrer
     * los tipos de tokens a crear de relleno
     * 
     * @param currentChallenge reto actual
     * @param index            indice de la lista
     * @return challenges lista enlazada de retos para generar tokens de relleno
     */
    public SinglyLinkedList<String> searchChallenge(String currentChallenge, int index) {

        SinglyLinkedList<String> challenges = new SinglyLinkedList<>();
        int i = 0;

        while (i < 4) {
            if (this.challengeList[i] != currentChallenge){
                challenges.add(this.challengeList[i]);
                i ++;
            }
            else i ++;
        }

        return challenges;
    }

    /**
     * Método para obtener un número entero random
     * 
     * @param min mínimo del rango
     * @param max maximo del rango
     * @return numero entero generado
     */
    public int getRandomNumber(int min, int max) {
        Random random = new Random();
        return random.nextInt(max - min) + min;
    }
    // Método para parsear esos tokens a JSON

    // Método para pasear JSON a String

    public static void main(String[] args) {
        ChallengeGenerator myChGenerator = new ChallengeGenerator();
        myChGenerator.challengeSelector();
        
        System.out.println("tokens en lista: " + myChGenerator.getAvlTokensList().getLength());
        System.out.println("tokens en lista: " + myChGenerator.getBstTokensList().getLength());
        System.out.println("tokens en lista: " + myChGenerator.getbTokensList().getLength());
        System.out.println("tokens en lista: " + myChGenerator.getSplayTokensList().getLength());

    }

    public SinglyLinkedList<Token> getBstTokensList() {
        return bstTokensList;
    }

    public void setBstTokensList(SinglyLinkedList<Token> bstTokensList) {
        this.bstTokensList = bstTokensList;
    }

    public SinglyLinkedList<Token> getAvlTokensList() {
        return avlTokensList;
    }

    public void setAvlTokensList(SinglyLinkedList<Token> avlTokensList) {
        this.avlTokensList = avlTokensList;
    }

    public SinglyLinkedList<Token> getbTokensList() {
        return bTokensList;
    }

    public void setbTokensList(SinglyLinkedList<Token> bTokensList) {
        this.bTokensList = bTokensList;
    }

    public SinglyLinkedList<Token> getSplayTokensList() {
        return splayTokensList;
    }

    public void setSplayTokensList(SinglyLinkedList<Token> splayTokensList) {
        this.splayTokensList = splayTokensList;
    }

    public String getChallenge() {
        return challenge;
    }

    public BinarySearchTree getMyBST() {
        return myBST;
    }

    public String getChallengeShape() {
        return challengeShape;
    }

    public void setChallengeShape(String challengeShape) {
        this.challengeShape = challengeShape;
    }

    public int getOrder() {
        return order;
    }

    public void setOrder(int order) {
        this.order = order;
    }

    public AVLTree getMyAVL() {
        return myAVL;
    }

    public BTree getMyBTree() {
        return myBTree;
    }
    
    public SplayTree getMySplay() {
        return mySplay;
    }


}
