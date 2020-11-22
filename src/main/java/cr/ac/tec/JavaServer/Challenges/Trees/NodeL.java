package cr.ac.tec.JavaServer.Challenges.Trees;

public class NodeL<T> {
    private T value;
    private NodeL<T> next;
    private NodeL<T> prev;

    public NodeL<T> getPrev() {
        return prev;
    }

    public void setPrev(NodeL<T> prev) {
        this.prev = prev;
    }




    public NodeL() {
        this.next = null;
    }

    public NodeL(T value) {
        this();
        this.value = value;
    }

    public NodeL(T value, NodeL<T> next) {
        this(value);
        this.next = next;
    }

    public T getValue() {
        return value;
    }

    public void setValue(T value) {
        this.value = value;
    }

    public NodeL<T> getNext() {
        return next;
    }

    public void setNext(NodeL<T> next) {
        this.next = next;
    }
}

