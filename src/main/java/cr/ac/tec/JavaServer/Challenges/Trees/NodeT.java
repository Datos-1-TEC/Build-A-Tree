package cr.ac.tec.JavaServer.Challenges.Trees;

public class NodeT {
    int key;
    int height;
    NodeT left, right;

    public NodeT(int item){
        this.key =  item;
        this.left = null;
        this.right = null;
        this.height = 1;
    }

}
