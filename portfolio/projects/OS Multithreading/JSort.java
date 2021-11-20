import java.util.Arrays;
import java.util.Random;
import java.util.concurrent.CountDownLatch;

public class JSort {

	public static final int MIN = 1;
	public static final int MAX = 1000;
	public static final boolean DEBUG = false;
	
	public static void main(String[] args) {
		
		int n, t, p;
		n = Integer.parseInt(args[0]);
		t = Integer.parseInt(args[1]);
		p = n/t;
		double arr[] = getUnsortedArray(n);
		CountDownLatch latch = new CountDownLatch(t);
		
		if(DEBUG)
		{
			System.out.println("\nUnsorted Array: \n");
			printArray(arr, 5);
			System.out.println("\nEnd Unsorted Array.");
		}
		
		long start = System.currentTimeMillis();
		//Split array
		double slices[][] = new double[t][n];
		for(int i = 0; i < slices.length; i++)
		{
			slices[i] = Arrays.copyOfRange(arr, i*p, i*p+p);
			Sorter sorter = new Sorter("S Thread" + i, slices[i], latch);
			sorter.start();
		}
		
		try {
			latch.await();
		} catch (InterruptedException e1) {
			e1.printStackTrace();
		}
		
		if(DEBUG)
		{
			System.out.println("\nSlices: ");
			Arrays.stream(slices).forEach( val -> {printArray(val, 5); });
			System.out.println("\nEnd Slices.");
		}
		
		double mergedArr[];
		latch = new CountDownLatch(1);
		Merger merger = new Merger("M Thread", slices, latch);
		merger.start();
		
		try {
			latch.await();
		} catch (InterruptedException e) {
			e.printStackTrace();
		}
		
		mergedArr = merger.getMergedArray();
		
		if(DEBUG)
		{
			System.out.println("\nMerged: ");
			printArray(mergedArr, 5);
			System.out.print("\nEnd Merged");
		}
		
		long end = System.currentTimeMillis();
		
		System.out.println("Execution time for args " + n +"," + t + ": " + ((double)(end-start)) + " ms");
	}

	public static double[] getUnsortedArray(int n) {
		
		Random rand = new Random();
		double result[] = new double[n];
		
		for(int i = 0; i < n; i++) {
			result[i] = (double) Math.round(rand.nextDouble() * (MAX - MIN) + MIN);
		}
		
		return result;
	}
	
	public static void printArray(double[] arr, int limit) {
		
		System.out.print("\n[");
		for (int i = 0; i < arr.length; i++) {

	        System.out.print(arr[i]);
	        
	        String joiner = i == arr.length-1 ? "]\n" : (i+1) % limit == 0 ? ",\n" : ", ";
	        System.out.print(joiner);
		    
		}
	}

}
