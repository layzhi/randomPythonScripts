import java.net.*;
import java.io.*;

public class Main {
    
	private static final String DATA_URL = "http://services.hanselandpetal.com/feeds/flowers.json";
    
    public static void main(String[] args) throws IOException {
    	
    	URL test = new URL(DATA_URL);
    	URLConnection yc = test.openConnection();
    	BufferedReader in = new BufferedReader(new InputStreamReader(yc.getInputStream()));
    	
    	String inputLine;
    	
    	while((inputLine = in.readLine()) != null) {
    		System.out.println(inputLine);
    	}
    	in.close();
     }
}