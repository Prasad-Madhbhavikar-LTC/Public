package com.lloyds.data.job.configuration.exception;

import java.io.IOException;
import java.time.LocalDateTime;

import org.springframework.http.HttpStatus;
import org.springframework.web.bind.annotation.ControllerAdvice;
import org.springframework.web.bind.annotation.ExceptionHandler;
import org.springframework.web.bind.annotation.ResponseBody;
import org.springframework.web.bind.annotation.ResponseStatus;
import org.springframework.web.servlet.mvc.method.annotation.ResponseEntityExceptionHandler;

import com.lloyds.data.job.configuration.dto.ErrorDto;

@ControllerAdvice
public class DataConfigControllerAdvice extends ResponseEntityExceptionHandler {

	@ExceptionHandler(IOException.class)
	@ResponseStatus((HttpStatus.INTERNAL_SERVER_ERROR))
	public @ResponseBody ErrorDto handleException(IOException ex) {
		return buildErrorDto(ex, HttpStatus.INTERNAL_SERVER_ERROR);

	}

	@ExceptionHandler(NullPointerException.class)
	@ResponseStatus(HttpStatus.BAD_REQUEST)
	public @ResponseBody ErrorDto handleNullPointerException(NullPointerException ex) {
		return buildErrorDto(ex, HttpStatus.BAD_REQUEST);
	}

	@ExceptionHandler(BadRequestFormatException.class)
	@ResponseStatus(HttpStatus.BAD_REQUEST)
	public @ResponseBody ErrorDto handleFileUnSupportedException(BadRequestFormatException ex) {
		return buildErrorDto(ex, HttpStatus.BAD_REQUEST);
	}

	private ErrorDto buildErrorDto(Exception ex, HttpStatus status) {
		ErrorDto errorDto = new ErrorDto();
		errorDto.setTimeStamp(LocalDateTime.now());
		errorDto.setStatus(status.value());
		errorDto.setError(status.getReasonPhrase());
		errorDto.setErrorMessage(ex.getMessage());
		return errorDto;

	}

}
