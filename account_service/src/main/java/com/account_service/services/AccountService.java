package com.account_service.services;

import com.account_service.entity.Account;

import java.util.List;
import java.util.UUID;

public interface AccountService {

    //create

    Account create(Account account);

    //get accounts

    List<Account> getAccounts();

    //get single account

    Account getAccount(UUID id);

    //get single account using customerId

    List<Account> getAccountByCustomerId(UUID customerId);

    //update Account
<<<<<<< HEAD
    Account updateAccount(UUID id, Account account);
=======
    Account updateAccount(String id, Account account);
>>>>>>> 106ab3190ee04cf6c8a7d2a89e202bba90b10530

    //delete

    void delete(UUID id);

    void deleteAccountUsingCustomerId(UUID customerId);

}
