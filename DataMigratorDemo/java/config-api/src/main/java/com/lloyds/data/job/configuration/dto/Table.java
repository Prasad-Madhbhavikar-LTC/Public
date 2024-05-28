package com.lloyds.data.job.configuration.dto;

import java.util.List;

import lombok.Data;

@Data
public class Table {

	private String name;
	private List<Column> columns;

}
