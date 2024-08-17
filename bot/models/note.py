"""
This module provides a Note class to create and manage notes with text and optional tags.

Classes:
- Note: Represents a note with text and optional tags.

Example usage:
    note = Note(
        text="This is a sample note.",
        tags=["sample", "note"]
    )
    note.add_tag("example")
    print(note)
"""

import uuid
from datetime import datetime
from typing import List

class Note:
    """
    Represents a note with text and optional tags.

    Args:
    - text (str): The content of the note.
    - tags (List[str], optional): A list of tags associated with the note. Defaults to None.

    Attributes:
    - id (str): A unique identifier for the note.
    - create_date (datetime): The date and time when the note was created.
    - text (str): The content of the note.
    - tags (List[str]): A list of tags associated with the note.
    """

    def __init__(self, text, tags: List[str] = None):
        """
        Initializes a new Note instance.

        Args:
        - text (str): The content of the note.
        - tags (List[str], optional): A list of tags associated with the note. Defaults to None.
        """
        self.id = str(uuid.uuid4())
        self.create_date = datetime.now()
        self.text = text
        self.tags = tags if tags else []

    def add_tag(self, tag):
        """
        Adds a tag to the note if it is not already present.

        Args:
        - tag (str): The tag to be added.
        """
        if tag not in self.tags:
            self.tags.append(tag)

    def remove_tag(self, tag):
        """
        Removes a tag from the note if it is present.

        Args:
        - tag (str): The tag to be removed.
        """
        if tag in self.tags:
            self.tags.remove(tag)

    def __str__(self):
        """
        Returns a string representation of the note.

        Returns:
        - str: A string representation of the note.
        """
        s = f"{self.id} | {self.create_date.strftime('%Y-%m-%d %H:%M:%S')} | {self.text}"
        if self.tags:
            s += f" ({', '.join(self.tags)})"
        return s
