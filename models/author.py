from pydantic import BaseModel, Field

# It should be noted that the descriptions for the Fields
# should be clear enough for the llm to interpret and use effectively.
# Otherwise, the results may not be as expected.
class Author(BaseModel):
    name: str = Field(description="The name of the author")
    number: int = Field(description="The number of books written by the author")
    books: list[str] = Field(description="The list of books written by the author")