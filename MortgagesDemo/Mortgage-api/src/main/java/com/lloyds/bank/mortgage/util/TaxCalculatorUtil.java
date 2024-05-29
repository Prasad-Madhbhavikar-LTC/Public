package com.lloyds.bank.mortgage.util;

import java.util.List;

public class TaxCalculatorUtil {
    private TaxCalculatorUtil(){

    }

    public static long calculateTax(long amount, List<Integer> incomeTaxBadSlab, List<Float> incomeSlabBandRate) {
        double incomeTaxSum = 0;
        int income_taxSlabIndex = incomeTaxBadSlab.size() - 1;
        while (income_taxSlabIndex >= 0) {
            if (amount > incomeTaxBadSlab.get(income_taxSlabIndex)) {
                incomeTaxSum += ((amount - incomeTaxBadSlab.get(income_taxSlabIndex)) * incomeSlabBandRate.get(income_taxSlabIndex));
                amount = incomeTaxBadSlab.get(income_taxSlabIndex);
            }
            income_taxSlabIndex = income_taxSlabIndex - 1;
        }
        return (long) incomeTaxSum;
    }
}
