
var score = 0;
var logflag = 0;


window.onload = function () {
    $.ajax({

        method: 'GET',
        url: "/logincheck",
        success: function (data) {
            console.log(data)

            const urlParams = new URLSearchParams(window.location.search);

            console.log(urlParams.get('movieName'))
            console.log(urlParams.get('URL'))
            $("#title").text(urlParams.get('movieName')) 
           $("#poster").attr("src",urlParams.get('URL')) 
            if (data == 1) {
                $("a#login").hide();
                $("a#logout").show();
            }
            else {
                $("a#login").show();
                $("a#logout").hide();
            }

        }
    });
}
$("#submitreview").click(submitReview)
function submitReview() {

    let title = $("#title")[0].innerText;
    let comment = $("#subject").val();
    $.post("/review/create",
        {
            'title': title,
            'comment': comment,
            'score': score
        },
        function (data, status) {
            alert("Data: " + data + "\nStatus: " + status);
        }, "json");

}

function displayReview() {
    console.log("Request sent");
    $.post("/history", function (data, status) {

        alert("Data: " + data + "\nStatus: " + status);
    });
}

$(document).ready(function () {
    $("#1star").click(function () {
        score = 1;
        document.getElementById("1star").style.color = "#f1c40f";
        document.getElementById("2star").style.color = "#313131";
        document.getElementById("3star").style.color = "#313131";
        document.getElementById("4star").style.color = "#313131";
        document.getElementById("5star").style.color = "#313131";
    })

    $("#2star").click(function () {
        score = 2;
        document.getElementById("1star").style.color = "#f1c40f";
        document.getElementById("2star").style.color = "#f1c40f";
        document.getElementById("3star").style.color = "#313131";
        document.getElementById("4star").style.color = "#313131";
        document.getElementById("5star").style.color = "#313131";
    })

    $("#3star").click(function () {
        score = 3;
        document.getElementById("1star").style.color = "#f1c40f";
        document.getElementById("2star").style.color = "#f1c40f";
        document.getElementById("3star").style.color = "#f1c40f";
        document.getElementById("4star").style.color = "#313131";
        document.getElementById("5star").style.color = "#313131";
    })

    $("#4star").click(function () {
        score = 4;
        document.getElementById("1star").style.color = "#f1c40f";
        document.getElementById("2star").style.color = "#f1c40f";
        document.getElementById("3star").style.color = "#f1c40f";
        document.getElementById("4star").style.color = "#f1c40f";
        document.getElementById("5star").style.color = "#313131";
    })

    $("#5star").click(function () {
        score = 5;
        document.getElementById("1star").style.color = "#f1c40f";
        document.getElementById("2star").style.color = "#f1c40f";
        document.getElementById("3star").style.color = "#f1c40f";
        document.getElementById("4star").style.color = "#f1c40f";
        document.getElementById("5star").style.color = "#f1c40f";
    })
});

function deleteReview() {
    console.log("Request sent");
    $.post("/history/delete", function (data, status) {
        alert("Data: " + data + "\nStatus: " + status);
    });
}


function updateReview() {
    console.log("Request sent");
    $.post("/history/update", function (data, status) {
        alert("Data: " + data + "\nStatus: " + status);
    });
}

function logout() {
    $.ajax({

        method: 'GET',
        url: "/logout",
        success: function (data) {
            console.log(data)

        }
    });
}

function login() {
    console.log("here")
    let username = $("#emailAddress").val();
    let password = $("#password").val();

    console.log(username + " " + password);

    $.post("/login",
        {
            'email': username,
            'password': password
        }, function (data, status) {
            $.ajax({

                method: 'GET',
                url: "/logincheck",
                success: function (data) {
                    console.log(data)

                    if (data == 1) {
                        $("a#login").hide();
                        $("a#logout").show();
                        window.location = "/index.html";
                    }
                    else {
                        alert("Incorrect Login!");
                    }

                }
            });
        }
    )


    //window.location.replace("index.html")
}

function register() {

    let first_name = $("#fname").val();
    let last_name = $("#lname").val();
    let username = $("#uname").val();
    let email = $("#emailAddress").val();
    let password = $("#password").val();

    console.log(first_name + " " + last_name);

    $.post("/users/register",
        {
            'first_name': first_name,
            'last_name': last_name,
            'email': email,
            'username': username,
            'password': password
        },
        function (data, status) {
            alert("Data: " + data + "\nStatus: " + status);
        });
}