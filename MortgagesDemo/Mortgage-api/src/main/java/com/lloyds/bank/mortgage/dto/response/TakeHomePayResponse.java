package com.lloyds.bank.mortgage.dto.response;

import com.fasterxml.jackson.annotation.JsonProperty;
import lombok.Data;

import java.io.Serializable;

@Data
public class TakeHomePayResponse implements Serializable {
    @JsonProperty("gross_annual_income")
    private Long grossAnnualIncome;
    @JsonProperty("annual_income")
    private Long annualIncome;
    @JsonProperty("monthly_pay")
    private Long monthlyPay;
    @JsonProperty("pension_deduction")
    private Long pensionDeduction;
    @JsonProperty("taxable_income")
    private Long taxableIncome;
    @JsonProperty("national_insurance")
    private Long nationalInsurance;
    @JsonProperty("student_loan")
    private Long studentLoan;
    @JsonProperty("mortgage_eligible_amount")
    private Long mortgageEligibleAmount;
}
