from typing import List, Dict, Tuple, Union, Optional
import uuid
from datetime import datetime
from enum import Enum
from pydantic import BaseModel, Field


class EntityType(Enum):
    IND = "ind"
    TEAM = "team"
    ORG = "org"
    
    

class Responses(BaseModel):
    """
    Usage example
    response_example = Responses(
        my_world=["A place of unity and respect"],
        my_planet=["A shared home for all beings"],
        care_physical=["Regular exercise", "Healthy eating"],
        care_mental=["Meditation", "Reading"],
        my_activities=["Public speaking", "Writing"],
        my_resources=["Books", "Community support"],
        care_who=["Family", "Nation"],
        how_cherish=["Promoting sustainability", "Educating others"],
        do_more=["Listening to diverse perspectives",
                "Engaging in community service"],
        do_less=["Spending time on trivial matters", "Neglecting self-care"],
        my_intent=["To foster a world of equality and understanding"]
    )
    """
    id: uuid.UUID = Field(default_factory=uuid.uuid4,
                        description="Unique identifier of the responses",
                        examples=["6c1ddca9-596f-492b-9420-6289058eb34f"])
    type: EntityType = Field(default=EntityType.IND, description="The type of entity that created the Intent statement")
    my_world: List[str] = Field(
        description="1. What is your world?")
    my_planet: List[str] = Field(
        description="2. What is 'the planet' is for you?")
    care_physical: List[str] = Field(
        description="3. How do you care for your physical well-being?")
    care_mental: List[str] = Field(
        description="4. How do you care for your mental well-being?")
    my_activities: List[str] = Field(
        description="5. What are your activities?")
    my_resources: List[str] = Field(
        description="6. What are your resources?")
    care_who: List[str] = Field(
        description="7. Who do you care about?")
    how_cherish: List[str] = Field(
        description="8. How do you cherish the planet?")
    do_more: List[str] = Field(
        description="9. What do you need to do more of?")
    do_less: List[str] = Field(
        description="10. What do you need to do less of?")
    my_intent: List[str] = Field(
        description="My Intent For the Planet")

    def responses(self):
        """Access the model's schema to get field descriptions
        
        Example usage
        print(response_example.responses())
        """
        schema = self.model_json_schema()["properties"]
        filtered_dict = {}
        for key, value in self.model_dump().items():
            if key in [
                "my_world", "my_planet", "care_physical", "care_mental", "my_activities",
                "my_resources", "care_who", "how_cherish", "do_more", "do_less", "my_intent"
            ]:
                description = schema[key].get("description", key)  # Fallback to key if no description
                # Join list values with '\n' to make them look nicer in text
                filtered_dict[description] = '<br>'.join(value) if isinstance(value, list) else value

        return filtered_dict



class Session(BaseModel):
    """
    Information regarding the Intent session, including the responses
    
    Usage examples
    session_example = Session(facilitator=4, responses=responses_example)

    Print all the session responses    
    print(session_example.responses.responses())
    
    Print the intent statement
    print(example_session.responses.my_intent)
    """
    id: uuid.UUID = Field(default_factory=uuid.uuid4,
                        description="Unique identifier of the session",
                        examples=["6c1ddca9-596f-492b-9420-6289058eb34f"])
    session_date: datetime = Field(default_factory=datetime.now,
        description="The date and time when the session occured in ISO 8601 format. This field is automatically populated when the session object is instatntiated.",
        examples=["2024-01-08T12:00:00Z"])
    facilitator: int = Field(
        description="creation number of the facilitator. This will migrate to uuid in future")
    language: str = Field(
        default='en', description="The language in which the Intent statement is written. Written as ISO 639 two-letter abbreviation (e.g., 'en' for English, 'es' for Spanish)",
        examples=["en", "es"])
    responses: Responses = Field(
        description="Structured responses from the session")
    
    

