from ...pybahn.structs import Products as Products
from _typeshed import Incomplete
from dataclasses import dataclass
from typing import List, Optional

class Serializable: ...

@dataclass
class Location(Serializable):
    latitude: str
    longitude: str

@dataclass
class BaseNamedStop(Serializable):
    evaNumber: str | None = ...
    name: str | None = ...
    canceled: bool | None = ...
    additional: bool | None = ...
    separation: bool | None = ...
    slug: str | None = ...
    displayPriority: int | None = ...
    nameParts: list | None = ...
    id = ...
    def __post_init__(self) -> None: ...

class StopPlace(BaseNamedStop): ...
class Destination(BaseNamedStop): ...
class Stop(BaseNamedStop): ...

class Message(Serializable):
    text: str
    locale: str
    type: str
    change: bool
    important: bool
    open: bool
    links: Incomplete
    def __init__(self, text, locale, type, change, important, open, links: list) -> None: ...

class Departure(Serializable):
    """
    Represents a real-time departure from a station.

    Includes platform, delay, scheduled/estimated times, and train information.
    Typically used for station boards or real-time monitoring.
    """

    canceled_stops_after_actual_destination: List[Stop]
    """List of cancelled stops after the actual destination the transport has reached."""

    origin: StopPlace
    """The station or stop where the transport originally departed from."""

    time_schedule: str
    """Scheduled departure time in ISO 8601 format."""

    time_delayed: str
    """Estimated (delayed) departure time in ISO 8601 format, if available."""

    is_delayed: bool
    """Indicates whether the departure is delayed."""

    platform: str
    """Actual platform number or name used for the departure, if different from the scheduled one."""

    platform_schedule: str
    """Scheduled platform number or name for the departure."""
    
    is_canceled: bool
    """Indicates whether the departure has been canceled."""

    lineName: str
    """Public-facing name of the line or service (e.g., RE5, S1)."""

    type: str
    """Type of transport service (e.g., train, bus, tram)."""

    current_position: StopPlace
    """Current known stop or position of the transport."""

    destination: Optional[Destination]
    """Final destination of the transport as planned."""

    stopovers: List[Stop]
    """List of all intermediate stops between the origin and destination."""

    additional_stops: List[Stop]
    """List of additional (non-scheduled or special) stops along the route."""

    canceled_stops: List[Stop]
    """List of originally scheduled stops that have been canceled."""

    messages: list
    """List of service or delay messages related to the departure."""

    provides_vehicle_sequence: bool
    """Indicates whether the departure provides detailed vehicle composition (e.g., wagon order)."""

    replacement_service_type: Incomplete
    """Information about replacement transport type if the departure is affected (e.g., bus instead of train)."""

    actual_destination: Destination
    """Updated actual destination of the transport based on current position or rerouting."""

    def __init__(self, canceledStopsAfterActualDestination: list | None = None, origin: str = '', actualDestination: str = '', direction: str = '', id: str = '', timeSchedule: str = '', timeDelayed: str = '', delayed: bool = False, platform: str = '', platformSchedule: str = '', timeType: str = '', canceled: bool = False, administrationID: str = '', virtual: bool = False, lineName: str = '', type: str = '', kind: str = '', journeyID: str = '', stopPlace: Incomplete | None = None, arrivalOrDepartureId: str = '', destination: Incomplete | None = None, viaStops: list[Stop] = [], additionalStops=[], canceledStops=[], messages=[], providesVehicleSequence: str = '', replacementServiceType: str = '') -> None: ...

class Station(Serializable):
    """
    Represents a public transport station or stop.

    Includes name, identifier values, geographical location, and available transport types.
    Typically used for searching, listing, or referencing transport hubs.
    """

    name: str
    """Human-readable name of the station (e.g., 'Berlin Hbf')."""

    id: str
    """Internal or external ID of the station, typically used for API requests or referencing."""

    lid: str
    """Logical ID (LID) of the station used for route planning or detailed queries."""

    location: Location
    """Geographic location of the station as a `Location` object (includes latitude and longitude)."""

    products: list[Products]
    """List of transport types (e.g., regional trains, buses, trams) available at this station."""
    
    def __init__(self, name: str, id: str, lid: str, lat: str, lon: str, products: list) -> None: ...

