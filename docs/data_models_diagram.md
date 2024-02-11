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
        +Individual representative
        +List Individual
    }
    class Organization {
        +Individual representative
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

    Session --* "1" Responses : contains
    Steward <|-- Individual : isA
    Steward <|-- Team : isA
    Steward <|-- Organization : isA
    Individual --o "*" Session : has
    Team --o "*" Session : has
    Organization --o "*" Session : has

```

</div>

## 
THE WELL is about INTENTs. It holds the INTENT statements and associated responses. It creates a resource --collective wisdom-- out of them.
STEWARD is about identity. It authenticates, maintains and protects identity information. It initiates all creation and changes to INTENT statements.


### Initial flow: 
1. The first Steward object is created by hand   
2. A Response object is created. 
3. A Session object is created. It contains the partifipant, facilitator, scribe and the responses
4. An Individual is created. It contains reference to their session

### Create an initial INTENT Statement
1. Individual facilitator authenticates with STEWARD and inputs Steward participant details (this is the representative in the case of a Team or Org) along with other details of the session (e.g., scribe, language)
3. STEWARD initializes a Steward class object (Ind, Team, or Org), sends consent request to Individual participant
4. Individual participant consents to STEWARD
5. STEWARD sends a Session_id to THE WELL
6. Participant creates a responses
7. Scribe populates THE WELL form with responses and submits 
8. THE WELL stores Reponses with session_id as temp and informs STEWARD 
9. STEWARD sends responses to partipant and facilitator
10. Participant receives thank you from STEWARD with responses, consent form, and link to their info
11. STEWARD informs THE WELL, assigns creation number, faciltator gets credit
12. THE WELL to publishes session  

## UPDATE and INTENT STATEMENT
