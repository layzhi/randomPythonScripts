package pondPreillePartOne;

import java.io.BufferedReader;
import java.io.File;
import java.io.FileReader;
import java.io.IOException;
import java.text.DateFormat;
import java.text.SimpleDateFormat;
import java.util.ArrayList;
import java.util.Date;

public class Trend {
	
	ArrayList<WeatherEntry> collectedData = new ArrayList<>();
	
	public void readData(String fileName) {
		
		DateFormat format = new SimpleDateFormat("yyy_MM_dd HH:mm:ss");
		try {
			BufferedReader buf = new BufferedReader(new FileReader(fileName));
			String line = null;
			String[] wordsArray;
			boolean skipFirstLine = true;
			
			while(true) {
				line = buf.readLine();
				if (skipFirstLine) { // skip data header
					skipFirstLine = false;
					continue;
				}
				if(line == null) {
					break;
				} else {
					wordsArray = line.split("\t");
					WeatherEntry entry = new WeatherEntry();
					entry.pressure = Float.valueOf(wordsArray[2]);
					entry.humidity = Float.valueOf(wordsArray[4]);
					entry.when = format.parse(wordsArray[0]);
					collectedData.add(entry);
				}
//				buf.close();
			}
			buf.close();
		} catch (Exception e) {
			e.printStackTrace();
		}
	}
	
	public String doCalc(String from, String to) {
		
		DateFormat format = new SimpleDateFormat("yyyy/MM/dd HH:mm:ss");
		Date d1 = null;
		Date d2 = null;
		try {
			d1 = format.parse(from);
			d2 = format.parse(to);
		} catch (Exception e) {
			System.out.println(e);
		}
		String result = "From " + format.format(d1) + " to " + format.format(d2) + "\n";
		WeatherEntry y1 = null;
		WeatherEntry y2 = null;
		int idx = 0, x1 = 0, x2 = 0;
		
		for (WeatherEntry x : collectedData) {
			if((y1 == null) && x.when.compareTo(d1) >= 0) {
				y1 = x;
				x1 = idx;
			}
			if(x.when.compareTo(d2) >= 0) {
				x2 = idx;
				y2 = x;
				break;
			}
			idx++;
		}
		float slope = (y2.pressure - y1.pressure)/(x2 - x1);
		
		result = result + " The barometric pressure slope is " + String.format("%.6f", slope) + " \n the forecast is: ";
		
		if(slope < 0) {
			result = result + "inclement weather is closing in\n";
		} else if (slope > 0) {
			result = result + "conditions are improving";
		} else {
			result = result + "current conditions are likely to persist";
		}
		
		return result;
	}
	
	public static void main(String[] args) {
		Trend calcTrend = new Trend();
		System.out.println("Reading Data . . . ");
		calcTrend.readData("src/pondPreillePartOne/Environmental_Data_Deep_Moor_2012.txt");
		calcTrend.readData("src/pondPreillePartOne/Environmental_Data_Deep_Moor_2013.txt");
		calcTrend.readData("src/pondPreillePartOne/Environmental_Data_Deep_Moor_2014.txt");
		calcTrend.readData("src/pondPreillePartOne/Environmental_Data_Deep_Moor_2015.txt");
		System.out.println("Done!");
		System.out.println("Total number of weather data entries: " + calcTrend.collectedData.size());
		
		String from = "";
		String to = "";
		
		 System.out.println("Test Case #1:");	 
		 from = "2012/01/01 00:30:00";
		 to = "2012/01/01 02:30:00";		 
		 System.out.println( calcTrend.doCalc(from, to));
		 
		 System.out.println("Test Case #2: ");
		 from = "2013/03/15 10:30:00";
		 to = "2013/03/17 02:30:00";
		 System.out.println(calcTrend.doCalc(from, to));
				 
	}
	
}
