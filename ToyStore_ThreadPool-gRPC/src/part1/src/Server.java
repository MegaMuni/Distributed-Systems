import java.lang.Thread;
import java.util.LinkedList;
import java.util.Queue;
import java.util.concurrent.locks.ReentrantLock;
import java.io.IOException;
import java.io.ObjectInputStream;
import java.io.ObjectOutputStream;
import java.lang.ClassNotFoundException;
import java.net.ServerSocket;
import java.net.Socket;
import java.util.HashMap;
import java.util.concurrent.Semaphore;
import java.util.ArrayList;

public class Server{
	public HashMap<String,Float[]> data;
	public Queue<Socket> q;
	public Semaphore sem;
	public Semaphore sem_q;
	public int max_threads = 5;
	public static void main(String[] args) {
		int port = 9714;
		ServerSocket serverSocket;
		Server server = new Server();
		HashMap data = new HashMap<String,Float[]>();
		server.data = data;
		Float[] tux = new Float[] {(float) 1500.0,(float)10.99};
		Float[] whale = new Float[] {(float) 350.0,(float)25.99};
		data.put("Tux", tux);
		data.put("Whale", whale);
			
		server.q = new LinkedList<>();
		server.sem = new Semaphore(0);
		server.sem_q = new Semaphore(1);
		
		ThreadPool threadPool = new ThreadPool(server);
		
		
		try {
			
			serverSocket = new ServerSocket(port);	
			System.out.println("Created the server socket");
			
			//Initiating my dispatched thread
			Thread dispatcher = new Thread(){
				public void run() {
					while(1==1) {
						try {
							Socket socket = serverSocket.accept();
							System.out.println("Waiting to acquire sem in dispatcher");
							server.sem_q.acquire();
							server.q.add(socket);
							server.sem.release();
							System.out.println("Released sem in dispatcher");
							server.sem_q.release();
							System.out.println("Released sem_q in dispatcher");
						} catch(Exception e) {
							System.out.println(e);
						}
					}
					
				}
			};
			
			dispatcher.start();
			
			//Initiates and starts the pool of threads
			threadPool.processRequest();
		} catch(Exception e) {
			
		}
	
	}
}