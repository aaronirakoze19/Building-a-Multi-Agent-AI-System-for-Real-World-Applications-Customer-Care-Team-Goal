ORDERS = {
    "KEN-10482": {"status": "Delivered", "amount": 79.99},
    "KEN-20411": {"status": "In Transit", "eta": "2026-02-02"},
}

FAQ = {
    "refund_policy": "Refunds within 14 days for unused items in original packaging.",
    "delivery_policy": "Delivery in 3–5 business days (standard) or 1–2 days (express)."
}

def get_order(order_id):
    return ORDERS.get(order_id, {"error": "Order not found"})

def lookup_faq(key):
    return FAQ.get(key, "No FAQ entry found")

def issue_refund(order_id):
    order = ORDERS.get(order_id)
    if not order:
        return {"ok": False, "message": "Order not found"}
    if order["status"] != "Delivered":
        return {"ok": False, "message": "Refund denied: Order not delivered"}
    return {"ok": True, "message": "Refund processed", "amount": order["amount"]}
