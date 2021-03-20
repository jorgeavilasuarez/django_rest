Date.prototype.toFormatDate = function () {
    var d = new Date(this),
        month = '' + (d.getMonth() + 1),
        day = '' + d.getDate(),
        year = d.getFullYear();

    if (month.length < 2)
        month = '0' + month;
    if (day.length < 2)
        day = '0' + day;

    return [year, month, day].join('-');
}

const date = new Date(), y = date.getFullYear(), m = date.getMonth();
const firstDay = new Date(y, m, 1).toFormatDate();
const lastDay = new Date(y, m + 1, 0).toFormatDate();

Vue.filter("formatNumber", function (value) {
    return value.toLocaleString();
});

var app = new Vue({
    el: '#app',
    methods: {
        onChange: function ($event) {

        },
        onChangeCustomer: function ($event) {
            this.products = this.customers
                .find(x => x.customer_id == $event.currentTarget.value)
                .products;

            this.form_data.product_list = [];
        },
        remove_product: function (index) {
            this.form_data.product_list.splice(index, 1);
        },
        onSubmit: async function () {
            const rs = await saveOrder(this.form_data);
            if (rs.result == 'ok') {
                this.form_data.product_list = [];
                loadOrders(this.form_data.customer_id, this.firstDay, this.lastDay);
            } else {
                alert("No se pudo guardar la orden");
            }
        },
        onClickListar: function () {
            loadOrders(this.form_data.customer_id, this.firstDay, this.lastDay);
        },
        onClickAdd: function () {
            let total_quantity = 0;
            this.form_data.total = 0;
            const product = this.products.find(x => x.product_id == this.form_data.product_id);

            this.form_data.product_list.push({
                product_id: this.form_data.product_id,
                quantity: this.form_data.quantity,
                name: product.name,
                product_description: product.product_description,
                price: product.price,
            });

            if (this.form_data.product_list.length) {
                this.form_data.product_list.forEach((a) => {
                    total_quantity += parseInt(a.quantity);
                    this.form_data.total = a.price * total_quantity;
                });
            }

            if (total_quantity > 5) {
                this.form_data.product_list.pop();
                alert("No se puede agregar mas de 5 producto por orden.");
                return;
            }
        }
    },
    data: {
        firstDay: firstDay,
        lastDay: lastDay,
        orders: null,
        customers: null,
        products: null,
        form_data: {
            customer_id: null,
            quantity: 1,
            product_list: [],
            total: 0,
            delivery_address: null
        },
    },
    mounted: function () {
        loadCustomers();
    }
});

/**
 * Transform data
 * @param {*} data 
 * @returns 
 */
function getModelData(data) {
    const order_details = data.order_details.map(order_detail => {
        order_detail.product = data.products.find(product => {
            return product.product_id == order_detail.product_id;
        });
        return order_detail;
    });

    const orders = data.order.map(order => {
        order.customer = data.customer.find(customer => {
            return customer.customer_id == order.customer_id;
        });
        order.order_details = order_details.filter(order_detail => {
            return order.order_id == order_detail.order_id;
        });
        return order;
    });
    return orders;
}
/**
 * Load orders via rest api
 */
async function loadOrders(customer_id = 2, date_ini = '2021-03-19', date_end = '2021-03-19') {
    const data = await fetch(`/orders?customer_id=${customer_id}&date_ini=${date_ini}&date_end=${date_end}`).then(x => x.json());
    const orders = getModelData(data);
    app.orders = orders;
}

/**
 * Load customers via rest api
 */
async function loadCustomers() {
    const data = await fetch('/customers').then(x => x.json());
    const customer_products = data.customer_product.map(customer_product => {
        customer_product.product = data.products.find(product => {
            return product.product_id == customer_product.product_id;
        });
        return customer_product;
    });
    const customers = data.customer.map(customer => {
        const _customer_products = customer_products.filter(customer_product => {
            return customer.customer_id == customer_product.customer_id;
        });
        customer.products = _customer_products.map(customer_product => {
            return customer_product.product;
        });
        return customer;
    });
    app.customers = customers;
}

/**
 * Saver order
 * @param {*} form_data 
 * @returns 
 */
async function saveOrder(form_data) {
    const rawResponse = await fetch('/orders/', {
        method: 'POST',
        headers: {
            'Accept': 'application/json',
            'Content-Type': 'application/json'
        },
        body: JSON.stringify(form_data)
    });

    const rs = await rawResponse.json();
    return rs;
}


