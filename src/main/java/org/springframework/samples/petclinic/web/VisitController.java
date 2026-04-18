/*
 * Copyright 2002-2022 the original author or authors.
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

import java.util.Map;

import jakarta.validation.Valid;

import org.springframework.samples.petclinic.model.Pet;
import org.springframework.samples.petclinic.model.Visit;
import org.springframework.samples.petclinic.service.ClinicService;
import org.springframework.stereotype.Controller;
import org.springframework.validation.BindingResult;
import org.springframework.web.bind.WebDataBinder;
import org.springframework.web.bind.annotation.*;

/**
 * @author Juergen Hoeller
 * @author Ken Krebs
 * @author Arjen Poutsma
 * @author Michael Isvy
 */
@Controller
public class VisitController {

    private final ClinicService clinicService;

    public VisitController(ClinicService clinicService) {
        this.clinicService = clinicService;
    }

    @InitBinder
    public void setAllowedFields(WebDataBinder dataBinder) {
        dataBinder.setDisallowedFields("id");
    }

    /**
     * Called before each and every @GetMapping or @PostMapping annotated method.
     * 2 goals:
     * - Make sure we always have fresh data
     * - Since we do not use the session scope, make sure that Pet object always has an id
     * (Even though id is not part of the form fields)
     *
     * @param petId the pet identifier from the URI
     * @return Pet
     */
    /**
     * AECF_META: skill=aecf_refactor topic=eager_loading_fix run_time=2026-04-17T00:00:00Z
     * generated_at=2026-04-17T00:00:00Z generated_by=lvillara touch_count=1
     * last_modified_skill=aecf_refactor last_modified_at=2026-04-17T00:00:00Z last_modified_by=lvillara
     *
     * visit.setPet(pet) instead of pet.addVisit(visit) to avoid accessing the LAZY Pet.visits
     * collection outside a transaction. Visit.pet is the owning side (@ManyToOne), so setting
     * the FK here is sufficient for correct JPA persistence via saveVisit(visit).
     */
    @ModelAttribute("visit")
    public Visit loadPetWithVisit(@PathVariable("petId") int petId) {
        Pet pet = this.clinicService.findPetById(petId);
        Visit visit = new Visit();
        visit.setPet(pet);
        return visit;
    }

    /**
     * AECF_META: skill=aecf_refactor topic=eager_loading_fix run_time=2026-04-17T00:00:00Z
     * generated_at=2026-04-17T00:00:00Z generated_by=lvillara touch_count=1
     * last_modified_skill=aecf_refactor last_modified_at=2026-04-17T00:00:00Z last_modified_by=lvillara
     *
     * Explicitly loads visits via findVisitsByPetId so the JSP can use ${visits} without
     * accessing the LAZY Pet.visits collection outside a transaction.
     */
    // Spring MVC calls method loadPetWithVisit(...) before initNewVisitForm is called
    @GetMapping(value = "/owners/*/pets/{petId}/visits/new")
    public String initNewVisitForm(@PathVariable("petId") int petId, Map<String, Object> model) {
        model.put("visits", this.clinicService.findVisitsByPetId(petId));
        return "pets/createOrUpdateVisitForm";
    }

    /**
     * AECF_META: skill=aecf_refactor topic=eager_loading_fix run_time=2026-04-17T00:00:00Z
     * generated_at=2026-04-17T00:00:00Z generated_by=lvillara touch_count=1
     * last_modified_skill=aecf_refactor last_modified_at=2026-04-17T00:00:00Z last_modified_by=lvillara
     *
     * On validation error, re-populates visits model attribute so the JSP can render
     * previous visits without accessing LAZY Pet.visits outside a transaction.
     */
    // Spring MVC calls method loadPetWithVisit(...) before processNewVisitForm is called
    @PostMapping(value = "/owners/{ownerId}/pets/{petId}/visits/new")
    public String processNewVisitForm(@Valid Visit visit, BindingResult result,
                                      @PathVariable int petId, Map<String, Object> model) {
        if (result.hasErrors()) {
            model.put("visits", this.clinicService.findVisitsByPetId(petId));
            return "pets/createOrUpdateVisitForm";
        }

        this.clinicService.saveVisit(visit);
        return "redirect:/owners/{ownerId}";
    }

    /**
     * AECF_META: skill=aecf_refactor topic=eager_loading_fix run_time=2026-04-17T00:00:00Z
     * generated_at=2026-04-17T00:00:00Z generated_by=lvillara touch_count=1
     * last_modified_skill=aecf_refactor last_modified_at=2026-04-17T00:00:00Z last_modified_by=lvillara
     *
     * Uses findVisitsByPetId instead of findPetById(petId).getVisits() to avoid accessing
     * the LAZY Pet.visits collection outside a transaction.
     */
    @GetMapping(value = "/owners/*/pets/{petId}/visits")
    public String showVisits(@PathVariable int petId, Map<String, Object> model) {
        model.put("visits", this.clinicService.findVisitsByPetId(petId));
        return "visitList";
    }

}
