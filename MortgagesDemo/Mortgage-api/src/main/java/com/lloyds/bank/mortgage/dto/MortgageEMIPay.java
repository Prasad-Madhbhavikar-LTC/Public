package com.lloyds.bank.mortgage.dto;

import lombok.Data;

@Data
public class MortgageEMIPay {
    private Long principalAmount;
    private float interestRate;
    private int terms;
    private Boolean isTermsInMonths = false;
}
