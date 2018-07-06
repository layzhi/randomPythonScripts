
import java.io.IOException;
import java.nio.file.Files;
import java.nio.file.LinkOption;
import java.nio.file.Path;
import java.nio.file.Paths;
import java.util.ArrayList;

public class Main {
	
	public static void main(String[] args) throws IOException {
		
		Path fileDir = Paths.get("file/nestedFile");
		
		FileFinder finder = new FileFinder("test.txt");
		Files.walkFileTree(fileDir, finder);
		
		ArrayList<Path> foundFiles = finder.foundPaths;
		
		if(foundFiles.size() > 0) {
			for (Path path : foundFiles) {
				System.out.println(path.toRealPath(LinkOption.NOFOLLOW_LINKS));
			}
		} else {
			System.out.println("No files were found!");
		}
	}
}
