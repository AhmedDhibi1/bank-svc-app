package com.account_service.entity;

import com.fasterxml.jackson.annotation.JsonProperty;
import lombok.AllArgsConstructor;
import lombok.Getter;
import lombok.NoArgsConstructor;
import lombok.Setter;

@Getter
@Setter
@NoArgsConstructor
@AllArgsConstructor
public class CloudEvent {
    private String specversion;
    private String id;
    private String source;
    private String type;
    private String datacontenttype;

    private Account data;


    public static class AccountUpdateData {
        private int accountId;
        private String status;

    }


}