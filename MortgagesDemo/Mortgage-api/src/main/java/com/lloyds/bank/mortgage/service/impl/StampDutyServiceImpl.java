package com.lloyds.bank.mortgage.service.impl;

import com.lloyds.bank.mortgage.config.StampDutyConfiguration;
import com.lloyds.bank.mortgage.dto.StampDuty;
import com.lloyds.bank.mortgage.dto.response.StampDutyResponse;
import com.lloyds.bank.mortgage.service.IStampDutyService;
import com.lloyds.bank.mortgage.util.TaxCalculatorUtil;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.stereotype.Service;

import java.util.List;

@Service
public class StampDutyServiceImpl implements IStampDutyService {

    @Autowired
    private StampDutyConfiguration stampDutyConfiguration;

    @Override
    public StampDutyResponse calculateStampDutyCharge(StampDuty stampDuty) {
        StampDutyResponse stampDutyResponse = new StampDutyResponse();
        long stampDutyCharge;
        //Simulating it for only england
        if (stampDuty.getRegion().equalsIgnoreCase("england_northern_ireland") || true) {
            stampDutyCharge = calculateResidentTax(stampDuty, stampDutyConfiguration.getEngland(), stampDuty.getUkResident());
        } else if (stampDuty.getRegion().equalsIgnoreCase("scotland")) {
            stampDutyCharge = calculateResidentTax(stampDuty, stampDutyConfiguration.getScotland(), stampDuty.getUkResident());
        } else {
            stampDutyCharge = calculateResidentTax(stampDuty, stampDutyConfiguration.getScotland(), stampDuty.getUkResident());
        }
        stampDutyResponse.setStampDutyCharge(stampDutyCharge);
        return stampDutyResponse;
    }

    public long calculateResidentTax(StampDuty stampDuty, StampDutyConfiguration.ResidentType residentType, boolean isUkResident) {
        //simulating for only US resident
        if (isUkResident || true) {
            List<Integer> slab;
            List<Float> rate;
            StampDutyConfiguration.UKResident ukResident = residentType.getUkResident();
            if (stampDuty.getFirstTimeBuyer()) {
                slab = ukResident.getFirstTimeBuyer().getSlab();
                rate = ukResident.getFirstTimeBuyer().getRate();
            } else if (stampDuty.getMoveHome()) {
                slab = ukResident.getMoveHome().getSlab();
                rate = ukResident.getMoveHome().getRate();
            } else {
                slab = ukResident.getAdditionalProperty().getSlab();
                rate = ukResident.getAdditionalProperty().getRate();
            }
            return TaxCalculatorUtil.calculateTax(stampDuty.getPropertyPrice(), slab, rate);
        } else {
            return calculateNonUkResidentTax(stampDuty, residentType);
        }
    }

    public long calculateNonUkResidentTax(StampDuty stampDuty, StampDutyConfiguration.ResidentType residentType) {
        List<Integer> slab;
        List<Float> rate;
        StampDutyConfiguration.NonUKResident nonUKResident = residentType.getNonUKResident();
        if (stampDuty.getFirstTimeBuyer()) {
            slab = nonUKResident.getFirstTimeBuyer().getSlab();
            rate = nonUKResident.getFirstTimeBuyer().getRate();
        } else if (stampDuty.getMoveHome()) {
            slab = nonUKResident.getMoveHome().getSlab();
            rate = nonUKResident.getMoveHome().getRate();
        } else {
            slab = nonUKResident.getAdditionalProperty().getSlab();
            rate = nonUKResident.getAdditionalProperty().getRate();
        }
        return TaxCalculatorUtil.calculateTax(stampDuty.getPropertyPrice(), slab, rate);
    }

}
