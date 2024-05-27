package com.lloyds.data.job.configuration.response;

import java.util.List;

import lombok.Data;

@Data
public class DataBaseSource extends Source {
	
	private String source_url;
	private String schema_keyspace;	
	
	private List<DataBaseJobConfigurations> job_Configurations;


}

