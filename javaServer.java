import java.io.*;
import java.net.*; 

public class Server{
    public static void main(String[] args) {
        int port = 6666;
        ServerSocket serverSocket = new ServerSocket(port);
        while(true){
            System.out.println("Waiting a connection in port " +port + "\n");
            Socket clientSocket = serverSocket.accept();
            InputStream request = clientSocket.getInputStream();
            DataInputStream in = new DataInputStream(request);
            String message = new String(in.readAllBytes());
            System.out.println("Message received: " + message);
        }
    }
}