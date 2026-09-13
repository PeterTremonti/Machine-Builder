# Machine Builder Relationship Matrix
## O0.1 Minimum Scope

The relationship vocabulary is semantic. Visual lines are views of relationships and are not themselves canonical relationships.

| Relationship | Source → Target | O0.1 use | Notes |
|---|---|---|---|
| contains | Machine/Subsystem → contained Object | Structure | Hierarchical containment |
| part_of | Object → parent Object | Structure | Inverse/related containment |
| classified_as | Object → Classification | Identity/type | Classification is not Role |
| has_role | Object → Role | Context | Role can vary by machine context |
| mounted_on | Component → Component/Structure | Physical | Mounting relation |
| connected_to | Electrical endpoint → Electrical endpoint | Electrical | Physical connectivity |
| assigned_to | Component/Function → Controller Resource | Allocation | Context-specific allocation |
| drives | Drive/Actuator → Axis/physical target | Motion | Supports many-to-many where required |
| realizes | Machine element → Function | Functional realization | Meaning must remain distinct from firmware implementation |
| supports | Component/Resource → Function/Capability | Support | Does not imply ownership of behavior |
| requires | Function/Component → Resource/condition | Dependency | Context-sensitive |
| measures | Sensor → Measurand/physical quantity | Sensing | Sensor is not result |
| uses | Function/Component → Resource/Component | Use dependency | General but not unlimited substitute for precise relations |
| decomposes_into | Function → Function | Function structure | Same semantic level |
| participates_in | Function/Object → Process/Activity | Deferred/limited | Existing research relationship; richer process model deferred |
| maps_to | Canonical concept ↔ Firmware representation | Translation | Version-specific possible |
| derived_from | Derived fact/value → supporting facts | Provenance | Keep lineage |
| validated_by | Fact/Result → Evaluation/Rule | Validation | Derived information |
| specified_by | Property/Requirement → source/specification | Evidence | Preserve source context |
| provides_capability | Machine element → Capability | Capability | Distinct from Function |
| decomposes | Resource/system → subresource | Resource structure | Use if needed by implementation |

## Cardinality principle

Multiplicity belongs to the relationship definition. O0.1 permits:

- one-to-one
- one-to-many
- many-to-one
- many-to-many

where semantically justified.

Contextual constraints may further restrict a relationship without changing the underlying ontology.

## Direction principle

Physical electrical connections are normally nondirectional.

Semantic signal/interaction direction is represented where the relevant semantic interface or transfer requires it.

## First-class relationship principle

Not every edge requires an independent object in storage. A relationship becomes first-class when the relationship itself needs identity, properties, context, lifecycle, provenance, or other semantics that cannot be represented adequately by its endpoints and relationship type.
