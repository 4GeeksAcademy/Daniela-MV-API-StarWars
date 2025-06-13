from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import String, Boolean,ForeignKey
from sqlalchemy.orm import Mapped, mapped_column,relationship

db = SQLAlchemy()

class User(db.Model):
    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(120), unique=True, nullable=False)
    user_name: Mapped[str] = mapped_column(String(120), unique=True, nullable=False)
    email: Mapped[str] = mapped_column(String(120), unique=True, nullable=False)
    password: Mapped[str] = mapped_column(nullable=False)
    is_active: Mapped[bool] = mapped_column(Boolean(), nullable=False)
    favorite_character: Mapped[list["Fav_character"]]=relationship(back_populates="user")
    favorite_planet:Mapped[list["Fav_planet"]]=relationship(back_populates="user")


    def serialize(self):
        return {
            "id": self.id,
            "name": self.name,
            "user_name": self.user_name,
            "email": self.email,
            # do not serialize the password, its a security breach
        }


class Characters(db.Model):
    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(120), nullable=False)
    gender: Mapped[str] = mapped_column(String(120), unique=True, nullable=False)
    hair_color: Mapped[str] = mapped_column(String(120), nullable=False)
    eye_color: Mapped[str] = mapped_column(String(120), nullable=False)
    birth_year: Mapped[str] = mapped_column(String(120), nullable=False)
    favorite_by_links: Mapped[list["Fav_character"]]=relationship(back_populates="character")

    def serialize(self):
        return {
            "id": self.id,
            "name": self.name,
            "gender": self.gender,
            "hair_color": self.hair_color,
            "eye_color": self.eye_color,
            "birth_year": self.birth_year,
        }


class Planets(db.Model):
    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(120), nullable=False)
    climate: Mapped[str] = mapped_column(String(120), nullable=False)
    diameter: Mapped[int] = mapped_column(nullable=False)
    terrain: Mapped[str] = mapped_column(String(120), nullable=False)
    population: Mapped[int] = mapped_column(nullable=False)
    favorite_planet_by_links: Mapped[list["Fav_planet"]]=relationship(back_populates="planet")

    def serialize(self):
        return {
            "id": self.id,
            "name": self.name,
            "climate": self.climate,
            "diameter": self.diameter,
            "terrain": self.terrain,
            "population": self.population,
        }


class Vehicles(db.Model):
    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(120), nullable=False)
    model: Mapped[str] = mapped_column(String(120), nullable=False)
    cargo_capacity: Mapped[int] = mapped_column(nullable=False)
    manufacturer: Mapped[str] = mapped_column(String(120), nullable=False)
    passengers: Mapped[int] = mapped_column(nullable=False)

    def serialize(self):
        return {
            "id": self.id,
            "name": self.name,
            "model": self.model,
            "cargo_capacity": self.cargo_capacity,
            "manufacturer": self.manufacturer,
            "passengers": self.passengers,
        }

class Fav_character(db.Model):
    id: Mapped[int] = mapped_column(primary_key=True)
    user_id: Mapped[int] = mapped_column(ForeignKey("user.id"))
    character_id: Mapped[int] = mapped_column(ForeignKey("characters.id"))
    user: Mapped['User'] = relationship(back_populates="favorite_character")
    character: Mapped['Characters'] = relationship(back_populates='favorite_by_links')

    
class Fav_planet(db.Model):
    id: Mapped[int] = mapped_column(primary_key=True)
    user_id: Mapped[int] = mapped_column(ForeignKey("user.id"))
    planet_id: Mapped[int] = mapped_column(ForeignKey("planets.id"))
    user: Mapped['User'] = relationship(back_populates="favorite_planet")
    planet: Mapped['Planets'] = relationship(back_populates='favorite_planet_by_links')   