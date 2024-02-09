## INTENT Data Models Diagram

<div style="border: 2px solid black; padding: 10px;">

```mermaid
classDiagram
    class Steward {
        +uuid id *STEWARD
        +Optional int creation_num
        +Optional str haplotype
        + str species**
        +Session session
        +List statement_log
    }
    class Individual {
    }
    class Team {
        +Individual Representative**
        +List Individual
    }
    class Organization {
        +Individual Representative**
        +List Individual
    }
    class Session {
        +datetime session_date
        +Individual Facilitator
        +Individual Scribe
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
        +uuid participant**
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
    Steward <|-- Individual : isA
    Steward <|-- Team : isA
    Steward <|-- Organization : isA
    Session--|> "1" IntentStatement : creates
    Individual --o "1" Session : has
    Individual <|-- Facilitator
    Individual <|-- Representative
    Individual <|-- Scribe
    Team --o "1" Session : has
    Organization --o "1" Session : has

```

</div>

### Initial flow: 
1. The first Entity object is created by hand   
2. A response object is created. 
3. A session object is created. It contains the facilitator entity and the responses
4. An entity is created. It contains reference to their session
