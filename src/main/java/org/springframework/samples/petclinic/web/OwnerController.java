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

import java.util.Collection;
import java.util.Map;

import jakarta.validation.Valid;

import org.springframework.samples.petclinic.model.Owner;
import org.springframework.samples.petclinic.service.ClinicService;
import org.springframework.stereotype.Controller;
import org.springframework.ui.Model;
import org.springframework.validation.BindingResult;
import org.springframework.web.bind.WebDataBinder;
import org.springframework.web.bind.annotation.*;
import org.springframework.web.servlet.ModelAndView;

/**
 * @author Juergen Hoeller
 * @author Ken Krebs
 * @author Arjen Poutsma
 * @author Michael Isvy
 */
@Controller
public class OwnerController {

    private static final String VIEWS_OWNER_CREATE_OR_UPDATE_FORM = "owners/createOrUpdateOwnerForm";
    private static final String VIEWS_OWNER_FIND_OWNERS = "owners/findOwners";
    private static final String VIEWS_OWNER_LIST = "owners/ownersList";
    private static final String VIEWS_OWNER_DETAILS = "owners/ownerDetails";
    private static final String MODEL_ATTRIBUTE_OWNER = "owner";
    private static final String MODEL_ATTRIBUTE_SELECTIONS = "selections";
    private static final String OWNER_EDIT_PATH = "/owners/{ownerId}/edit";
    private static final String OWNER_NEW_PATH = "/owners/new";
    private static final String REDIRECT_TO_OWNERS = "redirect:/owners/";
    private static final String REDIRECT_TO_OWNER = "redirect:/owners/{ownerId}";
    private final ClinicService clinicService;

    public OwnerController(ClinicService clinicService) {
        this.clinicService = clinicService;
    }

    @InitBinder
    public void setAllowedFields(WebDataBinder dataBinder) {
        dataBinder.setDisallowedFields("id");
    }

    @GetMapping(value = OWNER_NEW_PATH)
    public String initCreationForm(Map<String, Object> model) {
        initializeOwnerModel(model);
        return VIEWS_OWNER_CREATE_OR_UPDATE_FORM;
    }

    @PostMapping(value = OWNER_NEW_PATH)
    public String processCreationForm(@Valid Owner owner, BindingResult result) {
        if (result.hasErrors()) {
            return VIEWS_OWNER_CREATE_OR_UPDATE_FORM;
        }

        this.clinicService.saveOwner(owner);
        return buildOwnerRedirect(owner.getId());
    }

    @GetMapping(value = "/owners/find")
    public String initFindForm(Map<String, Object> model) {
        initializeOwnerModel(model);
        return VIEWS_OWNER_FIND_OWNERS;
    }

    private void initializeOwnerModel(Map<String, Object> model) {
        model.put(MODEL_ATTRIBUTE_OWNER, new Owner());
    }

    @GetMapping(value = "/owners")
    public String processFindForm(Owner owner, BindingResult result, Map<String, Object> model) {
        normalizeLastName(owner);

        // allow parameterless GET request for /owners to return all records
        // find owners by last name
        Collection<Owner> results = findMatchingOwners(owner);
        if (results.isEmpty()) {
            return handleNoOwners(result);
        }
        if (results.size() == 1) {
            return handleSingleOwner(results);
        }
        return handleMultipleOwners(model, results);
    }

    private void normalizeLastName(Owner owner) {
        // Empty string signifies broadest possible search.
        if (owner.getLastName() == null) {
            owner.setLastName("");
        }
    }

    private Collection<Owner> findMatchingOwners(Owner owner) {
        return this.clinicService.findOwnerByLastName(owner.getLastName());
    }

    private String handleNoOwners(BindingResult result) {
        result.rejectValue("lastName", "notFound", "not found");
        return VIEWS_OWNER_FIND_OWNERS;
    }

    private String handleSingleOwner(Collection<Owner> results) {
        return buildOwnerRedirect(results.iterator().next().getId());
    }

    private String buildOwnerRedirect(Integer ownerId) {
        return REDIRECT_TO_OWNERS + ownerId;
    }

    private String handleMultipleOwners(Map<String, Object> model, Collection<Owner> results) {
        model.put(MODEL_ATTRIBUTE_SELECTIONS, results);
        return VIEWS_OWNER_LIST;
    }

    @GetMapping(value = OWNER_EDIT_PATH)
    public String initUpdateOwnerForm(@PathVariable("ownerId") int ownerId, Model model) {
        addOwnerToModel(model, ownerId);
        return VIEWS_OWNER_CREATE_OR_UPDATE_FORM;
    }

    private void addOwnerToModel(Model model, int ownerId) {
        model.addAttribute(MODEL_ATTRIBUTE_OWNER, this.clinicService.findOwnerById(ownerId));
    }

    @PostMapping(value = OWNER_EDIT_PATH)
    public String processUpdateOwnerForm(@Valid Owner owner, BindingResult result, @PathVariable("ownerId") int ownerId) {
        if (result.hasErrors()) {
            return VIEWS_OWNER_CREATE_OR_UPDATE_FORM;
        }

        owner.setId(ownerId);
        this.clinicService.saveOwner(owner);
        return REDIRECT_TO_OWNER;
    }

    /**
     * Custom handler for displaying an owner.
     *
     * @param ownerId the ID of the owner to display
     * @return a ModelMap with the model attributes for the view
     */
    @GetMapping("/owners/{ownerId}")
    public ModelAndView showOwner(@PathVariable("ownerId") int ownerId) {
        return buildOwnerDetailsView(ownerId);
    }

    private ModelAndView buildOwnerDetailsView(int ownerId) {
        return new ModelAndView(VIEWS_OWNER_DETAILS).addObject(this.clinicService.findOwnerById(ownerId));
    }

}
