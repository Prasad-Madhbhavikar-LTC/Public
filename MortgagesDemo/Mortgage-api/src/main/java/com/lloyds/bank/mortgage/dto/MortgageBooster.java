package com.lloyds.bank.mortgage.dto;

import com.fasterxml.jackson.annotation.JsonProperty;
import lombok.Data;

@Data
public class MortgageBooster extends MortgageCustomer {
    @JsonProperty("property_value")
    private Long boosterPropertyValue;
}
