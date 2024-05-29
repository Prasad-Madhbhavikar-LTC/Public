package com.lloyds.bank.mortgage.config;

import lombok.Data;
import org.springframework.boot.context.properties.ConfigurationProperties;
import org.springframework.context.annotation.Configuration;

import java.util.List;

@Configuration
@Data
@ConfigurationProperties(prefix = "stamp-duty")
public class StampDutyConfiguration {

    private England england;
    private Scotland scotland;
    private Wales wales;

    @Data
    public static class ResidentType{
        private UKResident ukResident;
        private NonUKResident nonUKResident;
    }

    @Data
    public static class England extends ResidentType{}

    @Data
    public static class Scotland extends ResidentType{}

    @Data
    public static class Wales extends ResidentType{ }

    @Data
    public static class BuyerType{
        private FirstTimeBuyer firstTimeBuyer;
        private MoveHome moveHome;
        private AdditionalProperty additionalProperty;
    }

    @Data
    public static class UKResident extends BuyerType{
    }

    @Data
    public static class NonUKResident extends BuyerType{

    }

    @Data
    public static class Buyer{
        List<Integer> slab;
        List<Float> rate;
    }

    @Data
    public static class FirstTimeBuyer extends Buyer{
    }

    @Data
    public static class MoveHome extends Buyer{
    }
    @Data
    public static class AdditionalProperty extends Buyer{

    }
}
