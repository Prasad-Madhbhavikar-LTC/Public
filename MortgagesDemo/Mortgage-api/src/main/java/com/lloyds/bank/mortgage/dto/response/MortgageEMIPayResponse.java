package com.lloyds.bank.mortgage.dto.response;

import lombok.Builder;
import lombok.Data;

@Data
@Builder
public class MortgageEMIPayResponse {
    private Long monthlyPayment;
    private Long totalPaybackInTerms;
}
