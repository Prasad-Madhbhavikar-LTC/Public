package com.lloyds.bank.mortgage.service.impl;

import com.lloyds.bank.mortgage.config.MortgageConfiguration;
import com.lloyds.bank.mortgage.dto.Mortgage;
import com.lloyds.bank.mortgage.dto.MortgageEMIPay;
import com.lloyds.bank.mortgage.dto.TakeHomePay;
import com.lloyds.bank.mortgage.dto.response.MortgageEMIPayResponse;
import com.lloyds.bank.mortgage.dto.response.MortgageResponseDto;
import com.lloyds.bank.mortgage.dto.response.TakeHomePayResponse;
import com.lloyds.bank.mortgage.service.IMortgageCalculator;
import lombok.extern.slf4j.Slf4j;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.stereotype.Service;

import java.text.NumberFormat;
import java.util.Arrays;
import java.util.List;
import java.util.Locale;

import static com.lloyds.bank.mortgage.util.TaxCalculatorUtil.calculateTax;

@Service
@Slf4j
public class MortgageCalculatorImpl implements IMortgageCalculator {
    private static final Integer MONTHS_IN_YEAR = 12;

    @Autowired
    private MortgageConfiguration mortgageConfiguration;

    @Override
    public MortgageEMIPayResponse monthlyMortgagePayment(MortgageEMIPay mortgageDto) {
        Long principalAmount = mortgageDto.getPrincipalAmount();
        float interestRate = mortgageDto.getInterestRate();
        int termInMonths;
        if (mortgageDto.getIsTermsInMonths()) {
            termInMonths = mortgageDto.getTerms();
        } else {
            termInMonths = mortgageDto.getTerms() * MONTHS_IN_YEAR;
        }
        float interestRatePercentage = interestRate / 100;
        float monthlyInterestRate = interestRatePercentage / MONTHS_IN_YEAR;

        /*M = P i(1+i)^n
                ------------
                (1+i)^n - 1
         */

        double monthlyMortgagePayment = principalAmount * (
                (monthlyInterestRate * Math.pow(1 + monthlyInterestRate, termInMonths))) /
                (Math.pow(1 + monthlyInterestRate, termInMonths) - 1);
        String formattedMonthlyMortgagePayment = NumberFormat.getCurrencyInstance(Locale.UK)
                .format(monthlyMortgagePayment);
        log.info("Monthly Mortgage Payment {}", formattedMonthlyMortgagePayment);
        log.info("Total Mortgage payback amount {}", NumberFormat.getCurrencyInstance(Locale.UK)
                .format(monthlyMortgagePayment * termInMonths));

        MortgageEMIPayResponse mortgageResponseDto = MortgageEMIPayResponse.builder()
                .monthlyPayment((long) monthlyMortgagePayment)
                .totalPaybackInTerms((long) monthlyMortgagePayment * termInMonths).build();
        return mortgageResponseDto;
    }

    @Override
    public MortgageResponseDto calculateMortgage(Mortgage mortgage) {
        MortgageResponseDto mortgageResponseDto = new MortgageResponseDto();
        if (mortgage.getMortgageCustomer().getSaving() < mortgageConfiguration.getMortgageEligibleMinSaving()) {
            mortgageResponseDto.setEligibility(false);
            return mortgageResponseDto;
        }

        mortgageResponseDto.setEligibility(true);

        if (mortgage.getPropertyPrice() == null) {
            MortgageResponseDto.MortgageResponse response = getMortgageResponse(mortgage.getMortgageCustomer().getIncome(),
                    mortgage.getMortgageCustomer().getSaving(), mortgageConfiguration.getMortgageLendingMultiplierWithoutPropertyMention());
            response.setMortgageType("StandardMortgage");
            calculateMonthlyEMIPayAndSetInMortgageResponse(response.getMortgageAmount(),
                    mortgageConfiguration.getStandardMortgageInterestRate(),
                    mortgageConfiguration.getMortgageDefaultTerm(), mortgageResponseDto, response);
        } else {
            MortgageResponseDto.MortgageResponse response = getMortgageResponse(mortgage.getMortgageCustomer().getIncome(),
                    mortgage.getMortgageCustomer().getSaving(), mortgageConfiguration.getMortgageLendingMultiplier());
            response.setMortgageType("StandardMortgage");
            calculateMonthlyEMIPayAndSetInMortgageResponse(response.getMortgageAmount(),
                    mortgageConfiguration.getStandardMortgageInterestRate(),
                    mortgageConfiguration.getMortgageDefaultTerm(), mortgageResponseDto, response);
        }

        if (mortgage.getMortgageBooster() != null) {
            Long guarantorMortgage = (long) ((mortgage.getMortgageBooster().getIncome() * mortgageConfiguration.getMortgageLendingMultiplier()) +
                    mortgage.getMortgageBooster().getSaving());
            Long mortgageAmount = guarantorMortgage + mortgageResponseDto.getMortgageResponses().get(0).getMortgageAmount();
            MortgageResponseDto.MortgageResponse response = new MortgageResponseDto.MortgageResponse();
            response.setMortgageType("GuarantorMortgage");
            calculateMonthlyEMIPayAndSetInMortgageResponse(mortgageAmount,
                    mortgageConfiguration.getGuarantorMortgageInterestRate(),
                    mortgageConfiguration.getMortgageDefaultTerm(), mortgageResponseDto, response);
        }

        if (mortgage.getMortgageBooster() != null && mortgage.getMortgageBooster().getBoosterPropertyValue() != null) {
            Long standardMortgageAmount = mortgageResponseDto.getMortgageResponses().get(0).getMortgageAmount();
            Long boosterPropertyValue = mortgage.getMortgageBooster().getBoosterPropertyValue();
            Long familyMortgageAmount = standardMortgageAmount +
                    (long) ((boosterPropertyValue * mortgageConfiguration.getFamilyMortgagePropertyBoosterPercentage()) / 100);
            MortgageResponseDto.MortgageResponse response = new MortgageResponseDto.MortgageResponse();
            response.setMortgageType("FamilyMortgage");
            calculateMonthlyEMIPayAndSetInMortgageResponse(familyMortgageAmount,
                    mortgageConfiguration.getFamilyMortgageInterestRate(),
                    mortgageConfiguration.getMortgageDefaultTerm(), mortgageResponseDto, response);
        }
        return mortgageResponseDto;
    }

