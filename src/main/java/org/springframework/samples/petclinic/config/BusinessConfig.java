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
package org.springframework.samples.petclinic.config;

import org.springframework.context.annotation.Bean;
import org.springframework.context.annotation.ComponentScan;
import org.springframework.context.annotation.Configuration;
import org.springframework.context.annotation.Import;
import org.springframework.context.support.PropertySourcesPlaceholderConfigurer;
import org.springframework.core.io.ClassPathResource;
import org.springframework.transaction.annotation.EnableTransactionManagement;

/**
 * AECF_META: skill=aecf_refactor topic=xml_to_java_config run_time=2026-04-18T00:00:00Z
 * generated_at=2026-04-18T00:00:00Z generated_by=lvillara touch_count=1
 * last_modified_skill=aecf_refactor last_modified_at=2026-04-18T00:00:00Z last_modified_by=lvillara
 *
 * Root application context — Java Config equivalent of the global section in business-config.xml.
 * Activates @Transactional processing, scans service beans, loads data-access.properties.
 * DataSource is provided by DataSourceConfig (Phase 1: bridges via @ImportResource to datasource-config.xml).
 *
 * Migration phase: Phase 1 — XML files still present; tests can use either XML or Java Config.
 */
@Configuration
@EnableTransactionManagement   // defaults to AdviceMode.PROXY, matching <tx:annotation-driven/> default
@ComponentScan("org.springframework.samples.petclinic.service")
@Import(DataSourceConfig.class)
public class BusinessConfig {

    /**
     * Replaces <context:property-placeholder system-properties-mode="OVERRIDE"/> from business-config.xml.
     *
     * Must be static so Spring instantiates it early enough to resolve @Value annotations in other
     * @Configuration classes before the BeanFactory is fully initialised.
     *
     * PropertySourcesPlaceholderConfigurer uses Spring's Environment abstraction; StandardEnvironment
     * already gives system properties higher precedence than file-based properties, which preserves
     * the system-properties-mode="OVERRIDE" semantics from the XML. No explicit mode call needed.
     */
    @Bean
    public static PropertySourcesPlaceholderConfigurer propertySourcesPlaceholderConfigurer() {
        PropertySourcesPlaceholderConfigurer pspc = new PropertySourcesPlaceholderConfigurer();
        pspc.setLocation(new ClassPathResource("spring/data-access.properties"));
        return pspc;
    }

}
