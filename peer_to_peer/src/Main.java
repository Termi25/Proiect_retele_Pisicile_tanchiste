public class Main {
    public static void main(String[] args) {

        try{
            ClientServer clientServer=new ClientServer(5001);
            clientServer.startServerClient();
            clientServer.connectToAnotherServer(5001);
            clientServer.connectToAnotherServer(5001);
        }catch (Exception e){
            e.printStackTrace();
        }
    }
}