package com.account_service.repositories;

import com.account_service.entity.Account;
import org.springframework.data.jpa.repository.JpaRepository;

import java.util.List;
import java.util.UUID;

public interface AccountRepository extends JpaRepository<Account, UUID> {

    //Find accounts using userId
    List<Account> findByCustomerId(UUID customerId);

}
