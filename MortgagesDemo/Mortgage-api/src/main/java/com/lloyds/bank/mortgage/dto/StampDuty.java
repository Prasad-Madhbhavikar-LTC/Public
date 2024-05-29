package com.lloyds.bank.mortgage.dto;

import com.fasterxml.jackson.annotation.JsonProperty;
import lombok.Data;

@Data
public class StampDuty {
    @JsonProperty("purchase_price")
    private Long propertyPrice;
    @JsonProperty("region")
    private String region;
    @JsonProperty("first_time_buyer")
    private Boolean firstTimeBuyer = Boolean.FALSE;
    @JsonProperty("additional_property")
    private Boolean additionalProperty = Boolean.FALSE;
    @JsonProperty("move_home")
    private Boolean moveHome = Boolean.FALSE;
    @JsonProperty("uk_resident")
    private Boolean ukResident;
}
