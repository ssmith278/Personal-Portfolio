import java.util.concurrent.CountDownLatch;

public class Sorter implements Runnable{

	private Thread thread;
	private String threadName;
	double arr[];
	private CountDownLatch latch;
	
	public Sorter(String name, double[] arr, CountDownLatch latch) {
		threadName = name;
		thread = new Thread(this, threadName);
		this.arr = arr;
		this.latch = latch;
	}
	@Override
	public void run() {
		
		sort(arr);
		latch.countDown();
	}
	
	public static void sort(double[] arr) {
		
		//Sort arr
	    int i, j;
	    double k;
	    for(i = 1; i < arr.length; i++)
	    {
	        k = arr[i];
	        j = i-1;

	        while(j >= 0 && arr[j] > k)
	        {
	            arr[j+1] = arr[j];
	            j = j-1;
	        }
	        arr[j+1] = k;
	    }
	}
	
	public void start() {
		thread.start();
	}

}
