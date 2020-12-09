package cr.ac.tec.JavaServer.Challenges.Trees;

import java.util.Random;

import javax.sound.sampled.SourceDataLine;

public class BTree {

    private int T;
    private SinglyLinkedList<Integer> list = new SinglyLinkedList<>();
    private int level = 0;

    // Node creation
    public class Node {
        int n;
        int key[] = new int[2 * T - 1];
        Node child[] = new Node[2 * T];
        boolean leaf = true;

        public int Find(int k) {
            for (int i = 0; i < this.n; i++) {
                if (this.key[i] == k) {
                    return i;
                }
            }
            return -1;
        };
    }

    public BTree() {
    }

    public BTree(int t) {
        T = t;
        root = new Node();
        root.n = 0;
        root.leaf = true;
        
    }

    private Node root;
    private int order;

    // Search key
    private Node Search(Node x, int key) {
        int i = 0;
        if (x == null)
            return x;
        for (i = 0; i < x.n; i++) {
            if (key < x.key[i]) {
                break;
            }
            if (key == x.key[i]) {
                return x;
            }
        }
        if (x.leaf) {
            return null;
        } else {
            return Search(x.child[i], key);
        }
    }

    // Splitting the node
    private void Split(Node x, int pos, Node y) {
        Node z = new Node();
        z.leaf = y.leaf;

        z.n = T - 1;
        
        for (int j = 0; j < T - 1; j++) {
            z.key[j] = y.key[j + T];
        }
        if (!y.leaf) {
            for (int j = 0; j < T; j++) {
                z.child[j] = y.child[j + T];
            }
        }
        y.n = T - 1;
        for (int j = x.n; j >= pos + 1; j--) {
            x.child[j + 1] = x.child[j];
        }
        x.child[pos + 1] = z;

        for (int j = x.n - 1; j >= pos; j--) {
            x.key[j + 1] = x.key[j];
        }
        x.key[pos] = y.key[T - 1];
        x.n = x.n + 1;
    }

    // Inserting a value
    public void insert(int key) {
        Node r = root;
        if (r.n == 2 * T - 1) {
            Node s = new Node();
            root = s;
            level++;
            s.leaf = false;
            s.n = 0;
            s.child[0] = r;
            Split(s, 0, r);
            insertValue(s, key);
        } else {
            insertValue(r, key);
        }
    }

    // Insert the node
    final private void insertValue(Node x, int k) {

        if (x.leaf) {
            int i = 0;            
            for (i = x.n - 1; i >= 0 && k < x.key[i]; i--) {
                x.key[i + 1] = x.key[i];
            }
            x.key[i + 1] = k;
            x.n = x.n + 1;
        } else {
            int i = 0;
            for (i = x.n - 1; i >= 0 && k < x.key[i]; i--) {
            }
            ;
            i++;
            Node tmp = x.child[i];
            if (tmp.n == 2 * T - 1) {
                Split(x, i, tmp);
                if (k > x.key[i]) {
                    i++;
                }
            }
            insertValue(x.child[i], k);
        }
    }

    public void Show() {
        Show(root);
    }

    // Display
    private void Show(Node x) {
        assert (x == null);
        for (int i = 0; i < x.n; i++) {
            System.out.print(x.key[i] + " ");
        }
        if (!x.leaf) {
            for (int i = 0; i < x.n + 1; i++) {
                Show(x.child[i]);
            }
        }
    }

    // Check if present
    public boolean Contain(int k) {
        if (this.Search(root, k) != null) {
            return true;
        } else {
            return false;
        }
    }

    public BTree createB() {
        Random rand = new Random();
        int n = rand.nextInt((4 - 2) + 1) + 2;
        BTree tree = new BTree(n);
        
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

        for (int w = 0 ;w < list.getLength(); w++) {
            tree.insert(list.getElementAt(w));
        }
        //tree.setLevel(tree.root, level);
        setOrder(2 * tree.T);
        System.out.println("El orden del arbol es: " + 2 * tree.T);
        System.out.println("El nivel del arbol es: " + tree.getLevel());
        list.print();
        tree.Show();
        return tree;
    }
    public static void main(String[] args) {
        BTree b = new BTree(2);
        b = b.createB();
        /*
        b.insert(1);
        System.out.println(b.root.n);
        b.insert(2);
        System.out.println(b.root.n);
        b.insert(3);
        System.out.println(b.root.n);
        b.insert(10);
        System.out.println(b.root.n);
        b.insert(11);
        System.out.println(b.root.n);
        b.insert(12);
        System.out.println(b.root.n);
        b.insert(13);
        System.out.println(b.root.n);
        b.insert(15);
        System.out.println(b.root.n);
        b.insert(5);
        System.out.println(b.root.n);
        b.insert(4);
        System.out.println(b.root.n);
*/
        b.setLevel(b.root, b.level);
        b.setLevel(b.level);
        
        //b.Show();
        System.out.println("");
        System.out.println("El nivel del arbol es: " + b.level);
        System.out.println("Numero de elementos en raiz = " +b.root.n);
        System.out.println(b.root.child[0].n);
        System.out.println("Hijo 0: " + b.root.key[1]);
    }

    public int getOrder() {
        return this.order;
    }
    public void setOrder(int order) {
        this.order = order;
    }

    public void setLevel(Node x, int leveln) {
        if (x.leaf) this.level = leveln;
        else { setLevel(x.child[0], leveln + 1); }
    }
    public void setLevel(int level){
        this.level = level;
    }
    
    public int getLevel() {
        return level;
    }

    public SinglyLinkedList<Integer> getList() {
        return list;
    }

}