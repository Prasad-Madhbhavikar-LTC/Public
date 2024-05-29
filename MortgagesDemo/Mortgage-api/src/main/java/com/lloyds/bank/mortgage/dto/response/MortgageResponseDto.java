package com.lloyds.bank.mortgage.dto.response;

import com.fasterxml.jackson.annotation.JsonInclude;
import com.fasterxml.jackson.annotation.JsonProperty;
import lombok.AllArgsConstructor;
import lombok.Data;
import lombok.NoArgsConstructor;

import java.io.Serializable;
import java.util.ArrayList;
import java.util.List;

@Data
@NoArgsConstructor
@JsonInclude(JsonInclude.Include.NON_NULL)
public class MortgageResponseDto implements Serializable {

    private Boolean eligibility;

    @JsonProperty("mortgage_response")
    private List<MortgageResponse> mortgageResponses= new ArrayList<>();

    @Data
    @NoArgsConstructor
    @AllArgsConstructor
    public static class MortgageResponse {
        private String mortgageType;
        private Float interestRate;
        private Long monthlyPay;
        private Long mortgageAmount;
    }
}
