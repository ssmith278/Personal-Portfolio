import java.util.Arrays;
import java.util.concurrent.CountDownLatch;

public class Merger implements Runnable{

	private Thread thread;
	private String threadName;
	private double arrs[][];
	private double merged[];
	private CountDownLatch latch;
	
	public Merger(String name, double[][] arrs, CountDownLatch latch) {
		threadName = name;
		thread = new Thread(this, threadName);
		this.arrs = arrs;
		this.latch = latch;
	}
	
	public double[] getMergedArray(){
		return merged;
	}
	
	@Override
	public void run() {
		
		merged = merge(arrs);
		
		latch.countDown();
	}
	
	public static double[] merge(double slices[][]) {
		
		int n, t, p;
		t = slices.length;
		p = slices[0].length;
		n = t*p;
		
		double result[] = new double[n];
		int idx[] = new int[t];
		Arrays.fill(idx, 0);
		int totalIdx = 0;
		
		while(totalIdx < n)
	    {
	        int minSlice = -1;
	        
	        //Loop through slices
	        for(int i = 0; i < t; i++)
	        {
	            //Get slice idx for min element
	            if(idx[i] < p)
	            {
	                if(minSlice < 0) minSlice = i;
	                if(slices[i][idx[i]] < slices[minSlice][idx[minSlice]])
	                {
	                    minSlice = i;
	                }
	            }
	        }
	        // Add minimum element to new array
	        result[totalIdx] = slices[minSlice][idx[minSlice]];
	        idx[minSlice]++;
	        totalIdx++;       
	    }
		
		return result;
	}

	public void start() {
		thread.start();
	}

}
