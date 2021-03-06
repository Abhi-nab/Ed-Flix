function openNav() {
    document.getElementById("mySidenav").style.width = "100%";
    document.getElementById("main").style.marginLeft = "100%";
    document.body.style.backgroundColor = "rgba(0,0,0,0.4)";
}

function closeNav() {
    document.getElementById("mySidenav").style.width = "0";
    document.getElementById("main").style.marginLeft = "0";
    document.body.style.backgroundColor = "white";
}

/////////////////////////////// Filter Subjects ////////////////////////////

filterSelection("all");

function filterSelection(c) {
    var x, i;
    x = document.getElementsByClassName("filterDiv");
    if (c == "all") c = "";
    // Add the "show" class (display:block) to the filtered elements, and remove the "show" class from the elements that are not selected
    for (i = 0; i < x.length; i++) {
        removeClass(x[i], "show");
        if (x[i].className.indexOf(c) > -1) addClass(x[i], "show");
    }
}

// Show filtered elements
function addClass(element, name) {
    var i, arr1, arr2;
    arr1 = element.className.split(" ");
    arr2 = name.split(" ");
    for (i = 0; i < arr2.length; i++) {
        if (arr1.indexOf(arr2[i]) == -1) {
            element.className += " " + arr2[i];
        }
    }
}

// Hide elements that are not selected
function removeClass(element, name) {
    var i, arr1, arr2;
    arr1 = element.className.split(" ");
    arr2 = name.split(" ");
    for (i = 0; i < arr2.length; i++) {
        while (arr1.indexOf(arr2[i]) > -1) {
            arr1.splice(arr1.indexOf(arr2[i]), 1);
        }
    }
    element.className = arr1.join(" ");
}

// Customize the dropdown
const dropdownToggle = document.querySelector(".dropdown-toggle");
const dropdownItem = document.getElementsByClassName("dropdown-item");

for (let i = 0; i < dropdownItem.length; i++) {
    dropdownItem[i].addEventListener("click", () => {
        dropdownToggle.innerHTML = dropdownItem[i].innerHTML;
    });
}


$(".search-form").on("submit", function(e) { //prevent from enter key hit
    e.preventDefault();

});

// Search implementation
const searchSubjects = () => {

    const input = document.querySelector(".form-control.search");
    const inputValue = input.value.toLowerCase();
    // console.log(inputValue.trim());
    const subject = document.querySelectorAll(".bg-clip span"); // Array
    const subjectDiv = document.querySelectorAll(".bg-clip"); // Array
    const subjectShortcut = document.querySelectorAll("div.bg-clip"); // Array
    // console.log(subject[0]);
    // console.log(subjectDiv[0]);
    let subjectValue;
    let subjectShortcutValue;

    for (let i = 0; i < subject.length; i++) {
        subjectValue = subject[i].innerText.toLowerCase();
        if (subjectShortcut[i] == null) continue;
        subjectShortcutValue = subjectShortcut[i].innerText
            .split("\n")[0]
            .toLowerCase();
        // console.log(subjectShortcutValue); // [m-i, phy, be, ...]


        if (
            subjectValue.indexOf(inputValue.trim()) > -1 ||
            subjectShortcutValue.indexOf(inputValue.trim()) > -1
        ) {
            subjectDiv[i].style.display = "";
            // console.log(subjectValue + " " + subjectShortcutValue);
            //console.log();
        } else {
            subjectDiv[i].style.setProperty("display", "none", "important");
        }
    }
};

// console.log(subjectShortcut[0].innerText.split("\n")[0]);