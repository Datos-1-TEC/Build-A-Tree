package cr.ac.tec.JavaServer.Challenges.Trees;

import java.util.Random;

public class AVLTree {
    private NodeT root;
    private SinglyLinkedList<Integer> list = new SinglyLinkedList<>();
    private int points = 500;

    // A utility function to get the height of the tree
    int height(NodeT N) {
        if (N == null)
            return 0;

        return N.height;
    }

    // A utility function to get maximum of two integers
    int max(int a, int b) {
        return (a > b) ? a : b;
    }

    // A utility function to right rotate subtree rooted with y
    // See the diagram given above.
    NodeT rightRotate(NodeT y) {
        NodeT x = y.left;
        NodeT T2 = x.right;

        // Perform rotation
        x.right = y;
        y.left = T2;

        // Update heights
        y.height = max(height(y.left), height(y.right)) + 1;
        x.height = max(height(x.left), height(x.right)) + 1;

        // Return new root
        return x;
    }

    // A utility function to left rotate subtree rooted with x
    // See the diagram given above.
    NodeT leftRotate(NodeT x) {
        NodeT y = x.right;
        NodeT T2 = y.left;

        // Perform rotation
        y.left = x;
        x.right = T2;

        //  Update heights
        x.height = max(height(x.left), height(x.right)) + 1;
        y.height = max(height(y.left), height(y.right)) + 1;

        // Return new root
        return y;
    }

    // Get Balance factor of node N
    int getBalance(NodeT N) {
        if (N == null)
            return 0;

        return height(N.left) - height(N.right);
    }

    NodeT insert(NodeT node, int key) {

        /* 1.  Perform the normal BST insertion */
        if (node == null)
            return (new NodeT(key));

        if (key < node.key)
            node.left = insert(node.left, key);
        else if (key > node.key)
            node.right = insert(node.right, key);
        else // Duplicate keys not allowed
            return node;

        /* 2. Update height of this ancestor node */
        node.height = 1 + max(height(node.left),
                height(node.right));

        /* Get the balance factor of this ancestor
           node to check whether this node became
           unbalanced */
        int balance = getBalance(node);

        // If this node becomes unbalanced, then there
        // are 4 cases Left Left Case
        if (balance > 1 && key < node.left.key)
            return rightRotate(node);

        // Right Right Case
        if (balance < -1 && key > node.right.key)
            return leftRotate(node);

        // Left Right Case
        if (balance > 1 && key > node.left.key) {
            node.left = leftRotate(node.left);
            return rightRotate(node);
        }

        // Right Left Case
        if (balance < -1 && key < node.right.key) {
            node.right = rightRotate(node.right);
            return leftRotate(node);
        }

        /* return the (unchanged) node pointer */
        return node;
    }

    // A utility function to print preorder traversal
    // of the tree.
    // The function also prints height of every node
    void preOrder(NodeT node) {
        if (node != null) {
            System.out.print(node.key + " ");
            preOrder(node.left);
            preOrder(node.right);
        }
    }

    public AVLTree createAVL() {
        AVLTree tree = new AVLTree();
        
        Random rand = new Random();
        int randomNum = rand.nextInt((6 - 4) + 1) + 4;
        int k = rand.nextInt(100);
        list.add(k);
        System.out.println(k);

        for (int i=0; i < randomNum - 1; i++) {
            int q = rand.nextInt(100);
            System.out.println(q);
            for (int j = 0; j < i+1; j++) {
                if (q != list.getElementAt(j)) { 
                    if (j == i) {list.add(q);}                    
                } else{}
            }
        }

        for (int n=0 ;n < list.getLength(); n++) {
            tree.root = tree.insert(tree.root, list.getElementAt(n));
        }

        list.print();


        /* Constructing tree given in the above figure 
        tree.root = tree.insert(tree.root, 40);
        tree.root = tree.insert(tree.root, 20);
        tree.root = tree.insert(tree.root, 640);
        tree.root = tree.insert(tree.root, 840);
        tree.root = tree.insert(tree.root, 0);
        tree.root = tree.insert(tree.root, 65);

        The constructed AVL Tree would be
             30
            /  \
          20   40
         /  \     \
        10  25    50
        */
        System.out.println("Preorder traversal" + " of constructed tree is : ");
        tree.preOrder(tree.root);
        return tree;
    }
    
    public static void main(String[] args) {
        AVLTree a = new AVLTree();
        a.createAVL();
        //System.out.println("raiz del arbol es: " + a.createAVL().getRoot().key);
        //System.out.println("Factor de balance es:" + a.createAVL().getBalance(a.createAVL().getRoot()));
    }

    public SinglyLinkedList<Integer> getList() {
        return list;
    }

    public NodeT getRoot() {
        return root;
    }

    public int getPoints() {
        return points;
    }
}

