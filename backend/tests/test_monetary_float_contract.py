from typing import get_type_hints

from sqlalchemy import Float

from app.main import app
from app.models import DetallePedido, Pedido, Producto
from app.modules.catalog.schemas import ProductCreate, ProductRead, ProductUpdate
from app.modules.pedidos.schemas import OrderItemRead, OrderRead, OrderSummary


def test_persisted_monetary_fields_use_float_columns():
    fields = (
        (Producto, "precio_base"),
        (Pedido, "total"),
        (DetallePedido, "precio_unitario"),
        (DetallePedido, "subtotal"),
    )

    for model, field_name in fields:
        assert get_type_hints(model)[field_name] is float
        assert isinstance(model.__table__.columns[field_name].type, Float)


def test_monetary_schema_annotations_use_float():
    fields = (
        (ProductCreate, "precio_base", float),
        (ProductUpdate, "precio_base", float | None),
        (ProductRead, "precio_base", float),
        (OrderItemRead, "precio_unitario", float),
        (OrderItemRead, "subtotal", float),
        (OrderRead, "total", float),
        (OrderSummary, "ingresos_entregados", float),
    )

    for schema, field_name, expected in fields:
        assert get_type_hints(schema)[field_name] == expected


def test_openapi_exposes_monetary_fields_as_numbers():
    schemas = app.openapi()["components"]["schemas"]
    fields = (
        ("ProductCreate", "precio_base"),
        ("ProductUpdate", "precio_base"),
        ("ProductRead", "precio_base"),
        ("OrderItemRead", "precio_unitario"),
        ("OrderItemRead", "subtotal"),
        ("OrderRead", "total"),
        ("OrderSummary", "ingresos_entregados"),
    )

    for schema_name, field_name in fields:
        field_schema = schemas[schema_name]["properties"][field_name]
        variants = field_schema.get("anyOf", [field_schema])
        assert {variant["type"] for variant in variants} <= {"number", "null"}
