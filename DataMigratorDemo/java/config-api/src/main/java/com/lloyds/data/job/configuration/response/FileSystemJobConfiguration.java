package com.lloyds.data.job.configuration.response;

import java.util.List;

import com.lloyds.data.job.configuration.dto.CSVColumn;

import lombok.Data;

@Data
public class FileSystemJobConfiguration  {
	
	private List<CSVColumn> columns;

}
