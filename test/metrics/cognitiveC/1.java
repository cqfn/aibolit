import java.util.ArrayList;
import java.util.List;

public class Hospital {

	public static List<Instance> readDataGet(String file) throws FileNotFoundException {
		List<Instance> dataset = new ArrayList<Instance>();
		Scanner scanner = null;
		try {
			scanner = new Scanner(new File(file));
			while(scanner.hasNextLine()) {
				String line = scanner.nextLine();
				if (line.startsWith("#")) {
					continue;
				}
				String[] columns = line.split("\\s+");

				// skip first column and last column is the label
				int i = 1;
				int[] data = new int[columns.length-2];
				for (i=1; i<columns.length-1; i++) {
					data[i-1] = Integer.parseInt(columns[i]);
				}
				int label = Integer.parseInt(columns[i]);
				Instance instance = new Instance(label, data);
				dataset.add(instance);
			}
		} finally {
			if (scanner != null)
				scanner.close();
		}
		return dataset;
	}
		
}