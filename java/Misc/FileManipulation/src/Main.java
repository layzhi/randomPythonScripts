import java.io.IOException;
import java.nio.file.Files;
import java.nio.file.Path;
import java.nio.file.Paths;
import java.nio.file.StandardCopyOption;

public class Main {
	
	public static void main(String[] args) throws IOException {
		
		Path source = Paths.get("files/test.txt");
		System.out.println(source.getFileName());
		
		Path target = Paths.get("files/newfile.txt");
		Files.copy(source, target, StandardCopyOption.REPLACE_EXISTING);
		
		Path targetToDelete = Paths.get("files/toDelete.txt");
		Files.copy(source, targetToDelete, StandardCopyOption.REPLACE_EXISTING);
		
		Path toDelete = Paths.get("files/toDelete.txt");
		Files.delete(toDelete);
		
		Path newdir = Paths.get("files/newdir");
		Files.createDirectory(newdir);
		
		Files.move(source, newdir.resolve(source.getFileName()), StandardCopyOption.REPLACE_EXISTING);
	}
}
