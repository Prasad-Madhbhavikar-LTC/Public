package com.lloyds.bank.mortgage.service;

import com.lloyds.bank.mortgage.dto.Mortgage;
import com.lloyds.bank.mortgage.dto.MortgageEMIPay;
import com.lloyds.bank.mortgage.dto.TakeHomePay;
import com.lloyds.bank.mortgage.dto.response.MortgageEMIPayResponse;
import com.lloyds.bank.mortgage.dto.response.MortgageResponseDto;
import com.lloyds.bank.mortgage.dto.response.TakeHomePayResponse;

public interface IMortgageCalculator {
    MortgageEMIPayResponse monthlyMortgagePayment(MortgageEMIPay mortgageDto);

    MortgageResponseDto calculateMortgage(Mortgage mortgage);

    MortgageResponseDto calculateReMortgage(Mortgage mortgage);

    TakeHomePayResponse calculateTakeHomePay(TakeHomePay takeHomePay);
}
