from enum import Enum

class UserRoleEnum(str, Enum):
   USER = "user"
   SILVER = "silver"
   GOLD = "gold"
   PREMIUM = "premium"
   SUPER_ADMIN = "super_admin"

class SportCategoryEnum(str, Enum):
   FOOTBALL = "football"
   BASKETBALL = "basketball"

class StrongSideEnum(str, Enum):
   LEFT = "left"
   RIGHT = "right"
   BOTH = "both"

class FootballPositionsEnum(str, Enum):
   GK = "gk"
   CB = "cb"
   RB = "rb"
   LB = "lb"
   CDM = "cdm"
   CM = "cm"
   CAM = "cam"
   LM = "lm"
   RM = "rm"
   CF = "cf"
   LW = "lw"
   RW = "rw"
   ST = "st"

class BasketballPositionsEnum(str, Enum):
   PG = "pg"
   SG = "sg"
   SF = "sf"
   PF = "pf"
   C = "c"

class AccountStatusEnum(str, Enum):
   ACTIVE = "active"
   INACTIVE = "inactive"
   SUSPENDED = "suspended"
   LOCKED = "locked"
   PENDING_VERIFICATION = "pending_verification"

class RequestStatusEnum(str, Enum):
   PENDING = "pending"
   ACCEPTED = "accepted"
   REJECTED = "rejected"

class ClubStatusEnum(str, Enum):
   ACTIVE = "active"
   INACTIVE = "inactive"
   FULL = "full"

class EventStatusEnum(str, Enum):
    UPCOMING = "upcoming"
    FULL = "full"
    ONGOING = "ongoing"
    COMPLETED = "completed"
