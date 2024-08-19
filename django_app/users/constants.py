from core.constants import BaseChoiceEnum


class Gender(BaseChoiceEnum):
    """
    The enumeration of gender
    """

    CISMALE = "cisMale"
    CISFEMALE = "cisFemale"
    TRANSGENDERMALE = "transgenderMale"
    TRANSGENDERFEMALE = "transgenderFemale"
    NONBINARY = "nonBinary"
    NONE = "none"
    UNSPECIFIED = "unspecified"
    OTHER = "other"
    UNKNOWN = "unknown"
    DECLINEDTOANSWER = "declinedToAnswer"


class AssignedSex(BaseChoiceEnum):
    """
    The enumeration of assigned sex
    """

    MALE = "male"
    FEMALE = "female"
    UNSPECIFIED = "unspecified"
    NONE = "none"
    OTHER = "other"
    UNKNOWN = "unknown"
    DECLINEDTOANSWER = "declinedToAnswer"


class Race(BaseChoiceEnum):
    """
    The enumeration of race
    """

    AMERICANINDIANORALASKANATIVE = "American Indian or Alaska Native"
    ASIAN = "Asian"
    BLACKORAFRICANAMERICAN = "Black or African American"
    NATIVEHAWAIIANOROTHERPACIFICISLANDER = "Native Hawaiian or other Pacific Islander"
    HISPATICORLATINO = "Hispatic or Latino"
    WHITE = "White"
    OTHER = "Other"
    DECLINEDTOANSWER = "Declined To Answer"
