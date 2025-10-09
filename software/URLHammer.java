import java.net.URL;
import java.net.HttpURLConnection;
import java.io.*;
import java.net.MalformedURLException;

/*
Usage:
java URLHammer connectionNumber url

Intention:
Open as many simultaneous connections to a particular URL as possible.
Crude stress-testing tool. Very crude.

Potential enhancements:
Read list of URLs from a text file then hit each one with n hammers.
Read list of URLs from a text file then hit each one with a random percentage of the specified hammers.
Neat tricks with hammer distribution and sequencing can be used to simulate hordes of users wandering through a site
and following links.

*/
/**
 * Hammer a particular URL with as many concurrent hits as possible.
 * The concurrency of the hits is not guaranteed. It depends on conditions
 * such as available memory, available cpu resources, maximum number of 
 * available connections on the client machine and the available bandwidth on the
 * path between the client and the server.
 *
 * @author Adewale Oshineye
 * @version 1.0
 */
public class URLHammer extends Thread {
	//deliberately invalid defaults
	static int connections = -1;
	static String target = "";
	private URL u = null;
	public static void main(String args[]) {
		//check for user input
		if (args.length < 2) {
			System.out.println("Usage:: java URLHammer connectionNumber url");
			System.exit(1);
		}

		//parse user input
		try {
			connections = Integer.parseInt(args[0]);
			target = args[1];
		} catch (Exception e) {
			//ignore all errors
			System.err.println("Error:: " + e.getMessage());
			e.printStackTrace();
			System.exit(1);
		}

		Thread[] hammers = new Thread[connections];
		for (int i=0; i < hammers.length; i++) {
			hammers[i] = new URLHammer(target);//polymorphism is your friend!

			//using an array prevents the threads being garbage 
			//collected, thus increasing the simultaneous load
			hammers[i].start();
		}
	}
	
	/**
	This constructor overrides and completely changes the meaning of:
	public Thread(String name)
	*/
	public URLHammer(String urlToHit) {
		try {
			u = new URL(urlToHit);
		} catch (MalformedURLException m) {
			System.err.println("Error:: " + m.getMessage());
			m.printStackTrace();
		}
	}

	public void run() {
		//read the file at the specified url
		try {
			BufferedReader bis = new BufferedReader
				(new InputStreamReader(u.openStream()));
			while(bis.readLine() != null) {
				//do nothing with the input
			}
			bis.close();
		} catch (Exception e) {
			//ignore all errors
			System.err.println("Error:: " + e.getMessage());
			e.printStackTrace();
		} 
	}
}