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

import org.springframework.samples.petclinic.model.Owner;
import org.springframework.samples.petclinic.model.Pet;
import org.springframework.samples.petclinic.model.PetType;
import org.springframework.samples.petclinic.service.ClinicService;
import org.springframework.stereotype.Controller;
import org.springframework.ui.ModelMap;
import org.springframework.util.StringUtils;
import org.springframework.validation.BindingResult;
import org.springframework.web.bind.WebDataBinder;
import org.springframework.web.bind.annotation.*;

import jakarta.validation.Valid;

import java.util.Collection;

/**
 * @author Juergen Hoeller
 * @author Ken Krebs
 * @author Arjen Poutsma
 */
@Controller
@RequestMapping("/owners/{ownerId}")
public class PetController {

    private static final String VIEWS_PETS_CREATE_OR_UPDATE_FORM = "pets/createOrUpdatePetForm";
    private static final String MODEL_ATTRIBUTE_PET = "pet";
    private static final String PET_EDIT_PATH = "/pets/{petId}/edit";
    private static final String PET_NEW_PATH = "/pets/new";
    private static final String MODEL_ATTRIBUTE_OWNER = "owner";
    private static final String VIEW_REDIRECT_OWNERS = "redirect:/owners/{ownerId}";
    private final ClinicService clinicService;

    public PetController(ClinicService clinicService) {
        this.clinicService = clinicService;
    }

    @ModelAttribute("types")
    public Collection<PetType> populatePetTypes() {
        return this.clinicService.findPetTypes();
    }

    @ModelAttribute(MODEL_ATTRIBUTE_OWNER)
    public Owner findOwner(@PathVariable("ownerId") int ownerId) {
        return this.clinicService.findOwnerById(ownerId);
    }

    @InitBinder(MODEL_ATTRIBUTE_OWNER)
    public void initOwnerBinder(WebDataBinder dataBinder) {
        dataBinder.setDisallowedFields("id");
    }

    @InitBinder(MODEL_ATTRIBUTE_PET)
    public void initPetBinder(WebDataBinder dataBinder) {
        dataBinder.setValidator(new PetValidator());
    }

    @GetMapping(value = PET_NEW_PATH)
    public String initCreationForm(Owner owner, ModelMap model) {
        addPetToModel(owner, model);
        return VIEWS_PETS_CREATE_OR_UPDATE_FORM;
    }

    private void addPetToModel(Owner owner, ModelMap model) {
        Pet pet = new Pet();
        owner.addPet(pet);
        model.put(MODEL_ATTRIBUTE_PET, pet);
    }

    @PostMapping(value = PET_NEW_PATH)
    public String processCreationForm(Owner owner, @Valid Pet pet, BindingResult result, ModelMap model) {
        return savePetFormResult(owner, pet, result, model, hasDuplicatePetName(owner, pet));
    }

    private boolean hasDuplicatePetName(Owner owner, Pet pet) {
        return StringUtils.hasLength(pet.getName()) && pet.isNew() && owner.getPet(pet.getName(), true) != null;
    }

    @GetMapping(value = PET_EDIT_PATH)
    public String initUpdateForm(@PathVariable("petId") int petId, ModelMap model) {
        model.put(MODEL_ATTRIBUTE_PET, this.clinicService.findPetById(petId));
        return VIEWS_PETS_CREATE_OR_UPDATE_FORM;
    }

    @PostMapping(value = PET_EDIT_PATH)
    public String processUpdateForm(@Valid Pet pet, BindingResult result, Owner owner, ModelMap model) {
        return savePetFormResult(owner, pet, result, model, false);
    }

    private void savePetForOwner(Owner owner, Pet pet) {
        owner.addPet(pet);
        this.clinicService.savePet(pet);
    }

    private String savePetFormResult(Owner owner, Pet pet, BindingResult result, ModelMap model, boolean duplicate) {
        if (duplicate) {
            result.rejectValue("name", "duplicate", "already exists");
        }
        if (result.hasErrors()) {
            return showPetForm(model, pet);
        }

        savePetForOwner(owner, pet);
        return VIEW_REDIRECT_OWNERS;
    }

    private String showPetForm(ModelMap model, Pet pet) {
        model.put(MODEL_ATTRIBUTE_PET, pet);
        return VIEWS_PETS_CREATE_OR_UPDATE_FORM;
    }

}
