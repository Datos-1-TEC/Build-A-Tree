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
import com.fasterxml.jackson.databind.node.ObjectNode;

/**
 * Esta clase es el servidor que se encarga de controlar el flujo de eventos durante el juego
 * tales como: Enviar retos basados en estruturas de datos como lo son los árboles binarios (BST, AVL, Splay) y los 
 * árboles multi-way(B Tree)
 * Estas estructuras almacenan un numero entero que pertenece al valor de un objeto token generado de forma aleatoria
 * además puede recibir nuevos nodos especificados para cada jugador y un árbol objetivo
 * En cuando al envío de datos, esta clase tiene como meta enviar las instrucciones que el cliente ejecutará a lo 
 * largo de una partida, por ejemplo: cuando se genera un nuevo reto en la partida
 * se necesita enviar un archivo JSON estructurado de tal manera que se pueda discriminar entre los tokens que son
 * pertenecientes al reto actual y los tokens que se generan como relleno para los jugadores.
 * Posteriormente a la creación de un reto es necesario enviar las especificaciones que requiere ese reto:
 * si el reto es un BST, el servidor además de mandar una cantidad de tokens, debe indiciar qué profundidad tendrá
 * este árbol para completarlo. 
 * También envía el puntaje del jugador cada ver que el mismo toma un token, si el token pertenece al tipo de reto actual
 * se aumenta su puntaje, de lo contrario se vuelve 0 
 * @author Juan Peña
 * 
 */
public class gameServer {
    private String recibido = "", enviado = "";
    private char[] buffer = new char[4096];
    private String jsonChallenges = "";
    private OutputStreamWriter  out;
    private String currentChallenge;
    private static int port = 6666;
    private Boolean isOpen = true;
    private InputStreamReader in; 
    private ServerSocket server;
    private int numElements = 0;
    private int BTreeOrder = 0;
    private Player player1;
    private Player player2;
    private int depth = 0;
    private int level = 0;
    private Socket client;
    
    /**
     * Método para crear el thread donde se encuentra escuchando el server a todo lo que envía el client
     */
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
    /**
     * Este método se encarga de enviar todos los mensajes al client 
     * @param enviado String que se desea enviar
     * @param client  cliente objetivo
     * @throws IOException 
     */
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
    
