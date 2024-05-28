package com.lloyds.data.job.configuration.response;

import java.util.List;

import com.lloyds.data.job.configuration.dto.Table;

import lombok.Data;

@Data
public class DataBaseJobConfigurations {
	
	 private List<Table> tables;

}
