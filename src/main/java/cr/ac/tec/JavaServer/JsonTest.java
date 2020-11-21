package cr.ac.tec.JavaServer;

import com.fasterxml.jackson.databind.JsonNode;
import java.io.BufferedReader;
import java.io.FileReader;

public class JsonTest {
    public static void main(String[] args) {
        try{
            String json;
            // Read the file
            BufferedReader br = new BufferedReader(new FileReader("JsonResources/Player2.json"));
            try {
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