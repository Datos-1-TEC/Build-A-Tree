package cr.ac.tec.JavaServer;

import java.io.File;
import java.io.IOException;
import java.io.InputStreamReader;
import java.io.OutputStreamWriter;
import java.net.ServerSocket;
import java.net.Socket;
import java.util.Timer;
import java.util.TimerTask;

import com.fasterxml.jackson.databind.JsonNode;
import com.fasterxml.jackson.databind.ObjectMapper;

import cr.ac.tec.JavaServer.Challenges.ChallengeGenerator;
import cr.ac.tec.JavaServer.Challenges.parseTokens;
import cr.ac.tec.JavaServer.ServerFeatures.GameTimer;

import com.fasterxml.jackson.databind.node.ObjectNode;

public class gameServer {
    private String jsonChallenges = "";
    private static int port = 6666;
    private String recibido = "", enviado = "";
    private OutputStreamWriter  out;
    private InputStreamReader in; 
    private Boolean isOpen = true;
    private char[] charsMessage = new char[4096];
    private ServerSocket server;

    public void listen(){

        Thread thread = new Thread(() -> {
            try {
                server = new ServerSocket(port);
                System.out.println("Esperando cliente");
                Socket client = server.accept();
                this.out = new OutputStreamWriter(client.getOutputStream(), "UTF8");
                this.in = new InputStreamReader(client.getInputStream(), "UTF8");
                while (isOpen) {
                    //System.out.println("Esperando mensaje del cliente en python");
                    this.in.read(this.charsMessage);     
                    processMessage(fromChartoString());
                }
            } catch (Exception e) {
                e.printStackTrace();
            }
        });
        thread.start();

    }

    private String fromChartoString() {
        for (char c : charsMessage) {
            this.recibido += c;
            if (c == 00) {
                break;
            }
        }
        return this.recibido;
    }

    private void sendMessage(String enviado) throws IOException {
        try {
            this.enviado = enviado;
            out.write(this.enviado.toCharArray());
            out.flush(); 
        } catch (Exception e) {
            e.printStackTrace();
        }
        
    }
    /**
     * En este método se genera el JSON con los tokens de un reto BST, AVL, BTREE o SPLAY
     * de manera que en MainTokens se encuentran los objetos del reto y el FillerTokens están otros tokens generados que 
     *  se muestran en la GUI 
     * Además, dentro de la instancia myChallenge se puede acceder a los valores árbol generado mediante una lista enlazada
     *
     */
    public String generateTokens(){
        Json node = new Json();
        String json = new String();
        ChallengeGenerator myChallenge = new ChallengeGenerator();
        parseTokens parseTokens = new parseTokens();
        myChallenge.challengeSelector();
        String currentChallenge = myChallenge.getChallengeShape();
        try {
            parseTokens.tokensWriter(myChallenge.getBstTokensList(), currentChallenge);
            parseTokens.tokensWriter(myChallenge.getAvlTokensList(), currentChallenge);
            parseTokens.tokensWriter(myChallenge.getSplayTokensList(), currentChallenge);
            parseTokens.tokensWriter(myChallenge.getbTokensList(), currentChallenge);
            
            JsonNode nodoChallenges =  Json.parse(node.jsonReader(json, "JsonResources/Challenges.json"));
            this.jsonChallenges = Json.generateString(nodoChallenges, true);

            System.out.println("Cleaning JSON...");
            JsonNode value = Json.parse(node.jsonReader(json, "JsonResources/Challenge.json"));
			((ObjectNode) nodoChallenges.get("Challenges")).set("MainTokens", value);
            ((ObjectNode) nodoChallenges.get("Challenges")).set("FillerTokens", value);
           
            ObjectMapper objectMapper = new ObjectMapper();
            objectMapper.writeValue(new File("JsonResources/Challenges.json"), nodoChallenges);

        } catch (Exception e) {
        
            e.printStackTrace();
        }  
        return this.jsonChallenges;    
    }

    public void processMessage(String recibido) throws IOException {
        Timer myTimer = new Timer();
        this.recibido = recibido;
        
        
        if (this.recibido.contains("Connected")){
            myTimer.scheduleAtFixedRate(new TimerTask(){
                int currentTime = 0;
                public void run(){
                    currentTime++;
                    System.out.println("Current seconds: " + currentTime);
                    if (currentTime < 10){
                        enviado = "Temporizador iniciado";
                        try {
                            sendMessage(enviado);
                        } catch (IOException e) {
                            e.printStackTrace();
                        }
                        //System.out.println("Cliente dice: " + recibido);
                        System.out.println("Enviar a cliente: " + enviado);
                        //recibido = "";  
                        enviado = "";
                    }
                    else if(currentTime == 10) {
                        try {
                            enviado = "challenges";
                            sendMessage(enviado);
                            enviado = "";
                            enviado = generateTokens();
                            sendMessage(enviado);
                            System.out.println("Enviar a cliente: " + enviado);
                            enviado = "";
                            //cancel();
                        } catch (IOException e) {
                            e.printStackTrace();
                        }
                        
                    }
                    else {
                        try {
                            sendMessage("exit");
                            cancel();
                        } catch (IOException e) {
                           
                            e.printStackTrace();
                        }
                    }
                }}, 1000, 1000);    
        }
        if (this.recibido.contains("challenges")){
           
            try {
                enviado = "challenges";
                sendMessage(enviado);
                enviado = "";
                enviado = generateTokens();
                sendMessage(enviado);
                System.out.println("Enviar a cliente: " + enviado);
                enviado = "";
                //cancel();
            } catch (IOException e) {
                e.printStackTrace();
            }
            //System.out.println("Enviar a cliente: >>>" + this.enviado);
            this.recibido = ""; this.enviado = "";
        }
        else if(this.recibido.contains("exit")){
            isOpen = false;
            this.recibido = "";
            server.close();
            
        }          
        this.charsMessage = new char[4096];
        
    }
    public static void main(String[] args) throws IOException {
        gameServer server = new gameServer();
        server.listen();
    }
}