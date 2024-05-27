package com.lloyds.data.job.configuration.dto;


public enum Predicate {	
	
	IN("in"), AND("and"), OR("or"), BETWEEN("between"),
	NOT_EQUAL_TO("<>") ,LESS_THAN("<") ,GREATER_THAN(">"),
	GREATER_THAN_EQ(">="),LESS_THAN_EQ("<="),LIKE("like") ,EXISTS("exists"),IS_NULL("is null");

	Predicate(String predicate){
	    this.predicate=predicate;
	  }

	private String predicate;

	public String getPredicate() {
		return predicate;
	}

	public void setPredicate(String predicate) {
		this.predicate = predicate;
	}

	 

}
