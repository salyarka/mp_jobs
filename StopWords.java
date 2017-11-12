import org.apache.hadoop.filecache.DistributedCache;
import org.apache.hadoop.io.IntWritable;
import org.apache.hadoop.io.Text;
import org.apache.hadoop.conf.Configuration;
import org.apache.hadoop.mapreduce.Job;
import org.apache.hadoop.mapreduce.lib.input.FileInputFormat;
import org.apache.hadoop.mapreduce.lib.input.TextInputFormat;
import org.apache.hadoop.mapreduce.lib.output.FileOutputFormat;
import org.apache.hadoop.mapreduce.lib.output.TextOutputFormat;
import org.apache.hadoop.fs.Path;

import java.io.IOException;

public class StopWords {
    public static void main(String[] args)
            throws IOException, ClassNotFoundException, InterruptedException{
        if (args.length != 3) {
            System.out.println("Need 3 arguments (inputDir, outputDir, fileName)");
            System.exit(-1);
        }

        Configuration config = new Configuration();
        config.set("stopWords", args[2]);

        Job job = new Job(config, "stopWords");
        job.setJarByClass(StopWords.class);

        FileInputFormat.addInputPath(job, new Path(args[0]));
        FileOutputFormat.setOutputPath(job, new Path(args[1]));

        job.setInputFormatClass(TextInputFormat.class);
        job.setOutputFormatClass(TextOutputFormat.class);

        DistributedCache.addCacheFile(new Path(args[2]).toUri(), job.getConfiguration());

        job.setOutputKeyClass(Text.class);
        job.setOutputValueClass(Text.class);

        job.setMapperClass(StopWordsMapper.class);
        job.setReducerClass(StopWordsReducer.class);

        job.setMapOutputKeyClass(Text.class);
        job.setMapOutputValueClass(IntWritable.class);

        job.waitForCompletion(true);

    }
}
