package JavaServer;

import java.io.DataInputStream;
import java.io.DataOutputStream;
import java.io.IOException;
import java.net.Socket;

public class ConnectionHandler {
    private Socket socket;
    private boolean flag = true;
    private DataOutputStream out;
    private DataInputStream in;
    private javaServer listener;

    public ConnectionHandler(Socket socket, javaServer listener) throws IOException {
        this.socket = socket;
        this.listener = listener;
        this.in = new DataInputStream(this.socket.getInputStream());
        this.out = new DataOutputStream(this.socket.getOutputStream());
        
        Thread thread = new Thread(() -> {
            while(flag) {
                try {
                    String message = in.readUTF();
                    this.listener.processMessage(message);
                } catch (IOException e){
                    e.printStackTrace();
                }
            }
        });
        thread.start();       
        
    }
    public void sendMessage(String JsonFiles)  {

        try{
            out.writeUTF(JsonFiles);
            out.flush();
        }catch (IOException e){
            e.printStackTrace();
        }

    }
}
