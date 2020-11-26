package cr.ac.tec.JavaServer.Challenges;

import com.fasterxml.jackson.databind.JsonNode;
import com.fasterxml.jackson.databind.ObjectMapper;

import cr.ac.tec.JavaServer.Json;
import cr.ac.tec.JavaServer.Challenges.Trees.SinglyLinkedList;
import cr.ac.tec.JavaServer.TokensPrototype.*;
import java.io.*;
import com.fasterxml.jackson.databind.node.ObjectNode;

/**
 * Esta clase se encarga de escribir tokens del reto en un archivo JSON de Challenges y los clasifica en Filler tokens 
 * y Main Tokens
 * @author Juan Peña
 */
public class ParseTokens {
    /**
     * Este método escribe los tokens que se hayan creado para el respectivo reto 
     * @param tokensList : lista de tokens que existen en la clase Challenge Generator
     * @param currentChallenge : Nombre del reto que se generó
     */
    public void tokensWriter(SinglyLinkedList<Token> tokensList, String currentChallenge) {
        int index = 0;
        int cont = tokensList.getLength();

        while (cont > 0) {
            int size = 0;
            try {
                Json node = new Json();
                String json = new String();
                JsonNode nodoChallenges = Json.parse(node.jsonReader(json, "JsonResources/Challenges.json"));
                String currentShape = tokensList.getElementAt(index).getShape();
                JsonNode myTokenNode = Json.toJson(tokensList.getElementAt(index));
                ObjectMapper objectMapper = new ObjectMapper();
                
                if (currentShape.equals(currentChallenge)){
                    size = nodoChallenges.get("Challenges").get("MainTokens").size();
                    ((ObjectNode) nodoChallenges.get("Challenges").get("MainTokens")).set(String.valueOf(size +1), myTokenNode);
                    objectMapper.writeValue(new File("JsonResources/Challenges.json"), nodoChallenges);
                }
                else{
                    size = nodoChallenges.get("Challenges").get("FillerTokens").size();
                    ((ObjectNode) nodoChallenges.get("Challenges").get("FillerTokens")).set(String.valueOf(size+1), myTokenNode);
                    objectMapper.writeValue(new File("JsonResources/Challenges.json"), nodoChallenges);
                }
            } catch (Exception e) {
                // TODO: handle exception
                e.printStackTrace();
            }
            index++;
            cont--;

        }
    }

    public static void main(String[] args) {
        ChallengeGenerator myChallenge = new ChallengeGenerator();
        ParseTokens parseTokens = new ParseTokens();
        myChallenge.challengeSelector();
        String currentChallenge = myChallenge.getMyBST().getShape();
        try {
            parseTokens.tokensWriter(myChallenge.getBstTokensList(), currentChallenge);
            parseTokens.tokensWriter(myChallenge.getAvlTokensList(), currentChallenge);
            parseTokens.tokensWriter(myChallenge.getSplayTokensList(), currentChallenge);
            parseTokens.tokensWriter(myChallenge.getbTokensList(), currentChallenge);
            Json node = new Json();
            String json = new String();
            JsonNode nodoChallenges =  Json.parse(node.jsonReader(json, "JsonResources/Challenges.json"));
            String jsonChallenges = Json.generateString(nodoChallenges, true);
            System.out.println(jsonChallenges);
        } catch (Exception e) {
            //TODO: handle exception
            e.printStackTrace();
        }

    }

}
