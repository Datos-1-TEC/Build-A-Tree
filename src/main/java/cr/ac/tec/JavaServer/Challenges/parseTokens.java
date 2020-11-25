package cr.ac.tec.JavaServer.Challenges;

import com.fasterxml.jackson.databind.JsonNode;
import com.fasterxml.jackson.databind.ObjectMapper;

import cr.ac.tec.JavaServer.Json;
import cr.ac.tec.JavaServer.Challenges.Trees.SinglyLinkedList;
import cr.ac.tec.JavaServer.Player.Player;
import cr.ac.tec.JavaServer.TokensPrototype.*;


public class parseTokens {
    private SinglyLinkedList<Diamond> bstTokensList = new SinglyLinkedList<>(); 
    private SinglyLinkedList<Circle> avlTokensList = new SinglyLinkedList<>();
    private SinglyLinkedList<Rectangle> bTokensList = new SinglyLinkedList<>();
    private SinglyLinkedList<Triangle> splayTokensList = new SinglyLinkedList<>();

    public parseTokens(SinglyLinkedList<Diamond> bstTokensList, SinglyLinkedList<Circle> avlTokensList,
                        SinglyLinkedList<Rectangle> bTokensList, SinglyLinkedList<Triangle> splayTokensList) {

        this.bstTokensList = bstTokensList;
        this.avlTokensList = avlTokensList;
        this.bTokensList = bTokensList;
        this.splayTokensList = splayTokensList;
    }

    
          
}
