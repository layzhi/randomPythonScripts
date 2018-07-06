
public class MyThread extends Thread {
	
	@Override
	public void run() {
		
		int iterations = 5;
		
		try {
			for (int i = 0; i < iterations; i++) {
				System.out.println("From Secondary Thread");
				sleep(3000);
			}
		} catch (InterruptedException e) {
			System.err.println(e);
		}
	}
}
