function makePrice(curr, original_price) {
    var price = parseFloat(original_price)
    price *= curr == 'EUR' ? 1 : 1.18
    price = price.toFixed(2)
    return curr == 'USD' ? ('$' + price) : (price + '€')
}