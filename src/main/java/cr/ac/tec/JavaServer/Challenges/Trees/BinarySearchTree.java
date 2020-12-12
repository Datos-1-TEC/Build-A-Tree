package cr.ac.tec.JavaServer.Challenges.Trees;

import java.util.Random;

public class BinarySearchTree {
    private NodeT root;
    private int maxDepth = 0;
    private SinglyLinkedList<Integer> keysList = new SinglyLinkedList<>();
    private String shape = "Diamond";
    
    public boolean isEmpty() {
        return this.root == null;
    } 
    public BinarySearchTree() {
        this.root = null;
    }
    public void insert(int key){
        root = insertAux(root, key);
    }

    private NodeT insertAux(NodeT root, int item) {
        //If tree or subtree is empty
        if (root == null){
            return new NodeT(item);
        }
        //Else, recur down the tre
        if (item < root.key){
            root.left = insertAux(root.left, item);
        } else if (item > root.key){
            root.right = insertAux(root.right, item);
        }
        return root;
    }

    public void inOrder(){
        this.inOrderAux(root);

    }
    private void inOrderAux(NodeT root){
        if (root != null){
            inOrderAux(root.left);
            
            inOrderAux(root.right);
        }

    }
    public NodeT getRoot() {
        return root;
    }

    public int getMaxDepth(){
        return getMaxDepth(this.root)-1;
    }

    private int getMaxDepth(NodeT node) {
        if (node == null) return 0; 

        else { 
        /* compute the depth of each subtree */
            int lDepth = getMaxDepth(node.left); 
            int rDepth = getMaxDepth(node.right); 

            /* use the larger one */
            if (lDepth > rDepth) {
                this.maxDepth = lDepth;
                return this.maxDepth + 1;
            } 
            else {
                this.maxDepth = rDepth;
                return this.maxDepth + 1; 
            }
    }
} 

    private SinglyLinkedList<Integer> bstKeys(NodeT root) {
        traverseTree(root);
        return keysList;
    }

    private void traverseTree(NodeT nodeT) {
        if (nodeT != null) {
            traverseTree(nodeT.left);
            keysList.add(nodeT.key);
            traverseTree(nodeT.right);
        }
    }
    
    public SinglyLinkedList<Integer> getKeysList() {
        return keysList;
    }
    public int getRandomNumber(int min, int max) {
        Random random = new Random();
        return random.nextInt(max - min) + min;
    }

    public BinarySearchTree createBST(){
        BinarySearchTree bst = new BinarySearchTree();

        int depth = getRandomNumber(2, 4);
        int newKey;
        int position = 0;
        
        while(bst.getMaxDepth() < depth){
            newKey = getRandomNumber(10, 99);
            
            if ( bst.isEmpty()){ //agrega el primer key
                bst.insert(newKey);

                position ++;
            } 
            else if( bstKeys(bst.getRoot()).getElementAt(position-1) != newKey ){ //agrega y verifica que newKey no sea igual al anterior
                bst.insert(newKey);             
                position ++;
            } else{
                position --;
            } 

        }
        bst.bstKeys(bst.getRoot());
        System.out.println("La profundidad del arbol es: " + depth);
        bst.getKeysList().print();
        System.out.println("La raiz del arbol es: " + bst.getRoot().key);
        return bst;
    }

    public String getShape() {
        return shape;
    }

}
