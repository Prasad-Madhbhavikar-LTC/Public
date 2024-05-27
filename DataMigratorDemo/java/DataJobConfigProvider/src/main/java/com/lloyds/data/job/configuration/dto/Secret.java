package com.lloyds.data.job.configuration.dto;

import lombok.Data;

@Data
public class Secret {	
	
	
	private String vault_url;	

	private String access_key;
	
	private String secret_key;

	}
