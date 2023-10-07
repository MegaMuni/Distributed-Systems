import java.net.Socket;
import java.util.Queue;
import java.util.HashMap;
import java.util.ArrayList;
import java.util.concurrent.Semaphore;

public class ThreadPool extends MyThread {
	
	public MyThread[] myThreads;
	
	public ThreadPool(Server server) {
		MyThread.server = server;
		this.myThreads = new MyThread[server.max_threads];
	}
	
	public void processRequest() {
		System.out.println("In Process Request Pool");
		for(int i=0;i<server.max_threads;i++) {
			myThreads[i] = new MyThread();
			myThreads[i].start();
		}
	}
}
