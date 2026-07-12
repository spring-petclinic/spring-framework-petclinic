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

    private static final String VIEWS_VISIT_FORM = "pets/createOrUpdateVisitForm";
    private static final String MODEL_ATTRIBUTE_VISITS = "visits";
    private static final String VISIT_NEW_PATH = "/owners/{ownerId}/pets/{petId}/visits/new";
    private static final String REDIRECT_TO_VISIT_OWNER = "redirect:/owners/{ownerId}";
    private static final String VIEWS_VISIT_LIST = "visitList";
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
    @ModelAttribute("visit")
    public Visit loadPetWithVisit(@PathVariable("petId") int petId) {
        Visit visit = new Visit();
        this.clinicService.findPetById(petId).addVisit(visit);
        return visit;
    }

    // Spring MVC calls method loadPetWithVisit(...) before initNewVisitForm is called
    @GetMapping(value = VISIT_NEW_PATH)
    public String initNewVisitForm() {
        return VIEWS_VISIT_FORM;
    }

    // Spring MVC calls method loadPetWithVisit(...) before processNewVisitForm is called
    @PostMapping(value = VISIT_NEW_PATH)
    public String processNewVisitForm(@Valid Visit visit, BindingResult result) {
        return handleVisitSubmission(visit, result);
    }

    private String handleVisitSubmission(Visit visit, BindingResult result) {
        if (result.hasErrors()) {
            return VIEWS_VISIT_FORM;
        }

        saveVisit(visit);
        return REDIRECT_TO_VISIT_OWNER;
    }

    private void saveVisit(Visit visit) {
        this.clinicService.saveVisit(visit);
    }

    @GetMapping(value = "/owners/{ownerId}/pets/{petId}/visits")
    public String showVisits(@PathVariable int petId, Map<String, Object> model) {
        addVisitsToModel(petId, model);
        return VIEWS_VISIT_LIST;
    }

    private void addVisitsToModel(int petId, Map<String, Object> model) {
        model.put(MODEL_ATTRIBUTE_VISITS, this.clinicService.findPetById(petId).getVisits());
    }

}