    /**
     * En este método se procesan todos los mensajes que manda el client así como se generan las respuestas a los mismos
     * @param client cliente objetivo
     * @throws IOException
     */
    private void processMessage(Socket client) throws IOException {
        this.in = new InputStreamReader(client.getInputStream(), "UTF8");
        this.recibido = readInput(this.in);
        System.out.println("String leido");

        if (this.recibido.contains("Connected")){ //Esta condición se cumple en cuanto el cliente se conecta

            player1 = new Player(1, 3, 0);
            player2 = new Player(2, 3, 0);
            //Hilo para llevar el cronómetro de cada cuanto se manda un reto y cuando se acaba la partida
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
        //En esta condición se cierra la conexión de forma segura
        else if(recibido.contains("exit")){
            this.isOpen = false;
            recibido = "";
            server.close();
        }     
        this.buffer = new char[4096];             
    }
/**
 * En este método se chequea el token para responder al cliente que el jugador ganó x cantidad de puntos
 * @param player jugador objetivo
 * @param tokenNode JsonNode con los datos del token
 * @throws IOException
 */
    public void checkToken(Player player, JsonNode tokenNode) throws IOException {
        String tokenShape = tokenNode.get("ID1").get("Token").get("shape").asText();
        System.out.println("La forma del token recibido es: " + tokenShape);
        System.out.println("La forma del actual es: " + this.currentChallenge);
        
        //condiciones para agregar el valor del token al árbol del jugador correspondiente y reenviarlo 
        //al cliente para que lo muestre en interfaz. Si el token no pertenece el reto actual
        //se borra el progreso del reto actual para ese jugador
        if (tokenShape.equals(currentChallenge)){ //Si el token coincide se agregan los valores al árbol
            // y se suma el puntaje al jugador
            addTokenToTree(player, tokenNode, tokenShape);
            int id = player.getID();
            int score = player.getScore();
            String message = "player" + String.valueOf(id) + ":" + String.valueOf(score);
            sendMessage(message, this.client);            
        }
        else{
            //Si se equivoca de token se resetea el árbol y el puntaje acumulado en el reto
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
            player.getMyBTree(this.BTreeOrder).insert(tokenValue);
            player.setScore(tokenPoints);  
            System.out.println("La forma es: " + tokenShape);
            System.out.println("Los puntos del jugador son: " + player.getScore());
        }
        else if (tokenShape.contains("Circle")){
            player.getMyAVL().insert(tokenValue);
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

    /**
     * Este método se usa para leer una secuencia de caracteres provenientes de un Input Stream 
     * enviado por el client
     * @param inputStream mensaje serializado
     * @return message mensaje Deserializado
     * @throws IOException
     */
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
    /**
     * En este método se corre el hilo que está generando los retos cada cierto tiempo
     * Se envía el JSON con los tokens y se envían las condiciones para ese reto
     */
    public void gameTimer() throws IOException {
        Timer timer = new Timer();
        timer.scheduleAtFixedRate(new TimerTask(){

            private int currentTime = 0;
            @Override
            public void run() {
                this.currentTime ++;
                String enviado = "";

                try {

                    if (currentTime == 10){
                        enviado = generateTokens();
                        sendMessage(enviado, client);
                        sendMessage(checkChallengeConditions(currentChallenge), client);
                        //Verificar el tipo para mandar la especificación sobre si es profundidad orden o niveles, y cant elem
                    }
                    else if (currentTime == 20){
                        enviado = generateTokens();
                        sendMessage(enviado, client);
                        sendMessage(checkChallengeConditions(currentChallenge), client);
                        //Verificar el tipo para mandar la especificación sobre si es profundidad orden o niveles, y cant elem
                    }
                    else if (currentTime == 30){
                        enviado = generateTokens();
                        sendMessage(enviado, client);
                        sendMessage(checkChallengeConditions(currentChallenge), client);
                        //Verificar el tipo para mandar la especificación sobre si es profundidad orden o niveles, y cant elem
                    }
                    else if (currentTime == 40){
                        enviado = generateTokens();
                        sendMessage(enviado, client);
                        sendMessage(checkChallengeConditions(currentChallenge), client);
                        //Verificar el tipo para mandar la especificación sobre si es profundidad orden o niveles, y cant elem
                    }
   
                } catch (IOException e) {
                    e.printStackTrace();
                }

                if (this.currentTime == 45){
                    try {
                        sendMessage("exit", client);
                        this.cancel();
                        timer.cancel();
                    } catch (IOException e) {
                        
                        e.printStackTrace();
                    }
                }
            }
            
        }, 1000, 1000);
        sendMessage("True", this.client);
    }
    
    /**
     * Este método chequea las condiciones del reto actual para dar formato a la info para indicar al cliente 
     * dichas condiciones
     * @param currentChallenge reto actual que determina las condiciones
     * @return challengeParams String con los parámetros definidos según los árboles
     */
    public String checkChallengeConditions(String currentChallenge){
        String challengeParams = "";
        if (currentChallenge.contains("Diamond")){
            //Enviar profundidad
            challengeParams = "Depth:" + String.valueOf(this.depth);                         
        }
        else if (currentChallenge.contains("Rectangle")){
            //Enviar Orden y Niveles
            challengeParams = "Order: " + String.valueOf(this.BTreeOrder) + ":Level:" + String.valueOf(this.level);               
        }
        else {
            //Cantidad de elementos 
            challengeParams = "numElements:" + String.valueOf(this.numElements);
        }
        return challengeParams;
    }
    /**
     * Este método resetea el árbol del jugador en caso de que se equivoque de token según el reto en que se encuentre
     * @param player jugador que se equivoca de token
     * @param currentChallenge el reto actualmente
     */
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
     */
    public String generateTokens(){
        Json node = new Json();
        String json = new String();
        ChallengeGenerator myChallenge = new ChallengeGenerator();
        parseTokens parseTokens = new parseTokens();
        myChallenge.challengeSelector();
        this.currentChallenge = myChallenge.getChallengeShape();

        if (currentChallenge == "Rectangle"){
            this.BTreeOrder = myChallenge.getOrder();
            this.level = myChallenge.getMyBTree().getLevel();
        }
        else if (currentChallenge == "Diamond"){
            this.depth = myChallenge.getMyBST().getMaxDepth();
        }
        else if (currentChallenge == "Circle"){
            this.numElements = myChallenge.getMyAVL().getList().getLength();
        }
        else if (currentChallenge == "Triangle"){
            this.numElements = myChallenge.getMySplay().getList().getLength();
        }

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