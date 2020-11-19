package JavaServer;

import java.io.BufferedReader;
import java.io.DataInputStream;
import java.io.DataOutputStream;
import java.io.IOException;
import java.io.InputStreamReader;
import java.net.Socket;

public class ConnectionHandler {
    private Socket socket;
    private boolean flag = true;
    private DataOutputStream out;
    private BufferedReader in;
    private javaServer listener;

    public ConnectionHandler(Socket socket, javaServer listener) throws IOException {
        this.socket = socket;
        this.listener = listener;
        this.in = new BufferedReader(new InputStreamReader(socket.getInputStream()));
        this.out = new DataOutputStream(this.socket.getOutputStream());
        
        Thread thread = new Thread(() -> {
            while(flag) {
                try {
                    String message = streamProcessing(this.in);
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
