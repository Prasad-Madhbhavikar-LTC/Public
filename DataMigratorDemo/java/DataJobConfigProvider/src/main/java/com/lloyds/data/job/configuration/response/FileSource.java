package com.lloyds.data.job.configuration.response;

import java.util.List;

import lombok.Data;

@Data
public class FileSource extends Source {
	
	private String path;
	private String file_Type;
	private List<FileSystemJobConfiguration> job_Configurations;


	

	

}
