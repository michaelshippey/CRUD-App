from dataclasses import dataclass


@dataclass
class DatabaseConfig:
    db_host: str = "ec2-35-168-77-215.compute-1.amazonaws.com"
    db_port: int = 5432
    db_database: str = "d4g7f6di006pvh"
    db_user: str = "sxobojvxzmysit"
    db_passwd: str = "ed2d842e9f5770d6e72875ad081f35d59d1a197e0b99333f8a569d7b9f532943"
    db_user_table: str = "user_data"
    db_review_table: str = "reviews"
