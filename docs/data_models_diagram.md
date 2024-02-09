## INTENT Data Models Diagram

<div style="border: 2px solid black; padding: 10px;">

```mermaid
classDiagram
    class Entity {
        +uuid entity_id
        +Optional int creation_num
        +Optional str haplotype
        +Session session
        +List statement_log
    }
    class Individual {
    }
    class Team {
        +List ids
    }
    class Organization {
        +List members
    }
    class Session {
        +datetime session_date
        +uuid facilitator
        +Responses responses
        +str language
        +uuid session_id
    }
    class Responses {
        +uuid responses_id
        +str type
        +List my_world
        +List my_planet
        +List care_physical
        +List care_mental
        +List my_activities
        +List my_resources
        +List who_care
        +List how_cherish
        +List do_more
        +List do_less
        +List my_intent
    }
    class IntentStatement {
        +uuid id
        +uuid creator
        +str type
        +Optional str name
        +List statement
        +datetime updated_at
        +str language
    }
    class IntentsCollection {
        +List intents
    }
    IntentsCollection --* IntentStatement : contains
    Session --* "1" Responses : contains
    Entity <|-- Individual : isA
    Entity <|-- Team : isA
    Entity <|-- Organization : isA
    Session--|> "1" IntentStatement : creates
    Individual --o "1" Session : has
    Team --o "1" Session : has
    Organization --o "1" Session : has

```

</div>

### Initial flow: 
1. The first Entity object is created by hand   
2. A response object is created. 
3. A session object is created. It contains the facilitator entity and the responses
4. An entity is created. It contains reference to their session
