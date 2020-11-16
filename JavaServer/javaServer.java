package JavaServer;
import java.io.*;
import java.net.*; 

public class javaServer{
    private Boolean flag = true;
    private DataInputStream in;
    private DataOutputStream out;
    private ConnectionHandler handler; 
    private int port = 6666;
    private String JsonFiles;

    public void ConnectionListener(){
        
        Thread thread = new Thread(()-> {
            try {
                ServerSocket incoming = new ServerSocket(this.port);
                System.out.println("listening connections on: " + incoming.getLocalPort());
                while (flag){
                    Socket socket = incoming.accept();
                    processConnection(socket);

                }
            } catch (IOException e) {
                e.printStackTrace();
            }
        });
        thread.start();
    }

    public void processConnection(Socket socket) throws IOException {
        in = new DataInputStream(socket.getInputStream());
        String incomingInfo = in.readUTF();
        System.out.println("Invitado ha ingresado: "+ incomingInfo);

        //Codigo que genera las condiciones para responderle al cliente
        handler = new ConnectionHandler(socket, this);
        handler.sendMessage(this.JsonFiles);
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

}