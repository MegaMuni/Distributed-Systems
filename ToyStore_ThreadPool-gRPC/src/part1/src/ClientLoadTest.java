import java.io.BufferedReader;
import java.io.InputStreamReader;
import java.io.PrintStream;
import java.net.Socket;
import java.lang.Math;
import java.io.FileWriter;

public class ClientLoadTest {
	
	public static String hostname;
	public class ClientThread extends Thread{
		
		public float average_accuracy;
		public String method;
		private int client_num;
		
		public ClientThread(String method,int client_num) {
			this.average_accuracy = 0;
			this.method = method;
			this.client_num = client_num;
		}
		
		public void run() {
			long sum = 0;
			int max = 100;
			
			for(int i=0;i<max;i++) {
				try {
					Socket socket = new Socket(hostname, 9714);
					
					PrintStream out = new PrintStream( socket.getOutputStream() );
					BufferedReader in = new BufferedReader( new InputStreamReader( socket.getInputStream() ) );
					int rand1 = (int)Math.round( Math.random());
					int rand2 = (int)Math.round( Math.random());
					String msgLine = "";
					
					if(this.method!=null) {
						msgLine+=this.method;
					}
					else if(rand1==0) {
						msgLine+="Query";
					}
					else {
						msgLine+="Buy";
					}
					
					if(rand2==0) {
						msgLine+=" Tux";
					}
					else {
						msgLine+=" Whale";
					}
					System.out.println(msgLine);
					
					long start = System.currentTimeMillis();
		            out.println(msgLine);
		            String line = in.readLine();
		            long end = System.currentTimeMillis();
		            System.out.println( line );
		            System.out.println( "Client "+this.client_num +" - Latency for request " + i +" : "+(end-start) );
		            sum += (end-start);
					in.close();
					out.close();
					socket.close();
				} catch(Exception e) {
					e.printStackTrace();
				}
			}
			this.average_accuracy = (float)sum/max;
		}
	}
	
	public static void main(String[] args) {
		
		try {
		
			String hostname="";
			ClientLoadTest massLoader = new ClientLoadTest();
		
		
			String method = null;
			int numClients = -1;
			
			
			// Reading the arguments from the command line
			
			if(args.length>0) {	
				if(args[0].contains(".")) {
					hostname = args[0];
				} else {
					System.out.println("Please pass a valid host name in your command line");
					return;
				}
			} else {
				System.out.println("Please pass host name in your command line");
				return;
			}
			
			ClientLoadTest.hostname = hostname;
			
			if(args.length>1) {	
				try {
					numClients = Integer.parseInt(args[1]);
				} catch(Exception e){
					method = args[1];
				}	
			}
			if(args.length>2) {
				try {
					numClients = Integer.parseInt(args[2]);
				} catch(Exception e){
					method = args[2];
				}
			}
			
			//If the user gives numClients then run the code only for that number of clients
			
			if(numClients!=-1) {
				
				float latency = massLoader.runMultipleClients(numClients,method);
				System.out.println("Request latency when "+numClients+" client(s) are run simultaneously: "+latency);
				return; 
			}
		
			float[] compound_latency = new float[5];
			for (int num_clients=1;num_clients<6;num_clients++) {
					System.out.println("Number of clients that run simultaneously - "+num_clients+ " No of requests per each client : 100");
					compound_latency[num_clients-1]=massLoader.runMultipleClients(num_clients,method);
				
					System.out.println("-------------------------------------------------------");
			}
		
			System.out.println("Request latency when 1 client is run : "+compound_latency[0]);
			for(int i=2;i<6;i++) {
				System.out.println("Request latency when "+i+" clients are run simultaneously: "+compound_latency[i-1]);
			}
			
			//Writing the latencies to my json files based on the requests type
			
			FileWriter myObj=null;
			if(method == null) {
				method = "RandomMethodCalls";
				myObj = new FileWriter("jsonRandomMethodCalls.json");
			}
			
			if("buy".equalsIgnoreCase(method)) {
				method="BuyMethodCalls";
				myObj = new FileWriter("jsonBuyMethodCalls.json");
			}
			
			if("query".equalsIgnoreCase(method)) {
				method="QueryMethodCalls";
				myObj = new FileWriter("jsonQueryMethodCalls.json");
			}
			
			String loadJason = "{\n"
					+ "   \""+method+"\":"
					+ "      {\n"
					+ "         \"1\": \""+String.valueOf(compound_latency[0])+"\",\n"
					+ "         \"2\": \""+String.valueOf(compound_latency[1])+"\",\n"
					+ "         \"3\": \""+String.valueOf(compound_latency[2])+"\",\n"
					+ "         \"4\": \""+String.valueOf(compound_latency[3])+"\",\n"
					+ "         \"5\": \""+String.valueOf(compound_latency[4])+"\"\n"
					+ "      }\n"
					+"   \n"
					+ "}";
			
			myObj.write(loadJason);
			myObj.close();
			
			
		} catch(Exception e) {
			e.printStackTrace();
		}
	}
	
	public float runMultipleClients(int num_clients, String method) {
		
		ClientThread[] myClientThreads = new ClientThread[num_clients];
		for(int i=0; i<num_clients;i++) {
			myClientThreads[i] = new ClientThread(method,i+1);
			myClientThreads[i].start();
		}
		
		for(int i=0;i<num_clients;i++) {
			try {
				myClientThreads[i].join();
			}catch(Exception e) {
				e.printStackTrace();
			}
		}
		
		float latency = 0;
		
		for(int i=0;i< num_clients;i++) {
			latency+=myClientThreads[i].average_accuracy;
		}
		
		latency/=(float)num_clients;
		
		return latency;
	}
}