    @Override
    public MortgageResponseDto calculateReMortgage(Mortgage mortgage) {
        MortgageResponseDto mortgageResponseDto = new MortgageResponseDto();

        Long income = mortgage.getMortgageCustomer().getIncome();

        if (income * mortgageConfiguration.getRemortgageLendingMultiplier() < 10000) {
            mortgageResponseDto.setEligibility(false);
            return mortgageResponseDto;
        }
        mortgageResponseDto.setEligibility(true);

        MortgageResponseDto.MortgageResponse response = new MortgageResponseDto.MortgageResponse();
        response.setMortgageType("StandardRemortgage");
        long remortgageStandardAmount = (long) (income * mortgageConfiguration.getRemortgageLendingMultiplier());
        calculateMonthlyEMIPayAndSetInMortgageResponse(remortgageStandardAmount, mortgageConfiguration.getStandardReMortgageInterestRate(),
                mortgageConfiguration.getRemortgageDefaultTerm(), mortgageResponseDto, response);


        //Dummy simulation
        MortgageResponseDto.MortgageResponse response1 = new MortgageResponseDto.MortgageResponse();
        response1.setMortgageType("InterestOnlyRemortgage");
        long remortgageInterestOnlyMortgageAmount = (long) (income * 2.5);
        calculateMonthlyEMIPayAndSetInMortgageResponse(remortgageInterestOnlyMortgageAmount, 5,
                mortgageConfiguration.getRemortgageDefaultTerm(), mortgageResponseDto, response1);

        if (mortgage.getMortgageBooster() != null && mortgage.getMortgageBooster().getIncome() != null) {
            MortgageResponseDto.MortgageResponse response2 = new MortgageResponseDto.MortgageResponse();
            response2.setMortgageType("IncomeBoostRemortgage");
            long incomeBoostRemortgageAmount = (long) (income * mortgageConfiguration.getRemortgageLendingMultiplier() +
                    mortgage.getMortgageBooster().getIncome());
            calculateMonthlyEMIPayAndSetInMortgageResponse(incomeBoostRemortgageAmount, 4.85f,
                    mortgageConfiguration.getRemortgageDefaultTerm(), mortgageResponseDto, response2);
        }

        return mortgageResponseDto;
    }

    @Override
    public TakeHomePayResponse calculateTakeHomePay(TakeHomePay pay) {
        Long annualIncome = pay.getAnnualIncome();

        Long pensionContribution;

        if (pay.getPensionContributionAmount() != null) {
            pensionContribution = pay.getPensionContributionAmount();
        } else {
            pensionContribution = (long) (annualIncome * pay.getPensionContributionPercentage() / 100);
        }

        /*long nationalInsurance = nationalInsuranceCalculation(annualIncome,
                pay.getEmploymentType().equals("permanent_employment"));*/
        long nationalInsurance;
        if (pay.getEmploymentType().equals("permanent_employment")) {
            nationalInsurance = calculateTax(annualIncome, mortgageConfiguration.getNetIncomeInsuranceSlab(),
                    mortgageConfiguration.getNetIncomePermanentEmpInsuranceSlabRate());
        } else {
            nationalInsurance = calculateTax(annualIncome, mortgageConfiguration.getNetIncomeInsuranceSlab(),
                    mortgageConfiguration.getNetIncomeSelfEmpInsuranceSlabRate());
        }

        long studentLoan = pay.getStudentLoanMonthlyPayment() * 12;

        long amountEligibleForTax = annualIncome - pensionContribution;

        long taxAmount = calculateTax(amountEligibleForTax, mortgageConfiguration.getNetIncomeTaxSlab(),
                mortgageConfiguration.getNetIncomeTaxRate());

        long incomeAfterDeduction = annualIncome - pensionContribution - taxAmount - nationalInsurance - studentLoan;

        TakeHomePayResponse takeHomePayResponse = new TakeHomePayResponse();
        takeHomePayResponse.setGrossAnnualIncome(annualIncome);
        takeHomePayResponse.setPensionDeduction(pensionContribution);
        takeHomePayResponse.setTaxableIncome(taxAmount);
        takeHomePayResponse.setNationalInsurance(nationalInsurance);
        takeHomePayResponse.setStudentLoan(studentLoan);
        takeHomePayResponse.setMortgageEligibleAmount(annualIncome * 9);
        takeHomePayResponse.setAnnualIncome(incomeAfterDeduction);
        takeHomePayResponse.setMonthlyPay(incomeAfterDeduction / 12);
        return takeHomePayResponse;
    }

