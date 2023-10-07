import java.util.HashMap;
import java.io.ObjectInputStream;
import java.io.ObjectOutputStream;
import java.net.Socket;
import java.io.BufferedReader;
import java.io.InputStreamReader;
import java.io.PrintStream;
import java.io.PrintWriter;
import java.util.concurrent.Semaphore;
import java.util.Arrays;

public class MyThread extends Thread{

	public static Semaphore semdata_tux = new Semaphore(1);
	public static Semaphore semdata_whale = new Semaphore(1);
	public static Server server;
	public static Semaphore sem_q; 
	
	
	public void run() {
		try {
			while(1==1) {
				System.out.println("I am waiting to aquire Socket queue");				
				server.sem.acquire();
				server.sem_q.acquire();
				System.out.println("I am waiting to aquire a thread");	
				Socket socket = server.q.poll();
				server.sem_q.release();
				processRequest(socket);
				//semt.release();
				System.out.println("I released the thread");
			}
		} catch(Exception e) {
			
		}
	}
	
	public void processRequest(Socket socket) {
		try {
			System.out.println("Inside Thread: "+ this.getName());
			
			BufferedReader in = new BufferedReader( new InputStreamReader( socket.getInputStream() ) );
            PrintWriter out = new PrintWriter( socket.getOutputStream() );
            
            String line = in.readLine();
            line  = line.strip();
            String[] query = line.split(" ", 2);
            if(query.length!=2 || (!"Buy".equalsIgnoreCase(query[0]) && !"Query".equalsIgnoreCase(query[0]))) {
            	out.println("Invalid message entered");
            	out.flush();
            	in.close();
                out.close();
                socket.close();
                return;
            }
            if("Tux".equalsIgnoreCase(query[1])){
            	
            	System.out.println("I am waiting to aquire tux");
            	semdata_tux.acquire();
            	if(server.data.get("Tux")[0]>0) {
            		if("Buy".equalsIgnoreCase(query[0])) {
            			server.data.get("Tux")[0]--;
            		}
            		out.println("Number of items left: "+server.data.get("Tux")[0]+" Cost of the item: "+server.data.get("Tux")[1]);
            	}
            	else {
            		out.println("Stock over: "+0);
            	}
            	semdata_tux.release();
            	System.out.println("I released tux");
            } else if("Whale".equalsIgnoreCase(query[1])){
            	System.out.println("I am waiting to aquire whale");
            	semdata_whale.acquire();
            	if(server.data.get("Whale")[0]>0) {
            		if("Buy".equalsIgnoreCase(query[0])) {
            			server.data.get("Whale")[0]--;
            		}
            		out.println("Number of items left: "+server.data.get("Whale")[0]+" Cost of the item: "+server.data.get("Whale")[1]);
            	}
            	else {
            		out.println("Stock over: 0");
            	}
            	semdata_whale.release();
            	System.out.println("I released whale");
            } else {
            	out.println("Item not found: -1");
            }
            out.flush();
            	
            
            in.close();
            out.close();
            socket.close();
            System.out.println("Outside thread");
		}
		catch(Exception e) {
			
		}
	}
}
