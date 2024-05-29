package com.lloyds.bank.mortgage.config;

import lombok.Data;
import org.springframework.beans.factory.annotation.Value;
import org.springframework.context.annotation.Configuration;

import java.util.List;

@Configuration
@Data
//@ConfigurationProperties(prefix = "mortgage")
public class MortgageConfiguration {

    @Value("${mortgage.default.term}")
    private int mortgageDefaultTerm;

    @Value("${mortgage.family.property.booster.percentage}")
    private int familyMortgagePropertyBoosterPercentage;

    @Value("${mortgage.standardMortgage.interestRate}")
    private float standardMortgageInterestRate;

    @Value("${mortgage.lending.multiplier}")
    private float mortgageLendingMultiplier;

    @Value("${mortgage.lending.multiplier.without-property-mention}")
    private float mortgageLendingMultiplierWithoutPropertyMention;

    @Value("${mortgage.partBuyPartRent.interestRate}")
    private float partBuyPartRentMortgageInterestRate;

    @Value("${mortgage.guarantorMortgage.interestRate}")
    private float guarantorMortgageInterestRate;

    @Value("${mortgage.familyMortgage.interestRate}")
    private float familyMortgageInterestRate;

    @Value("${mortgage.eligible.min.saving}")
    private Integer mortgageEligibleMinSaving;


    @Value("${remortgage.lending.multiplier}")
    private float remortgageLendingMultiplier;
    @Value("${remortgage.standardMortgage.interestRate}")
    private float standardReMortgageInterestRate;
    @Value("${remortgage.default.term}")
    private int remortgageDefaultTerm;


    @Value("#{'${netIncome.income.tax-slab}'.split(',')}")
    List<Integer> netIncomeTaxSlab;

    @Value("#{'${netIncome.income.tax-rate}'.split(',')}")
    List<Float> netIncomeTaxRate;

    @Value("#{'${netIncome.national-insurance.slab}'.split(',')}")
    List<Integer> netIncomeInsuranceSlab;

    @Value("#{'${netIncome.national-insurance.permanent-employee.slab-rate}'.split(',')}")
    List<Float> netIncomePermanentEmpInsuranceSlabRate;

    @Value("#{'${netIncome.national-insurance.self-employee.slab-rate}'.split(',')}")
    List<Float> netIncomeSelfEmpInsuranceSlabRate;
}
