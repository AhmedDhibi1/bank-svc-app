package com.account_service.entity;

import jakarta.persistence.Entity;
import jakarta.persistence.Id;
import jakarta.persistence.Table;
import jakarta.persistence.Transient;
import lombok.*;
import org.springframework.format.annotation.DateTimeFormat;


import java.util.Date;
import java.util.UUID;

@Getter
@Setter
@NoArgsConstructor
@AllArgsConstructor
@Entity
@Table(name="Accounts")
public class Account {

    @Id
    private UUID accountId;

    private String accountType;

    @DateTimeFormat
    Date accountOpeningDate;

    @DateTimeFormat
    Date lastActivity;
    private int balance;

    private UUID customerId;

}
