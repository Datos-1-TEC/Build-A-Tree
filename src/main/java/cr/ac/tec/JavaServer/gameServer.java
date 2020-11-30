package cr.ac.tec.JavaServer;

import java.io.File;
import java.io.IOException;
import java.io.InputStreamReader;
import java.io.OutputStreamWriter;
import java.net.ServerSocket;
import java.net.Socket;

import com.fasterxml.jackson.databind.JsonNode;
import com.fasterxml.jackson.databind.ObjectMapper;

import cr.ac.tec.JavaServer.Challenges.ChallengeGenerator;
import cr.ac.tec.JavaServer.Challenges.parseTokens;
import com.fasterxml.jackson.databind.node.ObjectNode;

public class gameServer {
    private String jsonChallenges = "";

    static int port = 6666;
    String recibido = "", enviado = "";

    OutputStreamWriter  out;
    InputStreamReader in; 
    private Boolean isOpen = true;

    public void listen(){

        try {
            ServerSocket server = new ServerSocket(port);
            System.out.println("Esperando cliente");
            Socket client = server.accept();
            this.out = new OutputStreamWriter(client.getOutputStream(), "UTF8");
            this.in = new InputStreamReader(client.getInputStream(), "UTF8");

            char[] charsMessage = new char[4096];

            while (isOpen) {
                System.out.println("Esperando mensaje del cliente en python");
                this.in.read(charsMessage);
                
                for (char c : charsMessage) {
                    recibido += c;
                    if (c == 00) {
                        break;
                    }
                }

                if (recibido.contains("posicion")){
                    this.enviado = "Jugador recibido";
                    sendMessage(this.enviado);
                    System.out.println("Cliente dice: " + recibido);
                    System.out.println("Enviar a cliente: >>>" + this.enviado);
                    recibido = ""; this.enviado = "";
                }
                if (recibido.contains("challenges")){
                    this.enviado = generateTokens();
                    sendMessage(this.enviado);
                    System.out.println("Cliente dice: " + recibido);
                    System.out.println("Enviar a cliente: >>>" + this.enviado);
                    recibido = ""; this.enviado = "";
                }
                else if(recibido.contains("exit")){
                    server.close();
                    isOpen = false;
                    recibido = "";
                    
                }
            

                charsMessage = new char[4096];
            }
        } catch (Exception e) {
            e.printStackTrace();
        }

    }

    private void sendMessage(String enviado) throws IOException {
        this.enviado = enviado;
        out.write(this.enviado.toCharArray());
        out.flush();
    }

    public String generateTokens(){
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
            this.jsonChallenges = Json.generateString(nodoChallenges, true);
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
        return this.jsonChallenges;    
    }

    public static void main(String[] args) throws IOException {
        gameServer server = new gameServer();
        server.listen();

    }
    /*
    if (recibido.contains("challenges")){
                    this.enviado = generateTokens();
                    sendMessage(this.enviado);
                    System.out.println("Cliente dice: " + recibido);
                    System.out.println("Enviar a cliente: >>>" + this.enviado);
                    recibido = ""; this.enviado = "";
                }
    */
}