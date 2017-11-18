import org.apache.hadoop.filecache.DistributedCache;
import org.apache.hadoop.io.IntWritable;
import org.apache.hadoop.io.LongWritable;
import org.apache.hadoop.io.Text;
import org.apache.hadoop.mapreduce.Mapper;
import org.apache.hadoop.fs.Path;

import java.io.IOException;
import java.io.BufferedReader;
import java.io.FileReader;
import java.util.Arrays;
import java.util.HashSet;

public class StopWordsMapper
        extends Mapper<LongWritable, Text, Text, IntWritable> {
    private HashSet<String> stopWords = new HashSet<>();
    private Text outputKeyStop = new Text("stop");
    private Text outputKeyTotal = new Text("total");
    private IntWritable weight = new IntWritable(1);

    public StopWordsMapper(){}

    @Override
    public void setup(Context context) throws IOException {
        try {
            Path[] stopWordsFiles = DistributedCache.getLocalCacheFiles(
                    context.getConfiguration());
            if (stopWordsFiles != null && stopWordsFiles.length > 0) {
                for (Path stopWordFile : stopWordsFiles) {
                    readStopWordFile(stopWordFile);
                }
            }
        } catch (IOException e) {
            System.err.println("Exception reading stop word file: " + e);
        }
    }

    private void readStopWordFile(Path stopWordFile) {
        try {
            BufferedReader fis = new BufferedReader(new FileReader(
                    stopWordFile.toString()));
            String stopWord = null;
            while ((stopWord = fis.readLine()) != null) {
                String[] words = stopWord.split(",");
                stopWords.addAll(Arrays.asList(words));
            }
        } catch (IOException ioe) {
            System.err.println("Exception while reading stop word file '"
                    + stopWordFile + "' : " + ioe.toString());
        }
    }

    public void map(LongWritable key, Text value, Context con)
            throws IOException, InterruptedException {

        String line = value.toString();
        String[] words = line.split("\\W*\\s+\\W*");

        for(String word: words ){
            System.out.println(line);
            System.out.println(word);
            if (stopWords.contains(word)) {
                con.write(outputKeyStop, weight);
            }
            con.write(outputKeyTotal, weight);
        }
    }
}

