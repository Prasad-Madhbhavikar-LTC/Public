package com.lloyds.bank.mortgage.dto;

import com.fasterxml.jackson.annotation.JsonProperty;
import lombok.Data;

@Data
public class TakeHomePay {
    @JsonProperty("gross_income")
    private Long annualIncome;
    @JsonProperty("employment_type")
    private String employmentType;
    @JsonProperty("pension_contribution_percentage")
    private Float pensionContributionPercentage;
    @JsonProperty("pension_contribution_amount")
    private Long pensionContributionAmount;
    @JsonProperty("student_loan_monthly_payment")
    private Integer studentLoanMonthlyPayment;
}
