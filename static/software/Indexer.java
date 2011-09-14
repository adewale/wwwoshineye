/*
@author Adewale Oshineye
Use a hashmap to store the number of times each word in a file occurs
Done properly this should easily be able to do word-counts and even a 
sorted list of all the words in the document
Usage: java Indexer nameOfFileToBeIndexed

*/
import java.util.*;
import java.io.*;
public class Indexer {
	public static void main(String args[]) throws Exception {
		if (args.length != 1) {
			System.out.println("Usage: java Indexer nameOfFileToBeIndexed");
			System.exit(0);
		}
		
		
		//open the file
		FileReader fr = new FileReader(args[0]);
		BufferedReader br = new BufferedReader(fr);
		StreamTokenizer strTok = new StreamTokenizer(br);
		strTok.eolIsSignificant(false);//treat EOL as just another delimiter
		strTok.lowerCaseMode(false);//be case sensitive
		strTok.slashSlashComments(false);//ignore C-style comments
		strTok.slashStarComments(false);//ignore C++-style comments
		
		//instantiate the HashMap
		//keys are Strings and values are Integers
		Map map = new HashMap();
		
		//begin file reading loop
		//read a token
		//ignore it if it's null
		//check if it already exists as a key
		//if it's an existing key, get its value and increment it
		//otherwise create the new key and set its value to 1
		//end of file file reading loop
		
		while (StreamTokenizer.TT_EOF != strTok.nextToken()) {
			if (strTok.sval == null) {
			//we dont' want a key to be created for null as it can't be cast later
			//instead we do nothing
			}
			else if (map.containsKey(strTok.sval)) {
				Integer temp =(Integer) map.get(strTok.sval);
				Integer tempPlusOne = new Integer(temp.intValue() + 1);
				map.put(strTok.sval, tempPlusOne);
			}
			else {
				map.put(strTok.sval, new Integer(1));			
			}
		}
		
		/*
		THIS WAS AN ALTERNATIVE APPROACH CREATED BECAUSE I DIDN'T KNOW THAT ARRAYS CAN'T BE
		CAST IF THEY CONTAIN NULLS. THIS IS BECAUSE NULLS CAN'T BE CAST.
		//get the list of keys
		ArrayList arr = new ArrayList(map.keySet());
		
		//work from the alphabetical beginning to the end of the list of keys and
		//print out their values
		Iterator list = arr.iterator();
		while (list.hasNext()) {
			Object item = list.next();
			System.out.println(item + "::" + map.get(item));
		}*/
		
		//get the set of keys
		Set theSet = map.keySet();
		
		//convert the set to a string array
		String[] keys = (String[]) theSet.toArray(new String[0]);
		
		//sort the array
		Arrays.sort(keys);
		
		//print the key value pairs in alphabetical order
		for (int i=0;i<keys.length;i++) {
			System.out.println("Key:" + keys[i] + ":: " +map.get(keys[i]));
		}
		
		//print out that word count as the number of keys
		System.out.println("The number of words is:: " + keys.length);
	}
}
		
		
		