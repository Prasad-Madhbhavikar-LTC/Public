package com.lloyds.data.job.configuration.dto;

import java.util.List;

import lombok.Data;

@Data
public class Column {
	
	private String  name;
	private String  type;
	private String  value_range;
	private List<Predicate>  predicates;
	private List<Join>  joins;

}
