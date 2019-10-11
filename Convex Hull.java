import java.util.*;
import java.io.*;
import java.lang.*;

public class Challenge2ChenAD18_19{
	private static int timesLeft=1;
	private static float[] times=new float[timesLeft];
	public static void main(String[] args) throws FileNotFoundException{
		if(timesLeft--==0){
			getAverage();
			return;
		}
		long t =System.currentTimeMillis();
		ArrayList<Point> points= new ArrayList<>();
		Deque<Point> pointDeque=new LinkedList<>();
		String inputFileName=args[0];
		File inputFile=new File(inputFileName);
		Scanner inputStream = new Scanner(inputFile);
		while(inputStream.hasNextLine()==true){
			String line = inputStream.nextLine();
			String[] items=line.split(",");
			double x=Double.parseDouble(items[0]);
			double y=Double.parseDouble(items[1]);
			Point newPoint =new Point(x,y);
			points.add(newPoint);
		}
		//for easier sorting by angle, we change the startpoint to the point with lowest y value
		Point theStartPoint=points.get(0);
		Point theEndPoint=points.get(1);
		sortByAngle(points);
		int dequelength = getLegalPoints(pointDeque,points);
		ArrayList<Point> counterclockwise= counterclockwiseApproach(theEndPoint,pointDeque);
		ArrayList<Point> clockwise=clockwiseApproach(theEndPoint,pointDeque);
		double distance1= calculateRoute(counterclockwise);
		double distance2= calculateRoute(clockwise);
		if(distance1<distance2){
			printPoints(counterclockwise,distance1);
		}else{
			printPoints(clockwise,distance2);
		}
		long end =System.currentTimeMillis();
		times[timesLeft]=(end-t)/1000f;
		main(args);
	}

	/**
	 * Sort the Arraylist by the angle of each point
	 */
	public static void sortByAngle(ArrayList<Point> points){
		//set the angle for all the points in the arraylist
		Point startpoint = points.get(0);
		for(int i=1;i<points.size();i++){
			Point current = points.get(i);
			current.setAngle(points.get(0));
			current.setDistance(points.get(0));
		}
		points.remove(0);
		Collections.sort(points);
		points.add(0,startpoint);
	}
	/**
	 * Check if 3 consecutive points are going counter-clockwise way
	 * @param  a current point
	 * @param  b next point
	 * @param  c next next point
	 * @return   boolean whether they goes counter-clockwisely.
	 * This took me 30 minutes!!!
	 */
	public static boolean isCounterClockwise(Point a,Point b,Point c){
		double val = (c.x-b.x)*(b.y-a.y)-(b.x-a.x)*(c.y-b.y);
		return (val<0)?true:false;
	}
	/**
	 * Push all the points that are legal into the Deque
	 * @return the length of the deque
	 */
	public static int getLegalPoints(Deque<Point> pointDeque, ArrayList<Point> points){
		//the first two points must be legal
		int counter=2;
		pointDeque.addLast(points.get(0));
		pointDeque.addLast(points.get(1));
		pointDeque.addLast(points.get(2));
		for(int i=3;i<points.size();i++){
			counter++;
			while(!isCounterClockwise(secondLast(pointDeque),pointDeque.peekLast(),points.get(i))){
				pointDeque.removeLast();
				counter--;
			}
			pointDeque.addLast(points.get(i));
		}
		return counter;
	}

