package com.lloyds.data.job.configuration.helper;

import java.util.Arrays;
import java.util.List;
import java.util.stream.Stream;

import org.slf4j.Logger;
import org.slf4j.LoggerFactory;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.stereotype.Component;

import com.lloyds.data.job.configuration.ConfigProperties;
import com.lloyds.data.job.configuration.dto.Secret;
import com.lloyds.data.job.configuration.dto.SourceType;
import com.lloyds.data.job.configuration.dto.AccessInfo;
import com.lloyds.data.job.configuration.exception.BadRequestFormatException;

@Component
public class DataConfigHelper {

	@Autowired
	private ConfigProperties configProperties;
	private static Logger logger = LoggerFactory.getLogger(DataConfigHelper.class);

	public String getFileName(String jobName, String suffix) {
		return jobName + "_" + suffix + configProperties.getFileExtension();
	}

	public void validateBucket(String bucket) throws BadRequestFormatException {
		if (bucket == null || bucket.isEmpty()) {
			throw new NullPointerException("bucket must have value");
		} else if (bucket.length() > 4 && !bucket.substring(0, 4).equals("GCP:")) {
			throw new BadRequestFormatException("bucket name must start with 'GCP:'");
		} else if (bucket.length() <= 4) {
			throw new BadRequestFormatException("bucket name must have valid value");
		}

	}

	public void validateFileFormats(String format, String supportedFileFormats) throws BadRequestFormatException {
		if (format == null || format.isEmpty()) {
			throw new NullPointerException("format must have value");
		}

		boolean contains = Stream.of(supportedFileFormats.split(",")).anyMatch(s -> s.equals(format));

		logger.info("supported formats are: " + supportedFileFormats);
		if (!contains) {
			throw new BadRequestFormatException("Unsupported file format " + format);
		}

	}

	public void validateAccessInfo(AccessInfo accessInfo) {

		Secret secret = accessInfo.getConfiguration().getSecret();
		if (secret.getVault_url() == null || secret.getVault_url().isEmpty()) {
			throw new NullPointerException("vault_url must have value");
		}

		if (secret.getAccess_key() == null || secret.getAccess_key().isEmpty()) {
			throw new NullPointerException("access key must have value");
		}

	}

	public void validateJobName(String jobName) {
		if (jobName == null || jobName.isEmpty()) {
			throw new NullPointerException("jobName must have value");
		}

	}

	public void validatePathAndFileType(String path, String file_type) throws BadRequestFormatException {

		if (path == null || path.isEmpty()) {
			throw new NullPointerException("path must have value");
		}

		if (file_type == null || file_type.isEmpty()) {
			throw new NullPointerException("file_type must have value");
		} else {
			validateFileFormats(file_type, configProperties.getSourceSupportedFileFormats());

		}

	}

	public void validateSchemaAndSourceUrl(String schema, String source_url) {
		if (schema == null || schema.isEmpty()) {
			throw new NullPointerException("schema must have value");
		}

		if (source_url == null || source_url.isEmpty()) {
			throw new NullPointerException("source_url must have value");
		}
	}

	

	public void validateKafkaSource(String source_url, String topicName, String topicType) {
		if (source_url == null || source_url.isEmpty()) {
			throw new NullPointerException("source_url must have value");
		}

		if (topicName == null || topicName.isEmpty()) {
			throw new NullPointerException("topicName must have value");
		}

		if (topicType == null || topicType.isEmpty()) {
			throw new NullPointerException("topicType must have value");
		}
	}

}
