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

import org.springframework.context.annotation.Configuration;
import org.springframework.context.annotation.Profile;
import org.springframework.data.jpa.repository.config.EnableJpaRepositories;

/**
 * AECF_META: skill=aecf_refactor topic=xml_to_java_config run_time=2026-04-18T00:00:00Z
 * generated_at=2026-04-18T00:00:00Z generated_by=lvillara touch_count=1
 * last_modified_skill=aecf_refactor last_modified_at=2026-04-18T00:00:00Z last_modified_by=lvillara
 *
 * Spring Data JPA repository scanning for the "spring-data-jpa" profile.
 * Replaces <jpa:repositories base-package="...springdatajpa"/> in business-config.xml.
 *
 * entityManagerFactoryRef and transactionManagerRef are explicit to avoid relying on convention-based
 * defaults; this makes the dependency on JpaSharedConfig beans unambiguous and compile-time visible.
 */
@Configuration
@Profile("spring-data-jpa")
@EnableJpaRepositories(
    basePackages = "org.springframework.samples.petclinic.repository.springdatajpa",
    entityManagerFactoryRef = "entityManagerFactory",
    transactionManagerRef = "transactionManager"
)
public class SpringDataJpaConfig {
    // No explicit beans — Spring Data JPA proxies are created by @EnableJpaRepositories.
}
