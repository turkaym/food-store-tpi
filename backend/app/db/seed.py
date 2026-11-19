from decimal import Decimal

from sqlmodel import Session, select

from app.core.database import create_all_tables, engine
from app.core.security import hash_password
from app.models import Categoria, Producto, Usuario


SEED_CATEGORIES = {
    "Burgers": "Handmade burgers",
    "Pizzas": "Oven-baked pizzas",
    "Drinks": "Cold and hot drinks",
}
SEED_PRODUCTS = [
    ("Classic Burger", "Burgers", Decimal("8.50")),
    ("Double Burger", "Burgers", Decimal("11.00")),
    ("Veggie Burger", "Burgers", Decimal("9.25")),
    ("Margherita Pizza", "Pizzas", Decimal("10.00")),
    ("Pepperoni Pizza", "Pizzas", Decimal("12.50")),
    ("Four Cheese Pizza", "Pizzas", Decimal("13.00")),
    ("Lemonade", "Drinks", Decimal("3.50")),
    ("Iced Tea", "Drinks", Decimal("3.00")),
]


def seed() -> None:
    create_all_tables()
    with Session(engine) as session:
        admin = session.exec(select(Usuario).where(Usuario.username == "admin")).first()
        if admin is None:
            session.add(Usuario(username="admin", full_name="Store Administrator", email="admin@foodstore.example", hashed_password=hash_password("Admin1234!"), role="admin"))
        categories: dict[str, Categoria] = {}
        for name, description in SEED_CATEGORIES.items():
            category = session.exec(select(Categoria).where(Categoria.nombre == name)).first()
            if category is None:
                category = Categoria(nombre=name, descripcion=description)
                session.add(category)
                session.flush()
            categories[name] = category
        session.flush()
        for name, category_name, price in SEED_PRODUCTS:
            if session.exec(select(Producto).where(Producto.nombre == name)).first() is None:
                session.add(Producto(categoria_id=categories[category_name].id, nombre=name, descripcion=f"{name} from Food Store", precio_base=price, stock=25))
        session.commit()


if __name__ == "__main__":
    seed()