class Entity(BaseModel):
    """Base class for an entity creating an Intent statement."""
    id: uuid.UUID = Field(default_factory=uuid.uuid4,
                        description="Unique identifier of the entity")
    creation_num: Optional[int] = Field(
        description="The number of entities that have created an Intent statement at the time this entity created its first such statement.")
    haplotype: Optional[str] = Field(
        description="A code representing the lineage of the respondent as non-zero integers separated by dots", pattern=r'^[1-9]\d*(\.[1-9]\d*)*$',
        examples=["3.5.1.2"])
    session: Session = Field(
        description="Session encapsulates all session-related info including session id, facilitator, and responses")
    statement_log: List[Dict[str, Union[List[str], datetime]]] = Field(
        default_factory=list, description="History of Intent statements made by the entity.")

    def __init__(self, **data):
        super().__init__(**data)  # Call the super class __init__ to handle standard initialization
        # Automatically add the first entry to statement_log based on session information
        if self.session:  # Ensure session is provided
            self.statement_log.append({ # pylint: disable=no-member
                "intent": self.session.responses.my_intent, # pylint: disable=no-member
                "session_date": self.session.session_date # pylint: disable=no-member
            })

    @property
    def created_at(self) -> datetime:
        """Gets the Initial date for the Entity based on the date of that entity's first Intent statement."""
        if self.statement_log:
            updated_at = self.statement_log[0].get('updated_at') # pylint: disable=unsubscriptable-object
            if isinstance(updated_at, datetime):
                return updated_at
            else:
                raise ValueError("Expected a datetime object for 'updated_at'")
        return None
    

    @property
    def get_most_recent_intent_statement(self):
        """Most recent Intent statement."""
        if self.statement_log:
            return self.statement_log[-1] # pylint: disable=unsubscriptable-object
        return None
    


class Individual(Entity):
    """The person who has created an Intent statement.
    
    Usage example
    example_indvidividual = Individual(session=example_session)"""
    


class Team(Entity):
    """PLACEHOLDER CLASS The team that has created an Intent statement."""
    ids: List[uuid.UUID] = Field(
        description="List of individual IDs from the class Individual", examples=["6c1ddca9-596f-492b-9420-6289058eb34f","380b3fbe-68c3-448a-a57b-902fefadc6c6"])



class Organization(Entity):
    """PLACEHOLDER CLASS The organization that has created an Intent statement."""
    members: List[Tuple[str, uuid.UUID]] = Field(
        description="List of tuples, each containing a type (ind or team) and an entity UUID",
        examples=[[
                ("ind", "f334be7b-7ccc-4a00-ae56-2dd079029ddb"),
                ("ind", "c450d91d-0e81-4129-a702-ba8243e3e2e2"),
                ("ind", "cd97e8dc-1913-4841-aa78-d5edc5469793")
            ]])

    """
    Usage example
    organization = Organization(
    creation_num=2,
    session = session_example,
        ids=[
            ("ind", "f334be7b-7ccc-4a00-ae56-2dd079029ddb"),
            ("ind", "c450d91d-0e81-4129-a702-ba8243e3e2e2"),
            ("ind", "cd97e8dc-1913-4841-aa78-d5edc5469793")
        ]
    )
    """



class IntentStatement(BaseModel):
    """
    PLACEHOLDER CLASS An instance of this class represents a single intent statement made by the entity. We may not need this class at all since intent statements are easily accessible through the responses, session, and entity classes. If we do use this, we'll need to sort out how to assign the dates below.
    """
    id: uuid.UUID = Field(default_factory=uuid.uuid4,
                        description="The unique identifier of the Intent", examples=["380b3fbe-68c3-448a-a57b-902fefadc6c6"])
    entity_id: uuid.UUID = Field(
        description="The ID of the entity that created the statement")
    type: EntityType = Field(default=EntityType.IND, description="The type of entity that created the Intent statement")
    name: Optional[str] = Field(description="The name of the Intent")
    statement: List[str] = Field(
        default_factory=list, description="The Intent statement. Supports a statement that is a list")
    updated_at: datetime = Field(
        description="The date and time when the Intent statement was last updated. For the first version of an Intent, this is the creation date in ISO 8601 format", examples=["2024-01-08T12:00:00Z"])
    language: str = Field(
        default='en', description="The language in which the Intent statement is written (e.g., 'en' for English, 'es' for Spanish)", examples=["en", "es"])

    """
    Usage example
    intent_statement = IntentStatement(
        creator=session.facilitator,  # or another appropriate field for creator
        language=session.language,
        statement=session.responses.my_intent
    )
    """


class IntentsCollection(BaseModel):
    """
    PLACEHOLDER CLASS If we plan to perform operations on a collection of intent statements as a whole (e.g., filtering, sorting, aggregating, or managing intents in groups), we might consider having a separate class to represent a collection of intents. The IntentsCollection class, could contain methods and properties for working with multiple intent statements.
    """
    
    intents: List[IntentStatement] = []

    def add_intent(self, intent: IntentStatement):
        self.intents.append(intent)

    def get_intent_by_id(self, id: uuid.UUID):
        for intent in self.intents:
            if intent.id == id:
                return intent
        return None

