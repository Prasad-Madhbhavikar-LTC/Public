package com.lloyds.bank.mortgage;

import com.lloyds.bank.mortgage.config.MortgageConfiguration;
import org.springframework.boot.SpringApplication;
import org.springframework.boot.autoconfigure.SpringBootApplication;
import org.springframework.boot.context.properties.EnableConfigurationProperties;

@SpringBootApplication
public class MortgageManagementSystemApplication {

	public static void main(String[] args) {
		SpringApplication.run(MortgageManagementSystemApplication.class, args);
	}

}
