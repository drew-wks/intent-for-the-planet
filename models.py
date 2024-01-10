from typing import List, Dict, Tuple, Union, Optional
from pydantic import BaseModel, Field, field_validator, constr
import uuid
import re
from datetime import datetime


class Responses(BaseModel):
    type: str = Field(default='ind', description="The type of creator of the Intent statement", enum=[
                      "ind", "team", "org"])
    my_world: List[str] = Field(
        description="Response for '1. What is your world?'")
    my_planet: List[str] = Field(
        description="Response for '2. What is 'the planet' is for you?'")
    care_physical: List[str] = Field(
        description="Response for '3. How do you care for your physical well-being?'")
    care_mental: List[str] = Field(
        description="Response for '4. How do you care for your mental well-being?'")
    my_activities: List[str] = Field(
        description="Response for '5. What are your activities?'")
    my_resources: List[str] = Field(
        description="Response for '6. What are your resources?'")
    who_care: List[str] = Field(
        description="Response for '7. Who do you care about?'")
    how_cherish: List[str] = Field(
        description="Response for '8. How do you cherish the planet?'")
    do_more: List[str] = Field(
        description="Response for '9. What do you need to do more of?'")
    do_less: List[str] = Field(
        description="Response for '10. What do you need to do less of?'")
    my_intent: List[str] = Field(
        description="Response for 'My Intent For the Planet'")

    """
    Usage example

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
    session = Session(
        facilitator=4,
        language='en',
        responses=Responses
    )
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

    """
    Usage example

    """


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
        description="List of tuples, each containing a type ('team' or 'individual') and a UUID")
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
    creator: uuid.UUID = Field(
        description="The unique identifier of the creator (from class Individual)")
    type: str = Field(default='ind', description="The type of creator of the Intent statement", enum=[
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