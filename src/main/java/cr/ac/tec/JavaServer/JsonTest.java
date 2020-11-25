package cr.ac.tec.JavaServer;

import com.fasterxml.jackson.core.JsonProcessingException;
import com.fasterxml.jackson.databind.JsonNode;
import com.fasterxml.jackson.databind.ObjectMapper;

import cr.ac.tec.JavaServer.Player.Player;

import java.io.BufferedReader;
import java.io.File;
import java.io.FileReader;

public class JsonTest {
    public static void main(String[] args) throws JsonProcessingException {
        try{
            String json;
            // Read the file
            BufferedReader br = new BufferedReader(new FileReader("JsonResources/Player2.json"));
            try {
                Player player = new Player(4, 3);
                JsonNode nodePlayer = Json.toJson(player);
                ObjectMapper objectMapper = new ObjectMapper();
                String stringPlayer = Json.generateString(nodePlayer, true);
                JsonNode formatedPlayer = Json.parse(stringPlayer);
                objectMapper.writeValue(new File("JsonResources/Player.json")., formatedPlayer);
                System.out.println(stringPlayer);




                StringBuilder sb = new StringBuilder();
                String line = br.readLine();
                while (line != null) {
                    sb.append(line);
                    sb.append(System.lineSeparator());
                    line = br.readLine();
                }
                json = sb.toString();
            } finally {
                br.close();
            }
            JsonNode node = Json.parse(json);
            System.out.println(node.get("Player").get("miNodo").asText());
            System.out.println(node.get("Player").get("posicion").asText());

        } catch(Exception e) {
            e.printStackTrace();
        }
       

    }
}