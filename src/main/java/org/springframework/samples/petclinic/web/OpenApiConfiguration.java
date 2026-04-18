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

import io.swagger.v3.oas.models.OpenAPI;
import io.swagger.v3.oas.models.info.Info;
import io.swagger.v3.oas.models.info.License;
import org.springframework.context.annotation.Bean;
import org.springframework.context.annotation.Configuration;

/**
 * Registers the OpenAPI metadata bean consumed by SpringDoc to generate /v3/api-docs and Swagger UI.
 *
 * @author lvillara
 */
@Configuration
public class OpenApiConfiguration {

    /**
     * AECF_META: skill=aecf_new_feature topic=vet_rest_api run_time=2026-04-18T00:00:00Z
     * generated_at=2026-04-18T00:00:00Z generated_by=lvillara touch_count=1
     * last_modified_skill=aecf_new_feature last_modified_at=2026-04-18T00:00:00Z last_modified_by=lvillara
     *
     * Define los metadatos globales de la API que SpringDoc expone en /v3/api-docs y Swagger UI.
     */
    @Bean
    public OpenAPI petclinicOpenAPI() {
        return new OpenAPI()
            .info(new Info()
                .title("Spring PetClinic REST API")
                .description("REST endpoints for the Spring Framework PetClinic sample application")
                .version("1.0")
                .license(new License()
                    .name("Apache 2.0")
                    .url("https://www.apache.org/licenses/LICENSE-2.0")));
    }

}
