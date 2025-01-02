package com.account_service.services.Impl;

import org.springframework.beans.factory.annotation.Value;
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
    @Value("${customer.dapr.url}")
    private String customerUrl;

    @Autowired
    private AccountRepository accountRepository;
    @Override
    public Account create(Account account) {
        Customer customer = restTemplate.getForObject(customerUrl + account.getCustomerId(), Customer.class);
        if(customer == null) {
            throw new Error("No customer with this ID");
        }
        UUID accountId = UUID.randomUUID();
        account.setAccountId(String.valueOf(accountId));
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
    public Account getAccount(String id) {

        // Getting Accounts from ACCOUNT SERVICE

        return accountRepository.findById(id).orElseThrow(() -> new ResourceNotFoundException("Account with given id not found try again with correct details !!"));

    }

    @Override
    public List<Account> getAccountByCustomerId(String customerId) {

        return accountRepository.findByCustomerId(customerId);
    }


    @Override
    public Account updateAccount(String id, Account account) {
        Account newAccount = accountRepository.findById(id).orElseThrow(() -> new ResourceNotFoundException("Account with given id not found  try again with correct details!!"));newAccount.setAccountType(account.getAccountType());
        if(Objects.equals(newAccount.getCustomerId(), account.getCustomerId())) {
            newAccount.setLastActivity(new Date());
            System.out.println(account.getBalance());
            return accountRepository.save(account);
        }
        return null;
    }


    @Override
    public void delete(String id) {

        Account account = accountRepository.findById(id).orElseThrow(() -> new ResourceNotFoundException("Account with given id not found !!"));
        this.accountRepository.delete(account);

    }

    @Override
    public void deleteAccountUsingCustomerId(String customerId) {

        List<Account> accounts = accountRepository.findByCustomerId(customerId);

        for( Account account : accounts)
        {
            this.accountRepository.delete(account);
        }

    }

}
