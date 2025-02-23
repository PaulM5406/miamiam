from dataclasses import dataclass
from datetime import datetime


@dataclass
class Establishment:
    """
    Represents a food & beverage establishment from the SIRENE database.

    This class contains the essential information about a business establishment
    in France, focused on restaurants, cafes, and similar establishments.

    Attributes:
        siret: The unique 14-digit SIRET number identifying the establishment
        name: Official registered name of the establishment
        address: Street address of the establishment
        postal_code: 5-digit French postal code
        city: City/commune name
        activity_code: 5-character NAF/APE code indicating the primary business activity
        creation_date: Date when the establishment was officially registered
    """

    siret: str
    name: str
    address: str
    postal_code: str
    city: str
    activity_code: str  # NAF/APE code
    creation_date: datetime
