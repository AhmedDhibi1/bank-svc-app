package com.account_service.services.Impl;

import com.account_service.entity.Account;
import com.account_service.entity.Customer;
import com.account_service.exceptions.ResourceNotFoundException;
import com.account_service.repositories.AccountRepository;
import com.account_service.services.AccountService;
import io.dapr.client.DaprClient;
import io.dapr.client.DaprClientBuilder;
import org.slf4j.Logger;
import org.slf4j.LoggerFactory;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.stereotype.Service;
import org.springframework.web.client.RestTemplate;

import java.util.Date;
import java.util.List;
import java.util.Objects;
import java.util.UUID;

@Service
public class AccountServiceImpl implements AccountService {

    @Autowired
    private RestTemplate restTemplate;

    private Logger logger = LoggerFactory.getLogger(AccountServiceImpl.class);


    @Autowired
    private AccountRepository accountRepository;
    @Override
    public Account create(Account account) {
<<<<<<< HEAD
        Customer customer = restTemplate.getForObject("http://localhost:8081/customers/" + account.getCustomerId(), Customer.class);
=======
        Customer customer = restTemplate.getForObject("http://localhost:3510/v1.0/invoke/customer-service/method/customers/" + account.getCustomerId(), Customer.class);
>>>>>>> 106ab3190ee04cf6c8a7d2a89e202bba90b10530
        if(customer == null) {
            throw new Error("No customer with this ID");
        }
        UUID accountId = UUID.randomUUID();
<<<<<<< HEAD
        account.setAccountId(accountId);
=======
        account.setAccountId(String.valueOf(accountId));
>>>>>>> 106ab3190ee04cf6c8a7d2a89e202bba90b10530
        Date current_Date = new Date();
        account.setAccountOpeningDate(current_Date);
        account.setLastActivity(current_Date);
        return accountRepository.save(account);
    }

    @Override
    public List<Account> getAccounts() {
        return accountRepository.findAll();
    }

    @Override
    public Account getAccount(UUID id) {

        // Getting Accounts from ACCOUNT SERVICE

        return accountRepository.findById(id).orElseThrow(() -> new ResourceNotFoundException("Account with given id not found try again with correct details !!"));

    }

    @Override
<<<<<<< HEAD
    public List<Account> getAccountByCustomerId(UUID customerId) {
=======
    public List<Account> getAccountByCustomerId(String customerId) {
>>>>>>> 106ab3190ee04cf6c8a7d2a89e202bba90b10530

        return accountRepository.findByCustomerId(customerId);
    }


    @Override
<<<<<<< HEAD
    public Account updateAccount(UUID id, Account account) {
        Account newAccount = accountRepository.findById(id).orElseThrow(() -> new ResourceNotFoundException("Account with given id not found  try again with correct details!!"));newAccount.setAccountType(account.getAccountType());
        if(newAccount.getCustomerId()==account.getCustomerId()) {
            newAccount.setLastActivity(new Date());
=======
    public Account updateAccount(String id, Account account) {
        Account newAccount = accountRepository.findById(id).orElseThrow(() -> new ResourceNotFoundException("Account with given id not found  try again with correct details!!"));newAccount.setAccountType(account.getAccountType());
        if(Objects.equals(newAccount.getCustomerId(), account.getCustomerId())) {
            newAccount.setLastActivity(new Date());
            System.out.println(account.getBalance());
>>>>>>> 106ab3190ee04cf6c8a7d2a89e202bba90b10530
            return accountRepository.save(account);
        }
        return null;
    }

<<<<<<< HEAD
    @Override
    public void delete(UUID id) {
=======

    @Override
    public void delete(String id) {
>>>>>>> 106ab3190ee04cf6c8a7d2a89e202bba90b10530

        Account account = accountRepository.findById(id).orElseThrow(() -> new ResourceNotFoundException("Account with given id not found !!"));
        this.accountRepository.delete(account);

    }

    @Override
    public void deleteAccountUsingCustomerId(UUID customerId) {

        List<Account> accounts = accountRepository.findByCustomerId(customerId);

        for( Account account : accounts)
        {
            this.accountRepository.delete(account);
        }

    }

}
