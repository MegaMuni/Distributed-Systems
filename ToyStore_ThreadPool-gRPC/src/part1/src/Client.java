import java.net.Socket;

import java.io.BufferedReader;
import java.io.InputStreamReader;
import java.io.PrintStream;

public class Client {
	public static void main(String[] args) {
		try {
			
			System.out.println("Enter ip address/hostname of the server: ");
			BufferedReader reader = new BufferedReader(
					new InputStreamReader(System.in));
			String hostname = reader.readLine().toString();
			Socket socket = new Socket(hostname, 9714);
			
			PrintStream out = new PrintStream( socket.getOutputStream() );
			BufferedReader in = new BufferedReader( new InputStreamReader( socket.getInputStream() ) );
			
			System.out.println("Enter the message to server: ");
            	
            String msgLine = reader.readLine();
            out.println( msgLine );
            String line = in.readLine();
            System.out.println( line );
            
			in.close();
			out.close();
			socket.close();
		} catch(Exception e) {
			e.printStackTrace();
		}
	}
}
