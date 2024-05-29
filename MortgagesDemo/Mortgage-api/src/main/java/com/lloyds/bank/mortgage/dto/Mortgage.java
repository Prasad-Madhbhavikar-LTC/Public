package com.lloyds.bank.mortgage.dto;

import com.fasterxml.jackson.annotation.JsonProperty;
import lombok.Data;

@Data
public class Mortgage {
    @JsonProperty("purpose")
    private String purpose;
    @JsonProperty("customer")
    private MortgageCustomer mortgageCustomer;
    @JsonProperty("property_price")
    private Long propertyPrice;
    @JsonProperty("booster")
    private MortgageBooster mortgageBooster;
    //For RE-MORTGAGE
    @JsonProperty("mortgage_balance")
    private Long mortgageBalance;
    @JsonProperty("additional_borrowing")
    private Long additionalBorrowing;
}
