import java.io.File;
import java.io.FileNotFoundException;
import java.util.*;
public class DegreesOfSeparationChen{
    /**
     * Main Method
     * @param  args
     * @throws FileNotFoundException
     */
    public static void main(String[] args) throws FileNotFoundException{
        ArrayList<Country> countries = createCountries();
        int[] a = getStartEnd(countries);
        int[] prev = BFS(a[0], countries);
        ArrayList<Integer> path = printPath(prev,a[1]);
        path.add(0,a[0]);
        for(int i = 0; i< path.size();i++){
            System.out.print(countries.get(path.get(i))+", ");
        }
        System.out.println();
        System.out.println("Distance is: "+ (path.size()-1));
    }

    /**
     * SetUp countries and their adjcent countries
     * @return an ArrayList of countries
     * @throws FileNotFoundException
     */
    public static ArrayList<Country> createCountries() throws FileNotFoundException{
        //put all the country in an arrayList
        ArrayList<Country> countries = new ArrayList<Country>();
        File folder = new File("./Maps");
        File[] fileName = folder.listFiles();
        for(File file: fileName){
            String fn = file.getName();
            if(fn.equals(".DS_Store")){
                continue;
            }
            //remove the .csv extension name
            Country currCountry = new Country(fn.substring(0,fn.length()-4));
            countries.add(currCountry);
        }

        //A more efficient way than use ArrayList.indexOf()
        HashMap<String,Integer> index = new HashMap<String,Integer>();

        for(int i = 0; i<countries.size();i++){
            index.put(countries.get(i).getName(), i);
        }
        //Put the index of adjcent countries in the ArrayList
        for(Country x: countries){
            if(x.getName().equals(".DS_S")){
                break;
            }
            String nameOfFile = "./Maps/" + x.getName() +".csv";
            File inputfile = new File(nameOfFile);
            Scanner input = new Scanner(inputfile);
            while(input.hasNextLine()){
                String countryName = input.nextLine();
                int countryIndex = index.get(countryName);
                x.adj.add(countryIndex);
            }
            input.close();
        }
        return countries;
    }

    /**
     * Use console to get start and end country from the user
     * @param  countries Arraylist of all countries
     * @return           an array which the first item is the start index
     *                   and the second is the end index
     */
    public static int[] getStartEnd(ArrayList<Country> countries){
        int[] startEnd = new int[2];
        System.out.println("Please Enter Start Country:");
        String start = System.console().readLine();
        System.out.println("Please Enter End Country:");
        String end = System.console().readLine();
        boolean findStart = false;
        boolean findEnd = false;
        //Deal with problem when start and end is the same
        if(start.equals(end)){
            System.out.println("You are already here!");
            try{
                Thread.sleep(2000);
            }catch (InterruptedException e) {
                Thread.currentThread().interrupt();
              }
            System.exit(0);
        }
        //find index for start and end
        for(int i = 0; i < countries.size();i++){
            String name = countries.get(i).getName();
            if(name.equals(start)){
                findStart = true;
                startEnd[0] = i;
            }
            if(name.equals(end)){
                findEnd = true;
                startEnd[1] = i;
            }
        }
        //Deal with problem when input is not a country on the list
        if(!findStart||!findEnd){
            System.out.println("You cannot go to that country!");
            try{
                Thread.sleep(2000);
            }catch (InterruptedException e) {
                Thread.currentThread().interrupt();
              }
            System.exit(0);
        }
        return startEnd;
    }

    /**
     * Implement of Breadth First Search
     * @param  start     The start index
     * @param  countries Arraylist of countries
     * @return           A array tells what country is before each country
     */
    public static int[] BFS(int start, ArrayList<Country> countries){
        Queue<Integer> queue = new LinkedList<Integer>();
        queue.add(start);
        boolean[] visited = new boolean[countries.size()];
        Arrays.fill(visited, false);
        visited[start] = true;
        int[] prev = new int[countries.size()];
        Arrays.fill(prev,-1);
        while(!queue.isEmpty()){
            int countryIndex = queue.poll();
            for(int i: countries.get(countryIndex).adj){
                if(!visited[i]){
                    visited[i] = true;
                    prev[i] = countryIndex;
                    queue.add(i);
                }
            }
        }
        return prev;
    }

    /**
     * Get the Path
     * @param  prev The array tells what's before each country
     * @param  end  The destiny's index
     * @return      An Arraylist of the path
     */
    public static ArrayList<Integer> printPath(int[] prev, int end){
        ArrayList<Integer> result = new ArrayList<Integer>();
        int currentV = end;
        while(prev[currentV] != -1){
            result.add(0,currentV);
            currentV = prev[currentV];
        }
        return result;
    }
}
class Country{
    String name;
    ArrayList<Integer> adj = new ArrayList<Integer>(0);
    /**
     * Constructor
     * @param nameInput Name of the country
     */
    public Country(String nameInput){
        this.name = nameInput;
    }
    /**
     * Get the name of the country
     * @return name of the country
     */
    public String getName(){
        return this.name;
    }
    /**
     * Easily print countries
     * @return name of the country
     */
    public String toString(){
        return this.name;
    }
}
