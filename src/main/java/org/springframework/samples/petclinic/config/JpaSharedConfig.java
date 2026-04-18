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

import javax.sql.DataSource;

import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.beans.factory.annotation.Value;
import org.springframework.context.annotation.Bean;
import org.springframework.context.annotation.Configuration;
import org.springframework.context.annotation.Profile;
import org.springframework.dao.annotation.PersistenceExceptionTranslationPostProcessor;
import org.springframework.orm.jpa.JpaTransactionManager;
import org.springframework.orm.jpa.LocalContainerEntityManagerFactoryBean;
import org.springframework.orm.jpa.vendor.Database;
import org.springframework.orm.jpa.vendor.HibernateJpaVendorAdapter;
import org.springframework.transaction.PlatformTransactionManager;

import jakarta.persistence.EntityManagerFactory;

/**
 * AECF_META: skill=aecf_refactor topic=xml_to_java_config run_time=2026-04-18T00:00:00Z
 * generated_at=2026-04-18T00:00:00Z generated_by=lvillara touch_count=1
 * last_modified_skill=aecf_refactor last_modified_at=2026-04-18T00:00:00Z last_modified_by=lvillara
 *
 * JPA shared infrastructure active for profiles "jpa" and "spring-data-jpa".
 * Replaces <beans profile="jpa,spring-data-jpa"> in business-config.xml.
 *
 * Note on persistenceUnitName vs packagesToScan: the XML carried both, but commented that
 * persistenceUnitName wins. This class sets only persistenceUnitName — packagesToScan is
 * intentionally omitted to match actual runtime behavior and avoid ambiguity.
 */
@Configuration
@Profile({"jpa", "spring-data-jpa"})
public class JpaSharedConfig {

    @Autowired
    private DataSource dataSource;

    @Value("${jpa.database}")
    private Database jpaDatabase;

    @Value("${jpa.showSql}")
    private boolean showSql;

    @Bean("entityManagerFactory")
    public LocalContainerEntityManagerFactoryBean entityManagerFactory() {
        LocalContainerEntityManagerFactoryBean em = new LocalContainerEntityManagerFactoryBean();
        em.setDataSource(dataSource);
        HibernateJpaVendorAdapter vendorAdapter = new HibernateJpaVendorAdapter();
        vendorAdapter.setDatabase(jpaDatabase);
        vendorAdapter.setShowSql(showSql);
        em.setJpaVendorAdapter(vendorAdapter);
        em.setPersistenceUnitName("petclinic");
        return em;
    }

    /** Bean name "transactionManager" matches the default expected by @EnableTransactionManagement. */
    @Bean("transactionManager")
    public PlatformTransactionManager transactionManager(EntityManagerFactory emf) {
        return new JpaTransactionManager(emf);
    }

    /** Translates JPA/Hibernate native exceptions to Spring's DataAccessException hierarchy on @Repository beans. */
    @Bean
    public PersistenceExceptionTranslationPostProcessor exceptionTranslation() {
        return new PersistenceExceptionTranslationPostProcessor();
    }

}
