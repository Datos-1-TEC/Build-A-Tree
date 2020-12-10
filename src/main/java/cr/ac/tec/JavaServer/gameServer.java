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
import cr.ac.tec.JavaServer.Challenges.Trees.AVLTree;
import cr.ac.tec.JavaServer.Challenges.Trees.BTree;
import cr.ac.tec.JavaServer.Challenges.Trees.BinarySearchTree;
import cr.ac.tec.JavaServer.Challenges.Trees.SplayTree;
import cr.ac.tec.JavaServer.Player.Player;
import cr.ac.tec.JavaServer.TokensPrototype.Token;
import com.fasterxml.jackson.databind.node.ObjectNode;
import com.fasterxml.jackson.databind.ser.std.StdKeySerializers.Default;

public class gameServer {
    private String jsonChallenges = "";
    private static int port = 6666;
    private String recibido = "", enviado = "";
    private OutputStreamWriter  out;
    private InputStreamReader in; 
    private Boolean isOpen = true;
    private ServerSocket server;
    private String currentChallenge;
    private Socket client;
    private char[] buffer = new char[4096];
    Player player1;
    Player player2;

    public void listen(){

        Thread thread = new Thread(() -> {
            try {
                server = new ServerSocket(port);
                System.out.println("Esperando cliente");
                client = server.accept();
                System.out.println("Conectado");
                while (isOpen) {
                    //System.out.println("Esperando mensaje del cliente en python");
                    processMessage(client);
                }
            } catch (Exception e) {
                e.printStackTrace();
            }
        });
        thread.start();

    }

    private void sendMessage(String enviado, Socket client) throws IOException {
        this.out = new OutputStreamWriter(client.getOutputStream(), "UTF8");
        try {
            this.enviado = enviado;
            out.write(this.enviado.toCharArray());
            out.flush(); 
        } catch (Exception e) {
            e.printStackTrace();
        }      
    }
 
    public void processMessage(Socket client) throws IOException {
        this.in = new InputStreamReader(client.getInputStream(), "UTF8");
        this.recibido = readInput(this.in);
        System.out.println("String leido");

        if (this.recibido.contains("Connected")){

            player1 = new Player(1, 3, 0);
            player2 = new Player(2, 3, 0);
            //Hilo para llevar el cronómetro de cada cuanto se manda un reto y cuando se acaba la partida
            //Thread startingThread = new Thread(); 
            gameTimer();
           
        }
        /*
        En esta parte se verifica que el token que llega pertenece al del reto actual
        formato esperado del JSON con el token:
        {
            ID jugador "1|2": { 
                "Token":{
                    "value": integer
                    "Shape": a shape
                }
            }
        }

        */
        else if (this.recibido.contains("Token")){
           if (this.recibido.contains("ID1")){
                System.out.println("token recibido");
                JsonNode tokenNode = Json.parse(this.recibido);
                checkToken(this.player1, tokenNode);
           }
           else if (this.recibido.contains("ID2")){
                JsonNode tokenNode = Json.parse(this.recibido);
                checkToken(this.player2, tokenNode);
           }

        }
        else if(recibido.contains("exit")){
            this.isOpen = false;
            recibido = "";
            server.close();
        }     
        this.buffer = new char[4096];             
    }

