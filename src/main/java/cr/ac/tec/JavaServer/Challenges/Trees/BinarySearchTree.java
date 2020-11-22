package cr.ac.tec.JavaServer.Challenges.Trees;

public class BinarySearchTree {
    private NodeT root;
    private int maxDepth = 0;
    private SinglyLinkedList<Integer> keysList = new SinglyLinkedList<>();

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
            System.out.println(root.key);
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

    public static void main(String[] args){

    }

    public BinarySearchTree createBST(){
        BinarySearchTree bst = new BinarySearchTree();
        /*
        Let us create the tree below
                50
              /      \
              30    70
            /   \  /     \
            20  40 60    80

         */
        bst.insert(50);
        bst.insert(30);
        bst.insert(20);
        bst.insert(40);
        bst.insert(60);
        bst.insert(70);
        bst.insert(80);        
        bst.inOrder();
        bst.bstKeys(bst.getRoot());
        //System.out.println(bst);
        //System.out.println(bst.getRoot().key);
        //System.out.println("La profudidad del BST es: "+ bst.getMaxDepth());
        return bst;
    }

}