	public static boolean containsStartEnd(Deque pointDeque, Point theStartPoint,Point theEndPoint){
		return pointDeque.contains(theStartPoint)&&pointDeque.contains(theEndPoint);
	}
	/**
	 * the CounterClockwise way to approach to the theEndPoint
	 * @param  theEndPoint theEndPoint
	 * @return an arraylist of points surpassed
	 */
	public static ArrayList<Point> counterclockwiseApproach(Point theEndPoint, Deque<Point> pointDeque){
		ArrayList result = new ArrayList<Point>();
		Point start=pointDeque.peekFirst();
		while(!pointDeque.peekFirst().equals(theEndPoint)){
			result.add(pointDeque.pollFirst());
		}
		result.add(pointDeque.peekFirst());
		pointDeque.addLast(start);
		return result;
	}
	/**
	 * the Clockwise way to approach to the theEndPoint
	 * @param  theEndPoint theEndPoint
	 * @return an arraylist of points surpassed
	 */
	public static ArrayList<Point> clockwiseApproach(Point theEndPoint,Deque<Point> pointDeque){
		ArrayList result = new ArrayList<Point>();
		while(!pointDeque.peekLast().equals(theEndPoint)){
			result.add(pointDeque.pollLast());
		}
		result.add(pointDeque.peekLast());
		return result;
	}
	/**
	 * Claculate the distance of the route
	 * @param  route Arraylist of Points
	 * @return       total distance
	 */
	public static double calculateRoute(ArrayList<Point> route){
		int length=route.size();
		double result=0;
		for(int i=1;i<length;i++){
			Point curr = route.get(i);
			Point prev = route.get(i-1);
			result+= curr.getDistance(prev);
		}
		return result;
	}
	/**
	 * Method to get the second last element in deque
	 * @param  pointdeque [description]
	 * @return            [description]
	 */
	public static Point secondLast(Deque<Point> pointdeque){
		Point temp=pointdeque.removeLast();
		Point result = pointdeque.peekLast();
		pointdeque.addLast(temp);
		return result;
	}
	/**
	 * Method to print route to a csv file
	 * @param  arr
	 * @param  distance
	 * @throws FileNotFoundException
	 */
	public static void printPoints(ArrayList<Point> arr, double distance) throws FileNotFoundException{
		String outputFileName = "Challenge2ChenAD18_19.CSV";
		PrintWriter outputStream = new PrintWriter(outputFileName);
		outputStream.println("The shortest distance is " + distance);
		for(Point a: arr){
			outputStream.println(a);
		}
		outputStream.close();
	}
	/**
	 * Method to print runtime
	 */
	public static void getAverage(){
		float total=0;
		for(float e:times){
			total+=e;
		}
		System.out.println(total/times.length);
	}

}
/**
* Point class to store x,y value of points and several methods
*/
class Point implements Comparable<Point>{
	public double x;
	public double y;
	public double angle; //angle with the lowest point
	public double dist; //distance between two points
	public Point(double xin,double yin){
		x=xin;
		y=yin;
		angle=0;
	}
	/**
	 * Calculate and set the angle between the x-axis and the line
	 * @param  a the point with the lowest y value
	 */
	public void setAngle(Point a){
		double dx = this.x-a.x;
		double dy = this.y-a.y;
		double l = Math.sqrt(dx*dx+dy*dy);
		// if(dy<0){
		// 	dx=(-1)*Math.abs(dx);
		// }
		this.angle = Math.acos(dy/l);
	}
	/**
	 * Set the distance between two points
	 * @param  a lowest y value
	 */
	public void setDistance(Point a){
		this.dist=getDistance(a);
	}

	/**
	 * get the distance between two points
	 * @param  a the other point
	 * @return   the distance
	 */
	public double getDistance(Point a){
		double dx=this.x-a.x;
		double dy=this.y-a.y;
		return Math.sqrt(dx*dx+dy*dy);
	}
	/**
	 * Check if this point come before the other point in the sorted Arraylist
	 * @param  a The point to compare
	 * @return   if it comes before Point A, return true
	 */
	public int compareTo(Point a){
		if(a.angle<this.angle){
			return -1;
		}
		if(a.x==this.x&&a.y==this.y){
			return 0;
		}
		else{
			return 1;
		}
	}
	/**
	 * check if two Points are the same point
	 * @param  a the other point
	 * @return   true if they are the same
	 */
	public boolean equals(Point a){
		return (this.x==a.x&&this.y==a.y);
	}

	public String toString(){
		return +this.x+","+this.y;
	}
}
