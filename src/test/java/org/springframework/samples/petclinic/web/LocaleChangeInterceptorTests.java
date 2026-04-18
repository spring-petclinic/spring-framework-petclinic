/*
 * Copyright 2002-2026 the original author or authors.
 *
 * Licensed under the Apache License, Version 2.0 (the "License");
 * you may not use this file except in compliance with the License.
 * You may obtain a copy of the License at
 *
 *      http://www.apache.org/licenses/LICENSE-2.0
 *
 * Unless required by applicable law or agreed to in writing, software
 * distributed under the License is distributed on an "AS IS" BASIS,
 * WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
 * See the License for the specific language governing permissions and
 * limitations under the License.
 */
package org.springframework.samples.petclinic.web;

import org.junit.jupiter.api.BeforeEach;
import org.junit.jupiter.api.Test;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.test.context.junit.jupiter.web.SpringJUnitWebConfig;
import org.springframework.test.web.servlet.MockMvc;
import org.springframework.test.web.servlet.setup.MockMvcBuilders;
import org.springframework.web.context.WebApplicationContext;

import static org.springframework.test.web.servlet.request.MockMvcRequestBuilders.get;
import static org.springframework.test.web.servlet.result.MockMvcResultMatchers.cookie;
import static org.springframework.test.web.servlet.result.MockMvcResultMatchers.status;

/**
 * AECF_META: skill=aecf_new_feature topic=i18n_locale_selector run_time=2026-04-18T00:00:00Z
 * generated_at=2026-04-18T00:00:00Z generated_by=lvillara touch_count=1
 * last_modified_skill=aecf_new_feature last_modified_at=2026-04-18T00:00:00Z last_modified_by=lvillara
 *
 * Integration tests for LocaleChangeInterceptor + CookieLocaleResolver.
 * Uses webAppContextSetup so the full interceptor chain (including LocaleChangeInterceptor)
 * registered in mvc-core-config.xml is active. standaloneSetup would bypass the interceptors.
 */
@SpringJUnitWebConfig(locations = {"classpath:spring/mvc-core-config.xml", "classpath:spring/mvc-test-config.xml"})
class LocaleChangeInterceptorTests {

    @Autowired
    private WebApplicationContext wac;

    private MockMvc mockMvc;

    @BeforeEach
    void setup() {
        this.mockMvc = MockMvcBuilders.webAppContextSetup(wac).build();
    }

    @Test
    void testLangParamEs_setsCookieToSpanish() throws Exception {
        mockMvc.perform(get("/").param("lang", "es"))
            .andExpect(status().isOk())
            .andExpect(cookie().exists("PETCLINIC_LOCALE"))
            .andExpect(cookie().value("PETCLINIC_LOCALE", "es"));
    }

    @Test
    void testLangParamDe_setsCookieToGerman() throws Exception {
        mockMvc.perform(get("/").param("lang", "de"))
            .andExpect(status().isOk())
            .andExpect(cookie().exists("PETCLINIC_LOCALE"))
            .andExpect(cookie().value("PETCLINIC_LOCALE", "de"));
    }

    @Test
    void testLangParamEn_setsCookieToEnglish() throws Exception {
        mockMvc.perform(get("/").param("lang", "en"))
            .andExpect(status().isOk())
            .andExpect(cookie().exists("PETCLINIC_LOCALE"))
            .andExpect(cookie().value("PETCLINIC_LOCALE", "en"));
    }

    @Test
    void testNoLangParam_doesNotWriteCookie() throws Exception {
        mockMvc.perform(get("/"))
            .andExpect(status().isOk())
            .andExpect(cookie().doesNotExist("PETCLINIC_LOCALE"));
    }

    @Test
    void testLangParamOnNonRootPath_setsLocale() throws Exception {
        mockMvc.perform(get("/owners/find").param("lang", "es"))
            .andExpect(status().isOk())
            .andExpect(cookie().value("PETCLINIC_LOCALE", "es"));
    }

    @Test
    void testSubsequentLangSwitch_overridesCookie() throws Exception {
        mockMvc.perform(get("/").param("lang", "es"))
            .andExpect(cookie().value("PETCLINIC_LOCALE", "es"));

        mockMvc.perform(get("/").param("lang", "de"))
            .andExpect(cookie().value("PETCLINIC_LOCALE", "de"));
    }

}
