
import java.util.ArrayList;
import java.util.Iterator;


public class PancakeHouseMenu {
	ArrayList <String> menuItems;
	
	public PancakeHouseMenu() {
		menuItems = new ArrayList<String>();
		
		addItem("K&B's Pancake Breakfast");
		addItem("Regular Pancake Breakfast");
		addItem("Blueberry Pancakes");
		addItem("Waffles");
	}
	
	public void addItem(String name) {
		menuItems.add(name);
	}
	
	public ArrayList<String> getMenuItems() {
		return menuItems;
	}
	
	public Iterator<String> createIterator() {
		return menuItems.iterator();
	}
	
	public String toString() {
		return "Pnacake House Menu";
	}
}
