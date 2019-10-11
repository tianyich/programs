import java.util.*;
import java.lang.*;
import java.io.*;
public class Challenge1ChenAD18_19{
	private static int timesLeft=1;
	private static float[] times=new float[timesLeft];
	public static void main(String[] args) throws FileNotFoundException{
		if(timesLeft--==0){
			getAverage();
			return;
		}
		long t =System.currentTimeMillis();
		String inputFileName="BirthdatesYears84_86RawData.CSV";
		File inputFile=new File(inputFileName);
		Scanner inputStream = new Scanner(inputFile);
		inputStream.nextLine();
		HashMap<Integer,Integer> frequency =new HashMap<Integer,Integer>();
		while(inputStream.hasNextLine()){
			//read next line
			String line =inputStream.nextLine();
			//split line by ","
			String[] items=line.split(",");
			//combine month and day together
			int month=Integer.parseInt(items[0]);
			int day=Integer.parseInt(items[1]);
			int date=month*100+day;
			if(frequency.containsKey(date)){
				Integer count = frequency.get(date);
				frequency.put(date,count+1);
			}else{
				frequency.put(date,1);
			}
		}
		inputStream.close();
		//put dates in a hashmap to count the frequency of each date
		List<Integer> freq =new ArrayList<Integer>(frequency.values());
		Collections.sort(freq);
		Collections.reverse(freq);
		//create a reversed hashmap of frequency in order to use the sorted frequency to check the date
		HashMap<Integer,Integer> reversedFrequency =new HashMap<Integer,Integer>();
		for(Integer k:frequency.keySet()){
			reversedFrequency.put(frequency.get(k),k);
		}
		String outputFileName = "Challenge1ChenAD18_19.CSV";
		PrintWriter outputStream = new PrintWriter(outputFileName);
		outputStream.println("Month,Day,Frequency");
		for(int i=0;i<reversedFrequency.size();i++){
			int outputDate=reversedFrequency.get(freq.get(i));
			int outputMonth=outputDate/100;
			int outputDay=outputDate%100;
			outputStream.println(outputMonth+","+outputDay+","+freq.get(i));
		}
		outputStream.close();
		long end =System.currentTimeMillis();
		times[timesLeft]=(end-t)/1000f;
		main(args);
	}

	public static void getAverage(){
		float total=0;
		for(float e:times){
			total+=e;
		}
		System.out.println(total/times.length);
	}

}