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
package org.springframework.samples.petclinic.repository.jpa;

import java.util.Collection;
import java.util.List;

import jakarta.persistence.EntityManager;
import jakarta.persistence.Query;

import org.springframework.samples.petclinic.model.Owner;
import org.springframework.samples.petclinic.repository.OwnerRepository;
import org.springframework.stereotype.Repository;

/**
 * JPA implementation of the {@link OwnerRepository} interface.
 *
 * @author Mike Keith
 * @author Rod Johnson
 * @author Sam Brannen
 * @author Michael Isvy
 * @since 22.4.2006
 */
@Repository
public class JpaOwnerRepositoryImpl implements OwnerRepository {

    private final EntityManager em;

    public JpaOwnerRepositoryImpl(EntityManager em) {
        this.em = em;
    }

    /**
     * Important: in the current version of this method, we load Owners with all their Pets and Visits while
     * we do not need Visits at all, and we only need one property from the Pet objects (the 'name' property).
     * There are some ways to improve it such as:
     * - creating a Lightweight class
     * - Turning on lazy-loading and using the open session in view pattern
     */
    @SuppressWarnings("unchecked")
    public Collection<Owner> findByLastName(String lastName) {
        // using 'join fetch' because a single query should load both owners and pets
        // using 'left join fetch' because it might happen that an owner does not have pets yet
        Query query = this.em.createQuery("SELECT DISTINCT owner FROM Owner owner left join fetch owner.pets WHERE owner.lastName LIKE :lastName");
        query.setParameter("lastName", lastName + "%");
        return query.getResultList();
    }

    /**
     * AECF_META: skill=aecf_new_feature topic=owner_pagination run_time=2026-04-17T00:00:00Z
     * generated_at=2026-04-17T00:00:00Z generated_by=lvillara touch_count=1
     * last_modified_skill=aecf_new_feature last_modified_at=2026-04-17T00:00:00Z last_modified_by=lvillara
     *
     * Returns a page of owners whose last name starts with the given prefix.
     * Uses setFirstResult/setMaxResults on a join-fetch query — Hibernate may apply
     * in-memory pagination (HHH90003004) for correctness with collection fetch.
     */
    @SuppressWarnings("unchecked")
    @Override
    public Collection<Owner> findByLastName(String lastName, int page, int pageSize) {
        Query query = this.em.createQuery(
            "SELECT DISTINCT owner FROM Owner owner left join fetch owner.pets " +
            "WHERE owner.lastName LIKE :lastName ORDER BY owner.lastName, owner.id");
        query.setParameter("lastName", lastName + "%");
        query.setFirstResult((page - 1) * pageSize);
        query.setMaxResults(pageSize);
        return (List<Owner>) query.getResultList();
    }

    /**
     * AECF_META: skill=aecf_new_feature topic=owner_pagination run_time=2026-04-17T00:00:00Z
     * generated_at=2026-04-17T00:00:00Z generated_by=lvillara touch_count=1
     * last_modified_skill=aecf_new_feature last_modified_at=2026-04-17T00:00:00Z last_modified_by=lvillara
     *
     * Counts owners whose last name starts with the given prefix.
     */
    @Override
    public int countByLastName(String lastName) {
        Query query = this.em.createQuery(
            "SELECT COUNT(DISTINCT owner) FROM Owner owner WHERE owner.lastName LIKE :lastName");
        query.setParameter("lastName", lastName + "%");
        return ((Long) query.getSingleResult()).intValue();
    }

    @Override
    public Owner findById(int id) {
        // using 'join fetch' because a single query should load both owners and pets
        // using 'left join fetch' because it might happen that an owner does not have pets yet
        Query query = this.em.createQuery("SELECT owner FROM Owner owner left join fetch owner.pets WHERE owner.id =:id");
        query.setParameter("id", id);
        return (Owner) query.getSingleResult();
    }


    @Override
    public void save(Owner owner) {
        if (owner.getId() == null) {
            this.em.persist(owner);
        } else {
            this.em.merge(owner);
        }

    }

}
