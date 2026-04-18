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
import org.springframework.context.annotation.ImportResource;

/**
 * AECF_META: skill=aecf_refactor topic=xml_to_java_config run_time=2026-04-18T00:00:00Z
 * generated_at=2026-04-18T00:00:00Z generated_by=lvillara touch_count=1
 * last_modified_skill=aecf_refactor last_modified_at=2026-04-18T00:00:00Z last_modified_by=lvillara
 *
 * Phase 1 bridge — delegates to datasource-config.xml via @ImportResource so that
 * BusinessConfig and the profile configs can obtain the 'dataSource' bean without
 * requiring the XML context themselves.
 *
 * Phase 2 will replace the @ImportResource body with explicit @Bean declarations
 * for DataSource (Tomcat JDBC pool) and DataSourceInitializer (schema + data scripts),
 * at which point this annotation can be removed and datasource-config.xml deleted.
 */
@Configuration
@ImportResource("classpath:spring/datasource-config.xml")
public class DataSourceConfig {
    // Phase 1: datasource-config.xml provides the 'dataSource' bean and DB initializer.
    // Phase 2: replace with @Bean DataSource + DataSourceInitializer + optional javaee JNDI profile.
}
