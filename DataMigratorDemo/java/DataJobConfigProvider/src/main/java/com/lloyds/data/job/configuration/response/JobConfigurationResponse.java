package com.lloyds.data.job.configuration.response;

import lombok.Data;

@Data
public class JobConfigurationResponse {
	
	private String jobName;
	private String jobDesc;
	private Source source;
}
