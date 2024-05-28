package com.lloyds.data.job.configuration;

import org.springframework.boot.context.properties.ConfigurationProperties;
import org.springframework.stereotype.Component;

import lombok.Data;

@Data
@Component
@ConfigurationProperties(prefix = "data.config")
public class ConfigProperties {

	private String path;

	private String fileExtension;

	private String accessDataSuffix;
	
	private String destinationInfoSuffix;
	
	private String destinationSupportedFileFormats;
	
	private String jobConfigInfoSuffix;
	
	private String sourceSupportedFileFormats;
	
	private String gcsbucket;

}
