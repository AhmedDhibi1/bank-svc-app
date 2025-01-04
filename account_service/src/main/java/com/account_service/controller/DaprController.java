package com.account_service.controller;

import com.account_service.entity.Account;
import com.account_service.entity.CloudEvent;
import com.account_service.services.AccountService;
import org.springframework.web.bind.annotation.*;
import org.slf4j.Logger;
import org.slf4j.LoggerFactory;

@RestController("DaprController")
@RequestMapping("/dapr/subscribe")
public class DaprController {

    private  AccountService accountService;
    private static final Logger logger = LoggerFactory.getLogger(DaprController.class);

    @PostMapping("/updateAccount")
    public void handleUpdateAccount(@RequestBody CloudEvent cloudEvent) {
       Account account = cloudEvent.getData();
        if (account != null) {
            logger.info("Account ID: {}, balance: {}", account.getAccountId(), account.getBalance());
            accountService.updateAccount(account.getAccountId(),account);
        } else {
            logger.error("Received event with no data.");
        }
    }
}
