package cr.ac.tec.JavaServer.Challenges.Trees;

public class SinglyLinkedList<T> {
    private NodeL<T> first, tail;
    //

    public SinglyLinkedList() {
        this.first = this.tail = null;
    }  
    public boolean isEmpty() {
        return this.first == null;
    }
    /**
     * Adds an element at first position
     *
     * @param element the element to add
     */
    public void addFirst(T element){

        if(this.isEmpty()){
            this.first = new NodeL<>(element);
        } else{
            NodeL<T> ref = new NodeL<>(element);
            ref.setNext(this.first);
            first = ref;
        }
    }
    /**
     * Adds an element to the end
     *
     * @param element the element to add
     */
    public void add(T element) {
        if (this.isEmpty()) {
            this.first = new NodeL<>(element);
        } else {
            NodeL<T> ref = this.first;
            while (ref.getNext() != null) {
                ref = ref.getNext();
            }
            ref.setNext(new NodeL<>(element));
        }

    } 
    public void print(){
        NodeL<T> current = this.first;
        while (current != null){
            System.out.printf("|%s|-> ", current.getValue());
            current = current.getNext();
        }
        System.out.println();
    }   
}
