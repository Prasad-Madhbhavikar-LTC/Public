package com.lloyds.bank.mortgage.dto.response;

import com.fasterxml.jackson.annotation.JsonProperty;
import lombok.Data;

import java.io.Serializable;

@Data
public class StampDutyResponse implements Serializable {
    @JsonProperty("stamp_duty_charge")
    private Long stampDutyCharge;
}