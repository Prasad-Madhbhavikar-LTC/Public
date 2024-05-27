// package com.lbg.integrator.api;

import java.io.File;
import java.io.IOException;
import java.nio.file.*;
import java.util.Arrays;
import java.util.Objects;

public class JobWatcher {

    private static WatchKey key;

    public static void main(String[] args) throws IOException, InterruptedException {
        WatchService service = FileSystems.getDefault().newWatchService();
        Path path = Paths.get(args[0]);
        path.register(service, StandardWatchEventKinds.ENTRY_CREATE, StandardWatchEventKinds.ENTRY_MODIFY);

        while ((key = service.take()) != null) {
            System.out.println("Event is generated");
            for (WatchEvent<?> event : key.pollEvents()) {
                System.out.println("Event type: " + event.kind() + " FileName: " + event.context());
                if (event.kind().equals(StandardWatchEventKinds.ENTRY_CREATE)) {
                    if (event.context().toString().contains("_destination_details")) {
                        String jobName = event.context().toString().split("_destination_details")[0];
                        File f = path.toFile(); // Use path.toFile() instead of new File(path.toUri())
                        if (Arrays.stream(Objects.requireNonNull(f.listFiles())).filter(single -> single.toString().startsWith(jobName)).count() == 3) {
                            try {
                                ProcessBuilder pb = new ProcessBuilder(args[1], args[2], jobName);
                                pb.start(); // Handle any IOException here
                            } catch (IOException e) {
                                e.printStackTrace();
                            }
                        }
                    }
                }
            }
        }
    }
}
