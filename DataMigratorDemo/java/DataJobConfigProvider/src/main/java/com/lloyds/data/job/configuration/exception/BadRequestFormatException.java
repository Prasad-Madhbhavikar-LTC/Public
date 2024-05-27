package com.lloyds.data.job.configuration.exception;

public class BadRequestFormatException extends Exception {

	/**
	 * 
	 */
	private static final long serialVersionUID = 1L;
	
	public BadRequestFormatException(String errorMessage) {
        super(errorMessage);
    }

}
