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

import io.swagger.v3.oas.annotations.Operation;
import io.swagger.v3.oas.annotations.media.Content;
import io.swagger.v3.oas.annotations.media.Schema;
import io.swagger.v3.oas.annotations.responses.ApiResponse;
import io.swagger.v3.oas.annotations.tags.Tag;
import org.springframework.http.MediaType;
import org.springframework.samples.petclinic.model.Vets;
import org.springframework.samples.petclinic.service.ClinicService;
import org.springframework.web.bind.annotation.GetMapping;
import org.springframework.web.bind.annotation.RequestMapping;
import org.springframework.web.bind.annotation.RestController;

/**
 * REST controller for the veterinarians resource.
 *
 * <p>Exposes {@code GET /api/vets} with standard {@code Accept} header content negotiation
 * (JSON or XML). The HTML view at {@code /vets} is served by {@link VetController} and is
 * intentionally separate from this REST contract.
 *
 * @author lvillara
 */
@RestController
@RequestMapping("/api")
@Tag(name = "vets", description = "Operations about veterinarians")
public class VetRestController {

    private final ClinicService clinicService;

    public VetRestController(ClinicService clinicService) {
        this.clinicService = clinicService;
    }

    /**
     * AECF_META: skill=aecf_new_feature topic=vet_rest_api run_time=2026-04-18T00:00:00Z
     * generated_at=2026-04-18T00:00:00Z generated_by=lvillara touch_count=1
     * last_modified_skill=aecf_new_feature last_modified_at=2026-04-18T00:00:00Z last_modified_by=lvillara
     *
     * Devuelve la lista completa de veterinarios con sus especialidades.
     * Soporta JSON (Accept: application/json) y XML (Accept: application/xml).
     * La serialización XML usa Jaxb2RootElementHttpMessageConverter gracias a @XmlRootElement en Vets.
     */
    @Operation(
        summary = "List all veterinarians",
        description = "Returns the complete list of veterinarians with their specialties. " +
                      "Use Accept: application/json or Accept: application/xml."
    )
    @ApiResponse(
        responseCode = "200",
        description = "Successful operation",
        content = {
            @Content(mediaType = MediaType.APPLICATION_JSON_VALUE,
                     schema = @Schema(implementation = Vets.class)),
            @Content(mediaType = MediaType.APPLICATION_XML_VALUE,
                     schema = @Schema(implementation = Vets.class))
        }
    )
    @ApiResponse(responseCode = "406", description = "Requested media type not supported")
    @GetMapping(
        value = "/vets",
        produces = {MediaType.APPLICATION_JSON_VALUE, MediaType.APPLICATION_XML_VALUE}
    )
    public Vets listVets() {
        Vets vets = new Vets();
        vets.getVetList().addAll(this.clinicService.findVets());
        return vets;
    }

}
