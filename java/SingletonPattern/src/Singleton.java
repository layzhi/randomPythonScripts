
public class Singleton {
	
//	private static Singleton uniqueInstance = new Singleton();
//	
//	private Singleton() {}
//	
//	public static Singleton getInstance() {
//		return uniqueInstance;
//	}
	
	//thread safe
	private static Singleton uniqueInstance;
	
	private Singleton() {}
	
	public static synchronized Singleton getInstance() {
		if(uniqueInstance == null) {
			uniqueInstance = new Singleton();
		}
		return uniqueInstance;
	}
	
	// other useful methods 
	public String getDescription() {
		return "I'm a classic Singleton!";
	}
}
