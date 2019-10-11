public class Challenge3ChenAD18_19{
    public static void main(String[] args) {
        //test case
        String s = "";
        String e = encode(s);
        System.out.println(e);
    }

    public static String encode(String s){
        int n = s.length();
        //create a 2-d memo to store all the substring
        String[][] memo = new String[n][n];
        for(int x =0;x<n;x++){
            for(int i = 0; i+x<n;i++){
                //somehow in this way of iteration it doesn't throw NullPointerException
                int j = i+x;
                String subString = s.substring(i,j+1);
                memo[i][j] = subString;
                //cut the string in half and compress
                for(int k =i; k<j;k++){
                    if(memo[i][k].length()+memo[k+1][j].length()<memo[i][j].length()){
                        memo[i][j] = memo[i][k] + memo[k+1][j];
                    }
                }
                //compress each subString
                for(int l =i; l<j;l++){
                    String repeat = s.substring(i,l+1);
                    //those are hard code to find repitition 
                    if(subString.length()%repeat.length() == 0){
                        if(subString.replaceAll(repeat,"").length()==0){
                            String encodedString = subString.length()/repeat.length()+"("+memo[i][l]+")";
                            if(encodedString.length() < memo[i][j].length()){
                                memo[i][j] = encodedString;
                            }
                        }
                    }
                }
            }
        }
        return memo[0][n-1];
    }
}