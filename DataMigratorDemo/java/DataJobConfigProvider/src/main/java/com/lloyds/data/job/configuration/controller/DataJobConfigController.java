package com.lloyds.data.job.configuration.controller;

import java.io.File;
import java.io.IOException;

import org.slf4j.Logger;
import org.slf4j.LoggerFactory;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.core.io.Resource;
import org.springframework.core.io.ResourceLoader;
import org.springframework.http.HttpStatus;
import org.springframework.http.ResponseEntity;
import org.springframework.stereotype.Controller;
import org.springframework.web.bind.annotation.CrossOrigin;
import org.springframework.web.bind.annotation.PostMapping;
import org.springframework.web.bind.annotation.RequestBody;
import org.springframework.web.bind.annotation.RequestMapping;

import com.fasterxml.jackson.databind.ObjectMapper;
import com.fasterxml.jackson.dataformat.yaml.YAMLFactory;
import com.lloyds.data.job.configuration.ConfigProperties;
import com.lloyds.data.job.configuration.dto.AccessInfo;
import com.lloyds.data.job.configuration.dto.DestinationInfo;
import com.lloyds.data.job.configuration.dto.JobConfigurationInfo;
import com.lloyds.data.job.configuration.dto.SourceType;
import com.lloyds.data.job.configuration.exception.BadRequestFormatException;
import com.lloyds.data.job.configuration.helper.DataConfigHelper;
import com.lloyds.data.job.configuration.response.FileSource;
import com.lloyds.data.job.configuration.response.DataBaseSource;
import com.lloyds.data.job.configuration.response.JobConfigurationResponse;
import com.lloyds.data.job.configuration.response.KafkaSource;

@Controller
@RequestMapping("datajobconfig")
@CrossOrigin("http://localhost:4200")
public class DataJobConfigController {

	@Autowired
	private ConfigProperties configProperties;

	@Autowired
	ResourceLoader resourceLoader;

	@Autowired
	DataConfigHelper dataConfigHelper;

	private static Logger logger = LoggerFactory.getLogger(DataJobConfigController.class);

	@PostMapping("v1/api/accessdata")
	public ResponseEntity<?> postJobConfigurationAccessData(@RequestBody AccessInfo accessInfo) throws IOException {

		String jobName = accessInfo.getJobName();
		dataConfigHelper.validateJobName(jobName);
		dataConfigHelper.validateAccessInfo(accessInfo);

		String fileName = dataConfigHelper.getFileName(jobName, configProperties.getAccessDataSuffix());
		String path = configProperties.getPath();
		logger.info("fileName " + fileName);

		Resource resource = resourceLoader.getResource("file:" + path + fileName);

		if (!resource.exists()) {
			ObjectMapper objectMapper = new ObjectMapper(new YAMLFactory());
			objectMapper.writeValue(new File(path + fileName), accessInfo);
			return ResponseEntity.status(HttpStatus.CREATED)
					.body(" Created access data job file " + fileName + " in the Location " + path);

		} else {
			return ResponseEntity.status(HttpStatus.FOUND)
					.body(fileName + " file  already exist in the given Location " + path);
		}

	}

	@PostMapping("v1/api/jobconfigurations")
	public ResponseEntity<?> postJobConfigurationInfo(@RequestBody JobConfigurationInfo jobConfigInfo)
			throws IOException, BadRequestFormatException {

		String jobName = jobConfigInfo.getJobName();
		dataConfigHelper.validateJobName(jobName);

		String fileName = dataConfigHelper.getFileName(jobName, configProperties.getJobConfigInfoSuffix());
		String path = configProperties.getPath();
		logger.info("fileName " + fileName);

		Resource resource = resourceLoader.getResource("file:" + path + fileName);

		if (!resource.exists()) {
			JobConfigurationResponse response = buildJobConfigurationResponse(jobConfigInfo);
			ObjectMapper objectMapper = new ObjectMapper(new YAMLFactory());
			objectMapper.writeValue(new File(path + fileName), response);
			return ResponseEntity.status(HttpStatus.CREATED)
					.body(" Created job configuration file " + fileName + " in the Location " + path);

		} else {
			return ResponseEntity.status(HttpStatus.FOUND)
					.body(fileName + " file  already exist in the given Location " + path);
		}

	}

