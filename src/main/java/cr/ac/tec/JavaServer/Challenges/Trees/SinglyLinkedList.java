package cr.ac.tec.JavaServer.Challenges.Trees;

import javax.sound.midi.Track;

public class SinglyLinkedList<T> {
    private NodeL<T> first, tail;
    private int length = 0;
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
    public SinglyLinkedList<T> deleteNode(T element){
        if(!isEmpty()){
            if(this.first.getNext() == null && element == this.first.getValue())
                this.first = null;
            else if (element == this.first.getValue())
                this.first = this.first.getNext();
            else{
                NodeL<T> prev, tmp;
                for (prev = this.first, tmp = this.first.getNext();
                tmp != null && tmp.getValue() != element;
                prev = prev.getNext(), tmp = tmp.getNext());
                if(tmp != null){
                    prev.setNext(tmp.getNext());
                }if (tmp.getNext() == null){
                    prev.setNext(null);
                }
            }
        }
        return this;
    }
    /**
     * Adds an element to the end
     *
     * @param element the element to add
     */
    public void add(T element) {
        if (this.isEmpty()) {
            this.first = new NodeL<>(element);
            this.length ++;
        } else {
            NodeL<T> ref = this.first;
            while (ref.getNext() != null) {
                ref = ref.getNext();
            }
            ref.setNext(new NodeL<>(element));
            this.length ++;
        }

    } 
    public Boolean contains(T element){
        NodeL<T> current = this.first;
        Boolean result = false;
        while(current.getNext() != null){
            if (current.getValue() == element){
                return result;
            }
            current = current.getNext();
        }
        return result;
    }
    public void print(){
        NodeL<T> current = this.first;
        while (current != null){
            System.out.printf("|%s|-> ", current.getValue());
            current = current.getNext();
        }
        System.out.println();
    }

    public int getLength() {
        return this.length;
    }

    public T getElementAt(int position){
        NodeL<T> current = this.first;
        while (position > 0){
            current = current.getNext();
            position --;
        }
        return current.getValue();

    }
}
