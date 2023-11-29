$(function () {

    // ****************************************
    //  U T I L I T Y   F U N C T I O N S
    // ****************************************

    // Updates the form with data from the response
    function update_form_data(res) {
        $("#order_id").val(res.id);
        $("#order_name").val(res.name);
        $("#order_create_time").val(res.create_time);
        $("#order_address").val(res.address);
        $("#order_cost_amount").val(res.cost_amount);
        $("#order_status").val(res.status);
        $("#order_user_id").val(res.user_id);
    }

    /// Clears all form fields
    function clear_form_data() {
        $("#order_name").val("");
        $("#order_create_time").val("");
        $("#order_address").val("");
        $("#order_cost_amount").val("");
        $("#order_status").val("");
        $("#order_user_id").val("");
    }

    // Updates the flash message area
    function flash_message(message) {
        $("#flash_message").empty();
        $("#flash_message").append(message);
    }

    // ****************************************
    // Create an Order
    // ****************************************

    $("#create-btn").click(function () {

        let name = $("#order_name").val();
        let create_time = $("#order_create_time").val();
        let address = $("#order_address").val();
        let cost_amount = $("#order_cost_amount").val();
        let status = $("#order_status").val();
        let user_id = $("#order_user_id").val();
        

        let data = {
            "name": name,
            "create_time": create_time,
            "address": address,
            "cost_amount": parseInt(cost_amount, 10),
            "status": status,
            "user_id": parseInt(user_id, 10),
            "items" : []
        };

        $("#flash_message").empty();
        
        let ajax = $.ajax({
            type: "POST",
            url: "/orders",
            contentType: "application/json",
            data: JSON.stringify(data),
        });

        ajax.done(function(res){
            update_form_data(res)
            flash_message("Success")
        });

        ajax.fail(function(res){
            flash_message(res.responseJSON.message)
        });
    });


    // ****************************************
    // Update an Order
    // ****************************************

    $("#update-btn").click(function () {

        let id =  $("#order_id").val();
        let name = $("#order_name").val();
        let create_time = $("#order_create_time").val();
        let address = $("#order_name").val();
        let cost_amount = $("#order_cost_amount").val();
        let status = $("#order_status").val();
        let user_id = $("#order_user_id").val();

        let data = {
            "id" : id, 
            "name": name,
            "create_time": create_time,
            "address": address,
            "cost_amount": cost_amount,
            "status": status,
            "user_id": user_id
        };

        $("#flash_message").empty();

        let ajax = $.ajax({
                type: "PUT",
                url: `/orders/${order_id}`,
                contentType: "application/json",
                data: JSON.stringify(data)
            })

        ajax.done(function(res){
            update_form_data(res)
            flash_message("Success")
        });

        ajax.fail(function(res){
            flash_message(res.responseJSON.message)
        });

    });

    // ****************************************
    // Retrieve an Order
    // ****************************************

    $("#retrieve-btn").click(function () {

        let order_id = $("#order_id").val();

        $("#flash_message").empty();

        let ajax = $.ajax({
            type: "GET",
            url: `/orders/${order_id}`,
            contentType: "application/json",
            data: ''
        })

        ajax.done(function(res){
            //alert(res.toSource())
            update_form_data(res)
            flash_message("Success")
        });

        ajax.fail(function(res){
            clear_form_data()
            flash_message(res.responseJSON.message)
        });

    });

    // ****************************************
    // Delete an Order
    // ****************************************

    $("#delete-btn").click(function () {

        let order_id = $("#order_id").val();

        $("#flash_message").empty();

        let ajax = $.ajax({
            type: "DELETE",
            url: `/orders/${order_id}`,
            contentType: "application/json",
            data: '',
        })

        ajax.done(function(res){
            clear_form_data()
            flash_message("Order has been Deleted!")
        });

        ajax.fail(function(res){
            flash_message("Server error!")
        });
    });

    // ****************************************
    // Clear the form
    // ****************************************

    $("#clear-btn").click(function () {
        $("#order_id").val("");
        $("#flash_message").empty();
        clear_form_data()
    });

    // ****************************************
    // Search for an Order
    // ****************************************

    $("#search-btn").click(function () {

        let name = $("#order_name").val();
        let create_time = $("#order_create_time").val();
        let status = $("#order_status").val();
        let user_id = $("#order_user_id").val();


        let queryString = ""

        if (name) {
            queryString += 'name=' + name
        }
        if (create_time) {
            if (queryString.length > 0) {
                queryString += '&create_time=' + create_time
            } else {
                queryString += 'create_time=' + create_time
            }
        }
        if (status) {
            if (queryString.length > 0) {
                queryString += '&status=' + status
            } else {
                queryString += 'status=' + status
            }
        }
        if (user_id) {
            if (queryString.length > 0) {
                queryString += '&user_id=' + user_id
            } else {
                queryString += 'user_id=' + user_id
            }
        }

        $("#flash_message").empty();

        let ajax = $.ajax({
            type: "GET",
            url: `/orders?${queryString}`,
            contentType: "application/json",
            data: ''
        })

        ajax.done(function(res){
            //alert(res.toSource())
            $("#search_results").empty();
            let table = '<table class="table table-striped" cellpadding="10">'
            table += '<thead><tr>'
            table += '<th class="col-md-2">ID</th>'
            table += '<th class="col-md-2">Name</th>'
            table += '<th class="col-md-2">Create Time</th>'
            table += '<th class="col-md-2">Address</th>'
            table += '<th class="col-md-2">Cost Amount</th>'
            table += '<th class="col-md-2">Status</th>'
            table += '<th class="col-md-2">User ID</th>'
            table += '</tr></thead><tbody>'
            let firstOrder = "";
            for(let i = 0; i < res.length; i++) {
                let order = res[i];
                table +=  `<tr id="row_${i}"><td>${order.id}</td><td>${order.name}</td><td>${order.create_time}</td><td>${order.address}</td><td>${order.cost_amount}</td><td>${order.status}</td><td>${order.user_id}</td></tr>`;
                if (i == 0) {
                    firstOrder = order;
                }
            }
            table += '</tbody></table>';
            $("#search_results").append(table);

            // copy the first result to the form
            if (firstOrder != "") {
                update_form_data(firstOrder)
            }

            flash_message("Success")
        });

        ajax.fail(function(res){
            flash_message(res.responseJSON.message)
        });

    });

})
