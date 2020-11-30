package cr.ac.tec.JavaServer.Challenges.Trees.Btree;

public class NodeB {
    int m = 4;
    boolean leaf = true;
    int keyTally = 1;
    int keys[] = new int[m - 1];
    NodeB references[] = new NodeB[m];

    NodeB(int key) {
    keys[0] = key;
    for (int i = 0; i < m; i++)
    references[i] = null;
    }
}