class Operator(Serializable):
    id: int
    has_shop: bool
    code: str
    description: str
    logo: str
    short_description: str
    def __init__(self, code, hatShop, kuerzel, description, logo, shortDescription) -> None: ...

class J_StopOver(Serializable):
    """
    Represents a stopover (station) within a connection.

    A stopover may include planned and actual departure/arrival times, platform
    information, and station metadata.
    """

    id: str
    """Internal ID or index of the stopover."""

    departure_time: str
    """Planned departure time in ISO format (YYYY-MM-DDTHH:MM:SS)."""

    arrival_time: str
    """Planned arrival time in ISO format (YYYY-MM-DDTHH:MM:SS)."""

    platform: str
    """Planned platform information (Gleis)."""
    
    station_name: str
    """Name of the stopover station."""

    station_id: str
    """External station ID (extId) used for further API calls."""

    def __init__(self, id, abfahrtsZeitpunkt: Incomplete | None = None, ezAbfahrtsZeitpunkt: Incomplete | None = None, ankunftsZeitpunkt: Incomplete | None = None, ezAnkunftsZeitpunkt: Incomplete | None = None, auslastungsmeldungen: Incomplete | None = None, gleis: Incomplete | None = None, ezGleis: Incomplete | None = None, haltTyp: Incomplete | None = None, name: Incomplete | None = None, risNotizen: Incomplete | None = None, bahnhofsInfoId: Incomplete | None = None, extId: Incomplete | None = None, himMeldungen: Incomplete | None = None, routeIdx: Incomplete | None = None, priorisierteMeldungen: Incomplete | None = None) -> None: ...

class J_means_of_transport(Serializable):
    """
    Describes the vehicle or transport type used in a connection.

    Contains IDs, names, directions, and other labeling details of the transport.
    """

    name: str
    """Full transport mode name (e.g., 'ICE')."""

    transport_way_id: str
    """Vehicle or line number (e.g., 'ICE 123')."""

    direction: str
    """Direction or destination of the vehicle."""

    info: Optional[list]
    """List of vehicle attributes (e.g., 'wifi', 'bistro')."""

    short_name: str
    """Short display name (e.g., 'HLB')."""

    middle_name: str
    """Medium-length display name (e.g., 'HLB RE98')."""

    full_name: str
    """Long or verbose display name (e.g., 'HLB RE98 (24410)')."""

    def __init__(self, name: Incomplete | None = None, nummer: Incomplete | None = None, richtung: Incomplete | None = None, zugattribute: Incomplete | None = None, kurzText: Incomplete | None = None, mittelText: Incomplete | None = None, langText: Incomplete | None = None) -> None: ...

class Connection(Serializable):
    """
    A single leg of a journey, usually between two stations using a specific transport mode.

    Contains departure and arrival info, the vehicle used, and intermediate stopovers.
    """

    departure_time: str
    """Planned departure time (ISO format)."""
    
    departure_station: str
    """Name of the departure station."""

    arrival_time: str
    """Planned arrival time (ISO format)."""

    arrival_station: str
    """Name of the arrival station."""

    stopovers: list[J_StopOver]
    """List of intermediate stopovers on this connection."""

    journeyId: str
    """Identifier for this specific leg of the trip."""

    means_of_transport: J_means_of_transport
    """Information about the transport vehicle used in this connection."""

    def __init__(self, risNotizen: Incomplete | None = None, himMeldungen: Incomplete | None = None, priorisierteMeldungen: Incomplete | None = None, externeBahnhofsinfoIdOrigin: Incomplete | None = None, externeBahnhofsinfoIdDestination: Incomplete | None = None, abfahrtsZeitpunkt: Incomplete | None = None, ezAbfahrtsZeitpunkt: Incomplete | None = None, abfahrtsOrt: Incomplete | None = None, abfahrtsOrtExtId: Incomplete | None = None, abschnittsDauer: Incomplete | None = None, ezAbschnittsDauerInSeconds: Incomplete | None = None, abschnittsAnteil: Incomplete | None = None, ankunftsZeitpunkt: Incomplete | None = None, ezAnkunftsZeitpunkt: Incomplete | None = None, ankunftsOrt: Incomplete | None = None, ankunftsOrtExtId: Incomplete | None = None, auslastungsmeldungen: Incomplete | None = None, halte: Incomplete | None = None, idx: Incomplete | None = None, journeyId: Incomplete | None = None, verkehrsmittel: Incomplete | None = None) -> None: ...

