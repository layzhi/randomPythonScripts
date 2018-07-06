import junit.framework.Test;
import junit.framework.TestCase;
import junit.framework.TestSuite;

public class AppTest extends TestCase{
	
	/**
	 *  Create the test case
	 *  @params testName name of the test case
	 */
	public AppTest (String testName) {
		super(testName);
	}
	
	/**
	 * @return the suite of tests being tested
	 */
	public static Test suite() {
		return new TestSuite(AppTest.class);
	}
	
	/**
	 * Rigourous test
	 */
	public void testApp() {
		assertTrue(true);
	}
}
