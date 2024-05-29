package com.lloyds.bank.mortgage.service;

import com.lloyds.bank.mortgage.dto.StampDuty;
import com.lloyds.bank.mortgage.dto.response.StampDutyResponse;

public interface IStampDutyService {
    StampDutyResponse calculateStampDutyCharge(StampDuty stampDuty);
}