    public void checkToken(Player player, JsonNode tokenNode) throws IOException {
        String tokenShape = tokenNode.get("ID1").get("Token").get("shape").asText();
        System.out.println("La forma del token recibido es: " + tokenShape);
        System.out.println("La forma del actual es: " + this.currentChallenge);
        
        //condiciones para agregar el valor del token al árbol del jugador correspondiente y reenviarlo 
        //al cliente para que lo muestre en interfaz. Si el token no pertenece el reto actual
        //se borra el progreso del reto actual para ese jugador y se mandan los valores para el árbol
        // de nuevo
        if (tokenShape.equals(currentChallenge)){
            addTokenToTree(player, tokenNode, tokenShape);
            int id = player.getID();
            int score = player.getScore();
            String message = "player" + String.valueOf(id) + ":" + String.valueOf(score);
            sendMessage(message, this.client);
            
        }
        else{
            setNewTree(player, this.currentChallenge);
            player.setScore(0);
            int id = player.getID();
            int score = player.getScore();
            String message = "player" + String.valueOf(id) + ":" + String.valueOf(score);
            sendMessage(message, this.client);
            
        }
    }
    /**
     * En este método se agrega el valor del token que manda el cliente al árbol correspondiente y se le suman los 
     * puntos del token al jugador 
     * @param player Jugador al que se le agregarán los nodos para el árbol del reto y los puntos del token
     * @param tokenNode JsonNode que contiene los datos del token recién mandado por el cliente
     * @param tokenShape Forma del token recibido
     */
    public void addTokenToTree(Player player, JsonNode tokenNode, String tokenShape){
        int tokenValue = tokenNode.get("ID1").get("Token").get("value").asInt();
        int tokenPoints = tokenNode.get("ID1").get("Token").get("points").asInt();
        System.out.println("El valor del token recibido es: " + tokenValue);
    
        if (tokenShape.contains("Diamond")){
            player.getMyBST().insert(tokenValue);
            player.getMyBST().getKeysList().print();;
            player.setScore(tokenPoints);
            System.out.println("La forma es: " + tokenShape);
            System.out.println("Los puntos del jugador son: " + player.getScore());
        }
        else if (tokenShape.contains("Rectangle")){
            player.getMyBTree().insert(tokenValue);
            player.setScore(tokenPoints);  
            System.out.println("La forma es: " + tokenShape);
            System.out.println("Los puntos del jugador son: " + player.getScore());
        }
        else if (tokenShape.contains("Circle")){
            player.getMyAVL().insert(player.getMyAVL().getRoot(), tokenValue);
            player.setScore(tokenPoints);
            System.out.println("La forma es: " + tokenShape);
            System.out.println("Los puntos del jugador son: " + player.getScore());
        }
        else{
            player.getMySplay().insert(tokenValue);
            player.setScore(tokenPoints);
            System.out.println("La forma es: " + tokenShape);
            System.out.println("Los puntos del jugador son: " + player.getScore());
        }
    }

    public String readInput(InputStreamReader inputStream) throws IOException {
        inputStream.read(buffer);
        String message = "";
        for (char c:buffer){
            message += c;
            if (c == 0){
                break;
            }
        }
        
        return message;   
    }

    public void gameTimer() throws IOException {
        Timer timer = new Timer();
        timer.scheduleAtFixedRate(new TimerTask(){

            private int currentTime = 0;
            @Override
            public void run() {
                this.currentTime ++;
                String enviado = generateTokens();

                try {
                    
                    sendMessage(enviado, client);
                } catch (IOException e) {
                    e.printStackTrace();
                }
                if (this.currentTime > 2){
                    try {
                        sendMessage("exit", client);
                        this.cancel();
                        timer.cancel();
                    } catch (IOException e) {
                        
                        e.printStackTrace();
                    }
                }
            }
            
        }, 1000, 3000);
        sendMessage("True", this.client);
    }

    public void setNewTree(Player player, String currentChallenge){
        if (currentChallenge.contains("Diamond")){
            BinarySearchTree myBST = new BinarySearchTree();
            player.setMyBST(myBST);
        }
        else if (currentChallenge.contains("Rectangle")){
            BTree myBTree = new BTree();
            player.setMyBTree(myBTree);            
        }
        else if (currentChallenge.contains("Circle")){
            AVLTree myAVL = new AVLTree();
            player.setMyAVL(myAVL);
        }
        else{
            SplayTree mySplay = new SplayTree();
            player.setMySplay(mySplay);
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
        this.currentChallenge = myChallenge.getChallengeShape();
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
    public static void main(String[] args) throws IOException {
        gameServer server = new gameServer();
        server.listen();
    }

}