	@PostMapping("v1/api/destinationDetail")
	public ResponseEntity<?> postDestinationDetails(@RequestBody DestinationInfo destinationInfo)
			throws IOException, BadRequestFormatException {

		String jobName = destinationInfo.getJobName();

		dataConfigHelper.validateJobName(jobName);
		dataConfigHelper.validateBucket(destinationInfo.getDestination().getBucket());
		dataConfigHelper.validateFileFormats(destinationInfo.getDestination().getFormat(),
				configProperties.getDestinationSupportedFileFormats());

		String fileName = dataConfigHelper.getFileName(jobName, configProperties.getDestinationInfoSuffix());
		String path = configProperties.getPath();
		logger.info("fileName " + fileName);

		Resource resource = resourceLoader.getResource("file:" + path + fileName);

		if (!resource.exists()) {
			ObjectMapper objectMapper = new ObjectMapper(new YAMLFactory());
			objectMapper.writeValue(new File(path + fileName), destinationInfo);
			return ResponseEntity.status(HttpStatus.CREATED)
					.body(" Created destination details job file " + fileName + " in the Location " + path);

		} else {
			return ResponseEntity.status(HttpStatus.FOUND)
					.body(fileName + " file  already exist in the given Location " + path);
		}

	}

	private JobConfigurationResponse buildJobConfigurationResponse(JobConfigurationInfo jobConfigInfo)
			throws BadRequestFormatException {

		SourceType sourceType = jobConfigInfo.getSource_type();
		JobConfigurationResponse response = new JobConfigurationResponse();
		response.setJobName(jobConfigInfo.getJobName());
		response.setJobDesc(jobConfigInfo.getJobDescription());

		if (sourceType.equals(SourceType.FILE_SYSTEM)) {
			dataConfigHelper.validatePathAndFileType(jobConfigInfo.getPath(), jobConfigInfo.getFile_type());
			// System.out.println("size-->"+jobConfigInfo.getCsvJobConfigurations().size());
			FileSource source = new FileSource();
			source.setSource_type(jobConfigInfo.getSource_type());
			source.setPath(jobConfigInfo.getPath());
			source.setFile_Type(jobConfigInfo.getFile_type());
			source.setJob_Configurations(jobConfigInfo.getJobConfigurations());
			response.setSource(source);
		}
		if (sourceType.equals(SourceType.DATABASE)) {
			dataConfigHelper.validateSchemaAndSourceUrl(jobConfigInfo.getSchema(), jobConfigInfo.getSource_url());
			// System.out.println("size-->"+jobConfigInfo.getDataBaseJobConfigurations().size());
			DataBaseSource databaseResource = new DataBaseSource();
			databaseResource.setSource_type(jobConfigInfo.getSource_type());
			databaseResource.setSource_url(jobConfigInfo.getSource_url());
			databaseResource.setSchema_keyspace(jobConfigInfo.getSchema());
			databaseResource.setJob_Configurations(jobConfigInfo.getDataBaseJobConfigurations());
			response.setSource(databaseResource);
		}

		if (sourceType.equals(SourceType.KAFKA_STREAM)) {
			dataConfigHelper.validateKafkaSource(jobConfigInfo.getSource_url(), jobConfigInfo.getTopicName(),
					jobConfigInfo.getTopicType());
			// System.out.println("size-->"+jobConfigInfo.getDataBaseJobConfigurations().size());
			KafkaSource resource = new KafkaSource();
			resource.setSource_type(jobConfigInfo.getSource_type());
			resource.setSource_url(jobConfigInfo.getSource_url());
			resource.setTopic_name(jobConfigInfo.getTopicName());
			resource.setTopic_type(jobConfigInfo.getTopicType());
			resource.setJob_Configurations(jobConfigInfo.getJobConfigurations());
			response.setSource(resource);
		}

		return response;

	}

}
