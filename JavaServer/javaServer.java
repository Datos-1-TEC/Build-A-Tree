package JavaServer;

import java.io.*;
import java.net.*;

public class javaServer {
    private Boolean flag = true;
    private BufferedReader in;
    private ConnectionHandler handler;
    private int port = 6666;
    private String JsonFiles;

    public void ConnectionListener() {

        Thread thread = new Thread(() -> {
            try {
                ServerSocket incoming = new ServerSocket(this.port);
                System.out.println("listening connections on: " + incoming.getLocalPort());
                while (flag) {
                    Socket socket = incoming.accept();
                    System.out.println("Cliente ha ingresado");
                    processConnection(socket);

                }
            } catch (IOException e) {
                e.printStackTrace();
            }
        });
        thread.start();
    }

    public void processConnection(Socket socket) throws IOException {
        this.in = new BufferedReader(new InputStreamReader(socket.getInputStream()));
        String incomingMessage = streamProcessing(this.in);
        System.out.println("Mensaje de cliente: " + incomingMessage);
        
        if (incomingMessage.contains("posicion")){
            handler = new ConnectionHandler(socket, this);
            handler.sendMessage("Hi from server");

        }

        //Codigo que genera las condiciones para responderle al cliente
        
    }

    public void processMessage(String message){
        //Código para procesar la info recibida
        System.out.println("Procesando mensaje del cliente");
    }

    
    public String getJsonFiles() {
        return JsonFiles;
    }

    public void setJsonFiles(String jsonFiles) {
        this.JsonFiles = jsonFiles;
    }
    
    public static void main(String[] args) throws IOException {
        javaServer listener = new javaServer();
        listener.ConnectionListener();
    
    }

    public String streamProcessing(BufferedReader in) throws IOException {
        String incomingInfo = "";
        try {
            StringBuilder sb = new StringBuilder();
            String line = this.in.readLine();
            while (line != null) {
                sb.append(line);
                sb.append(System.lineSeparator());
                line = this.in.readLine();
            }
            incomingInfo = sb.toString();
        } catch (IOException e) {
            e.printStackTrace();
        }finally{
            in.close();
        }
        return incomingInfo;

    }

}