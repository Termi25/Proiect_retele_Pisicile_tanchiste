import java.io.DataInputStream;
import java.io.DataOutputStream;
import java.io.IOException;
import java.net.*;

public class TCPServer {
    public static void main(String[] args) throws IOException {
        ServerSocket serverSocket = new ServerSocket(5001);
        System.out.println("Listening for clients at "+
                serverSocket.getInetAddress().toString()+':'
                +serverSocket.getLocalPort());
        while (true){
            Socket socketClient = serverSocket.accept();
            String clientSocketIP = socketClient.getInetAddress().toString();
            int clientSocketPort = socketClient.getPort();
            System.out.println("[IP: "+clientSocketIP+" ,Port: "+clientSocketPort);

            DataInputStream dataIn=new DataInputStream(
                    socketClient.getInputStream());
            DataOutputStream dataOut=new DataOutputStream(
                    socketClient.getOutputStream());

            String clientMessage =dataIn.readUTF();
            System.out.println(clientMessage);
            String serverMessage = "Hi this is coming from the server!";
            dataOut.writeUTF(serverMessage);
            dataIn.close();
            dataOut.close();
//            serverSocket.close();
            socketClient.close();
        }
    }
}
