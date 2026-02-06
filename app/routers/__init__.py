"""
API route handlers
"""
from .invoices import router as invoices_router
from .ocr import router as ocr_router
from .counter import router as counter_router
from .health import router as health_router

__all__ = [
    'invoices_router',
    'ocr_router',
    'counter_router',
    'health_router'
]
