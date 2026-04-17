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
package org.springframework.samples.petclinic.repository.springdatajpa;

import java.util.Collection;
import java.util.List;

import org.springframework.data.domain.PageRequest;
import org.springframework.data.domain.Pageable;
import org.springframework.data.jpa.repository.Query;
import org.springframework.data.repository.Repository;
import org.springframework.data.repository.query.Param;
import org.springframework.samples.petclinic.model.Owner;
import org.springframework.samples.petclinic.repository.OwnerRepository;

/**
 * Spring Data JPA specialization of the {@link OwnerRepository} interface
 *
 * @author Michael Isvy
 * @since 15.1.2013
 */
public interface SpringDataOwnerRepository extends OwnerRepository, Repository<Owner, Integer> {

    @Override
    @Query("SELECT DISTINCT owner FROM Owner owner left join fetch owner.pets WHERE owner.lastName LIKE :lastName%")
    Collection<Owner> findByLastName(@Param("lastName") String lastName);

    @Override
    @Query("SELECT owner FROM Owner owner left join fetch owner.pets WHERE owner.id =:id")
    Owner findById(@Param("id") int id);

    /**
     * AECF_META: skill=aecf_new_feature topic=owner_pagination run_time=2026-04-17T00:00:00Z
     * generated_at=2026-04-17T00:00:00Z generated_by=lvillara touch_count=1
     * last_modified_skill=aecf_new_feature last_modified_at=2026-04-17T00:00:00Z last_modified_by=lvillara
     *
     * Spring Data internal method — applies Pageable to the join-fetch query.
     */
    @Query("SELECT DISTINCT owner FROM Owner owner left join fetch owner.pets " +
           "WHERE owner.lastName LIKE :lastName% ORDER BY owner.lastName, owner.id")
    List<Owner> findPagedByLastName(@Param("lastName") String lastName, Pageable pageable);

    @Override
    @Query("SELECT COUNT(DISTINCT owner) FROM Owner owner WHERE owner.lastName LIKE :lastName%")
    int countByLastName(@Param("lastName") String lastName);

    /**
     * AECF_META: skill=aecf_new_feature topic=owner_pagination run_time=2026-04-17T00:00:00Z
     * generated_at=2026-04-17T00:00:00Z generated_by=lvillara touch_count=1
     * last_modified_skill=aecf_new_feature last_modified_at=2026-04-17T00:00:00Z last_modified_by=lvillara
     *
     * Implements OwnerRepository contract by converting (page, pageSize) to a Pageable and
     * delegating to the Spring Data proxy method findPagedByLastName.
     */
    @Override
    default Collection<Owner> findByLastName(String lastName, int page, int pageSize) {
        return findPagedByLastName(lastName, PageRequest.of(page - 1, pageSize));
    }
}