    private long calculateIncomeTax(long pay) {
        

        List<Integer> income_band_slab = Arrays.asList(12570, 50270, 15000);
        List<Float> income_slab_band_rate = Arrays.asList(0.0f, 0.20f, 0.40f, 0.45f);

        long band1_top = 12570;
        long band2_top = 50270;
        long band3_top = 150000;

        float band1_rate = 0.0f;
        float band2_rate = 0.20f;
        float band3_rate = 0.40f;
        float band4_rate = 0.45f;

        double band1_tax, band2_tax, band3_tax, band4_tax;
        band1_tax = band2_tax = band3_tax = band4_tax = 0;
        long income = pay;
        if (pay > band3_top) {
            band4_tax = (income - band3_top) * band4_rate;
            income = band3_top;
        }

        if (income > band2_top) {
            band3_tax = (income - band2_top) * band3_rate;
            income = band2_top;
        }

        if (income > band1_top) {
            band2_tax = (income - band1_top) * band2_rate;
            income = band1_top;
        }

        band1_tax = income * band1_rate;

        return (long) (band1_tax + band2_tax + band3_tax + band4_tax);

    }

    /**
     * Developed this formula for calculating tax
     *
     * @param income
     * @param permanentEmployee
     * @return
     */

    private long nationalInsuranceCalculation(long income, boolean permanentEmployee) {
        long top_band1 = 12570;
        long top_band2 = 50270;

        float band1_tax_rate = 0.0f;
        float band2_tax_rate;
        if (permanentEmployee) {
            band2_tax_rate = 0.12f;
        } else {
            band2_tax_rate = 0.09f;
        }
        float band3_tax_rate = 0.02f;

        double band1_insurance, band2_insurance, band3_insurance;
        band1_insurance = band2_insurance = band3_insurance = 0;

        if (income > top_band2) {
            band3_insurance = (income - top_band2) * band3_tax_rate;
            income = top_band2;
        }

        if (income > top_band1) {
            band2_insurance = (income - top_band1) * band2_tax_rate;
            income = top_band1;
        }

        band1_insurance = income * band1_tax_rate;

        return (long) (band1_insurance + band2_insurance + band3_insurance);

    }

    private void calculateMonthlyEMIPayAndSetInMortgageResponse(Long principleAmount, float interestRate, int termYear, MortgageResponseDto mortgageResponseDto,
                                                                MortgageResponseDto.MortgageResponse mortgageResponse) {
        MortgageEMIPay mortgageEMIPay = new MortgageEMIPay();
        mortgageEMIPay.setPrincipalAmount(principleAmount);
        mortgageEMIPay.setInterestRate(interestRate);
        mortgageEMIPay.setTerms(termYear);
        MortgageEMIPayResponse mortgageEMIPayResponse = monthlyMortgagePayment(mortgageEMIPay);
        mortgageResponse.setMortgageAmount(principleAmount);
        mortgageResponse.setInterestRate(interestRate);
        mortgageResponse.setMonthlyPay(mortgageEMIPayResponse.getMonthlyPayment());
        mortgageResponseDto.getMortgageResponses().add(mortgageResponse);
    }

    private static MortgageResponseDto.MortgageResponse getMortgageResponse(Long income, Long saving,
                                                                            float multipleTimesEligibility) {
        long mortgageFromSaving = saving * 20;
        double mortgageFromIncome = income * multipleTimesEligibility;

        double eligibleMortgageAmount;

        if (mortgageFromSaving < mortgageFromIncome) {
            eligibleMortgageAmount = mortgageFromSaving;
        } else {
            eligibleMortgageAmount = mortgageFromIncome + saving;
        }

        MortgageResponseDto.MortgageResponse response = new MortgageResponseDto.MortgageResponse();
        response.setMortgageAmount((long) eligibleMortgageAmount);
        return response;
    }


}