class Journey(Serializable):
    """
    Represents a complete journey between two locations.

    A journey is composed of multiple `Connection` segments, each potentially
    representing a train, bus, or other means of transport. The class aggregates
    metadata such as number of transfers, total duration, occupancy info, and pricing.
    """

    trip_lid: str
    """
    The unique journey context (ctxRecon) required for follow-up requests, e.g., booking.
    """

    changes_amont: int
    """
    The number of transfers or changes required during the journey.
    """


    departure_name: str
    """
    Name of the departure location for the first connection.
    """


    arrival_name: str
    """
    Name of the arrival location for the last connection.
    """


    connections: list[Connection]
    """
    A list of individual connections (legs) that make up the journey.
    """

    journey_time_in_seconds: int
    """
    Total planned journey time in seconds.
    """


    journey_time_in_seconds_e: int
    """
    Total estimated journey time in seconds, adjusted for real-time data if available.
    """


    is_alternative_connection: bool
    """
    Indicates whether this journey is an alternative to a recommended or primary option.
    """
    auslastungstexte: Optional[List[str]]
    """
    Passenger load texts for each segment of the journey (e.g., occupancy levels).
    """
    meldungen: Optional[List[str]]
    """
    General service messages related to this journey.
    """

    meldungenAsObject: Optional[List[dict]]
    """
    Detailed service messages in structured format (used for internal display or analysis).
    """

    preis: Optional[str]
    """
    Total price of the journey in formatted string (e.g., "29.90 EUR").
    """

    def get_db_link(self) -> str:
        """Returns a link compatible with `DB Navigator` and [int.bahn.de](https://int.bahn.de) """
    def __init__(self, tripId: Incomplete | None = None, ctxRecon: Incomplete | None = None, verbindungsAbschnitte: Incomplete | None = None, umstiegsAnzahl: Incomplete | None = None, verbindungsDauerInSeconds: Incomplete | None = None, ezVerbindungsDauerInSeconds: Incomplete | None = None, isAlternativeVerbindung: Incomplete | None = None, auslastungsmeldungen: Incomplete | None = None, auslastungstexte: Incomplete | None = None, himMeldungen: Incomplete | None = None, risNotizen: Incomplete | None = None, priorisierteMeldungen: Incomplete | None = None, reservierungsMeldungen: Incomplete | None = None, isAngebotseinholungNachgelagert: Incomplete | None = None, isAlterseingabeErforderlich: Incomplete | None = None, serviceDays: Incomplete | None = None, angebotsPreis: Incomplete | None = None, angebotsPreisKlasse: Incomplete | None = None, hasTeilpreis: Incomplete | None = None, reiseAngebote: Incomplete | None = None, hinRueckPauschalpreis: Incomplete | None = None, isReservierungAusserhalbVorverkaufszeitraum: Incomplete | None = None, gesamtAngebotsbeziehungList: Incomplete | None = None, ereignisZusammenfassung: Incomplete | None = None, meldungen: Incomplete | None = None, meldungenAsObject: Incomplete | None = None) -> None: ...
