package com.lloyds.data.job.configuration.response;

import java.util.List;

import lombok.Data;

@Data
public class KafkaSource extends Source {
	
	private String source_url;
	private String topic_name;
	private String topic_type;
	
	private List<FileSystemJobConfiguration> job_Configurations;


}
