import java.io.DataInputStream;
import java.io.DataOutputStream;
import java.io.IOException;
import java.net.InetSocketAddress;
import java.net.ServerSocket;
import java.net.Socket;
import java.util.HashMap;
import java.util.Map;
import java.util.Scanner;

public class ClientServer {
    private Map<Integer,Socket> listaConexiuni;
    private int port;
    private ServerSocket serverSocket;
    private boolean isRunning;
    public ClientServer(int port)throws IOException {
        this.listaConexiuni = new HashMap<>();
        this.port=port;
        this.serverSocket=new ServerSocket(port);
        this.isRunning=true;
    }

    public void startServerClient()throws IOException{
        Thread threadServer= new Thread(() -> {
            System.out.println("Listening for clients at "+
                    serverSocket.getInetAddress().toString()+':'
                    +serverSocket.getLocalPort());
            while (isRunning){
                Scanner keyboard = new Scanner(System.in);
                System.out.println("Do you wish to close the server (Yes/No) ?");
                String optiuneInchidereServer = keyboard.nextLine();
                if(optiuneInchidereServer.equalsIgnoreCase("yes")){
                    isRunning=false;
                    break;
                }
                try{
                    Socket socketClient = serverSocket.accept();
                    listaConexiuni.put(socketClient.getPort(),socketClient);

                    for (Socket socket:listaConexiuni.values()){
                        System.out.println("| IP: "+socket.getInetAddress().toString()+" ,Port: "
                                +socket+" |");
                    }


                    DataInputStream dataIn=new DataInputStream(
                            socketClient.getInputStream());
                    DataOutputStream dataOut=new DataOutputStream(
                            socketClient.getOutputStream());

                    String clientMessage =dataIn.readUTF();
                    System.out.println(clientMessage);
                    String serverMessage = "Hi, this is coming from the server!";
                    dataOut.writeUTF(serverMessage);
                    dataIn.close();
                    dataOut.close();
//                    serverSocket.close();
//                    socketClient.close();
                }catch (Exception e){
                    e.printStackTrace();
                }
            }
        });
        threadServer.start();
    }

    public void connectToAnotherServer(int port) throws IOException {
        Thread threadClient=new Thread(()->{
            try{
                while (true){
                    Socket socket=new Socket();
                    socket.connect(new InetSocketAddress("127.0.0.1",port),1000);
                    System.out.println("Connection succesful");

                    DataInputStream dataIn=new DataInputStream(socket.getInputStream());
                    DataOutputStream dataOut=new DataOutputStream(socket.getOutputStream());

                    dataOut.writeUTF("Hello, this is coming from the client!");
                    System.out.println(dataIn.readUTF());

                }
            }catch (Exception e){
                e.printStackTrace();
            }
        });
        threadClient.start();
    }
}
