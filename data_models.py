from typing import List, Dict, Tuple, Union, Optional
from pydantic import BaseModel, Field, field_validator, constr
import uuid
from datetime import datetime
import json


class Responses(BaseModel):
    id: uuid.UUID = Field(default_factory=uuid.uuid4, description="Unique identifier of the responses")
    type: str = Field(default='ind', description="The type of entity that created the Intent statement", enum=[
                      "ind", "team", "org"])
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
        # Access the model's schema to get field descriptions
        schema = self.model_json_schema()["properties"]
        filtered_dict = {}
        for key, value in self.model_dump().items():
            if key in [
                "my_world", "my_planet", "care_physical", "care_mental", "my_activities",
                "my_resources", "care_who", "how_cherish", "do_more", "do_less", "my_intent"
            ]:
                description = schema[key].get("description", key)  # Fallback to key if no description
                # Join list values with '\n' to make them look nicer in text
                filtered_dict[description] = '\n'.join(value) if isinstance(value, list) else value

        # Convert the filtered dictionary to a JSON string
        return json.dumps(filtered_dict, ensure_ascii=False, indent=4)


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

    print(response_example.responses())
    """


class Session(BaseModel):
    id: uuid.UUID = Field(default_factory=uuid.uuid4,
                          description="Unique identifier of the session")
    facilitator: int = Field(
        description="creation number of the facilitator. This will migrate to uuid in future")
    language: str = Field(
        default='en', description="The language in which the Intent statement is written (e.g., 'en' for English, 'es' for Spanish)")
    responses: Responses = Field(
        description="Structured responses from the session")

    """
    Usage example
    session_example = Session(
        facilitator=4,
        language='en',
        responses=Responses
    )
    
    
    """
    print(session_example.responses.responses())
    """


class Entity(BaseModel):
    """Base class for an entity (individual or organization) creating an Intent statement."""
    id: uuid.UUID = Field(default_factory=uuid.uuid4,
                          description="Unique identifier of the entity")
    creation_num: int = Field(
        description="The number of entities that have created an Intent statement at the time this entity created their first such statement.")
    haplotype: str = Field(
        description="A code representing the lineage of the respondent as non-zero integers separated by dots", pattern=r'^[1-9]\d*(\.[1-9]\d*)*$')
    session: Session = Field(
        description="Session encapsulates all session-related info including session id, facilitator, and responses")
    statement_log: List[Dict[str, Union[List[str], datetime]]] = Field(
        default_factory=list, description="History of Intent statements made by the entity.")

    @property
    def created_at(self) -> datetime:
        """Initial date as the date of the first Intent statement."""
        if self.statement_log:
            return self.statement_log[0]['updated_at']
        return None

    @property
    def most_recent_intent_statement(self):
        """Most recent Intent statement."""
        if self.statement_log:
            return self.statement_log[-1]
        return None
    


class Individual(Entity):
    """The person who has created an Intent statement."""
    # Additional fields or methods specific to Individual

    """
    individual = Individual(
        creation_num=1,
        responses=Responses(my_world=["My personal world view..."], ...)
    )
    """


class Team(Entity):
    """The team that has created an Intent statement."""
    ids: List[uuid.UUID] = Field(
        description="List of individual IDs from the class Individual")
    # Additional fields or methods specific to Organization


class Organization(Entity):
    """The organization that has created an Intent statement."""
    ids: List[Tuple[str, uuid.UUID]] = Field(
        description="List of tuples, each containing a type ('team' or 'individual') and an entity UUID")
    # Additional fields or methods specific to Organization

    """
    Usage example
    organization = Organization(
    creation_num=2,
    responses=Responses(my_world=["My personal world view..."], ...)
    member_ids=[uuid.uuid4(), uuid.uuid4()]
)
    """


class IntentStatement(BaseModel):
    """An instance of this class represents a statement made by the individual."""
    id: uuid.UUID = Field(default_factory=uuid.uuid4,
                          description="The unique identifier of the Intent")
    entity_id: uuid.UUID = Field(
        description="The ID of the entity that created the statement")
    type: str = Field(default='ind', description="The type of entity that created the Intent statement", enum=[
                      "ind", "team", "org"])
    name: Optional[str] = Field(description="The name of the Intent")
    statement: List[str] = Field(
        default_factory=list, description="The Intent statement")
    updated_at: datetime = Field(
        description="The date and time when the Intent statement was last updated. For the first version of an Intent, this is the creation date in ISO 8601 format", example="2024-01-08T12:00:00Z")
    language: str = Field(
        default='en', description="The language in which the Intent statement is written (e.g., 'en' for English, 'es' for Spanish)")

    """
    Usage example
    intent_statement = IntentStatement(
        creator=session.facilitator,  # or another appropriate field for creator
        language=session.language,
        statement=session.responses.my_intent
    )
    """


class IntentsCollection(BaseModel):
    """If we plan to perform operations on a collection of intent statements as a whole (e.g., filtering, sorting, aggregating, or managing intents in groups), we might consider having a separate class to represent a collection of intents. The IntentsCollection class, could contain methods and properties for working with multiple intent statements."""
    intents: List[IntentStatement] = []

    def add_intent(self, intent: IntentStatement):
        self.intents.append(intent)

    def get_intent_by_id(self, id: uuid.UUID):
        for intent in self.intents:
            if intent.id == id:
                return intent
        return None

    """
    Usage example

    """