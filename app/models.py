from typing import List, Optional
from pydantic import BaseModel, Field

class InvoiceItem(BaseModel):
    description: Optional[str] = None
    quantity: Optional[float] = None
    unitPrice: Optional[float] = None
    amount: Optional[float] = None

class InvoiceExtract(BaseModel):
    invoiceId: Optional[str] = None
    invoiceDate: Optional[str] = None
    dueDate: Optional[str] = None
    vendorName: Optional[str] = None
    customerName: Optional[str] = None
    billingAddress: Optional[str] = None
    shippingAddress: Optional[str] = None
    total: Optional[float] = None
    subTotal: Optional[float] = None
    tax: Optional[float] = None
    purchaseOrder: Optional[str] = None
    items: List[InvoiceItem] = Field(default_factory=list)   # <- wichtig
