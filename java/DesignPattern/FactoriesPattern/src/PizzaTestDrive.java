
public class PizzaTestDrive {
	
	public static void main(String[] args) {
		PizzaStore nyStore = new NYPizzaStore();
		PizzaStore chicagoStore = new ChicagoPizzaStore();
 
		Pizza pizza = nyStore.orderPizza("cheese");
		System.out.println("Ethan ordered a " + pizza.getName() + "\n");
		
		System.out.println(" - - - - - - - - - - - - - - - - ");
		
		pizza = chicagoStore.orderPizza("cheese");
		System.out.println("someone ordered a " + pizza.getName() + "\n");
		
	}
}
