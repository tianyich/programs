public class OneEditAway{
	public static void main(String[] args) {
		System.out.println(checkWord("cookie","cookie"));
	}
	public static boolean checkWord(String s1,String s2,int index){
		if(Math.abs(s1.length()-s2.length())>1){
			return false;
		}
		if(((s1.length()==0&&s2.length()==1)||(s1.length()==1&&s2.length()==0))){
			return true;
		}
		if(s1.equals(s2)){
			return true;
		}
		if(s1.charAt(s1.length()-1)==s2.charAt(s2.length()-1)){
			return checkWord(s1.substring(0,s1.length()-1),s2.substring(0,s2.length()-1));
		}
		else{
			return s1.substring(0,s1.length()-1).equals(s2)||
			s2.substring(0,s2.length()-1).equals(s1)||
			s1.substring(0,s1.length()-1).equals(s2.substring(0,s2.length()-1));
		}
	}
}

