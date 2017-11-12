import org.apache.hadoop.io.IntWritable;
import org.apache.hadoop.io.Text;
import org.apache.hadoop.mapreduce.Reducer;

import java.io.IOException;

public class StopWordsReducer
        extends Reducer<Text, IntWritable, Text, IntWritable> {

    public void reduce(Text key, Iterable<IntWritable> values, Context con)
            throws IOException, InterruptedException{

        int sum = 0;
        for(IntWritable value: values){
            sum += value.get();
        }
        con.write(key, new IntWritable(sum));
    }
}