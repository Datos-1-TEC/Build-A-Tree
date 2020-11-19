package JavaServer;

import java.io.IOException;
import java.io.InputStreamReader;
import java.io.OutputStreamWriter;
import java.net.ServerSocket;
import java.net.Socket;

public class gameServer {

    static int port = 2018;
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

            char[] charsMessage = new char[1024];

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
                else if(recibido.contains("exit")){
                    server.close();
                    isOpen = false;
                    recibido = "";
                    
                }
            

                charsMessage = new char[1024];
            }
        } catch (Exception e) {
            e.printStackTrace();
        }

    }

    private void sendMessage(String enviado) throws IOException {
        this.enviado = "S:" + enviado;
        out.write(this.enviado.toCharArray());
        out.flush();
    }

    public static void main(String[] args) throws IOException {
        gameServer server = new gameServer();
        server.listen();

    }
}