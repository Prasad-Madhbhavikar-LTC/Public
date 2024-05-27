package com.lloyds.data.job.configuration.dto;

import java.time.LocalDateTime;

import lombok.Data;

@Data
public class ErrorDto {

	private LocalDateTime timeStamp;
	private int status;
	private String error;
	private String errorMessage;
	

}
