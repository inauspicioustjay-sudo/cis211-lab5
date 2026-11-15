import streamlit as st

menu = {
    "cupcake": 3.75,
    "cookie": 2.00,
    "muffin": 2.75,
    "scone": 3.25,
    "brownie": 3.00,
}

sample_sales = {
    "Product": ["cupcake", "cookie", "muffin", "scone", "brownie"],
    "Units sold": [18, 30, 12, 10, 15],
}


def apply_discount(subtotal):
    # >= so exactly $50.00 still gets the discount
    if subtotal >= 50.00:
        return round(subtotal * 0.90, 2)
    return subtotal


def shipping_fee(subtotal):
    # uses the original subtotal, not the discounted one
    if subtotal >= 35.00:
        return 0.0
    return 5.99


st.title("Bright Bakery Interactive Order Calculator")

with st.sidebar:
    st.header("Order options")
    customer_name = st.text_input("Customer name or nickname", value="")
    product = st.selectbox("Product", list(menu.keys()))
    quantity = st.number_input(
        "Quantity", min_value=1, max_value=30, value=1, step=1
    )
    fulfillment = st.selectbox("Fulfillment", ["Pickup", "Delivery"])
    show_chart = st.checkbox("Show sample sales chart", value=True)

unit_price = menu[product]
subtotal = unit_price * quantity
discounted_subtotal = apply_discount(subtotal)
discount_amount = round(subtotal - discounted_subtotal, 2)

# pickup is free, only delivery uses shipping_fee
if fulfillment == "Pickup":
    delivery_fee = 0.0
else:
    delivery_fee = shipping_fee(subtotal)

total = round(discounted_subtotal + delivery_fee, 2)

# quote is outside the button so it always shows
st.header("Current quote")
details_col, amounts_col = st.columns(2)

with details_col:
    st.write(f"**Product:** {product}")
    st.write(f"**Quantity:** {quantity}")
    st.write(f"**Unit price:** ${unit_price:.2f}")
    st.write(f"**Fulfillment:** {fulfillment}")

with amounts_col:
    st.write(f"**Original item subtotal:** ${subtotal:.2f}")
    st.write(f"**Discount amount:** ${discount_amount:.2f}")
    st.write(f"**Delivery fee:** ${delivery_fee:.2f}")
    st.metric("Final total", f"${total:.2f}")

st.header("Menu")
menu_table = {
    "Product": list(menu.keys()),
    "Price ($)": list(menu.values()),
}
st.dataframe(menu_table, hide_index=True)

# chart only uses sample_sales, the order doesn't change it
if show_chart:
    st.header("Sample sales")
    st.caption("Fictional practice data, not real sales.")
    st.bar_chart(sample_sales, x="Product", y="Units sold", sort=False)

if st.button("Check quote"):
    cleaned_name = customer_name.strip()
    if cleaned_name == "":
        st.warning("Please enter a name or nickname.")
    else:
        st.success(
            f"Quote checked for {cleaned_name}. This is a practice app, "
            "no order is saved and no payment is taken."
        )
