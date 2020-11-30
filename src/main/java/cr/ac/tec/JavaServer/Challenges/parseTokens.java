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
public class parseTokens {
    /**
     * Este método escribe los tokens que se hayan creado para el respectivo reto 
     * @param tokensList : lista de tokens que existen en la clase Challenge Generator
     * @param currentChallenge : Nombre del reto que se generó
     */
    public void tokensWriter(SinglyLinkedList<Token> tokensList, String currentChallenge) {

        int listLength = tokensList.getLength();
        int index = 0;

        int size = 0;
        try {
            Json node = new Json();
            String json = new String();
            JsonNode nodoChallenges = Json.parse(node.jsonReader(json, "JsonResources/Challenges.json"));
            String currentShape = tokensList.getElementAt(0).getShape();
            
            ObjectMapper objectMapper = new ObjectMapper();

            if (currentShape == currentChallenge) {
                while (index < listLength){
                    JsonNode myTokenNode = Json.toJson(tokensList.getElementAt(index));
                    size = nodoChallenges.get("Challenges").get("MainTokens").size();
                    ((ObjectNode) nodoChallenges.get("Challenges").get("MainTokens")).set(String.valueOf(size + 1),
                            myTokenNode);
                    objectMapper.writeValue(new File("JsonResources/Challenges.json"), nodoChallenges);
                    index ++;
                }
            } else {
                while (index < listLength){
                    JsonNode myTokenNode = Json.toJson(tokensList.getElementAt(index));
                    size = nodoChallenges.get("Challenges").get("FillerTokens").size();
                    ((ObjectNode) nodoChallenges.get("Challenges").get("FillerTokens")).set(String.valueOf(size + 1),
                            myTokenNode);
                    objectMapper.writeValue(new File("JsonResources/Challenges.json"), nodoChallenges);
                    index ++;
                }

            }

        } catch (Exception e) {
            // TODO: handle exception
            e.printStackTrace();
        }
            

        
    }

    public static void main(String[] args) {
        ChallengeGenerator myChallenge = new ChallengeGenerator();
        parseTokens parseTokens = new parseTokens();
        myChallenge.challengeSelector();
        String currentChallenge = myChallenge.getChallengeShape();
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

            System.out.println("Cleaning JSON...");
            JsonNode value = Json.parse(node.jsonReader(json, "JsonResources/Challenge.json"));
			((ObjectNode) nodoChallenges.get("Challenges")).set("MainTokens", value);
            ((ObjectNode) nodoChallenges.get("Challenges")).set("FillerTokens", value);
           
            ObjectMapper objectMapper = new ObjectMapper();
            objectMapper.writeValue(new File("JsonResources/Challenges.json"), nodoChallenges);
            String jsonChallenge = Json.generateString(nodoChallenges, true);

            System.out.println(jsonChallenge);
        } catch (Exception e) {
            //TODO: handle exception
            e.printStackTrace();
        }

    }

}
