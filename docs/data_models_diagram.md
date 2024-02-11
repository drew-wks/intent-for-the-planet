## INTENT Data Models Diagram

<div style="border: 2px solid black; padding: 10px;">

```mermaid
classDiagram
    class Steward {
        +uuid steward_id
        +Optional int creation_num
        +Optional str haplotype
        + str species**
        +Session session
        +List statement_log
    }
    class Individual {
    }
    class Team {
        +Individual representative**
        +List Individual
    }
    class Organization {
        +Individual representative**
        +Optional List Team
        +Optional List Individual
    }
    class Session {
        +datetime session_date
        +Individual participant
        +Individual facilitator
        +Individual scribe
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
        +uuid intent_id
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
    Individual <|-- participant
    Individual <|-- facilitator
    Individual <|-- representative
    Individual <|-- scribe
    Team --o "1" Session : has
    Organization --o "1" Session : has

```

</div>

## 
THE WELL is about INTENTs. It holds the INTENT statements and associated responses. It creates a resource --collective wisdom-- out of them.
STEWARD is about identity. It authenticates, maintains and protects identity information. It initiates all creation and changes to INTENT statements.


### Initial flow: 
1. The first Entity object is created by hand   
2. A response object is created. 
3. A session object is created. It contains the facilitator entity and the responses
4. An entity is created. It contains reference to their session

### Create an initial INTENT Statement
1. Facilitator authenticates with STEWARD and provides participant contact info
3. STWEARD initializes a Steward object, sends consent request to participant
4. Participant consents
5. STEWARD sends a unique ID to THE WELL
6. Participant creates a responses 
7. Facilitator populates THE WELL form with responses and submits 
8. THE WELL stores reponses with unique ID as temp and informs STEWARD 
9. STEWARD sends to partipant and facilitator
10. Participant receives thank you from STEWARD with responses and consent form
11. STEWARD informs THE WELL, assigns creation number, faciltator gets credit
12. THE WELL to publishes session  

## UPDATE and INTENT STATEMENT
