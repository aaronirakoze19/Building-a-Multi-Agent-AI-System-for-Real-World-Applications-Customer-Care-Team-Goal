# this is used in simple in-memory "databases" for demo purposes
ORDERS = {
    "KEN-10482": {"status": "Delivered", "amount": 79.99},
    "KEN-20411": {"status": "In Transit", "eta": "2026-02-02"},
}

FAQ = {
    "refund_policy": "Refunds within 14 days for unused items in original packaging.",
    "delivery_policy": "Delivery in 3–5 business days (standard) or 1–2 days (express)."
}

def get_order(order_id):
    # this key operates by showing the return order details or a safe error message
    return ORDERS.get(order_id, {"error": "Order not found"})

def lookup_faq(key):
    #This reads the FAQ text by text
    return FAQ.get(key, "No FAQ entry found")

def issue_refund(order_id):
    #This key ensures and enforces a business rule (only delivered orders can be refunded)
    order = ORDERS.get(order_id)
    if not order:
        return {"ok": False, "message": "Order not found"}
    if order["status"] != "Delivered":
        return {"ok": False, "message": "Refund denied: Order not delivered"}
    
    #This key uses functions to show the success response and how it includes the amount for transparency/logging
    return {"ok": True, "message": "Refund processed", "amount": order["amount"]}
