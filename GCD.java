public class GCD{
	public static void main(String[] args) {
		System.out.println(GCD(255,285));
	}
	public static int GCD(int a,int b){
		int r =a%b;
		if(r==0){
			return b;
		}
		return GCD(b,r);
	}
}