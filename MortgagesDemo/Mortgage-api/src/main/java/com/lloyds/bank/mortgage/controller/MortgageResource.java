package com.lloyds.bank.mortgage.controller;

import com.lloyds.bank.mortgage.config.StampDutyConfiguration;
import com.lloyds.bank.mortgage.dto.Mortgage;
import com.lloyds.bank.mortgage.dto.MortgageEMIPay;
import com.lloyds.bank.mortgage.dto.StampDuty;
import com.lloyds.bank.mortgage.dto.TakeHomePay;
import com.lloyds.bank.mortgage.dto.response.MortgageEMIPayResponse;
import com.lloyds.bank.mortgage.dto.response.MortgageResponseDto;
import com.lloyds.bank.mortgage.dto.response.StampDutyResponse;
import com.lloyds.bank.mortgage.dto.response.TakeHomePayResponse;
import com.lloyds.bank.mortgage.service.IMortgageCalculator;
import com.lloyds.bank.mortgage.service.IStampDutyService;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.http.HttpStatus;
import org.springframework.http.MediaType;
import org.springframework.http.ResponseEntity;
import org.springframework.web.bind.annotation.PostMapping;
import org.springframework.web.bind.annotation.RequestBody;
import org.springframework.web.bind.annotation.RequestMapping;
import org.springframework.web.bind.annotation.RestController;

@RestController
@RequestMapping(value = "/v1/calculators", consumes = MediaType.APPLICATION_JSON_VALUE,
        produces = MediaType.APPLICATION_JSON_VALUE)
public class MortgageResource {

    @Autowired
    private IMortgageCalculator mortgageCalculator;

    @Autowired
    private IStampDutyService stampDutyService;

    @PostMapping("/emi-pay")
    public ResponseEntity<MortgageEMIPayResponse> calculateMonthlyEmi(@RequestBody MortgageEMIPay mortgageEMIPay) {
        MortgageEMIPayResponse mortgageResponseDto = mortgageCalculator.monthlyMortgagePayment(mortgageEMIPay);
        return ResponseEntity.ok(mortgageResponseDto);
    }

    @PostMapping("/mortgage")
    public ResponseEntity<MortgageResponseDto> mortgageEligibility(@RequestBody Mortgage mortgage) {
        if (mortgage.getPurpose().equals("purchase")) {
            MortgageResponseDto mortgageResponseDto = mortgageCalculator.calculateMortgage(mortgage);
            return ResponseEntity.status(HttpStatus.OK).body(mortgageResponseDto);
        }
        if (mortgage.getPurpose().equals("remortgage")) {
            MortgageResponseDto mortgageResponseDto = mortgageCalculator.calculateReMortgage(mortgage);
            return ResponseEntity.status(HttpStatus.OK).body(mortgageResponseDto);
        }
        return ResponseEntity.status(HttpStatus.BAD_REQUEST).build();
    }

    @PostMapping("/stamp-duty")
    public ResponseEntity<StampDutyResponse> stampDuty(@RequestBody StampDuty stampDuty) {
        StampDutyResponse stampDutyResponse = stampDutyService.calculateStampDutyCharge(stampDuty);
        return ResponseEntity.status(HttpStatus.OK).body(stampDutyResponse);
    }


    @PostMapping("/net-income")
    public ResponseEntity<TakeHomePayResponse> calculateTakeHomePay(@RequestBody TakeHomePay pay) {
        TakeHomePayResponse takeHomePayResponse = mortgageCalculator.calculateTakeHomePay(pay);
        return ResponseEntity.status(HttpStatus.OK).body(takeHomePayResponse);
    }

}


